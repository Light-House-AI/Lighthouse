"""Datasets service"""


def upload_dataset(project_id: int, data: bytes, db: Session):
    """
    Uploads a dataset to a project.
    """
    pass


def get_dataset_cleaning_rules_recommendations(project_id: int,
                                               dataset_id: int, db: Session):
    """
    Returns dataset cleaning rules recommendations.
    """
    pass


def create_cleaned_dataset(project_id: int, raw_dataset_id: int, rules: Dict,
                           db: Session):
    """
    Creates a processed dataset.
    """
    pass