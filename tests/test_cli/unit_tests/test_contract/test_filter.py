import pytest
from typer import Exit
from epicevents.cli.contract import filter


def test_filter_signed_successful(
    monkey_token_check_correct_sales,
    fake_contract,
    fake_contract2,
    fake_contract3,
    fake_contract_unsigned,
    capsys,
):
    """
    GIVEN a sales collaborator with the correct token and a set of contracts with different signed statuses
    WHEN the filter() function is called to filter signed contracts
    THEN the function should display contracts with signed status 'True' and not display contracts with signed status 'False'
    """
    filter(ns=True)

    captured = capsys.readouterr()

    assert "3200.0" in captured.out.strip()
    assert "False" in captured.out.strip()
    assert "True" not in captured.out.strip()
    assert "10000.0" not in captured.out.strip()
    assert "None" not in captured.out.strip()


def test_filter_signed_fails_with_null_queryset(
    monkey_token_check_correct_sales,
    capsys,
):
    """
    GIVEN a sales collaborator with the correct token and an empty set of contracts
    WHEN the filter() function is called to filter signed contracts
    THEN the function should raise an exit error, and an error message should indicate that all contracts are signed
    """
    with pytest.raises(Exit):
        filter(ns=True)

    captured = capsys.readouterr()

    assert "Tous les contrats sont signés !" in captured.out.strip()


def test_filter_unpaid_successful(
    monkey_token_check_correct_sales,
    fake_contract,
    fake_contract2,
    fake_contract3,
    fake_contract_unsigned,
    capsys,
):
    """
    GIVEN a sales collaborator with the correct token and a set of contracts with different unpaid amounts
    WHEN the filter() function is called to filter unpaid contracts
    THEN the function should display contracts with unpaid amount or with 'None' value
    """
    filter(u=True)

    captured = capsys.readouterr()

    assert "3200.0" in captured.out.strip()
    assert "None" in captured.out.strip()


def test_filter_unpaid_fails_with_null_queryset(
    monkey_token_check_correct_sales,
    capsys,
):
    """
    GIVEN a sales collaborator with the correct token and an empty set of contracts
    WHEN the filter() function is called to filter unpaid contracts
    THEN the function should raise an exit error, and an error message should indicate that all contracts are paid
    """
    with pytest.raises(Exit):
        filter(u=True)

    captured = capsys.readouterr()

    assert "Tous les contrats sont payés !" in captured.out.strip()


def test_filter_fails_without_attribute(
    monkey_token_check_correct_sales,
    fake_contract,
    fake_contract2,
    fake_contract3,
    fake_contract_unsigned,
    capsys,
):
    """
    GIVEN a sales collaborator with the correct token and a set of contracts
    WHEN the filter() function is called without specifying a filter attribute
    THEN the function should raise an exit error, and an error message should indicate that no filter was selected
    """
    with pytest.raises(Exit):
        filter()

    captured = capsys.readouterr()

    assert "Vous n'avez pas sélectionné de filtre à appliquer." in captured.out.strip()


def test_filter_not_authorized(
    monkey_token_check_support,
    fake_contract,
    fake_contract2,
    fake_contract3,
    fake_contract_unsigned,
    capsys,
):
    """
    GIVEN a support collaborator with the correct token and a set of contracts
    WHEN the filter() function is called to filter contracts
    THEN the function should raise an exit error, and an error message should indicate that the action is restricted
    """
    with pytest.raises(Exit):
        filter()

    captured = capsys.readouterr()

    assert "Action restreinte." in captured.out.strip()


def test_filter_fails_without_authentication(
    monkey_token_check_false,
    fake_contract,
    fake_contract2,
    fake_contract3,
    fake_contract_unsigned,
    capsys,
):
    """
    GIVEN an unauthenticated collaborator and a set of contracts
    WHEN the filter() function is called to filter contracts
    THEN the function should raise an exit error, and an error message should indicate that authentication is required
    """
    with pytest.raises(Exit):
        filter()

    captured = capsys.readouterr()

    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
