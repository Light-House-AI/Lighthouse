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
