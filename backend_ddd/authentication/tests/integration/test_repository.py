import pytest
from ...adapters.repository import ClosedLoopRepository, UserRepository
from ...domain.model import ClosedLoop, ClosedLoopVerificationType
from backend_ddd.entrypoint.uow import UnitOfWork


def test_closed_loop_repository_add_get():
    uow = UnitOfWork()

    with uow:
        closed_loop = ClosedLoop(
            name="Lums",
            logo_url="logo.lums.edu.pk.jpeg",
            description="Lums best uni",
            regex="no regex yet",
            verification_type=ClosedLoopVerificationType.ROLLNUMBER,
        )
        uow.closed_loops.add(closed_loop=closed_loop)
        fetched_closed_loop = uow.closed_loops.get(closed_loop_id=closed_loop.id)

        assert fetched_closed_loop == closed_loop
