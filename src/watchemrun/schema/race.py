from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from watchemrun.schema.route import Route


class Race(BaseModel):

    name: str
    date: Optional[datetime] = None
    route: Route
    location: Optional[str] = "Chicago"
