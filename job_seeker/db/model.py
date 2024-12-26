from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class Job(BaseModel):
    role: str
    company: str
    location: str
    link: Optional[str] = None
    date: Optional[datetime] = None
    description: Optional[str] = None
