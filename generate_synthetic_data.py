"""
ShopFlow E-commerce Synthetic Data Generator
Target: AWS S3 Data Lake (Parquet/CSV)

This script generates synthetic e-commerce data for the ShopFlow project.
It creates the following datasets:
1. customers (100k) - With churn indicators and segments
2. products (5k) - With categories, brands, and costs
3. orders (500k) - Transactional history linked to customers/products
4. events (2M) - Clickstream data for behavioral analysis
5. inventory (10k) - Stock levels across warehouses

Output:
- Local files in 'data/' directory (Parquet and CSV)
- Optional upload to AWS S3 if credentials are provided in .env
"""

import os
import random
import boto3
from datetime import datetime
import numpy as np
import pandas as pd
from faker import Faker
from botocore.exceptions import NoCredentialsError, ClientError

# Initialize Faker and Seeds
fake = Faker()
np.random.seed(42)
random.seed(42)

# ======================================================
# CONFIGURATION
# ======================================================
NUM_CUSTOMERS = 100_000
NUM_ORDERS = 500_000
NUM_PRODUCTS = 5_000
NUM_EVENTS = 2_000_000
NUM_INVENTORY = 10_000

START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2025, 2, 28)  # Updated to current project timeline
DAYS_RANGE = (END_DATE - START_DATE).days

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# AWS Configuration (loaded from environment variables)
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", "shopflow-data-lake")
AWS_REGION = os.getenv("AWS_REGION", "eu-west-2")

print("🚀 Starting ShopFlow synthetic data generation...")
print(f"📂 Output directory: {DATA_DIR}/")

# ======================================================
# 1. GENERATE CUSTOMERS
# ======================================================
def generate_customers(n: int) -> pd.DataFrame:
    print(f"   Generating {n:,} customers...")
    
    customer_ids = [f"CUST{i:06d}" for i in range(1, n + 1)]
    
    # Segments: 10% Churned, 10% At Risk, others active
    segments = np.random.choice(
        ["High Value", "Medium Value", "Low Value", "At Risk", "Churned"],
        size=n,
        p=[0.15, 0.30, 0.35, 0.10, 0.10],
    )

    days_since_start = np.random.randint(0, DAYS_RANGE, size=n)
    signup_dates = START_DATE + pd.to_timedelta(days_since_start, unit="D")

    emails = [f"{cid.lower()}@shopflow.com" for cid in customer_ids]

    df = pd.DataFrame({
        "customer_id": customer_ids,
        "email": emails,
        "first_name": [fake.first_name() for _ in range(n)],
        "last_name": [fake.last_name() for _ in range(n)],
        "city": [fake.city() for _ in range(n)],
        "country": np.random.choice(["USA", "Canada", "UK", "Germany", "France"], size=n),
        "signup_date": signup_dates,
        "customer_segment": segments,
    })
    return df

# ======================================================
# 2. GENERATE PRODUCTS
# ======================================================
def generate_products(n: int) -> pd.DataFrame:
    print(f"   Generating {n:,} products...")
    
    categories = ["Electronics", "Clothing", "Home", "Sports", "Books", "Beauty"]
    brands = ["BrandA", "BrandB", "BrandC", "Generic"]
    
    product_ids = [f"PROD{i:05d}" for i in range(1, n + 1)]
    selected_categories = np.random.choice(categories, size=n)
    prices = np.round(np.random.uniform(10, 500, size=n), 2)
    costs = np.round(prices * np.random.uniform(0.4, 0.7, size=n), 2)
    
    df = pd.DataFrame({
        "product_id": product_ids,
        "product_name": [f"{fake.word().title()} {cat}" for cat in selected_categories],
        "category": selected_categories,
        "brand": np.random.choice(brands, size=n),
        "price": prices,
        "cost": costs,
        "stock_status": np.random.choice(["In Stock", "Low Stock", "Out of Stock"], size=n, p=[0.7, 0.2, 0.1])
    })
    return df

