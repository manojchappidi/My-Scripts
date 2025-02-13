import os
import shutil

def move_images(src_dir, dest_dir):
    # Check if the source directory exists
    if not os.path.exists(src_dir):
        print(f"Source directory {src_dir} does not exist.")
        return

    # Create the destination 'Archived' folder if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"Created destination folder: {dest_dir}")

    # Loop through all the folders in the source directory
    for folder_name in os.listdir(src_dir):
        folder_path = os.path.join(src_dir, folder_name)

        # Consider only folders
        if os.path.isdir(folder_path):
            completed_folder = os.path.join(folder_path, 'completed')
            
            # Check if 'completed' folder exists inside the folder
            if os.path.exists(completed_folder):
                # Create the corresponding folder in the destination directory
                dest_folder = os.path.join(dest_dir, folder_name)
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                    print(f"Created folder: {dest_folder}")
                
                # Loop through all the files in the 'completed' folder
                for file_name in os.listdir(completed_folder):
                    file_path = os.path.join(completed_folder, file_name)
                    
                    # Move the file to the destination folder
                    if os.path.isfile(file_path):
                        shutil.move(file_path, os.path.join(dest_folder, file_name))
                        print(f"Moved: {file_name} to {dest_folder}")
            else:
                print(f"Completed folder not found in {folder_path}")
        else:
            print(f"Skipping non-folder: {folder_path}")

# Set your source directory (PathflowDX folder) and destination directory (Archived folder)
src_directory = r"C:\Users\onwar\Desktop\PathflowDX"
dest_directory = r"C:\Users\onwar\Desktop\PathflowDX\Archived"

# Call the function
move_images(src_directory, dest_directory)
