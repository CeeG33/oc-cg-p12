import pytest
from epicevents.cli import collaborator
from epicevents.data_access_layer.collaborator import Collaborator


def test_collaborator_CRUD_successful(
    monkey_token_check_management, fake_department_management, monkey_capture_message_collaborator, capsys
):
    collaborator.create(
        first_name="Test",
        name="Collaborator",
        email="test@test.fr",
        password="testpass",
        department=1,
    )

    created_collaborator = Collaborator.get(Collaborator.email == "test@test.fr")

    assert created_collaborator.first_name == "Test"

    collaborator.list()

    captured = capsys.readouterr()

    assert "test@test.fr" in captured.out.strip()

    collaborator.update(created_collaborator.id, "Toto", first_name=True)

    updated_collaborator = Collaborator.get(Collaborator.email == "test@test.fr")

    assert updated_collaborator.first_name == "Toto"

    collaborator.delete(updated_collaborator.id)

    deleted_collaborator = Collaborator.get_or_none(
        Collaborator.email == "test@test.fr"
    )

    assert deleted_collaborator is None
