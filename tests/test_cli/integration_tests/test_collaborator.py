import pytest
from epicevents.cli import collaborator
from epicevents.data_access_layer.collaborator import Collaborator


def test_collaborator_CRUD_successful(
    monkey_token_check_management,
    fake_department_management,
    monkey_capture_message_collaborator,
    capsys,
):
    """
    Given a valid management collaborator token,
    When a collaborator is created with specific details,
    Then the collaborator should be created and have the expected first name.

    When listing collaborators,
    Then the created collaborator's email should appear in the output.

    When the created collaborator's first name is updated to "Toto",
    Then the updated collaborator should have the first name "Toto".

    When the collaborator is deleted,
    Then the deleted collaborator should not be found.
    """
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
