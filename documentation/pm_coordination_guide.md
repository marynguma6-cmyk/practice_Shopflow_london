# Project Management Coordination & Implementation Guide

**ShopFlow Customer Intelligence Platform — 2-Week Sprint**  
**Project:** ShopFlow by PrimeCart Inc.  
**Audience:** PM Lead, PM Team 1 (Technical Delivery), PM Team 2 (Business Delivery), PM Team 3 (QA and Documentation)  
**Repository Path:** `documentation/pm_coordination_guide.md`

---

## Before You Start: Understanding the PM Role in This Sprint

This is not an administrative role. Each PM team is directly connected to a DS team's ability to deliver.

- **PM Team 1** keeps the development environment running so DS teams can focus on modeling.
- **PM Team 2** ensures what gets built is tied to real business outcomes.
- **PM Team 3** is the quality gate before anything reaches the demo.
- **The PM Lead** manages everything that crosses team boundaries.

The DS teams work through a defined sequence of handoffs — contracts, feature store, model staging, API integration, and demo. PM teams are active participants at every one of those handoffs, not observers. This guide maps exactly what that looks like, day by day.

This guide does not repeat what is in `team_responsibilities.md` (ownership) or `repository_collaboration.md` (Git workflow). It answers a different question: at exactly which point does each PM team act, and what does that action look like in practice?

---

## Part 1: Team Responsibilities at a Glance

| Team                                 | Primary DS Relationship   | Core Focus                                                            |
| :----------------------------------- | :------------------------ | :-------------------------------------------------------------------- |
| **PM Team 1 — Technical Delivery**   | DS Teams 1 and 2          | Environment setup, integration support, GitHub progress monitoring    |
| **PM Team 2 — Business Delivery**    | DS Teams 1 and 2, DS Lead | KPI alignment, business impact translation, stakeholder communication |
| **PM Team 3 — QA and Documentation** | DS Team 3                 | Model validation, API testing, documentation, demo coordination       |

Each PM team has a primary DS relationship, but coordination between PM teams is frequent — particularly at handoff points. Part 3 describes exactly where those cross-PM interactions happen.

---

## Part 2: How PM and DS Teams Connect

Understanding which PM team is responsible for which part of the DS workflow is essential before reading the handoff details.

---

## Part 3: PM Role at Each Sprint Handoff

There are seven handoff points across the 10-day sprint where PM coordination is critical. Each one is described below with the specific action each PM team takes.

### Handoff 1 — Days 1 and 2: Contract Session

**What is happening:** All three DS teams agree on the exact structure of every API response and shared data output before any development begins. This is the most important alignment moment of the sprint. Full contract details are in `ds_coordination_guide.md`.

**PM Team 1:**

- Attend the full session and document the agreed contracts in Confluence under the Technical Decisions log
- Confirm the contracts are committed to `data_science/contracts/` in GitHub before end of Day 2
- If DS teams cannot reach agreement or the session overruns, notify PM Lead immediately.

**PM Lead:**

- Protect the time for this session — it must be completed by end of Day 2
- Facilitate only if DS teams cannot reach agreement independently
- Confirm with PM Team 1 at end of Day 2 that contracts are committed and documented

### Handoff 2 — Day 3: MLflow Server Confirmation

**What is happening:** DS Team 3 sets up the shared MLflow tracking infrastructure on Dagshub (a free cloud service). All three DS teams log experiments to the same Dagshub project. If Teams 1 and 2 log to separate local instances instead, experiment history is fragmented and cross-team model comparison becomes impossible.

**PM Team 1:**

- At the Day 3 morning standup, confirm with DS Team 3 that the Dagshub MLflow project is live
- Confirm DS Teams 1 and 2 have the tracking URL and credentials and can connect
- Mark the Jira milestone "MLflow server live" complete only when all three DS teams confirm they can log test runs
- If the Dagshub setup is not complete by Day 3, escalate to PM Lead — this is a sprint-level blocker

### Handoff 3 — Day 5: Feature Store Delivery

**What is happening:** DS Teams 1 and 2 commit their engineered feature tables to `data_science/feature_store/`. DS Team 3 pulls these tables to build dashboard visualisations. A late or undocumented delivery directly impacts Team 3's Week 2 timeline.

**PM Team 1:**

- Track this as a hard Day 5 milestone in Jira
- By end of Day 4, confirm with DS Teams 1 and 2 that the feature tables are on track
- If either team will be delayed, notify PM Team 3 and DS Team 3 immediately so they can adjust.

**PM Team 3:**

