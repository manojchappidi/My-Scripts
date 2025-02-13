import os
import re
import shutil
import logging
from datetime import datetime

# Set to track already created remote folders
created_remote_folders = set()

def setup_logging(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    logging.info("\n" + "-" * 70 + "\n")

def is_filename_valid(filename):
    return re.match(r'^[\w\-]+\.[\w]+$', filename) is not None

def is_failed_filename(filename):
    return re.search(r'-(verification|processed)-failed\.', filename) is not None

def create_remote_folder(remote_folder, ip, username, ssh_key="C:/Users/onwar/.ssh/id_rsa"):
    if remote_folder in created_remote_folders:
        logging.info(f"Remote folder {remote_folder} already ensured.")
        return True

    try:
        ssh_command = f'ssh -i {ssh_key} {username}@{ip} "mkdir -p {remote_folder}"'
        logging.info(f"Creating remote folder with command: {ssh_command}")
        result = os.system(ssh_command)
        if result == 0:
            logging.info(f"Remote folder {remote_folder} ensured.")
            created_remote_folders.add(remote_folder)
            return True
        else:
            logging.error(f"Failed to create remote folder: {remote_folder}")
            return False
    except Exception as e:
        logging.error(f"Error creating remote folder {remote_folder}: {e}")
        return False

def transfer_to_server(local_path, remote_path, ip, username, ssh_key="C:/Users/onwar/.ssh/id_rsa"):
    try:
        local_path = local_path.replace("\\", "/")
        remote_path = remote_path.replace("\\", "/")

        if not os.path.exists(local_path):
            logging.error(f"File {local_path} does not exist, skipping transfer.")
            return False

        remote_folder = os.path.dirname(remote_path)
        if not create_remote_folder(remote_folder, ip, username, ssh_key):
            logging.error(f"Cannot proceed without the remote folder: {remote_folder}")
            return False

        scp_command = f"scp -i {ssh_key} {local_path} {username}@{ip}:{remote_path}"
        logging.info(f"Running SCP command: {scp_command}")
        result = os.system(scp_command)

        if result == 0:
            logging.info(f"Successfully transferred {local_path} to {remote_path}")
            return True
        else:
            logging.error(f"SCP command failed with result {result}: {scp_command}")
            return False
    except Exception as e:
        logging.error(f"Failed to transfer {local_path} to server: {e}")
        return False

def process_study_folder(root_folder, study_folder, server_ip, username, remote_folder, ssh_key="C:/Users/onwar/.ssh/id_rsa"):
    study_path = os.path.join(root_folder, study_folder)
    if not os.path.isdir(study_path):
        logging.warning(f"Skipping non-existent study folder: {study_path}")
        return

    verified_folder = os.path.join(study_path, 'verified')
    processed_folder = os.path.join(study_path, 'processed')
    completed_folder = os.path.join(study_path, 'completed')

    for folder in [verified_folder, processed_folder, completed_folder]:
        os.makedirs(folder, exist_ok=True)

    for filename in os.listdir(study_path):
        file_path = os.path.join(study_path, filename)

        if not os.path.isfile(file_path) or is_failed_filename(filename):
            logging.info(f"Skipping failed or already processed file: {filename}")
            continue

        try:
            if is_filename_valid(filename):
                shutil.move(file_path, os.path.join(verified_folder, filename))
                logging.info(f"Verified: {filename}")
            else:
                new_name = f"{os.path.splitext(filename)[0]}-verification-failed{os.path.splitext(filename)[1]}"
                shutil.move(file_path, os.path.join(study_path, new_name))
                logging.warning(f"Verification failed: {filename} renamed to {new_name}")
        except Exception as e:
            logging.error(f"Error processing file {filename}: {e}")

    for filename in os.listdir(verified_folder):
        file_path = os.path.join(verified_folder, filename)
        remote_path = os.path.join(remote_folder, study_folder, filename)

        if is_failed_filename(filename):
            logging.info(f"Skipping already failed file: {filename}")
            continue

        try:
            if transfer_to_server(file_path, remote_path, server_ip, username, ssh_key):
                shutil.move(file_path, os.path.join(processed_folder, filename))
                logging.info(f"Transferred: {filename}")
            else:
                new_name = f"{os.path.splitext(filename)[0]}-processed-failed{os.path.splitext(filename)[1]}"
                shutil.move(file_path, os.path.join(study_path, new_name))
                logging.warning(f"Copy failed: {filename} renamed to {new_name}")
        except Exception as e:
            logging.error(f"Error transferring file {filename}: {e}")

    for filename in os.listdir(processed_folder):
        file_path = os.path.join(processed_folder, filename)
        try:
            shutil.move(file_path, os.path.join(completed_folder, filename))
            logging.info(f"Completed: {filename}")
        except Exception as e:
            logging.error(f"Error moving file {filename} to completed: {e}")

def main():
    root_folder = r"C:\\Users\\onwar\\Desktop\\PathflowDX"
    log_file = os.path.join(root_folder, "process.log")
    setup_logging(log_file)

    server_ip = "13.203.152.86"
    username = "ubuntu"
    remote_folder = "/mnt/minio/pathflowdx-dev/JRF"
    ssh_key = "C:/Users/onwar/.ssh/id_rsa"

    start_time = datetime.now()
    logging.info(f"Script started at {start_time}")

    for folder in os.listdir(root_folder):
        if os.path.isdir(os.path.join(root_folder, folder)) and folder not in ["Archived"]:
            try:
                process_study_folder(root_folder, folder, server_ip, username, remote_folder, ssh_key)
            except Exception as e:
                logging.error(f"Error processing folder {folder}: {e}")

    end_time = datetime.now()
    logging.info(f"Script ended at {end_time}")
    logging.info(f"Total duration: {end_time - start_time}")

if __name__ == "__main__":
    main()
