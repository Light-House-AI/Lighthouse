from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from .cleaned_dataset import CleanedDataset
from .project import Project


class Model(Base):
    id = Column(Integer, primary_key=True)

    project_id = Column(ForeignKey(Project.id), index=True, nullable=False)
    dataset_id = Column(ForeignKey(CleanedDataset.id),
                        index=True,
                        nullable=False)

    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_trained = Column(Boolean, nullable=False, default=False)

    number_of_layers = Column(Integer, nullable=True)
    maximum_neurons_per_layer = Column(Integer, nullable=True)
    learning_rate = Column(Float, nullable=True)
    batch_size = Column(Integer, nullable=True)
    score = Column(Float, nullable=True)

    # relationships
    project = relationship("Project", back_populates="models")
    dataset = relationship("CleanedDataset", back_populates="models")

    primary_deployments = relationship(
        "Deployment",
        primaryjoin="Model.id==Deployment.primary_model_id",
        back_populates="primary_model",
    )

    secondary_deployments = relationship(
        "Deployment",
        primaryjoin="Model.id==Deployment.secondary_model_id",
        back_populates="secondary_model",
    )

    # methods
    def get_data_cleaning_pipeline_id(self):
        return str(self.dataset_id)

    def __repr__(self):
        return "<Model(id={}, project_id={}, dataset_id={}, name={}, created_at={}, data_cleaning_pipeline_id={})>".format(
            self.id, self.name, self.project_id, self.dataset_id,
            self.created_at, self.get_data_cleaning_pipeline_id())

    def __str__(self):
        return self.__repr__()

    def to_dict(self):
        data = super().to_dict()
        data["data_cleaning_pipeline_id"] = self.get_data_cleaning_pipeline_id(
        )
        return data
