from pathlib import Path

from pydantic import BaseModel


class GitSection(BaseModel):
    url: str
    branch: str
    name: str
    dst: Path
