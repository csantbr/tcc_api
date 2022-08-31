from database.session import Base
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import UUID, uuid4


class Problem(Base):
    __tablename__ = 'problems'

    id: UUID = Column(PG_UUID(as_uuid=True), default=uuid4, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    description = Column(String)
    data_entry = Column(String, nullable=True)
    entry_description = Column(String)
    data_output = Column(String)
    output_description = Column(String)

    def __repr__(self):
        return f'<Problem {self.name}>'
