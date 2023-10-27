import pytest
from datetime import datetime
from typer import Exit
from epicevents.data_access_layer.contract import Contract
from epicevents.cli.contract import update


def test_client_update_successful(
    monkey_token_check_management, fake_contract, fake_client, capsys
):
    """
    GIVEN a collaborator with the correct management token, a contract, and a new client
    WHEN the update() function is called to change the contract's client
    THEN the contract's client should be updated, and a success message should be printed
    """
    contract = fake_contract
    new_client = fake_client

    update(contract.id, new_client.id, client=True)

    updated_contract = Contract.get(Contract.id == contract.id)

    captured = capsys.readouterr()

    assert updated_contract.client.id == new_client.id
    assert updated_contract.client.first_name == new_client.first_name
    assert (
        f"Le champ 'Client' du contrat n°{contract.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_client_update_fails_with_wrong_id(
    monkey_token_check_management, fake_contract, capsys
):
    """
    GIVEN a collaborator with the correct management token and a contract
    WHEN the update() function is called to change the contract's client with an invalid client ID
    THEN the function should raise an exit error, and an error message should indicate that a valid client ID is required
    """
    contract = fake_contract

    with pytest.raises(Exit):
        update(contract.id, -50, client=True)

    captured = capsys.readouterr()

    assert "Veuillez entrer un numéro de client valide." in captured.out.strip()


def test_collaborator_update_successful(
    monkey_token_check_management, fake_contract, fake_collaborator_management, capsys
):
    """
    GIVEN a collaborator with the correct management token, a contract, and a new collaborator
    WHEN the update() function is called to change the contract's collaborator
    THEN the contract's collaborator should be updated, and a success message should be printed
    """
    contract = fake_contract
    new_collaborator = fake_collaborator_management

    update(contract.id, new_collaborator.id, collaborator=True)

    updated_contract = Contract.get(Contract.id == contract.id)

    captured = capsys.readouterr()

    assert updated_contract.collaborator.id == new_collaborator.id
    assert updated_contract.collaborator.first_name == new_collaborator.first_name
    assert (
        f"Le champ 'Collaborateur' du contrat n°{contract.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_collaborator_update_fails_with_wrong_id(
    monkey_token_check_management, fake_contract, capsys
):
    """
    GIVEN a collaborator with the correct management token and a contract
    WHEN the update() function is called to change the contract's collaborator with an invalid collaborator ID
    THEN the function should raise an exit error, and an error message should indicate that a valid collaborator ID is required
    """
    contract = fake_contract

    with pytest.raises(Exit):
        update(contract.id, -50, collaborator=True)

    captured = capsys.readouterr()

    assert "Veuillez entrer un numéro de collaborateur valide." in captured.out.strip()


def test_total_sum_update_successful(
    monkey_token_check_management, fake_contract, capsys
):
    """
    GIVEN a collaborator with the correct management token and a contract
    WHEN the update() function is called to change the contract's total sum
    THEN the contract's total sum should be updated, and a success message should be printed
    """
    contract = fake_contract
    new_total_sum = 1000

    update(contract.id, new_total_sum, total_sum=True)

    updated_contract = Contract.get(Contract.id == contract.id)

    captured = capsys.readouterr()

    assert updated_contract.total_sum == new_total_sum
    assert (
        f"Le champ 'Montant total' du contrat n°{contract.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_amount_due_update_successful(
    monkey_token_check_management, fake_contract, capsys
):
    """
    GIVEN a collaborator with the correct management token and a contract
    WHEN the update() function is called to change the contract's amount due
    THEN the contract's amount due should be updated, and a success message should be printed
    """
    contract = fake_contract
    new_amount_due = 1000

    update(contract.id, new_amount_due, amount_due=True)

    updated_contract = Contract.get(Contract.id == contract.id)

    captured = capsys.readouterr()

    assert updated_contract.amount_due == new_amount_due
    assert (
        f"Le champ 'Montant dû' du contrat n°{contract.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_creation_date_update_successful(
    monkey_token_check_management, fake_contract, capsys
):
    """
    GIVEN a collaborator with the correct management token and a contract
    WHEN the update() function is called to change the contract's creation date
    THEN the contract's creation date should be updated, and a success message should be printed
    """
    contract = fake_contract
    new_creation_date = "2023-10-25"

    update(contract.id, new_creation_date, creation_date=True)

    updated_contract = Contract.get(Contract.id == contract.id)

    captured = capsys.readouterr()

    assert updated_contract.creation_date == datetime(2023, 10, 25)
    assert (
        f"Le champ 'Date de création' du contrat n°{contract.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_signed_update_successful(
    monkey_capture_message_contract,
    monkey_token_check_management,
    fake_contract,
    capsys,
):
    """
    GIVEN a collaborator with the correct management token, a contract, and the correct capture message monkey patch
    WHEN the update() function is called to change the contract's signed status
    THEN the contract's signed status should be updated, and a success message should be printed
    """
    contract = fake_contract

    update(contract.id, True, signed=True)

    updated_contract = Contract.get(Contract.id == contract.id)

    captured = capsys.readouterr()

    assert updated_contract.signed == True
    assert (
        f"Le champ 'Signé' du contrat n°{contract.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_contract_update_fails_without_attributes(
    monkey_token_check_management, fake_contract, capsys
):
    """
    GIVEN a collaborator with the correct management token and a contract
    WHEN the update() function is called without specifying any attributes to change
    THEN the function should raise an exit error, and an error message should indicate that no attribute was selected for modification
    """
    contract = fake_contract

    with pytest.raises(Exit):
        update(contract.id, "10")

    captured = capsys.readouterr()

    assert "Vous n'avez pas sélectionné d'attribut à modifier." in captured.out.strip()


