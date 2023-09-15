from core.marketing.entrypoint import commands as mktg_cmd
from core.payment.domain import model as mdl
from dataclasses import dataclass
from core.entrypoint.uow import AbstractUnitOfWork
from abc import ABC, abstractmethod
from core.authentication.entrypoint import queries as auth_qry
from core.payment.entrypoint import queries as pmt_qry
from core.payment.entrypoint import view_models as pmt_vm
from core.authentication.domain import model as auth_mdl


@dataclass
class AbstractMarketingService(ABC):

    @abstractmethod
    def add_loyalty_points_and_give_cashback(
        self,
        sender_wallet_id: str,
        recipient_wallet_id: str,
        transaction_amount: float,
        transaction_type: str,
        uow: AbstractUnitOfWork,
    ):
        pass

    @abstractmethod
    def add_and_set_missing_weightages_to_zero(self, uow: AbstractUnitOfWork):
        pass


@dataclass
class MarketingService(AbstractMarketingService):

    def add_loyalty_points_and_give_cashback(
        self,
        sender_wallet_id: str,
        recipient_wallet_id: str,
        transaction_amount: float,
        transaction_type: mdl.TransactionType,
        uow: AbstractUnitOfWork,
    ):
        mktg_cmd.add_loyalty_points(
            sender_wallet_id=sender_wallet_id,
            recipient_wallet_id=recipient_wallet_id,
            transaction_amount=transaction_amount,
            transaction_type=transaction_type,
            uow=uow,
        )
        mktg_cmd.give_cashback(
            recipient_wallet_id=recipient_wallet_id,
            deposited_amount=transaction_amount,
            transaction_type=transaction_type,
            uow=uow,
        )

    def add_and_set_missing_weightages_to_zero(self, uow: AbstractUnitOfWork):
        mktg_cmd.add_and_set_missing_weightages_to_zero(uow=uow)

@dataclass
class FakeMarketingService(AbstractMarketingService):

    def add_loyalty_points_and_give_cashback(
        self,
        sender_wallet_id: str,
        recipient_wallet_id: str,
        transaction_amount: float,
        transaction_type: mdl.TransactionType,
        uow: AbstractUnitOfWork,
    ):
        pass

    def add_and_set_missing_weightages_to_zero(self, uow: AbstractUnitOfWork):
        pass


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
    def get_wallet_id_from_unique_identifier(
            self,
            unique_identifier:str,
            closed_loop_id:str,
            uow:AbstractUnitOfWork,
        )->str:
        pass

    @abstractmethod
    def get_wallet_balance(
        self,
        wallet_id: str,
        uow: AbstractUnitOfWork,
    )->int:
        pass

    @abstractmethod
    def get_starred_wallet_id(self, uow: AbstractUnitOfWork)->str:
        pass

    @abstractmethod
    def get_user_wallet_id_and_type_from_qr_id(
        self,
        qr_id: str,
        uow: AbstractUnitOfWork,
    ):
        pass

class PaymentService(AbstractPaymentService):

    def get_wallet_id_from_unique_identifier(
            self,
            unique_identifier:str,
            closed_loop_id:str,
            uow:AbstractUnitOfWork,
        )->str:
        return pmt_qry.get_wallet_id_from_unique_identifier(
            unique_identifier=unique_identifier,
            closed_loop_id=closed_loop_id,
            uow=uow,
        )

    def get_wallet_balance(
        self,
        wallet_id: str,
        uow: AbstractUnitOfWork,
    )->int:
        return pmt_qry.get_wallet_balance(
            wallet_id=wallet_id,
            uow=uow,
        )

    def get_starred_wallet_id(self, uow: AbstractUnitOfWork)->str:
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

    def get_wallet_id_from_unique_identifier(
            self,
            unique_identifier:str,
            closed_loop_id:str,
            uow:AbstractUnitOfWork,
        )->str:
        return self.wallet_id_from_unique_identifier

    def set_wallet_balance(self, wallet_balance: int):
        self.wallet_balance = wallet_balance

    def get_wallet_balance(
        self,
        wallet_id: str,
        uow: AbstractUnitOfWork,
    )->int:
        return self.wallet_balance

    def set_starred_wallet_id(self, wallet_id: str):
        self.starred_wallet_id = wallet_id

    def get_starred_wallet_id(self, uow: AbstractUnitOfWork)->str:
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