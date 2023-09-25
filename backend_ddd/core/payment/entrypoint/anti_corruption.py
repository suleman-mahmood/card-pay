from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.authentication.domain import model as auth_mdl
from core.authentication.entrypoint import queries as auth_qry
from core.entrypoint.uow import AbstractUnitOfWork
from core.payment.entrypoint import paypro_service as pp_svc
from core.payment.entrypoint import queries as pmt_qry
from core.payment.entrypoint import view_models as pmt_vm

PAYPRO_USER_ID = "93c74873-294f-4d64-a7cc-2435032e3553"


@dataclass
class AbstractAuthenticationService(ABC):
    @abstractmethod
    def user_verification_status_from_user_id(
        self,
        user_id: str,
        uow: AbstractUnitOfWork,
    ) -> bool:
        pass


@dataclass
class AuthenticationService(AbstractAuthenticationService):
    def user_verification_status_from_user_id(
        self,
        user_id: str,
        uow: AbstractUnitOfWork,
    ) -> bool:
        return auth_qry.user_verification_status_from_user_id(user_id=user_id, uow=uow)


@dataclass
class FakeAuthenticationService(AbstractAuthenticationService):
    user_verification_status: bool = True

    def set_user_verification_status(self, user_verification_status: bool):
        self.user_verification_status = user_verification_status

    def user_verification_status_from_user_id(
        self,
        user_id: str,
        uow: AbstractUnitOfWork,
    ) -> bool:
        return self.user_verification_status


@dataclass
class AbstractPaymentService(ABC):
    @abstractmethod
    def get_wallet_id_from_unique_identifier_and_closed_loop_id(
        self,
        unique_identifier: str,
        closed_loop_id: str,
        uow: AbstractUnitOfWork,
    ) -> str:
        pass

    @abstractmethod
    def get_wallet_balance(
        self,
        wallet_id: str,
        uow: AbstractUnitOfWork,
    ) -> int:
        pass

    @abstractmethod
    def get_starred_wallet_id(self, uow: AbstractUnitOfWork) -> str:
        pass

    @abstractmethod
    def get_user_wallet_id_and_type_from_qr_id(
        self,
        qr_id: str,
        uow: AbstractUnitOfWork,
    ):
        pass


class PaymentService(AbstractPaymentService):
    def get_wallet_id_from_unique_identifier_and_closed_loop_id(
        self,
        unique_identifier: str,
        closed_loop_id: str,
        uow: AbstractUnitOfWork,
    ) -> str:
        return pmt_qry.get_wallet_id_from_unique_identifier_and_closed_loop_id(
            unique_identifier=unique_identifier,
            closed_loop_id=closed_loop_id,
            uow=uow,
        )

    def get_wallet_balance(
        self,
        wallet_id: str,
        uow: AbstractUnitOfWork,
    ) -> int:
        return pmt_qry.get_wallet_balance(
            wallet_id=wallet_id,
            uow=uow,
        )

    def get_starred_wallet_id(self, uow: AbstractUnitOfWork) -> str:
        return pmt_qry.get_starred_wallet_id(uow=uow)

    def get_user_wallet_id_and_type_from_qr_id(
        self,
        qr_id: str,
        uow: AbstractUnitOfWork,
    ):
        return pmt_qry.get_user_wallet_id_and_type_from_qr_id(
            qr_id=qr_id,
            uow=uow,
        )


@dataclass
class FakePaymentService(AbstractPaymentService):
    user_wallet_id_and_type: pmt_vm.UserWalletIDAndTypeDTO = None
    starred_wallet_id: str = ""
    wallet_balance: int = 0
    wallet_id_from_unique_identifier: str = ""

    def set_wallet_id_from_unique_identifier(self, wallet_id: str):
        self.wallet_id_from_unique_identifier = wallet_id

    def get_wallet_id_from_unique_identifier_and_closed_loop_id(
        self,
        unique_identifier: str,
        closed_loop_id: str,
        uow: AbstractUnitOfWork,
    ) -> str:
        return self.wallet_id_from_unique_identifier

    def set_wallet_balance(self, wallet_balance: int):
        self.wallet_balance = wallet_balance

    def get_wallet_balance(
        self,
        wallet_id: str,
        uow: AbstractUnitOfWork,
    ) -> int:
        return self.wallet_balance

    def set_starred_wallet_id(self, wallet_id: str):
        self.starred_wallet_id = wallet_id

    def get_starred_wallet_id(self, uow: AbstractUnitOfWork) -> str:
        return self.starred_wallet_id

    def set_user_wallet_id_and_type(self, wallet_id: str, user_type: auth_mdl.UserType):
        self.user_wallet_id_and_type = pmt_vm.UserWalletIDAndTypeDTO(
            user_wallet_id=wallet_id,
            user_type=user_type,
        )

    def get_user_wallet_id_and_type_from_qr_id(
        self,
        qr_id: str,
        uow: AbstractUnitOfWork,
    ):
        return self.user_wallet_id_and_type
        # return "wallet_id", mdl.UserType.CUSTOMER


@dataclass
class AbstractPayproService(ABC):
    @abstractmethod
    def get_deposit_checkout_url(
        self,
        amount: int,
        transaction_id: str,
        full_name: str,
        phone_number: str,
        email: str,
        uow: AbstractUnitOfWork,
    ) -> str:
        pass

    @abstractmethod
    def get_paypro_wallet(self) -> str:
        pass


@dataclass
class FakePayproService(AbstractPayproService):
    pp_wallet_id: str = ""

    def get_deposit_checkout_url(
        self,
        amount: int,
        transaction_id: str,
        full_name: str,
        phone_number: str,
        email: str,
        uow: AbstractUnitOfWork,
    ) -> str:
        return ""

    def set_paypro_wallet(self, wallet_id):
        self.pp_wallet_id = wallet_id

    def get_paypro_wallet(self) -> str:
        return self.pp_wallet_id


@dataclass
class PayproService(AbstractPayproService):
    def get_deposit_checkout_url(
        self,
        amount: int,
        transaction_id: str,
        full_name: str,
        phone_number: str,
        email: str,
        uow: AbstractUnitOfWork,
    ) -> str:
        return pp_svc.get_deposit_checkout_url(
            amount=amount,
            transaction_id=transaction_id,
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            uow=uow,
        )

    def get_paypro_wallet(self) -> str:
        return PAYPRO_USER_ID
