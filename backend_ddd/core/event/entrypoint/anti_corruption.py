from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.authentication.adapters import exceptions as auth_repo_exc
from core.authentication.domain import model as auth_mdl
from core.entrypoint.uow import AbstractUnitOfWork


@dataclass
class AbstractAuthenticationService(ABC):
    @abstractmethod
    def is_organizer(self, id: str, uow: AbstractUnitOfWork) -> bool:
        pass

    @abstractmethod
    def is_valid_closed_loop(self, id: str, uow: AbstractUnitOfWork) -> bool:
        pass


@dataclass
class AuthenticationService(AbstractAuthenticationService):
    def is_organizer(self, id: str, uow: AbstractUnitOfWork) -> bool:
        fetched_user = uow.users.get(user_id=id)

        return fetched_user.user_type == auth_mdl.UserType.EVENT_ORGANIZER

    def is_valid_closed_loop(self, id: str, uow: AbstractUnitOfWork) -> bool:
        try:
            uow.closed_loops.get(closed_loop_id=id)
        except auth_repo_exc.ClosedLoopNotFound:
            return False

        return True


@dataclass
class FakeAuthenticationService(AbstractAuthenticationService):
    def is_organizer(self, id: str, uow: AbstractUnitOfWork) -> bool:
        return True

    def is_valid_closed_loop(self, id: str, uow: AbstractUnitOfWork) -> bool:
        return True