- On Day 6 morning, confirm with DS Team 3 that the feature tables have been pulled successfully
- If there are schema issues — wrong column names, missing `customer_id`, undocumented fields — flag to PM Team 1 to resolve with the relevant DS team

### Handoff 4 — Day 7: Model Staging and DS Lead Review

**What is happening:** DS Teams 1 and 2 promote their best-performing models to Staging in the shared MLflow registry. The DS Lead conducts a formal review before Production approval. This is the last gate before API endpoints are built.

**PM Team 1:**

- Track MLflow Staging promotion for both DS teams as Day 7 milestones in Jira
- If either team has not promoted by end of Day 7, flag to PM Lead

**PM Team 2:**

- Attend or review the DS Lead's model review session
- Translate model metrics into business terms for the final presentation: what does an AUC of 0.78 mean in customers retained? What does a recommendation score translate to in revenue?
- Begin drafting the business impact section of the final presentation

**PM Lead:**

- Confirm the DS Lead has reviewed and approved Staging models before Day 8 begins
- API endpoint development does not start before DS Lead sign-off on Staging.

### Handoff 4.5 — Day 7-8: API Deployment to Render

**What is happening:** DS Teams 1 and 2 transition from local development (ngrok) to deploying their final APIs to Render for stable, permanent URLs. This happens between the model Staging promotion and final integration testing.

**PM Team 1:**

- Confirm DS Teams 1 and 2 have their `requirements.txt` files ready and pushed to GitHub
- Verify both teams have created free Render accounts
- Track "Deploy to Render" as a Day 7-8 task in Jira for both DS teams
- Once deployed, verify the Render URLs are accessible and functional before notifying PM Team 3

**PM Team 3:**

- Prepare to receive the Render URLs from Teams 1 and 2
- Update integration test plan to use Render URLs instead of ngrok URLs

### Handoff 5 — Day 8: Real API Integration

**What is happening:** DS Teams 1 and 2 have deployed their FastAPI endpoints to Render with permanent public URLs. DS Team 3 switches the dashboard from mock data to live API responses. This is the integration moment the entire Week 1 contract-first approach was designed to enable smoothly.

**PM Team 1:**

- Confirm with DS Teams 1 and 2 that their endpoints are deployed to Render, accessible via public URL, and have been tested in Postman against the agreed contracts
- Confirm the Render URLs are stable and not spinning down unexpectedly
- Coordinate the timing with DS Team 3 — the switch does not happen until Teams 1 and 2 have confirmed their Render endpoints are contract-compliant
- Create a Jira subtask for "API integration swap" and mark it complete only when DS Team 3 confirms the dashboard is pulling live data from Render

**PM Team 3:**

- Once the switch is confirmed, begin the QA checklist: response times (note: first request after idle may take 30 sec on Render free tier), JSON validity, error handling, and dashboard rendering
- Test that Render URLs are publicly accessible and stable
- Any failures are logged as GitHub Issues and communicated to PM Team 1 as immediate blockers
- If an endpoint is not deployed to Render by Day 8, DS Team 3 remains on mock data. PM Lead decides whether to extend or proceed with a mock for the demo. The decision is documented in Confluence.

### Handoff 6 — Days 9 and 10: QA Sign-Off and Demo Readiness

**What is happening:** PM Team 3 completes the full QA checklist and provides a written go/no-go to PM Lead. PM Lead coordinates the final demo environment and brief.

**PM Team 3:**

- Complete all items in the QA checklist (detailed in Part 5)
- Deliver a written go/no-go to PM Lead by end of Day 9
- All open issues are logged as GitHub Issues with priority levels assigned

**PM Team 2:**

- Final business narrative and metrics are ready for the demo presentation
- Brief PM Lead on which outcomes to highlight for stakeholders

**PM Lead:**

- Review the go/no-go from PM Team 3
- Confirm the demo runs from a stable environment, not the active development setup
- Conduct a demo rehearsal on Day 10 before the actual presentation

---

## Part 4: Day-by-Day Sprint Plan

The table below shows what each PM team is doing each day alongside the DS sprint. **Bold** entries are sprint milestones that must be confirmed complete and communicated to the PM Lead.

