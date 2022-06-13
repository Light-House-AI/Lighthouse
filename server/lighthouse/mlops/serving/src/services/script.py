from .run import *


def get_command_from_terminal(startup_config_dict: dict):
    exit_input = False
    while not exit_input:
        command = input("Enter command: ")
        try:
            action = command.split(" ")[0]

            if action == "deploy":
                model_id = command.split(" ")[1]
                deploy_model(model_id, startup_config_dict)
            elif action == "delete":
                model_id = command.split(" ")[1]
                delete_model(model_id, startup_config_dict)
            elif action == "update-ingress":
                models_ids_str = command.split(" ")[1]
                models_list = convert_str_to_list(models_ids_str)
                recreate_ingress_rules(models_list, startup_config_dict)
            elif action == "exit":
                exit_input = True
            else:
                print("Invalid command!")
        except Exception as e:
            print("Check the command format!")


def convert_str_to_list(models_str: str):
    try:
        models_str = models_str.replace("[", "")
        models_str = models_str.replace("]", "")
        models_list = models_str.split(",")
        models_list = [model_id for model_id in models_list]

        return models_list
    except Exception as e:
        print("List format is not correct. No spaces between elements!")
