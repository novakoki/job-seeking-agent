from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Job(BaseModel):
    id: Optional[str] = None
    role: str
    company: str
    location: str
    link: str
    date: Optional[datetime] = None
    description: Optional[str] = None


class Resume(BaseModel):
    id: Optional[str] = None
    location: str
    education: List[str]
    experience: List[str]
    skills: List[str]
    projects: List[str]
    certifications: List[str]
    publications: List[str]
    summary: Optional[List[str]]


class DesiredPosition(BaseModel):
    id: Optional[str] = None
    role: Optional[List[str]]
    company: Optional[List[str]]
    location: Optional[List[str]]
    description: Optional[str]
