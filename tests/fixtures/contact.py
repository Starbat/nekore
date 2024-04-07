import pytest

from nekore.models import Contact


@pytest.fixture
def aurore_jones() -> Contact:
    return Contact("Aurore Jones", "White Avenue", "738", "78405", "Shreveport")


@pytest.fixture
def kim_jackson() -> Contact:
    return Contact("Aurore Jones", "Bloomfield Township", "893", "48302", "Northampton")


@pytest.fixture
def frank_maldonado() -> Contact:
    return Contact("Frank Maldonado", "Ferguson Street", "472", "72766", "Chicago")
