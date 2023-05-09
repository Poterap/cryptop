import datetime
import os


def create_folder_in_directory(name: str, path: str, add_date: bool = True):
    try:
        if add_date:
            date_string = datetime.datetime.now().strftime("%Y-%m-%d")
            name = f"{name}_{date_string}"
        dir_path = os.path.join(path, name)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path
    except Exception as e:
        print(f"Error occurred while creating directory: {e}")
        return None
