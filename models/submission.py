from database.session import Base
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import UUID, uuid4


class Submission(Base):
    __tablename__ = 'submissions'

    id: UUID = Column(PG_UUID(as_uuid=True), default=uuid4, primary_key=True, index=True)
    problem_id: UUID = Column(PG_UUID(as_uuid=True), ForeignKey('problems.id'), nullable=False)
    language_type: str = Column(String, nullable=False)
    content: str = Column(String, nullable=False)
    status: str = Column(String, nullable=False)

    def __repr__(self):
        return f'<Submission {self.id}>'
