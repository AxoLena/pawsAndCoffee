import pytest
import os

def is_test():
    return os.environ.get('MODE') == 'TEST'

@pytest.fixture(autouse=True, scope='session')
def django_db_setup():
    if is_test():
	    print('ok')
    
    
# @pytest.fixture(scope='function')
# def create_cat(db, mocker):
#     if is_test():
#         isinstance = mocker.path("Cats.models.Cats")
#         return isinstance