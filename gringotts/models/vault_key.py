from opentelemetry import trace
import uuid

from fastapi import HTTPException, status
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from gringotts.models.base import Base
from sqlalchemy.orm import relationship

tracer = trace.get_tracer(__name__)


class VaultKey(Base):
    __tablename__ = "vault_keys"
    __table_args__ = {"schema": "gringotts"}


    key = Column(String, nullable=False, primary_key=True, unique=True)
    vault = relationship("Vault", back_populates="key", uselist=False)

    def __init__(self, key: str):
        self.key = key

    @classmethod
    async def find(cls, db_session: AsyncSession, key: str):
        """

        :param db_session:
        :param name:
        :return:
        """
        with tracer.start_as_current_span('Retrieving key by key id'):
            stmt = select(cls).where(cls.key == key)
            result = await db_session.execute(stmt)
            instance = result.scalars().first()
            return instance

    @classmethod
    async def all(cls, db_session: AsyncSession):
        """

        :param db_session:
        :return:
        """
        return await db_session.execute(select(cls))
