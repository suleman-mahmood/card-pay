from dataclasses import dataclass
from core.entrypoint.uow import AbstractUnitOfWork
from core.comms.entrypoint import queries as comms_qry
from abc import ABC, abstractmethod

@dataclass
class AbstractCommunicationService(ABC):
    @abstractmethod
    def get_fcm_token(self, user_id: str, uow: AbstractUnitOfWork) -> str:
        pass

@dataclass
class FakeCommunicationService(AbstractCommunicationService):
    def get_fcm_token(self, user_id: str, uow: AbstractUnitOfWork) -> str:
        return ""

@dataclass
class CommunicationService(AbstractCommunicationService):
    def get_fcm_token(self, user_id: str, uow: AbstractUnitOfWork) -> str:
        return comms_qry.get_fcm_token(user_id=user_id, uow=uow)
