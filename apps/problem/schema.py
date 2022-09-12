from pydantic import BaseModel


class ProblemIn(BaseModel):
    name: str
    description: str
    data_entry: str | None
    entry_description: str
    data_output: str
    output_description: str
