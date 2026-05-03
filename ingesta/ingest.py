import boto3
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os

DB_URL = os.getenv("DATABASE_URL")
S3_BUCKET = os.getenv("S3_BUCKET")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

def ingest():
    print("Conectando a MySQL...")
    engine = create_engine(DB_URL)
    
    print("Extrayendo datos...")
    df_users = pd.read_sql("SELECT * FROM users", engine)
    df_profiles = pd.read_sql("SELECT * FROM user_profiles", engine)
    
    print(f"Usuarios encontrados: {len(df_users)}")
    print(f"Perfiles encontrados: {len(df_profiles)}")
    
    s3 = boto3.client(
        's3',
        region_name=AWS_REGION,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN")
    )
    
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("Subiendo users a S3...")
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=f"usuarios/users_{ts}.csv",
        Body=df_users.to_csv(index=False)
    )
    
    print("Subiendo perfiles a S3...")
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=f"usuarios/profiles_{ts}.csv",
        Body=df_profiles.to_csv(index=False)
    )
    
    print(f"✅ Listo! {len(df_users)} usuarios y {len(df_profiles)} perfiles subidos a S3")

if __name__ == "__main__":
    ingest()
