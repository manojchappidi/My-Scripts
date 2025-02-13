import os
import shutil
import smtplib
from datetime import datetime
import subprocess
import time

# Configurations
localFolder = r"<path-to-images-folder>"
verifiedFolder = r"<path-to-verified-folder>"
syncedFolder = r"<path-to-synced-folder>"
bucketPath = "s3://<S3-bucket/path>"

# Email settings
fromEmail = "<mention-SMTP-from-email-address>"
toEmail = "<mention-SMTP-to-email-address>"
smtpServer = "smtp.gmail.com"
smtpPort = 587
smtpUser = "<mention-from-email-address>"
smtpPass = "<mention-SMTP-server-password>"

# Log file path
log_file = r"<path-to-logs-folder>"

# Function to append custom log entries
def append_log(message):
    with open(log_file, 'a') as f:
        f.write(message + '\n')

# Email notification function
def send_email(subject, message):
    try:
        with smtplib.SMTP(smtpServer, smtpPort) as server:
            server.starttls()
            server.login(smtpUser, smtpPass)
            email_message = f"Subject: {subject}\n\n{message}"
            server.sendmail(fromEmail, toEmail, email_message)
    except Exception as e:
        append_log(f"Failed to send email: {str(e)}")

# Function to upload to AWS S3 using aws CLI
def upload_to_s3(source_folder, bucket):
    try:
        # Run the aws s3 cp command to copy files recursively
        command = f'aws s3 cp "{source_folder}" {bucket} --recursive'
        subprocess.check_call(command, shell=True)
        append_log(f"Copied files from {source_folder} to AWS S3 bucket {bucket}")
    except subprocess.CalledProcessError as e:
        append_log(f"Error copying files to AWS S3: {str(e)}")
        send_email("Error uploading to AWS S3", f"Error while uploading files to AWS S3: {str(e)}")

# Function to send delayed email alerts
def send_delayed_email(subject, message, delay_in_seconds):
    time.sleep(delay_in_seconds)
    send_email(subject, message)

# Main function to process images
def process_images():
    try:
        # Log the start of a new execution
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        append_log(f"\n------------------------ {now} ------------------------")
        
        for root, _, files in os.walk(localFolder):
            oir_files = [f for f in files if f.endswith('.oir')]
            for oir_file in oir_files:
                base_name = oir_file.replace('.oir', '')
                checksum_file = f"{base_name}.checksum"
                hdf5_file = f"{base_name}.oir.hdf5"
                
                # Check if all required files are present
                if checksum_file in files and hdf5_file in files:
                    required_files = [oir_file, checksum_file, hdf5_file]
                    append_log(f"All required files found for {base_name}: {required_files}")
                    
                    # Move files to verified folder
                    for file in required_files:
                        shutil.move(os.path.join(localFolder, file), os.path.join(verifiedFolder, file))
                    append_log(f"Moved files from {localFolder} to {verifiedFolder}")
                    
                    # Upload to AWS S3 using aws CLI
                    upload_to_s3(verifiedFolder, bucketPath)
                    
                    # Move files to synced folder
                    for file in required_files:
                        shutil.move(os.path.join(verifiedFolder, file), os.path.join(syncedFolder, file))
                    append_log(f"Moved files from {verifiedFolder} to {syncedFolder}")
                    
                    # Scenario 1: Delayed email if files are only in the verified folder
                    send_delayed_email(
                        "Images moved to Verified Folder but not uploaded to Synced Folder",
                        f"Images for {base_name} have been moved to the Verified folder but not uploaded to the Synced folder within 1 hour.",
                        delay_in_seconds=3600  # 1 hour delay
                    )

                    # Scenario 2: Delayed email if files are in synced folder but not uploaded to S3
                    send_delayed_email(
                        "Images moved to Synced Folder but not uploaded to AWS S3",
                        f"Images for {base_name} have been moved to the Synced folder but not uploaded to AWS S3 within 1 hour.",
                        delay_in_seconds=3600  # 1 hour delay
                    )
                else:
                    # If not all files are present, send an email and log the error
                    present_files = [f for f in [oir_file, checksum_file, hdf5_file] if f in files]
                    missing_files_message = (
                        f"Missing files in folder: {localFolder}.\n\n"
                        f"Found: {present_files}\n\n"
                        "Please upload all required files."
                    )
                    send_email("Missing files", missing_files_message)
                    append_log(f"Missing files for {base_name}. Present files: {present_files}")
                    continue

        append_log("                                  !!! The script is successfully executed !!!")
        append_log("----------------------------------------------------------------------------------------\n")
    except Exception as e:
        send_email("Script error", f"An error occurred while processing images: {str(e)}")
        append_log(f"An error occurred: {str(e)}")
        append_log("----------------------------------------------------------------------------------------\n")

if __name__ == "__main__":
    process_images()
