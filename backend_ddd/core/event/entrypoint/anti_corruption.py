from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.authentication.adapters import exceptions as auth_repo_exc
from core.authentication.domain import model as auth_mdl
from core.entrypoint.uow import AbstractUnitOfWork
from core.event.entrypoint import queries as event_qry
from core.event.entrypoint import view_models as event_vm


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


@dataclass
class AbstractEventsService(ABC):
    @abstractmethod
    def get_event_from_registration(
        self, registration_id: str, uow: AbstractUnitOfWork
    ) -> event_vm.AttendanceEventDTO:
        pass


@dataclass
class EventsService(AbstractEventsService):
    def get_event_from_registration(
        self, registration_id: str, uow: AbstractUnitOfWork
    ) -> event_vm.AttendanceEventDTO:
        return event_qry.get_event_from_registration(registration_id=registration_id, uow=uow)


@dataclass
class FakeEventsService(AbstractEventsService):
    attendance_event_dto: event_vm.AttendanceEventDTO

    def set_event_from_registration(self, event_id: str, user_id: str):
        self.attendance_event_dto = event_vm.AttendanceEventDTO(event_id=event_id, user_id=user_id)

    def get_event_from_registration(
        self, registration_id: str, uow: AbstractUnitOfWork
    ) -> event_vm.AttendanceEventDTO:
        return self.attendance_event_dto
