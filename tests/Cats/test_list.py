import pytest

from Cats.models import FormForAdopt, Cats


class TestAdopt:
	@pytest.mark.django_db
	def test_create_adopt(self, mocker):
		adopt = FormForAdopt(name='Лена', 
								phone='89141112233', 
								email='test@smail.ru', 
								cat_name=1,
								why_this_cat='Он милашка',
								children=False,
								has_pet=True,
								pets='Шпиц')
		assert FormForAdopt.objects.count() == 1