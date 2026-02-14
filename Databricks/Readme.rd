🚀 Instagram End-to-End Predictive Analytics Pipeline
🎵 Project Theme: 2016 2.0 - High Energy, Big Data, No Regrets
An enterprise-grade data intelligence platform built on Databricks that processes 1.5M records to predict user behavior, stress levels, and lifestyle segments using a modular Medallion Architecture.

🏗️ Technical Architecture (Medallion Pattern)
The project utilizes a multi-layered storage strategy to ensure data reliability and high-performance analytics.

Bronze Layer (Raw): Ingests 1.5M original records as Delta tables directly from source ingestion (Kaggle CSV/JSON).

Silver Layer (Validated): Performs deduplication, schema enforcement, and error handling to remove invalid data.

Gold Layer (Star Schema): Organizes data into specific Dimension and Fact tables (dim_users, fact_engagement, etc.) optimized for business logic.

Intelligence Layer (ML): Executes three predictive models in parallel to generate stress categories, engagement scores, and user personas.

🛠️ Tech Stack & Orchestration
Data Lakehouse: Databricks & Delta Lake.

Compute Engine: Apache Spark (PySpark).

Orchestration: Databricks Job YAML with parallel task execution.

Machine Learning: Scikit-Learn with MLflow for experiment tracking.

Polyglot Persistence: Apache Cassandra (Fact storage) and Amazon SimpleDB (Metadata management).

Environment: Docker (for local Cassandra/SimpleDB instances).

🧠 Machine Learning Insights
Our pipeline triggers three specialized models simultaneously to turn raw usage data into actionable signals:

Stress Classifier: Predicts High/Medium/Low Stress categories using behavioral and health metrics.

Engagement Forecaster: A regression model predicting numeric user_engagement_score.

User Persona Segmenter: K-Means clustering to identify distinct user archetypes.

🚀 The "Omnitrix" Pipeline Execution
The entire system is managed through a Job Orchestra:

Nuke Task: A safety-coded reset script (nuke.py) to purge existing tables and start fresh.

ETL Flow: Automated movement through Bronze, Silver, and Gold tasks.

Parallel ML: Parallel execution of Stress, Engagement, and Segmenter notebooks to optimize compute.

Joiner: Consolidates all model outputs into a final table for Power BI ingestion.

📊 Business Intelligence (Power BI)
The final output is a high-performance Power BI Dashboard connected via Databricks SQL.

Executive Summary: High-level view of 1.5M users across countries.

Security Maturity: Visualization of 2FA and Biometric login adoption.

Behavioral Heatmaps: Correlating Instagram active minutes with predicted stress categories.

🎓 Lessons Learned
Task Concurrency: Optimized Job YAML to run multiple ML models in parallel, significantly reducing runtime.

Data Integrity: Implemented strict Silver-layer validation for large-scale (1.5M) datasets.

Schema Design: Designed a robust Star Schema ERD to support complex Power BI filtering.

🥇 Author
Ayush M Rawat

Role: Lead Data Architect [Illustration]

Focus: Big Data, ML Engineering