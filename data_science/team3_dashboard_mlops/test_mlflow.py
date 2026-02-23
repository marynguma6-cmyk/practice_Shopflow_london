import dagshub
import mlflow

dagshub.init(repo_owner='abebiyinusa38', repo_name='shopflow-mlflow', mlflow=True)

mlflow.set_experiment("test-connection")

with mlflow.start_run():
    mlflow.log_param("project", "shopflow")
    mlflow.log_metric("accuracy", 0.95)

print("MLflow connection successful 🎉")