"""CoreModel Definition Module"""
from pydantic import BaseModel


class CoreModel(BaseModel):
    """
    Any common logic will be shared with all models
    """
    pass


class IDMixinModel(BaseModel):
    """ID definition class"""
    id: int
