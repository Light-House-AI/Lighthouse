from services.run import *


def get_command_from_terminal(startup_config_dict: dict):
    exit_input = False
    while not exit_input:
        command = input("Enter command: ")
        try:
            action = command.split(" ")[0]

            if action == "deploy":
                project_id = command.split(" ")[1]
                deployment_type = command.split(" ")[2]
                model_id = command.split(" ")[3]
                challenger_model_id = command.split(" ")[4]
                deploy_model(startup_config_dict, project_id, deployment_type,
                             model_id, challenger_model_id)
            elif action == "delete":
                project_id = command.split(" ")[1]
                delete_model(startup_config_dict, project_id)
            elif action == "update-ingress":
                project_ids_str = command.split(" ")[1]
                project_list = convert_str_to_list(project_ids_str)
                recreate_ingress_rules(startup_config_dict, project_list)
            elif action == "exit":
                exit_input = True
            else:
                print("Invalid command!")
        except Exception as e:
            print("Check the command format!")


def convert_str_to_list(projects_str: str):
    try:
        projects_str = projects_str.replace("[", "")
        projects_str = projects_str.replace("]", "")
        project_list = projects_str.split(",")
        project_list = [project_id for project_id in project_list]

        return project_list
    except Exception as e:
        print("List format is not correct. No spaces between elements!")
