from datetime import datetime

from core.entrypoint.uow import FakeUnitOfWork, UnitOfWork


def test_closed_loop_repository(seed_closed_loop):
    closed_loop = seed_closed_loop()

    for uow in [UnitOfWork(), FakeUnitOfWork()]:
        uow.closed_loops.add(closed_loop=closed_loop)
        fetched_closed_loop = uow.closed_loops.get(closed_loop_id=closed_loop.id)

        assert fetched_closed_loop == closed_loop

        closed_loop.name = "New test loop"
        closed_loop.description = "New description"
        closed_loop.logo_url = "New logo url"
        closed_loop.regex = "New regex"

        uow.closed_loops.save(closed_loop=closed_loop)
        fetched_closed_loop = uow.closed_loops.get(closed_loop_id=closed_loop.id)

        assert fetched_closed_loop == closed_loop


def test_user_repository(seed_user, seed_closed_loop_user):
    user = seed_user()
    cl_1 = seed_closed_loop_user()
    cl_2 = seed_closed_loop_user()
    cl_3 = seed_closed_loop_user()
    user.closed_loops = {cl_1.closed_loop_id: cl_1, cl_2.closed_loop_id: cl_2}

    for uow in [UnitOfWork(), FakeUnitOfWork()]:
        if uow.__class__.__name__ == "UnitOfWork":
            uow.cursor.execute(
                """
                    alter table users drop constraint if exists users_wallet_id_fkey cascade;
                    alter table user_closed_loops drop constraint if exists user_closed_loops_closed_loop_id_fkey cascade;
                """
            )

        uow.users.add(user=user)
        fetched_user = uow.users.get(user_id=user.id)

        assert fetched_user == user

        user.pin = "4321"
        user.is_active = False
        user.full_name = "New name"
        user.closed_loops = {}

        uow.users.save(user=user)
        fetched_user = uow.users.get(user_id=user.id)

        assert fetched_user == user

        user.closed_loops = {cl_3.closed_loop_id: cl_3}

        uow.users.save(user=user)
        fetched_user = uow.users.get(user_id=user.id)

        assert fetched_user == user
