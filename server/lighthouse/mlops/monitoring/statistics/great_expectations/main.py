from services.helpers import *

if __name__ == "__main__":
    # *VARS
    dataset_name = "yellow_tripdata_sample_2019-01.csv"
    expectation_suite_name = "taxi-demo"
    ##
    expectations_suite = generate_data_statistics(dataset_name,
                                                  expectation_suite_name)
    # * VARS
    dataset_name_2 = "yellow_tripdata_sample_2019-02.csv"
    html_content = validate_original_data_with_new(
        dataset_name_2, expectations_suite, expectation_suite_name)
