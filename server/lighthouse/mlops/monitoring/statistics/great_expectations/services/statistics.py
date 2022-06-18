from .constants import *

import os
import great_expectations as ge
from great_expectations.core.batch import BatchRequest
from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler

_context_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def generate_expectations_for_data(dataset_name: str, expectation_suite_name: str):
    context = ge.DataContext(context_root_dir=_context_path)
        
    suite = context.create_expectation_suite(
        expectation_suite_name=expectation_suite_name, overwrite_existing=True)
    batch_request = {"datasource_name": f"{DATASOURCE_NAME}",
                     "data_connector_name": "default_inferred_data_connector_name",
                     "data_asset_name": f"{dataset_name}"}
    validator = context.get_validator(
        batch_request=BatchRequest(**batch_request),
        expectation_suite_name=expectation_suite_name
    )
    profiler = UserConfigurableProfiler(
        profile_dataset=validator,
        excluded_expectations=None,
        ignored_columns=[],
        not_null_only=False,
        primary_or_compound_key=False,
        semantic_types_dict=None,
        table_expectations_only=False,
        value_set_threshold="MANY",
    )
    suite = profiler.build_suite()
    return suite, batch_request
