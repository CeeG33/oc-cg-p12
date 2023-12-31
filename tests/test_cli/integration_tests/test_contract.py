import pytest
from epicevents.cli import contract
from epicevents.data_access_layer.contract import Contract


def test_contract_create_read_and_update_successful(
    monkey_token_check_management,
    fake_collaborator_sales,
    monkey_capture_message_contract,
    fake_client,
    capsys,
):
    """
    Given a valid management collaborator token,
    When a contract is created with specific details,
    Then the contract should be created and have the expected total sum.

    When listing contracts,
    Then the "Tableau des contrats" should appear in the output.

    When the created contract's amount due is updated to 0,
    Then the updated contract should have the amount due set to 0.0.
    """
    contract.create(
        client=fake_client.id,
        total_sum=1500,
        amount_due=1500,
    )

    created_contract = Contract.get(Contract.total_sum == 1500)

    assert created_contract.total_sum == 1500.0

    contract.list()

    captured = capsys.readouterr()

    assert "Tableau des contrats" in captured.out.strip()

    contract.update(created_contract.id, 0, amount_due=True)

    updated_contract = Contract.get(Contract.total_sum == 1500)

    assert updated_contract.amount_due == 0.0

    updated_contract.delete_instance()
