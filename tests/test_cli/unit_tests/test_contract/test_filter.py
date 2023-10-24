import pytest
from typer import Exit
from epicevents.cli.contract import filter
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def test_filter_signed_successful(
    monkey_token_check_correct_sales,
    fake_contract,
    fake_contract2,
    fake_contract3,
    fake_contract_unsigned,
    capsys,
):
    filter(ns=True)

    captured = capsys.readouterr()

    assert "[Montant restant dû] : 3200.0" in captured.out.strip()
    assert "[Contrat signé ?] : False" in captured.out.strip()
    assert "[Contrat signé ?] : True" not in captured.out.strip()
    assert "[Montant restant dû] : 10000.0" not in captured.out.strip()
    assert "[Montant restant dû] : None" not in captured.out.strip()


def test_filter_unpaid_successful(
    monkey_token_check_correct_sales,
    fake_contract,
    fake_contract2,
    fake_contract3,
    fake_contract_unsigned,
    capsys,
):
    filter(u=True)

    captured = capsys.readouterr()

    assert "[Montant restant dû] : 3200.0" in captured.out.strip()
    assert "[Montant restant dû] : None" in captured.out.strip()
    assert "[Montant restant dû] : 0.0" not in captured.out.strip()


def test_filter_fails_without_attribute(
    monkey_token_check_correct_sales,
    fake_contract,
    fake_contract2,
    fake_contract3,
    fake_contract_unsigned,
    capsys,
):
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
    with pytest.raises(Exit):
        filter()

    captured = capsys.readouterr()

    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
