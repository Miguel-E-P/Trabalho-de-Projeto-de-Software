#Fixture do Pytest para configurar o SQLite :memory:
# para a suíte de testes de integração.

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from estacionamento.adapters.orm import metadata, start_mappers


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()