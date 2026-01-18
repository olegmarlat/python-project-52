import pytest
from django.core.management import call_command


@pytest.fixture(scope="session", autouse=True)
def django_db_setup(django_db_setup, django_db_blocker):
    """Автоматически применяет миграции перед всеми тестами."""
    with django_db_blocker.unblock():
        call_command("migrate", "--noinput")
