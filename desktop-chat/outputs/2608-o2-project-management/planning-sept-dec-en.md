# Planning, September to December (English translation)

## Infrastructure and platform

**September**
- Stand up the target environment (a second workspace).
- Connect the CRM system.
- Connect SharePoint.
- Connect the EPM system (read as Workday's EPM module, Workday Adaptive Planning. Unconfirmed, check the tool name).

**October**
- Provision the data platform's catalogs as infrastructure as code, using Terraform.
- Build a validation environment for testing.

**November**
- Generate the dev, staging and prod environments.

## Engineering

**October**
- Configure Unity Catalog (Databricks' data governance and catalog layer).
- Build the Power BI import workflow.
- Set up CI/CD pipelines.

**November**
- Build the cost and usage tracking model.

**December**
- Review the cost dashboard with CG (read as Contrôle de Gestion, financial controlling or FP&A. Unconfirmed, check the team).

## Slice: Whoz, CRM, SmartRecruiters

**September**
- Build the Power BI report for Whoz (a staffing and resource management platform).
- Build the Power BI report for SmartRecruiters (the applicant tracking system).
- Reuse the existing Bronze and Silver pipeline for SharePoint data (medallion architecture: raw then cleaned layers).
- Validate SmartRecruiters as a data source.
- Validate TBP as a data source (acronym unclear from context, check what TBP refers to).
- Validate the Whoz Staff & Deploy module as a data source.

**October**
- Build Bronze and Silver pipelines covering SmartRecruiters, TBP and Whoz Staff & Deploy, landing through SharePoint.
- Import and map fields for the SmartRecruiters Power BI report.
- Import and map fields for the Whoz Search & Match Power BI report.
- Import and map fields for the Whoz Staff & Deploy Power BI report.
- Write specifications.

**November**
- Review and sign off the reports.

## Slice: APP, EPM

This plan is indicative and will be reassessed once the use case task is finished.

**September**
- Define BI and AI use cases.
- Validate EPM as a data source.

**October**
- Build the Bronze layer pipeline for EPM data.
- Design the Gold layer schema and write specifications.

**November**
- Build the dashboard.

**December**
- Review and sign off the reports.

## Slice: Skill-up, Lucca

**October**
- Define BI and AI use cases.
- Validate Skill-up as a data source (skills and competency management tool).
- Validate Lucca as a data source (HR software suite).

**November**
- Land raw source data (ingestion into the landing zone).
- Build the Bronze and Silver pipelines.
- Design the Gold layer schema and write specifications.

**December**
- Build the dashboard.
- Review and sign off the dashboard.

## Project management

**September**
- Create the project tracking board.
- Hand over from or to Elijah.
- Hand over from or to Thiané.
- Onboard and assess Farez Dossou Gbété.
- Onboard and assess Tom Perez Le Tiec.

**Definitions used throughout**
- Validation means the project team reviews and approves deliverables, with adjustments as needed.
- Verification means the business reviews and approves deliverables, with adjustments as needed.

**Open points**
- TBP as a source name is not resolved.
- CG as the reviewing team for the cost dashboard is not resolved.