# ======================================================
# 3. GENERATE ORDERS
# ======================================================
def generate_orders(customers_df, products_df, n: int) -> pd.DataFrame:
    print(f"   Generating {n:,} orders...")
    
    # Weighted sampling for active vs churned customers
    weights = customers_df["customer_segment"].map({
        "High Value": 0.3, "Medium Value": 0.3, "Low Value": 0.2, "At Risk": 0.15, "Churned": 0.05
    }).values
    weights /= weights.sum()
    
    sampled_customers = customers_df.sample(n=n, replace=True, weights=weights)
    sampled_products = products_df.sample(n=n, replace=True)
    
    # Dates: Churned customers have older orders
    is_churned = sampled_customers["customer_segment"] == "Churned"
    days = np.empty(n, dtype=int)
    
    churn_cutoff_days = int(DAYS_RANGE * 0.7) # Churned stopped 30% ago
    days[is_churned] = np.random.randint(0, churn_cutoff_days, size=is_churned.sum())
    days[~is_churned] = np.random.randint(0, DAYS_RANGE, size=(~is_churned).sum())
    
    order_dates = START_DATE + pd.to_timedelta(days, unit="D")
    quantities = np.random.randint(1, 6, size=n)
    amounts = np.round(sampled_products["price"].values * quantities, 2)
    
    df = pd.DataFrame({
        "order_id": [f"ORD{i:07d}" for i in range(1, n + 1)],
        "customer_id": sampled_customers["customer_id"].values,
        "product_id": sampled_products["product_id"].values,
        "order_date": order_dates,
        "amount": amounts,
        "quantity": quantities,
        "payment_method": np.random.choice(["Credit Card", "PayPal", "Debit"], size=n)
    })
    return df

# ======================================================
# 4. GENERATE EVENTS
# ======================================================
def generate_events(customers_df, products_df, n: int) -> pd.DataFrame:
    print(f"   Generating {n:,} events...")
    
    sampled_customers = customers_df.sample(n=n, replace=True)
    sampled_products = products_df.sample(n=n, replace=True)
    
    timestamps = START_DATE + pd.to_timedelta(np.random.randint(0, DAYS_RANGE, size=n), unit="D")
    
    df = pd.DataFrame({
        "event_id": [f"EVT{i:08d}" for i in range(1, n + 1)],
        "customer_id": sampled_customers["customer_id"].values,
        "session_id": [f"SES{np.random.randint(1000, 9999)}" for _ in range(n)],
        "event_type": np.random.choice(["view", "cart", "purchase"], size=n, p=[0.7, 0.2, 0.1]),
        "timestamp": timestamps,
        "product_id": sampled_products["product_id"].values,
        "device": np.random.choice(["Mobile", "Desktop"], size=n)
    })
    return df

# ======================================================
# 5. S3 UPLOAD UTILITY
# ======================================================
def upload_folder_to_s3(folder, bucket):
    s3_client = boto3.client('s3')
    print(f"\n📤 Uploading to S3 Bucket: {bucket}")
    
    try:
        # Check if bucket exists
        s3_client.head_bucket(Bucket=bucket)
    except ClientError:
        print(f"❌ Bucket {bucket} not found or access denied. Skipping upload.")
        return

    for root, _, files in os.walk(folder):
        for file in files:
            local_path = os.path.join(root, file)
            s3_path = f"raw/{file}" # Determine S3 prefix
            try:
                print(f"   From: {local_path} -> To: s3://{bucket}/{s3_path}")
                s3_client.upload_file(local_path, bucket, s3_path)
            except Exception as e:
                print(f"   ❌ Failed to upload {file}: {e}")

# ======================================================
# MAIN EXECUTION
# ======================================================
if __name__ == "__main__":
    # Generate Data
    customers = generate_customers(NUM_CUSTOMERS)
    products = generate_products(NUM_PRODUCTS)
    orders = generate_orders(customers, products, NUM_ORDERS)
    events = generate_events(customers, products, NUM_EVENTS)
    
    # Save Locally
    print(f"\n💾 Saving data locally to {DATA_DIR}...")
    
    datasets = {
        "customers": customers,
        "products": products,
        "orders": orders,
        "events": events
    }
    
    for name, df in datasets.items():
        # Save as Parquet (preferred for S3/Analytics)
        parquet_path = f"{DATA_DIR}/{name}.parquet"
        df.to_parquet(parquet_path, index=False)
        print(f"   ✓ {name}.parquet ({len(df):,} rows)")
        
        # Save as CSV (backup/easy view)
        csv_path = f"{DATA_DIR}/{name}.csv"
        df.to_csv(csv_path, index=False)

    print("\n✅ Data generated successfully!")

    # Optional S3 Upload
    if os.getenv("AWS_ACCESS_KEY_ID"):
        upload_folder_to_s3(DATA_DIR, AWS_BUCKET_NAME)
    else:
        print("\nℹ️  AWS credentials not found. Skipping S3 upload.")
        print("   To upload, set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in your environment.")
