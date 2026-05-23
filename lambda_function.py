import awswrangler as wr
import pandas as pd
import urllib.parse
import os

def lambda_handler(event, context):
    try:
        #Getting the bucket and file name from the event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        
        #Ingestion and Handling Multi-language/Hindi Encoding
        #Try UTF-8, then fallback to latin-1 to avoid UnicodeDecodeErrors
        try:
            df = wr.s3.read_csv(path=f"s3://{bucket}/{key}", encoding='utf-8')
        except:
            df = wr.s3.read_csv(path=f"s3://{bucket}/{key}", encoding='latin-1')

        #Clean Column Names Lowercase
        df.columns = [c.lower().replace(' ', '_').replace('.', '_').strip() for c in df.columns]

        #Null Handling Any Column, Any Position
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64']:
                df[col] = df[col].fillna(0)
            else:
                df[col] = df[col].fillna('NA')

        #Standadised Datetime
        #If a column name has 'date' or 'time', we try to convert it
        for col in df.columns:
            if 'date' in col or 'time' in col:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        #Deduplication
        df = df.drop_duplicates()

        #Converting as Parquet
        output_path = f"s3://{bucket}/processed/{key.split('/')[-1].replace('.csv', '.parquet')}"
        wr.s3.to_parquet(
            df=df,
            path=output_path,
            dataset=True,
            mode="overwrite"
        )

        return {"status": "Success", "path": output_path}

    except Exception as e:
        print(f"Error: {str(e)}")
        raise e
