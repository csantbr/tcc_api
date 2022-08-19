from pydantic import BaseModel


class Problem(BaseModel):
    name: str
    description: str
    data_entry: str
    data_output: str
