import pytest
from datetime import datetime
from typer import Exit
from peewee import DoesNotExist
from epicevents.data_access_layer.event import Event
from epicevents.cli.event import update
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def test_contract_update_successful(monkey_token_check_management, fake_event, fake_contract, capsys):
    update(fake_event.id, fake_contract.id, contract=True)

    updated_event = Event.get(Event.id == fake_event.id)
    
    captured = capsys.readouterr()
    
    assert updated_event.contract.id == fake_contract.id
    assert updated_event.contract.total_sum == fake_contract.total_sum
    assert f"Le champ 'Contrat' de l'évènement n°{fake_event.id} a été mis à jour avec succès." in captured.out.strip()
    
def test_contract_update_fails_with_wrong_id(monkey_token_check_management, fake_event, capsys):
    with pytest.raises(Exit):
        update(fake_event.id, -50, contract=True)
    
    captured = capsys.readouterr()
    
    assert "Veuillez entrer un numéro de contrat valide." in captured.out.strip()
    
def test_support_update_successful(monkey_token_check_management, fake_event, fake_collaborator_support, capsys):
    update(fake_event.id, fake_collaborator_support.id, support=True)

    updated_event = Event.get(Event.id == fake_event.id)
    
    captured = capsys.readouterr()
    
    assert updated_event.support.id == fake_collaborator_support.id
    assert updated_event.support.first_name == fake_collaborator_support.first_name
    assert f"Le champ 'Assistant en charge' de l'évènement n°{fake_event.id} a été mis à jour avec succès." in captured.out.strip()

def test_support_update_fails_with_wrong_id(monkey_token_check_management, fake_event, capsys):
    with pytest.raises(Exit):
        update(fake_event.id, -50, support=True)
    
    captured = capsys.readouterr()
    
    assert "Veuillez entrer un numéro de collaborateur valide et faisant partie du département Support." in captured.out.strip()
    
def test_support_update_fails_with_not_support_collaborator(monkey_token_check_management, fake_event, fake_collaborator_sales, capsys):
    with pytest.raises(Exit):
        update(fake_event.id, fake_collaborator_sales.id, support=True)
    
    captured = capsys.readouterr()
    
    assert "Veuillez entrer un numéro de collaborateur valide et faisant partie du département Support." in captured.out.strip()

# def test_collaborator_update_fails_with_wrong_id(monkey_token_check_management, fake_contract, capsys):
#     contract = fake_contract
    
#     with pytest.raises(Exit):
#         update(contract.id, -50, collaborator=True)
    
#     captured = capsys.readouterr()
    
#     assert "Veuillez entrer un numéro de collaborateur valide." in captured.out.strip()
    
# def test_total_sum_update_successful(monkey_token_check_management, fake_contract, capsys):
#     contract = fake_contract
#     new_total_sum = 1000
    
#     update(contract.id, new_total_sum, total_sum=True)

#     updated_contract = Contract.get(Contract.id == contract.id)
    
#     captured = capsys.readouterr()
    
#     assert updated_contract.total_sum == new_total_sum
#     assert f"Le champ 'Montant total' du contrat n°{contract.id} a été mis à jour avec succès." in captured.out.strip()
    
# def test_amount_due_update_successful(monkey_token_check_management, fake_contract, capsys):
#     contract = fake_contract
#     new_amount_due = 1000
    
#     update(contract.id, new_amount_due, amount_due=True)

#     updated_contract = Contract.get(Contract.id == contract.id)
    
#     captured = capsys.readouterr()
    
#     assert updated_contract.amount_due == new_amount_due
#     assert f"Le champ 'Montant dû' du contrat n°{contract.id} a été mis à jour avec succès." in captured.out.strip()
    
# def test_creation_date_update_successful(monkey_token_check_management, fake_contract, capsys):
#     contract = fake_contract
#     new_creation_date = "2023-10-25"
    
#     update(contract.id, new_creation_date, creation_date=True)

#     updated_contract = Contract.get(Contract.id == contract.id)
    
#     captured = capsys.readouterr()
    
#     assert updated_contract.creation_date == datetime(2023, 10, 25)
#     assert f"Le champ 'Date de création' du contrat n°{contract.id} a été mis à jour avec succès." in captured.out.strip()
    
# def test_signed_update_successful(monkey_token_check_management, fake_contract, capsys):
#     contract = fake_contract
    
#     update(contract.id, True, signed=True)

#     updated_contract = Contract.get(Contract.id == contract.id)
    
#     captured = capsys.readouterr()
    
#     assert updated_contract.signed == True
#     assert f"Le champ 'Signé' du contrat n°{contract.id} a été mis à jour avec succès." in captured.out.strip()
    
    
# def test_contract_update_fails_without_attributes(monkey_token_check_management, fake_contract, capsys):
#     contract = fake_contract
    
#     with pytest.raises(Exit):
#         update(contract.id, "10")
    
#     captured = capsys.readouterr()
    
#     assert "Vous n'avez pas sélectionné d'attribut à modifier." in captured.out.strip()
    
# def test_contract_update_fails_with_wrong_contract_id(monkey_token_check_management, capsys):
#     fake_id = 100
#     with pytest.raises(Exit):
#         update(fake_id, 2, client=True)
    
#     captured = capsys.readouterr()
    
#     assert f"Aucun contrat trouvé avec l'ID n°{fake_id}." in captured.out.strip()
    
# def test_contract_update_not_authorized(monkey_token_check_support, fake_contract, capsys):
#     contract = fake_contract
    
#     with pytest.raises(Exit):
#         update(contract.id, 2, client=True)
    
#     captured = capsys.readouterr()
    
#     assert "Action restreinte." in captured.out.strip()
    
# def test_contract_update_fails_without_authentication(monkey_token_check_false, fake_contract, capsys):
#     contract = fake_contract
    
#     with pytest.raises(Exit):
#         update(contract.id, 2, client=True)
    
#     captured = capsys.readouterr()
    
#     assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
    
# def test_contract_update_fails_with_wrong_salesman(monkey_token_check_fake_sales, fake_contract, capsys):
#     contract = fake_contract
    
#     with pytest.raises(Exit):
#         update(contract.id, 2, client=True)
    
#     captured = capsys.readouterr()
    
#     assert "Action restreinte." in captured.out.strip()
    
# def test_contract_update_with_correct_salesman_succesful(monkey_token_check_correct_sales, fake_contract, fake_client, capsys):
#     print(fake_contract.collaborator.id)
#     update(fake_contract.id, fake_client.id, client=True)

#     updated_contract = Contract.get(Contract.id == fake_contract.id)
    
#     captured = capsys.readouterr()
    
#     assert updated_contract.client.id == fake_client.id
#     assert f"Le champ 'Client' du contrat n°{fake_contract.id} a été mis à jour avec succès." in captured.out.strip()