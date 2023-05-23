import datetime
import os


def create_folder_in_directory(name: str, path_directory: str, add_date: bool = True):#
    try:
        dir_path = create_full_file_path(name, path_directory, add_date)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path
    except Exception as e:
            print(f"Error occurred while creating directory: {e}")
            return None
    
def create_full_file_path(name: str, dir_path: str, add_date: bool = True, file_extension: str = ""):

        if file_extension and not file_extension.startswith("."):
            file_extension = "." + file_extension

        name = create_file_name(name, add_date, file_extension)
        filepath = os.path.join(dir_path, name)
        return filepath
    
def create_file_name(name: str, add_date: bool = True, file_extension: str = ""):
    if add_date:
        date_string = datetime.datetime.now().strftime("%Y-%m-%d")
        return f"{name}_{date_string}{file_extension}"
    return f"{name}{file_extension}"

def get_datas_from_folder(folder_path):
    """
    Displays the last part of the name of all folders in a directory.
    """
    if not os.path.isdir(folder_path):
        raise ValueError(f"{folder_path} is not a directory.")

    datas = [get_part_of_folder_name(name, -1) for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
    return datas

def get_files_from_folder(folder_path):
    """
    Displays the names of files in a directory.
    """
    if not os.path.isdir(folder_path):
        raise ValueError(f"{folder_path} is not a directory.")

    files = [name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))]
    return files

def get_part_of_folder_name(name: str, part_number: int):
     parts = name.split('_')
     return parts[part_number]
