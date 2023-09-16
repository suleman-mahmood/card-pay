from core.marketing.domain import model as mdl
from core.payment.domain import model as pmt_mdl


def calculate_cashback(
    amount: int,
    invoker_transaction_type: pmt_mdl.TransactionType,
    all_cashbacks: mdl.AllCashbacks,
) -> int:
    cc = mdl.CashbackCalculator(all_cashbacks=all_cashbacks)
    return cc.calculate_cashback(
        deposit_amount=amount, invoker_transaction_type=invoker_transaction_type
    )
