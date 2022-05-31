from services.helpers import *

if __name__ == "__main__":
    # TODO get names from requester
    # TODO separate to 2 functions
    dataset_name = ""
    expectation_suite_name = ""
    dataset_name_2 = ""

    expectations_suite = generate_data_statistics(dataset_name,
                                                  expectation_suite_name)

    html_content = validate_original_data_with_new(
        dataset_name_2, expectations_suite, expectation_suite_name)
