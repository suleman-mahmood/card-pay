import pytest

from core.payment.domain import model as pmt_mdl
from core.marketing.domain import exceptions as ex
from core.marketing.domain import model as mdl


def test_add_loyalty_points_for_deposit(seed_user):
    transaction_amount = 1000
    weightage = mdl.Weightage(
        weightage_type=pmt_mdl.TransactionType.PAYMENT_GATEWAY, weightage_value=0.1
    )
    user = seed_user()
    user.verify_user()
    user.add_loyalty_points(
        pmt_mdl.TransactionType.PAYMENT_GATEWAY, transaction_amount, weightage
    )

    assert user.loyalty_points == transaction_amount * weightage.weightage_value


def test_add_loyalty_points_for_push_transaction(seed_user):
    transaction_amount = 1000
    weightage = mdl.Weightage(weightage_type=pmt_mdl.TransactionType.P2P_PUSH, weightage_value=0.1)
    user = seed_user()
    user.verify_user()
    user.add_loyalty_points(pmt_mdl.TransactionType.P2P_PUSH, transaction_amount, weightage)

    assert user.loyalty_points == transaction_amount * weightage.weightage_value


def test_add_loyalty_points_for_pull_transaction(seed_user):
    transaction_amount = 1000
    weightage = mdl.Weightage(weightage_type=pmt_mdl.TransactionType.P2P_PULL, weightage_value=0.1)
    user = seed_user()
    user.verify_user()
    user.add_loyalty_points(pmt_mdl.TransactionType.P2P_PULL, transaction_amount, weightage)

    assert user.loyalty_points == transaction_amount * weightage.weightage_value


def test_use_reference_and_add_referral_loyalty_points(seed_user):
    referral = seed_user()
    referee_1 = seed_user()
    referral_2 = seed_user()

    with pytest.raises(ex.NotVerifiedException, match="User is not verified"):
        referee_1.use_reference(referral.id)

    referee_1.verify_user()

    with pytest.raises(ex.InvalidReferenceException, match="User cannot refer themselves"):
        referee_1.use_reference(referee_1.id)

    referral.verify_user()
    # Marketing command 'use reference' will check if both the referee and referral are verified

    referee_1.use_reference(referral.id)
    assert referee_1.referral_id == referral.id

    with pytest.raises(
        ex.InvalidReferenceException, match="User has already been referred"
    ):
        referee_1.use_reference(referral.id)

    with pytest.raises(
        ex.InvalidReferenceException, match="User has already been referred"
    ):
        referee_1.use_reference(referral_2.id)

    weightage = mdl.Weightage(weightage_type=pmt_mdl.TransactionType.REFERRAL, weightage_value=50)

    referral.add_referral_loyalty_points(
        weightage=weightage, referee_verified=referee_1.marketing_user_verified
    )  # This function will be called by the marketing commands

    assert referral.loyalty_points == weightage.weightage_value

    referee_2 = seed_user()
    referee_2.verify_user()

    referee_2.use_reference(referral.id)
    assert referee_2.referral_id == referral.id

    referral.add_referral_loyalty_points(
        weightage=weightage, referee_verified=referee_2.marketing_user_verified
    )  # This function will be called by the marketing commands

    assert referral.loyalty_points == 2 * weightage.weightage_value


def test_cashback_on_deposit(seed_user):
    user = seed_user()
    with pytest.raises(
        ex.InvalidSlabException, match="ending amount is smaller than starting amount"
    ):
        cashback_slab_1 = mdl.CashbackSlab(
            start_amount=1000,
            end_amount=500,
            cashback_type=mdl.CashbackType.PERCENTAGE,
            cashback_value=0.1,
        )
        mdl.AllCashbacks(cashback_slabs=[cashback_slab_1]).handle_invalid_slabs()

    with pytest.raises(ex.InvalidSlabException, match="Cashback value is negative"):
        cashback_slab_1 = mdl.CashbackSlab(
            start_amount=1000,
            end_amount=5000,
            cashback_type=mdl.CashbackType.PERCENTAGE,
            cashback_value=-0.1,
        )
        mdl.AllCashbacks(cashback_slabs=[cashback_slab_1]).handle_invalid_slabs()

    with pytest.raises(
        ex.InvalidSlabException, match="Cashback type is neither PERCENTAGE nor ABSOLUTE"
    ):
        cashback_slab_1 = mdl.CashbackSlab(
            start_amount=1000,
            end_amount=5000,
            cashback_type="random",
            cashback_value=0.1,
        )
        mdl.AllCashbacks(cashback_slabs=[cashback_slab_1]).handle_invalid_slabs()

    with pytest.raises(
        ex.InvalidSlabException, match="Cashback percentage value is greater than 1"
    ):
        cashback_slab_1 = mdl.CashbackSlab(
            start_amount=1000,
            end_amount=5000,
            cashback_type=mdl.CashbackType.PERCENTAGE,
            cashback_value=2,
        )
        mdl.AllCashbacks(cashback_slabs=[cashback_slab_1]).handle_invalid_slabs()

    with pytest.raises(
        ex.InvalidSlabException,
        match="Cashback absolute value is greater than the slab ending amount",
    ):
        cashback_slab_1 = mdl.CashbackSlab(
            start_amount=1000,
            end_amount=5000,
            cashback_type=mdl.CashbackType.ABSOLUTE,
            cashback_value=7000,
        )
        mdl.AllCashbacks(cashback_slabs=[cashback_slab_1]).handle_invalid_slabs()

    with pytest.raises(ex.InvalidSlabException, match="Slabs are not continuous"):
        cashback_slab_1 = mdl.CashbackSlab(
            start_amount=1000,
            end_amount=5000,
            cashback_type=mdl.CashbackType.ABSOLUTE,
            cashback_value=100,
        )
        cashback_slab_2 = mdl.CashbackSlab(
            start_amount=6000,
            end_amount=7000,
            cashback_type=mdl.CashbackType.ABSOLUTE,
            cashback_value=100,
        )
        mdl.AllCashbacks(
            cashback_slabs=[cashback_slab_1, cashback_slab_2]
        ).handle_invalid_slabs()

    all_cashbacks = mdl.AllCashbacks(cashback_slabs=[])
    all_cashbacks.handle_invalid_slabs()

    assert all_cashbacks.cashback_slabs[0].start_amount == 0
    assert all_cashbacks.cashback_slabs[0].end_amount == 10
    assert all_cashbacks.cashback_slabs[0].cashback_type == mdl.CashbackType.ABSOLUTE
    assert all_cashbacks.cashback_slabs[0].cashback_value == 0


