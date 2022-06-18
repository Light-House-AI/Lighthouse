from .constants import *

import json
import os
from os.path import dirname
from ruamel.yaml import YAML
import great_expectations as ge
from great_expectations.core.expectation_suite import expectationSuiteSchema


def save_expectation_suite_as_json_file(suite_object, suite_name):
    file_path = f"./expectations/{suite_name}.json"
    jsonString = json.dumps(
        expectationSuiteSchema.dump(suite_object),
        indent=2,
        sort_keys=True,
    )
    jsonFile = open(file_path, "w")
    jsonFile.write(jsonString)
    jsonFile.close()


def validate_data(suite_name, new_dataset_name):
    context = ge.get_context()
    yaml = YAML()
    yaml_config = f"""
            name: {CHECKPOINT_NAME}
            config_version: 1.0
            class_name: SimpleCheckpoint
            run_name_template: "output"
            validations:
            - batch_request:
                datasource_name: {DATASOURCE_NAME}
                data_connector_name: default_inferred_data_connector_name
                data_asset_name: {new_dataset_name}
                data_connector_query:
                    index: -1
              expectation_suite_name: {suite_name}
            """
    _ = context.test_yaml_config(yaml_config=yaml_config)
    context.add_checkpoint(**yaml.load(yaml_config))
    context.run_checkpoint(checkpoint_name=CHECKPOINT_NAME)


def retrieve_html_validation_report(expectation_suite_name: str):
    root_dir = dirname(dirname(
        __file__)) + f"/uncommitted/data_docs/local_site/validations/{expectation_suite_name}/output/"

    # obtain the folder containing the html file
    for file in os.listdir(root_dir):
        root_dir = root_dir + file + "/"

    # obtain the html file
    for file in os.listdir(root_dir):
        root_dir += file

    html_file = open(root_dir, 'rb')
    html_file_content = html_file.read()
    html_file.close()

    return html_file_content
