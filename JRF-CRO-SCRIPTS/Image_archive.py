import os
import shutil
import logging
from datetime import datetime

# Define the root folder path and the "Archived" folder path
root_folder = r"C:\Users\onwar\Desktop\PathflowDx"
archived_folder = os.path.join(root_folder, "Archived")
log_file = os.path.join(archived_folder, "move_images_log.txt")

# Function to set up logging
def setup_logging():
    # Create log directory if it doesn't exist
    if not os.path.exists(archived_folder):
        os.makedirs(archived_folder)

    # Set up logging configuration
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

# Function to move images from the completed folder to Archived folder
def move_images_to_archived():
    setup_logging()

    # Log the start of the script
    logging.info("Script started")

    # Check if the "Archived" folder exists, if not, create it
    if not os.path.exists(archived_folder):
        os.makedirs(archived_folder)
        logging.info(f"Created 'Archived' folder at: {archived_folder}")

    # Walk through each folder in the root folder (folder-1, folder-2, etc.)
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)

        # Check if it's a folder and has a 'completed' subfolder
        if os.path.isdir(folder_path):
            completed_folder = os.path.join(folder_path, "completed")

            if os.path.exists(completed_folder):
                # Create the corresponding folder inside the "Archived" folder if it doesn't exist
                archived_folder_path = os.path.join(archived_folder, folder_name)
                if not os.path.exists(archived_folder_path):
                    os.makedirs(archived_folder_path)
                    logging.info(f"Created folder: {archived_folder_path}")

                # Move the images (files) from 'completed' to the corresponding 'Archived' folder
                for file_name in os.listdir(completed_folder):
                    file_path = os.path.join(completed_folder, file_name)
                    if os.path.isfile(file_path):
                        try:
                            # Define the destination path in the "Archived" folder
                            destination_path = os.path.join(archived_folder_path, file_name)

                            # Move the file
                            shutil.move(file_path, destination_path)
                            logging.info(f"Moved: {file_name} -> {destination_path}")
                        except Exception as e:
                            logging.error(f"Error moving {file_name}: {e}")

    # Log the end of the script
    logging.info("Script completed")

# Run the function
move_images_to_archived()