def test_calculate_cashback():
    deposit_amount = 7000

    cashback_slab_1 = mdl.CashbackSlab(
        start_amount=0,
        end_amount=5000,
        cashback_type=mdl.CashbackType.PERCENTAGE,
        cashback_value=0.1,
    )

    cashback_slab_2 = mdl.CashbackSlab(
        start_amount=5000,
        end_amount=10000,
        cashback_type=mdl.CashbackType.ABSOLUTE,
        cashback_value=100,
    )

    all_cashbacks = mdl.AllCashbacks(cashback_slabs=[cashback_slab_1, cashback_slab_2])
    all_cashbacks.handle_invalid_slabs()
    cc = mdl.CashbackCalculator(all_cashbacks=all_cashbacks)

    # with pytest.raises(ex.NotVerifiedException, match="User is not verified"):
    #     cc.calculate_cashback(
    #         deposit_amount=deposit_amount,
    #         invoker_transaction_type=pmt_mdl.TransactionType.PAYMENT_GATEWAY,
    #     )

    with pytest.raises(ex.NegativeAmountException, match="amount cannot be negative"):
        cc.calculate_cashback(
            deposit_amount=-1 * deposit_amount,
            invoker_transaction_type=pmt_mdl.TransactionType.PAYMENT_GATEWAY,
        )

    with pytest.raises(ex.InvalidTransactionTypeException, match="not deposit"):
        cc.calculate_cashback(
            deposit_amount=deposit_amount,
            invoker_transaction_type=pmt_mdl.TransactionType.P2P_PUSH,
        )

    assert (
        cc.calculate_cashback(
            deposit_amount=deposit_amount,
            invoker_transaction_type=pmt_mdl.TransactionType.PAYMENT_GATEWAY,
        )
        == cashback_slab_2.cashback_value
    )

    all_cashbacks = mdl.AllCashbacks(cashback_slabs=[])
    all_cashbacks.handle_invalid_slabs()
    cc = mdl.CashbackCalculator(all_cashbacks=all_cashbacks)

    assert (
        cc.calculate_cashback(
            deposit_amount=deposit_amount,
            invoker_transaction_type=pmt_mdl.TransactionType.PAYMENT_GATEWAY,
        )
        == 0
    )

    cashback_slab_1 = mdl.CashbackSlab(
        start_amount=100,
        end_amount=5000,
        cashback_type=mdl.CashbackType.PERCENTAGE,
        cashback_value=0.1,
    )

    cashback_slab_2 = mdl.CashbackSlab(
        start_amount=5000,
        end_amount=10000,
        cashback_type=mdl.CashbackType.ABSOLUTE,
        cashback_value=100,
    )
    all_cashbacks = mdl.AllCashbacks(cashback_slabs=[cashback_slab_1, cashback_slab_2])
    all_cashbacks.handle_invalid_slabs()
    cc = mdl.CashbackCalculator(all_cashbacks=all_cashbacks)

    assert (
        cc.calculate_cashback(
            deposit_amount=99,
            invoker_transaction_type=pmt_mdl.TransactionType.PAYMENT_GATEWAY,
        )
        == 0
    )

    assert (
        cc.calculate_cashback(
            deposit_amount=10001,
            invoker_transaction_type=pmt_mdl.TransactionType.PAYMENT_GATEWAY,
        )
        == 0
    )
