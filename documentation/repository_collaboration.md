# Repository Collaboration & Git Workflow
## ShopFlow 2-Week Sprint

This document outlines the Git workflow for the sprint. It ensures teams can collaborate without conflicts.

**Repository:** https://github.com/datascience-muhammad/Shopflow_london

---

## 1. Branch Protection & Access Rules

### Main Branch — LOCKED

The `main` branch is **protected** and locked. No one can push directly to `main`.

**Purpose:** Production-ready code only. Final demo code lives here.

**Who can merge to main:** PM Lead only, at end of sprint after all testing passes.

---

### Dev Branch — Integration Testing

The `dev` branch is where all team branches come together for integration testing.

**Who can merge to dev:** PM Team 1 (Technical Delivery) coordinates merges from team branches.

**When:** Periodically throughout the sprint, usually after major milestones (Day 5, Day 7, Day 9).

---

## 2. Branching Strategy

We use a **three-tier branching model** to allow each team to work independently while coordinating at key points.

```
main (locked, production-ready)
  │
  └── dev (integration testing)
       │
       ├── team/ds-churn (DS Team 1 shared workspace)
       │    │
       │    ├── feature/baseline-model (individual work by Team 1 member)
       │    └── feature/feature-engineering (individual work by Team 1 member)
       │
       ├── team/ds-recommendation (DS Team 2 shared workspace)
       │    │
       │    ├── feature/collab-filtering (individual work by Team 2 member)
       │    └── feature/api-development (individual work by Team 2 member)
       │
       └── team/ds-dashboard-mlops (DS Team 3 shared workspace)
            │
            ├── feature/mock-api (individual work by Team 3 member)
            └── feature/streamlit-dashboard (individual work by Team 3 member)
```

### Branch Types

| Branch | Pattern | Who Uses | Lifetime |
|--------|---------|----------|----------|
| **main** | `main` | No direct access | Permanent |
| **dev** | `dev` | PM Team 1 merges team branches here | Permanent |
| **Team Branch** | `team/ds-churn` | Entire DS Team 1 | Entire sprint |
| **Feature Branch** | `feature/model-training` | Individual team member | 1-3 days |

---

## 3. How Teams Collaborate Within Their Team Branch

Each DS team has a **shared team branch** where all their work comes together. Individual team members create **feature branches** for their specific tasks.

### DS Team Lead Responsibilities

**The DS Team Lead decides:**
- Who works on which task
- When a feature branch is ready to merge into the team branch
- When the team branch is ready to be promoted to `dev`

**Team leads do NOT need to ask PM or project lead for permission** to assign tasks within their team or merge feature branches into their team branch.

---

## 4. Step-by-Step Workflow

### Step 1: Team Lead Assigns a Task

**Example:** DS Team 1 Lead assigns "Build baseline churn model" to a team member.

The team member creates a feature branch from the team branch.

---

### Step 2: Individual Creates Feature Branch

```bash
# 1. Switch to your team branch
git checkout team/ds-churn

# 2. Pull latest changes
git pull origin team/ds-churn

# 3. Create your feature branch
git checkout -b feature/baseline-model

# 4. Confirm you're on the right branch
git branch
```

**Branch naming convention:**
- `feature/baseline-model`
- `feature/api-development`
- `feature/dashboard-filters`

Use descriptive names. Keep them short.

---

### Step 3: Do Your Work

**Work only in your team's folder:**
- DS Team 1: `data_science/team1_churn/`
- DS Team 2: `data_science/team2_recommendation/`
- DS Team 3: `data_science/team3_dashboard_mlops/`

**Commit frequently:**

```bash
git add .
git commit -m "feat: add xgboost baseline model"
```

**Commit message format:**
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation updates

---

### Step 4: Push Your Feature Branch

```bash
git push origin feature/baseline-model
```

Your work is now on GitHub, but not yet merged.

---

### Step 5: Create Pull Request (PR)

1. Go to GitHub: https://github.com/datascience-muhammad/Shopflow_london/pulls
2. Click "New Pull Request"
3. **CRITICAL:** Set base branch to your **team branch** (e.g., `team/ds-churn`), NOT `main`
4. Set compare branch to your feature branch (e.g., `feature/baseline-model`)
5. Add title and description
6. Assign your **team lead** as reviewer
7. Click "Create Pull Request"

---

### Step 6: Team Lead Reviews and Merges

**Team lead:**
1. Reviews the code
2. Checks it works in the team folder
3. Approves the PR
4. Merges it into the team branch using "Squash and merge"

**The feature branch is now part of the team branch.** The individual team member can delete their feature branch.

---

## 5. When Teams Coordinate (Cross-Team Handoffs)

### Day 5: Feature Store Delivery

**What happens:** DS Teams 1 and 2 commit their feature tables to `data_science/feature_store/`.

**Workflow:**
1. Team member creates feature branch from team branch
2. Adds feature table files to `data_science/feature_store/`
3. Updates `feature_store/README.md` with schema
4. Creates PR to team branch
5. Team lead reviews and merges
6. **Coordinate in WhatsApp DS sub-group** before pushing to avoid conflicts

**Rule:** Only ONE team should update `feature_store/README.md` at a time. Check WhatsApp first.

---

### Day 8: API Integration

