# Event-Driven/Semi-Automated YouTube (Ind) Trending Videos Data Pipeline

An end-to-end, serverless cloud data pipeline built on AWS to automate cleaning, transformation and storing data on Amazon S3, and analytical querying of YouTube India's trending video datasets.

## ☁️ Architecture & Data Flow

1. **Storage (Bronze Layer):** Raw daily trending CSV datasets containing multi-language metadata (Hindi/English) are uploaded to an Amazon S3 Landing zone.
2. **Compute (Serverless ETL):** An event-driven **AWS Lambda** function triggers instantaneously upon file discovery, executing cleaning and schema standardization and validation via a resilient Python engine.
3. **Storage (Silver/Gold Layer):** The cleaned, structured data is compressed into **Snappy-Parquet** format and saved back to a processed S3 folder.
4. **Data Cataloging:** An **AWS Glue Crawler** scans the processed layer to dynamically infer data types and manage schema drift.(We need to trigger after the cleaned data is saved. Since this is event based keeping the glue crawlers on may be risky and not cost efficient or free.)
5. **Analytics Layer:** **Amazon Athena** functions as the serverless query engine to run SQL analytics directly on top of the S3 Data Lake.

---

## 🛠️ Tech Stack & Services
* **Languages:** Python (Pandas, AWS Wrangler), SQL
* **Cloud Platform:** Amazon Web Services (AWS)
* **Compute:** AWS Lambda (Serverless)
* **Storage & Catalog:** Amazon S3, AWS Glue Data Catalog, Glue Crawlers
* **Analytics:** Amazon Athena

---

## 🚀 Key Engineering & Architecture

* **Generic Resilient Ingestion:** Shifted from hardcoded column tracking to a fully dynamic data engine. The pipeline automatically sanitizes arbitrary column configurations into standardized `lowercase_with_underscore` formats.
* **Character Encoding Resilience:** Implemented multi-stage encoding handlers (`UTF-8` falling back to `Latin-1`) to process complex regional multi-language text characters (e.g., Hindi titles) seamlessly without system crashes.
* **Cost & Query Performance Optimization:** Converted CSV data into an industry-standard columnar **Parquet format**, dropping downstream Athena scan metrics and saving storage space.
* **Global Data Quality Management:** Automated full-row profiling to trap structural anomalies, dynamically filling text anomalies with `'NA'` and numeric null values with `0` globally.

---

## 📂 Repository Structure
```text
├── README.md
├── src/
│   └── lambda_function.py       # Resilient Generic Cleaning Logic (Version 2)
