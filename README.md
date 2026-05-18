<img width="2427" height="1076" alt="image" src="https://github.com/user-attachments/assets/aaadfc21-dd06-4d71-852a-bfe87c9e03a9" />
GTM Engine

Developed a production-grade, secure data pipeline and analytics infrastructure designed to unify Scope 3 supply chain intelligence with B2B SaaS revenue operations. This engine breaks down data silos between cloud data warehouses and CRM environments, empowering Account Executives (AEs) to deliver value-based ROI narratives, automate account prioritization, and eliminate multi-million dollar regulatory tariff risks directly inside Salesforce.

🛠️ The Core Infrastructure Tech Stack

Data Engineering & Extraction: Python 3.11, Pandas, Requests, Dotenv, Logging

Third-Party Data Enrichment: Climatiq Global Carbon Registry REST API

Cloud Data Warehousing: AWS RDS (PostgreSQL Instance), SQLAlchemy

Enterprise CRM & Business Intelligence: Salesforce, CRM Analytics (CRMA / Tableau CRM)

Security & Compliance: SSL-encrypted database tunneling, secure .env credential isolation


🏗️ Architecture Pipeline Blueprint

+------------------------+      Secure REST API      +-----------------------+
|  Climatiq Carbon API   | <=======================> |  Python ETL Pipeline  |
+------------------------+                           +-----------------------+
                                                                 │
                                                                 
                                                       Bulk Write via SSL Mode
                                                       
                                                                 ▼
+------------------------+     JDBC Native Connect    +-----------------------+
| Salesforce CRMA Engine | <========================> | AWS RDS (PostgreSQL)  |
+------------------------+                            +-----------------------+
