from pydantic import BaseModel
from typing import List, Optional

class Education(BaseModel):
    degree: Optional[str]
    institution: Optional[str]
    start_year: Optional[str]
    end_year: Optional[str]
    gpa: Optional[str]

class Experience(BaseModel):
    company: Optional[str]
    title: Optional[str]
    start_date: Optional[str]  # e.g., "2022-01"
    end_date: Optional[str]    # e.g., "2023-12" or "Present"
    duration: Optional[int]    # Duration in months
    responsibilities: Optional[str]

class Project(BaseModel):
    name: Optional[str]
    description: Optional[str]
    technologies: Optional[List[str]]

class ResumeData(BaseModel):
    full_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    summary: Optional[str]
    skills: Optional[List[str]]
    education: Optional[List[Education]]
    experience: Optional[List[Experience]]
    certifications: Optional[List[str]]
    projects: Optional[List[Project]]
    languages: Optional[List[str]]

class ResumeRequest(BaseModel):
    text: str

class StructuredResumeResponse(BaseModel):
    id: str
    data: ResumeData

