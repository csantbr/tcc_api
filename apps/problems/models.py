from uuid import UUID, uuid4

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from database.session import Base


class Problem(Base):
    __tablename__ = 'problems'

    id: UUID = Column(PG_UUID(as_uuid=True), default=uuid4, primary_key=True, index=True)
    name: str = Column(String, index=True, unique=True)
    description: str = Column(String, nullable=False)
    data_entry: str = Column(String, nullable=False)
    entry_description: str = Column(String, nullable=False)
    data_output: str = Column(String, nullable=False)
    output_description: str = Column(String, nullable=False)

    def __repr__(self):
        return f'<Problem {self.name}>'
