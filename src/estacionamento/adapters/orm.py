from sqlalchemy import Column, ForeignKey, MetaData, String, Table
from sqlalchemy.orm import registry, relationship

from estacionamento.domain.model import Cliente, Placa, Veiculo

#Mapeamento Imperativo (registry.map_imperatively)
#Este arquivo faz a ligação entre o SQLite/SQLAlchemy e o modelo 
#puro (Cliente, Veiculo, Placa) sem poluir as dataclasses do domínio
#com dependências do ORM
metadata = MetaData()
mapper_registry = registry(metadata=metadata)

clientes_table = Table(
    "clientes",
    metadata,
    Column("id_cliente", String(36), primary_key=True),
    Column("nome", String(255), nullable=False),
    Column("cpf", String(14), nullable=False),
    Column("telefone", String(20), nullable=False),
    Column("email", String(255), nullable=False),
)

veiculos_table = Table(
    "veiculos",
    metadata,
    Column("id_veiculo", String(36), primary_key=True),
    Column("id_cliente", String(36), ForeignKey("clientes.id_cliente"), nullable=False),
    Column("placa", String(10), nullable=False),
    Column("tipo", String(50), nullable=False),
)


def start_mappers():
    """Inicia o mapeamento imperativo do SQLAlchemy para o modelo de domínio."""
    # Mapeamento do Value Object Placa via Composite
    veiculos_mapper = mapper_registry.map_imperatively(
        Veiculo,
        veiculos_table,
        properties={
            "_placa_str": veiculos_table.c.placa,
        },
    )

    # Mapeamento da Raiz do Agregado Cliente com seus Veículos
    mapper_registry.map_imperatively(
        Cliente,
        clientes_table,
        properties={
            "veiculos": relationship(veiculos_mapper, collection_class=list, cascade="all, delete-orphan"),
        },
    )

    #Parcial do mapeamento ORM para o agregado Cliente