| Day    | PM Lead                                                | PM Team 1 — Technical                                                                          | PM Team 2 — Business                                                                        | PM Team 3 — QA and Docs                                                |
| :----- | :----------------------------------------------------- | :--------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------- |
| **1**  | Facilitate contract session                            | Attend contract session. Begin documenting in Confluence.                                      | Review project objectives and KPI framework                                                 | Set up Jira board and sprint milestones                                |
| **2**  | Confirm contracts committed by end of day              | Confirm contracts in `data_science/contracts/`. Confirm S3 access and local environment setup. | Begin stakeholder update draft                                                              | Draft API and model card templates                                     |
| **3**  | Confirm MLflow server live                             | Verify all DS teams can connect to MLflow. Update Jira milestone.                              | Validate feature alignment with business KPIs                                               | Review EDA outputs for data quality flags                              |
| **4**  | Daily standup facilitation                             | Monitor DS Teams 1 and 2 feature engineering progress via PR activity                          | Document stakeholder requirements                                                           | Begin populating model card templates                                  |
| **5**  | Confirm feature store delivery                         | Check both teams on track. Notify PM3 and DS3 immediately if delayed.                          | Draft mid-sprint stakeholder update                                                         | Confirm on Day 6 that DS Team 3 can pull feature tables                |
| **6**  | Monitor sprint velocity                                | Track PR activity on `team/ds-churn` and `team/ds-recommendation`                              | Review model output framing in business language                                            | Begin integration test plan                                            |
| **7**  | Confirm Staging promotions and DS Lead review complete | Track MLflow Staging milestone for both DS teams in Jira                                       | Attend model review. Translate metrics to business outcomes. Begin business impact section. | Finalise QA checklist                                                  |
| **8**  | Coordinate API integration swap                        | Confirm endpoints live and contract-tested. Coordinate timing with DS Team 3.                  | Prepare business impact section of final presentation                                       | Begin QA on integrated dashboard. Log all issues in GitHub.            |
| **9**  | Review go/no-go from PM Team 3                         | Monitor end-to-end testing across all DS teams                                                 | Finalise business narrative and demo metrics                                                | Deliver written go/no-go to PM Lead. All open issues logged in GitHub. |
| **10** | Demo rehearsal and final coordination                  | Confirm Render APIs are live and stable for demo                                               | Final presentation confirmed                                                                | Demo environment confirmed stable                                      |

---

## Part 5: QA Responsibilities (PM Team 3)

PM Team 3 owns quality assurance across the sprint. QA preparation begins in Week 1 and active testing runs through Week 2.

### Week 1 — Preparation

- Review EDA findings from DS teams for data quality concerns
- Flag issues with feature engineering logic or missing schema documentation to PM Team 1
- Set up the QA issues log in Confluence and agree on GitHub Issues labelling conventions

### Week 2 — Active QA Checklist

**API Validation**

- [ ] Endpoints return valid JSON responses that conform to the agreed contracts
- [ ] Response time is below 300ms across a minimum of 100 consecutive requests
- [ ] Error handling covers edge cases: missing features, invalid customer IDs, empty responses
- [ ] API documentation reflects actual endpoint behaviour

**Model Accuracy Audit**

- [ ] Independently verify Precision and Recall on the holdout test set
- [ ] Confirm AUC score meets the target: Churn model above 0.75
- [ ] Review confusion matrices to confirm class imbalance has been addressed

**Dashboard Validation**

- [ ] All visualisations render correctly with no broken panels
- [ ] Real-time predictions display without noticeable lag
- [ ] Dashboard loads within 5 seconds

**Documentation Review**

- [ ] Model cards include methodology, feature list, and performance metrics
- [ ] Feature store README is complete with all column descriptions
- [ ] Deployment guide covers ngrok setup and Render deployment steps

_All QA findings are logged as GitHub Issues: `bug` for broken functionality, `docs` for documentation gaps, `enhancement` for non-blocking improvements._

---

## Part 6: GitHub — What PMs Do Without Writing Code

PMs are not expected to write or review code. GitHub is nonetheless a key coordination tool that each PM team uses actively throughout the sprint.

**PM Team 1 — Monitor Pull Request Activity**
The most reliable signal of DS team progress is PR activity on the `team` branches. Check that feature branches are being opened, reviewed, and merged at a reasonable cadence. A branch with no new commits for more than one working day during an active sprint period typically indicates a blocker — raise it at standup. Review the activity, not the code.

**PM Team 3 — Log QA Issues as GitHub Issues**
QA findings are logged in GitHub Issues, not communicated only through WhatsApp. Each issue must include a label, a description of expected versus actual behaviour, and the relevant endpoint or component. This creates a traceable record for the DS Lead to prioritise fixes.

**PM Lead — Monitor the `dev` Branch**
The `dev` branch is where team branches are periodically merged for integration testing. If no team branches have been merged into `dev` by Day 6, the sprint is behind schedule. Merge conflicts in `data_science/contracts/` or `data_science/feature_store/` require immediate attention and must be flagged to the DS Lead.

---

## Part 7: Communication Structure

### WhatsApp Groups

WhatsApp is the primary communication channel for this sprint. The team is organised across three groups:

