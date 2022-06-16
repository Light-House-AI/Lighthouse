# ML monitoring (GE)

## About 
- All of this module is built on the extremely powerful **`great_expectations`** library.
- This module is used to integrate with the library to reflect the needs of the Lighthouse project in monitoring machine learning models in production and determine when there has been a data drift.
## Functionality

- This module is a part of the monitoring module that does the following 2 functionalities
  1. Generate expectations and statistics about the original data by invoking `generate_data_statistics` function.
  2. Validate a new data batch with the statistics of the original data to determine if there has been a data drift in any of the data attributes by invoking `validate_original_data_with_new` function.


## How to run
- Place your data csv files in the data folder (both original and new)
- Run 
    ```shell
        python main.py
    ```
## TODOS:
- Write the data path folder in ```great_expectations.yml``` file