**What happens:** DS Teams 1 and 2 deploy APIs to Render. Team 3 updates `.env` with URLs.

**Workflow:**
1. Teams 1 and 2 confirm their Render URLs are live
2. Post URLs in WhatsApp DS sub-group
3. Team 3 member creates feature branch
4. Updates `.env` file with Render URLs
5. Creates PR to `team/ds-dashboard-mlops`
6. Team 3 lead reviews and merges

---

## 6. Promoting Team Branches to Dev (PM Team 1 Coordinates)

**When:** After major milestones (Day 5, Day 7, Day 9)

**Who does it:** PM Team 1 (Technical Delivery)

**Process:**

1. PM Team 1 confirms milestone complete with DS team leads
2. PM Team 1 creates PR from team branch to `dev`
3. Example: `team/ds-churn` → `dev`
4. DS Lead reviews the PR
5. DS Lead approves
6. PM Team 1 merges to `dev`

**Important:** All three team branches should be merged to `dev` before the final demo.

---

## 7. Final Merge to Main (End of Sprint)

**When:** Day 10, after demo rehearsal

**Who does it:** PM Lead

**Process:**

1. PM Team 3 delivers written go/no-go
2. If go: PM Lead creates PR from `dev` to `main`
3. DS Lead does final review
4. PM Lead merges to `main`
5. `main` branch now contains the complete, tested sprint deliverable

---

## 8. Folder Ownership — Stay in Your Lane

| Team | Folder | What You Work On |
|------|--------|------------------|
| **DS Team 1** | `data_science/team1_churn/` | Churn model, feature engineering, FastAPI endpoint |
| **DS Team 2** | `data_science/team2_recommendation/` | Recommendation engine, FastAPI endpoint |
| **DS Team 3** | `data_science/team3_dashboard_mlops/` | Streamlit dashboard, mock API, MLOps setup |

**Shared folders** (coordinate before committing):
- `data_science/contracts/` — API contracts (all teams read, coordinate writes)
- `data_science/feature_store/` — Feature tables (Teams 1 & 2 write, Team 3 reads)

**Rule:** Do not edit files outside your team folder unless coordinating with other teams.

---

## 9. Best Practices

### Before You Start Working

```bash
git checkout team/ds-churn
git pull origin team/ds-churn
```

Always pull latest changes from your team branch before creating a feature branch.

---

### Commit Often

Don't wait until everything is perfect. Commit small, logical changes.

```bash
git add data_science/team1_churn/model.py
git commit -m "feat: add initial xgboost model structure"
```

---

### Clear Notebook Outputs

Before committing Jupyter notebooks:

```bash
jupyter nbconvert --clear-output --inplace notebook.ipynb
git add notebook.ipynb
git commit -m "docs: add EDA notebook"
```

This keeps the Git history clean.

---

### Large Files Go to S3

**Do not commit:**
- CSV files larger than 100MB
- Model `.pkl` files larger than 100MB
- Any data files

**Instead:** Upload to S3 and reference the path in your code.

---

### Sync Frequently

Pull from your team branch at least once a day:

```bash
git checkout team/ds-churn
git pull origin team/ds-churn
```

This avoids large merge conflicts later.

---

## 10. Common Git Commands Reference

| Task | Command |
|------|---------|
| See which branch you're on | `git branch` |
| Switch to team branch | `git checkout team/ds-churn` |
| Create feature branch | `git checkout -b feature/my-task` |
| See what changed | `git status` |
| Add files to commit | `git add .` |
| Commit changes | `git commit -m "feat: description"` |
| Push to GitHub | `git push origin feature/my-task` |
| Pull latest changes | `git pull origin team/ds-churn` |
| Delete local feature branch | `git branch -d feature/my-task` |

---

## 11. What to Do When Something Goes Wrong

### "I committed to the wrong branch"

If you haven't pushed yet:
```bash
git reset --soft HEAD~1  # Undoes last commit, keeps changes
git checkout correct-branch
git add .
git commit -m "your message"
```

If you already pushed, ask your team lead or DS Lead for help.

---

### "I have merge conflicts"

1. Pull latest changes: `git pull origin team/ds-churn`
2. Git will show which files have conflicts
3. Open the files and look for `<<<<<<<` markers
4. Edit the file to keep the correct version
5. Remove the conflict markers
6. `git add .`
7. `git commit -m "fix: resolve merge conflict"`

If stuck, ask your team lead.

---

### "I accidentally worked on main"

**Stop immediately.** Do not push.

1. Create a new branch: `git checkout -b feature/my-work`
2. Your changes move to the new branch
3. Switch back: `git checkout main`
4. Pull clean main: `git pull origin main`
5. Continue from your feature branch

---

## 12. Decision Authority

| Decision | Who Decides |
|----------|-------------|
| Which team member works on which task | DS Team Lead |
| When to merge feature branch to team branch | DS Team Lead |
| When to promote team branch to dev | PM Team 1 + DS Lead |
| When to merge dev to main | PM Lead + DS Lead |
| Code quality and technical approach | DS Lead |

**Team leads have full authority** to manage work within their team branch. No need to escalate every decision.

---

**Summary:** Each team works in their own team branch. Individual members create feature branches for specific tasks. Team leads review and merge within the team. PM Team 1 coordinates cross-team merges to `dev`. Main branch stays locked until final demo.
