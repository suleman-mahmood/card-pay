from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

from core.authentication.entrypoint import queries as auth_qry
from core.authentication.entrypoint import view_models as auth_vm
from core.comms.entrypoint import queries as comms_qry
from core.entrypoint.uow import AbstractUnitOfWork


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


@dataclass
class AbstractAuthenticationService(ABC):
    @abstractmethod
    def get_all_emails(self, uow: AbstractUnitOfWork) -> List[auth_vm.EmailInfoDTO]:
        pass


@dataclass
class FakeAuthenticationService(AbstractAuthenticationService):
    all_emails: List[auth_vm.EmailInfoDTO] = field(default_factory=list)

    def get_all_emails(self, uow: AbstractUnitOfWork) -> List[auth_vm.EmailInfoDTO]:
        return self.all_emails

    def set_all_emails(self, all_emails: List[auth_vm.EmailInfoDTO]):
        self.all_emails = all_emails


@dataclass
class AuthenticationService(AbstractAuthenticationService):
    def get_all_emails(self, uow: AbstractUnitOfWork) -> List[auth_vm.EmailInfoDTO]:
        return auth_qry.get_all_emails(uow=uow)