- **General Group** — sprint-wide announcements, milestone confirmations, and cross-team updates. The PM Lead is the primary voice here. All major decisions and milestone completions are posted here so both PM and DS teams are aligned.
- **PM Sub-Group** — internal PM coordination, Jira updates, escalation discussions, and daily standup preparation before the full team session
- **DS Sub-Group** — technical updates between DS teams on model progress, endpoint status, and integration notes. PM Team 1 should be active here to stay close to DS progress without disrupting DS working time.

_All formal decisions, blockers, and milestone confirmations are documented in Confluence regardless of which WhatsApp group the discussion happened in. WhatsApp is for speed and day-to-day coordination; Confluence is the permanent record._

### Morning Standup — 15 Minutes

The standup is a blocker-clearing exercise, not a status report. If nothing is blocked, it ends early.

- **Minutes 1–5:** Each DS team lead gives one sentence — completed yesterday, planned today, any blockers. PM teams listen and note anything requiring action.
- **Minutes 6–10:** PM Team 1 on infrastructure and integration status. PM Team 2 on any business or stakeholder updates that affect priorities. PM Team 3 on QA status and open issues.
- **Minutes 11–15:** Active blockers only. PM Lead resolves priority conflicts. Anything requiring more than two minutes moves to a separate call.

### End-of-Day Sync — 10 Minutes

PM Team 1 updates the Jira board at end of day. Any risk that emerged during the day is flagged to the PM Lead in the PM sub-group before close. No blocker carries forward to the next morning without PM Lead awareness.

---

## Part 8: Tools and Platforms Reference

### Project Management

| Tool           | Purpose                                                                 |
| :------------- | :---------------------------------------------------------------------- |
| **Jira**       | Sprint board, task tracking, milestone management, burn-down chart      |
| **Confluence** | Documentation hub — decisions log, standup notes, QA log, demo runsheet |
| **GitHub**     | Code repository, PR tracking, QA issue logging                          |
| **WhatsApp**   | Day-to-day communication across General, PM, and DS sub-groups          |

### Jira Sprint Board

PM Team 1 maintains the Jira board throughout the sprint using the following column structure:
`BACKLOG` -> `TO DO` -> `IN PROGRESS` -> `IN REVIEW` -> `BLOCKED` -> `DONE`

Ticket labelling follows a consistent convention:

- `ds-team1`, `ds-team2`, `ds-team3` identify the owning DS team
- `pm-team1`, `pm-team2`, `pm-team3` identify the owning PM team
- `cross-team` applies to anything requiring coordination between two or more teams
- `blocker` marks anything actively preventing another ticket from progressing

**Sprint milestones are tracked as epics and align directly with the handoff points in Part 3:**

- Contracts committed — Day 2
- MLflow server live — Day 3
- Feature store populated — Day 5
- Models in Staging — Day 7
- API integration complete — Day 8
- QA sign-off — Day 9
- Demo ready — Day 10

### Confluence Documentation

PM Team 3 owns the Confluence space. The following pages are maintained throughout the sprint:

| Page                      | Owner                | Cadence                         |
| :------------------------ | :------------------- | :------------------------------ |
| Sprint overview and goals | PM Lead              | Set at start, updated as needed |
| Daily standup notes       | PM Team 1 (rotating) | After every standup             |
| Technical decisions log   | PM Team 1            | Same day a decision is made     |
| Business impact tracker   | PM Team 2            | End of each week                |
| QA issues log             | PM Team 3            | Ongoing from Day 7              |
| Final demo runsheet       | PM Team 3            | Complete by Day 9               |

At the end of the sprint, the Confluence space is the primary record of how the project was managed.

---

## Part 9: Managing Delays and Blockers

If a DS team is behind on a deliverable that another team depends on, the relevant PM team flags it at the **next morning standup** — naming the specific deliverable, the team responsible, and the day it was due. The PM Lead is informed immediately.

The DS Lead makes the call on any technical or scope adjustment needed. The PM Lead makes the call on any timeline or demo adjustment. No blocker carries forward more than one working day without both leads being aware.

If a live endpoint is not ready by Day 9, the demo proceeds with mock data. This is an acceptable and documented outcome provided it is communicated to stakeholders clearly and noted in the demo runsheet.

---

_For DS team handoffs and the contract-first approach, refer to:_ `ds_coordination_guide.md`  
_For Git and branching workflow, refer to:_ `repository_collaboration.md`  
_For team ownership and responsibilities, refer to:_ `team_responsibilities.md`  
_For full project specifications, model targets, and API details, refer to:_ `project_reference_guide.md`
