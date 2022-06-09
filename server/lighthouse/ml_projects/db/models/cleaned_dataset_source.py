from sqlalchemy import Column, ForeignKey

from .base import Base
from .cleaned_dataset import CleanedDataset
from .raw_dataset import RawDataset


class CleanedDatasetSource(Base):

    cleaned_dataset_id = Column(ForeignKey(CleanedDataset.id),
                                primary_key=True)

    raw_dataset_id = Column(ForeignKey(RawDataset.id), primary_key=True)

    def __repr__(self):
        return "<CleanedDatasetSource(cleaned_dataset_id={}, raw_dataset_id={}>".format(
            self.cleaned_dataset_id, self.raw_dataset_id)

    def __str__(self):
        return self.__repr__()

    def dict(self):
        return {
            "cleaned_dataset_id": self.cleaned_dataset_id,
            "raw_dataset_id": self.raw_dataset_id,
        }
