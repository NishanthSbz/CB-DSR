import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

# Initialize AWS S3 client
def init_s3_client():
    try:
        return boto3.client('s3')
    except (NoCredentialsError, PartialCredentialsError):
        st.error("AWS credentials not found. Please configure your AWS credentials.")
        return None

# Function to upload data to S3
def upload_to_s3(file, bucket_name, object_name, s3_client):
    try:
        s3_client.upload_fileobj(file, bucket_name, object_name)
        return True
    except NoCredentialsError:
        st.error("Credentials not available.")
        return False
    except ClientError as e:
        st.error(f"Failed to upload file: {e}")
        return False

# Function to download data from S3
def download_from_s3(bucket_name, object_name, download_path, s3_client):
    try:
        s3_client.download_file(bucket_name, object_name, download_path)
        return True
    except NoCredentialsError:
        st.error("Credentials not available.")
        return False
    except ClientError as e:
        st.error(f"Failed to download file: {e}")
        return False

# Streamlit app
st.title("Cloud Disaster Recovery System")

# Initialize S3 client
s3_client = init_s3_client()

if s3_client:
    # Configuration
    bucket_name = st.text_input("S3 Bucket Name:")
    backup_path = st.text_input("Backup Path (S3 object name):")
    restore_path = st.text_input("Restore Path (local path):")

    # Backup data
    st.header("Backup Data")
    file_to_backup = st.file_uploader("Choose a file to backup")

    if st.button("Backup to Cloud"):
        if file_to_backup is not None and bucket_name and backup_path:
            success = upload_to_s3(file_to_backup, bucket_name, backup_path, s3_client)
            if success:
                st.success("File backed up successfully!")
        else:
            st.error("Please provide all the necessary details.")

    # Recover data
    st.header("Recover Data")
    object_to_recover = st.text_input("Object to Recover from Cloud (S3 object name):")

    if st.button("Recover from Cloud"):
        if object_to_recover and bucket_name and restore_path:
            success = download_from_s3(bucket_name, object_to_recover, restore_path, s3_client)
            if success:
                st.success("File recovered successfully!")
        else:
            st.error("Please provide all the necessary details.")
