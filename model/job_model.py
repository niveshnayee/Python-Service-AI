from pydantic import BaseModel
from typing import List, Optional

class JobDescriptionData(BaseModel):
    title: Optional[str]
    keySkills: Optional[List[str]]
    responsibility: Optional[str]
    requirements: Optional[str]

class StructuredJobDescriptionResponse(BaseModel):
    data: JobDescriptionData

class JobRequest(BaseModel):
    text: str