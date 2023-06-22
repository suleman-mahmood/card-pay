import pytest
from ....entrypoint.uow import UnitOfWork
from ....authentication.entrypoint.commands import create_user 
def test_marketing_user_repository_add_get():
    uow = UnitOfWork()
   #Use Authentication command to create a user first, then use marketing command to fill the 4 marketing related columns in the users table