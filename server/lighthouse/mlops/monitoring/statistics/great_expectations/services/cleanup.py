import os
import shutil


def delete_suite_expectations_file(suite_name: str):
    """
    An automatically created json file is created when the expectations suite is initialized
    """
    file_path = f"./expectations/{suite_name}.json"
    os.remove(file_path)


def delete_uncommitted_folder():
    folder_path = "./uncommitted/"
    shutil.rmtree(folder_path)


def delete_csv_data_file(datafile_name: str):
    """
    The file that should be created as a data source to obtain statistics 
    """
    file_path = f"./../data/{datafile_name}"
    os.remove(file_path)


def delete_yml_checkpoint_file(datafile_name: str):
    file_path = f"./checkpoints/{datafile_name}"
    os.remove(file_path)