def test_contract_update_fails_with_wrong_contract_id(
    monkey_token_check_management, capsys
):
    """
    GIVEN a collaborator with the correct management token
    WHEN the update() function is called with an invalid contract ID
    THEN the function should raise an exit error, and an error message should indicate that no contract was found with the given ID
    """
    fake_id = 100
    with pytest.raises(Exit):
        update(fake_id, 2, client=True)

    captured = capsys.readouterr()

    assert f"Aucun contrat trouvé avec l'ID n°{fake_id}." in captured.out.strip()


def test_contract_update_not_authorized(
    monkey_token_check_support, fake_contract, capsys
):
    """
    GIVEN a collaborator with the incorrect support token and a contract
    WHEN the update() function is called to update the contract
    THEN the function should raise an exit error, and an error message should indicate that this action is restricted
    """
    contract = fake_contract

    with pytest.raises(Exit):
        update(contract.id, 2, client=True)

    captured = capsys.readouterr()

    assert "Action restreinte." in captured.out.strip()


def test_contract_update_fails_without_authentication(
    monkey_token_check_false, fake_contract, capsys
):
    """
    GIVEN a collaborator with an incorrect token and a contract
    WHEN the update() function is called to update the contract
    THEN the function should raise an exit error, and an error message should indicate that authentication is required
    """
    contract = fake_contract

    with pytest.raises(Exit):
        update(contract.id, 2, client=True)

    captured = capsys.readouterr()

    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()


def test_contract_update_fails_with_wrong_salesman(
    monkey_token_check_fake_sales, fake_contract, capsys
):
    """
    GIVEN a collaborator with the sales token and a contract whose client is not that of the collaborator's
    WHEN the update() function is called to update the contract
    THEN the function should raise an exit error, and an error message should indicate that this action is restricted
    """
    contract = fake_contract

    with pytest.raises(Exit):
        update(contract.id, 2, client=True)

    captured = capsys.readouterr()

    assert "Action restreinte." in captured.out.strip()


def test_contract_update_with_correct_salesman_succesful(
    monkey_token_check_correct_sales, fake_contract, fake_client, capsys
):
    """
    GIVEN a collaborator with the sales token, a contract whose client is that of the collaborator's, and a new client
    WHEN the update() function is called to change the contract's client
    THEN the contract's client should be updated, and a success message should be printed
    """
    print(fake_contract.collaborator.id)
    update(fake_contract.id, fake_client.id, client=True)

    updated_contract = Contract.get(Contract.id == fake_contract.id)

    captured = capsys.readouterr()

    assert updated_contract.client.id == fake_client.id
    assert (
        f"Le champ 'Client' du contrat n°{fake_contract.id} a été mis à jour avec succès."
        in captured.out.strip()
    )
