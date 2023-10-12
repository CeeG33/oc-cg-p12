import pytest
from epicevents.data_access_layer.collaborator import Collaborator
from epicevents.cli.collaborator import list, _memorize_token, _verify_token


def test_list_successful(monkey_dotenv, valid_token, capsys):
    _memorize_token(valid_token)
    
    list()

    captured = capsys.readouterr()
    
    assert "[ID]" in captured.out.strip() 

def test_list_token_fails(monkey_dotenv, capsys):
    list()

    captured = capsys.readouterr()
    
    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
    
def test_list_wrong_department(monkey_dotenv, wrong_department_token, capsys):
    _memorize_token(wrong_department_token)
    
    list()

    captured = capsys.readouterr()
    
    assert "Action restreinte." in captured.out.strip()
    
# def test_list_is_empty(monkey_dotenv, monkeypatch, valid_token, capsys):
#     def mock_count_zero():
#         return []
    
#     monkeypatch.setattr(Collaborator, "select", mock_count_zero)
    
#     _memorize_token(valid_token)
    
#     list()

#     captured = capsys.readouterr()
    
#     assert "La base de donnée ne contient aucun collaborateur." in captured.out.strip() 
