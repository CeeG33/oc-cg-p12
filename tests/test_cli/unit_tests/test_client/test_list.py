import pytest
from epicevents.cli.client import list
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


# def test_list_successful(monkey_token_check_management, fake_client, capsys):
#     list()

#     captured = capsys.readouterr()
    
#     assert "[ID]" in captured.out.strip() 

# def test_list_token_fails(monkey_token_check_false, fake_client, capsys):
#     with pytest.raises(InvalidTokenError):
#         list()
    
# def test_list_token_expired(monke, fake_client, capsys):
#     with pytest.raises(ExpiredSignatureError):
#         list()
    
