from services.script import get_command_from_terminal
from services.run import add_main_ingress_path
from services.startup import startup


if __name__ == "__main__":
    add_main_ingress_path()
    startup_config_dict = startup()
    get_command_from_terminal(startup_config_dict)
