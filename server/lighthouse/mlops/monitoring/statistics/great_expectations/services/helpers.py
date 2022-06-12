from services.statistics import *
from services.validations import *
from services.cleanup import *


def generate_data_statistics(dataset_name: str):
    expectation_suite_name = dataset_name.split(".")[0]
    expectations_suite, batch_request = generate_expectations_for_data(
        dataset_name, expectation_suite_name)
    delete_suite_expectations_file(expectation_suite_name)
    return expectations_suite, expectation_suite_name


def validate_original_data_with_new(new_dataset_name: str, expectations_suite,
                                    expectation_suite_name: str):
    save_expectation_suite_as_json_file(
        expectations_suite, expectation_suite_name)
    validate_data(expectation_suite_name, new_dataset_name)
    html_content = retrieve_html_validation_report(expectation_suite_name)
    delete_suite_expectations_file(expectation_suite_name)
    delete_yml_checkpoint_file(CHECKPOINT_NAME+".yml")
    delete_uncommitted_folder()
    return html_content
