from pydantic import BaseModel


class CreateMLProject(BaseModel):
    name: str
    description: str
    user_id: int
    project_type: str
