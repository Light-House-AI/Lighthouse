from services.helpers import *

if __name__ == "__main__":
    # TODO get names from requester
    # TODO separate to 2 functions
    dataset_name = "yellow_tripdata_sample_2019-01.csv"
    dataset_name_2 = "yellow_tripdata_sample_2019-02.csv"

    expectations_suite, expectation_suite_name = generate_data_statistics(
        dataset_name)

    html_content = validate_original_data_with_new(
        dataset_name_2, expectations_suite, expectation_suite_name)
