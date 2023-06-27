# import pytest
# from ....entrypoint.uow import UnitOfWork, AbstractUnitOfWork
# from ....authentication.entrypoint import commands as authentication_commands
# from ...domain.model import (User, Weightage, CashbackSlab, CashbackType,)
# from ....authentication.domain.model import Location, PersonalEmail, PhoneNumber, UserType
# from ....authentication.domain.model import User as AuthenticationUser
# from ....payment.entrypoint import commands as payment_commands
# from ....payment.domain.model import TransactionType
# from ...adapters.repository import (MarketingUserRepository, WeightageRepository, CashbackSlabRepository,)
# from ....authentication.tests.conftest import seed_auth_user
# from uuid import uuid4


# def test_marketing_user_repository_add_get_save(seed_auth_user):
#     uow = UnitOfWork()
#     #Use Authentication command to create a user first, then use marketing command to fill the 4 marketing related columns in the users table

#     # authentication_user = authentication_commands.create_user(
#     #     user_id =  str(uuid4()),
#     #     personal_email =  "asdasd@asdasd.com",
#     #     phone_number = "1231241231",
#     #     user_type = "CUSTOMER",
#     #     pin =  "4251",
#     #     full_name = "Shaheer",
#     #     location = (1.2,5.2),
#     #     uow = uow,
#     # )

#     authentication_user = seed_auth_user(uow)
#     with uow:
                  
#         marketing_user = User(
#             id = authentication_user.id,
#         )
#         uow.marketing_users.save(marketing_user)
        
#         fetched_user = uow.marketing_users.get(id = marketing_user.id)

#         assert fetched_user == marketing_user

#         marketing_user.loyalty_points = 100
#         uow.marketing_users.save(marketing_user)

#         fetched_user = uow.marketing_users.get(id = marketing_user.id)

#         assert fetched_user == marketing_user


# # def test_weightage_repository_add_get_save():

# #     uow = UnitOfWork()
# #     with uow:
# #         weightage = Weightage(
# #             weightage_type= TransactionType.REFERRAL,
# #             weightage_value= 10,
# #         )

# #         uow.weightages.save(weightage)
# #         fetched_weightage = uow.weightages.get(weightage_type= TransactionType.REFERRAL)
# #         assert fetched_weightage == weightage

# #         weightage.weightage_value = 20
# #         uow.weightages.save(weightage)
# #         fetched_weightage = uow.weightages.get(weightage_type= TransactionType.REFERRAL)
# #         assert fetched_weightage == weightage

# def test_cashback_slab_repository_add_get_save():
#     uow = UnitOfWork()
#     with uow:
#         cashback_slab_1 = CashbackSlab(
#             start_amount= 0,
#             end_amount= 100,
#             cashback_type= CashbackType.PERCENTAGE,
#             cashback_value= 10,
#         )

#         cashback_slab_2 = CashbackSlab(
#             start_amount= 100,
#             end_amount= 200,
#             cashback_type= CashbackType.PERCENTAGE,
#             cashback_value= 20,
#         )
        
#         cashback_slabs = [cashback_slab_1, cashback_slab_2]

#         uow.cashback_slabs.save(cashback_slabs)
#         fetched_cashback_slabs = uow.cashback_slabs.get()
#         assert fetched_cashback_slabs == cashback_slabs

#         cashback_slabs[0].cashback_value = 20
#         uow.cashback_slabs.save(cashback_slabs)
#         fetched_cashback_slab = uow.cashback_slabs.get()
#         assert fetched_cashback_slab == cashback_slabs