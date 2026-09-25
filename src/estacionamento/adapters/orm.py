from sqlalchemy import Column, ForeignKey, MetaData, String, Table, Uuid, TypeDecorator
from sqlalchemy.orm import registry, relationship

from estacionamento.domain.model import Cliente, Placa, Veiculo

#Mapeamento Imperativo (registry.map_imperatively)
#Este arquivo faz a ligação entre o SQLite/SQLAlchemy e o modelo 
#puro (Cliente, Veiculo, Placa) sem poluir as dataclasses do domínio
#com dependências do ORM
#Type decoarator para traduzir objetos uuid / str para sql
metadata = MetaData()
mapper_registry = registry(metadata=metadata)


metadata = MetaData()
mapper_registry = registry(metadata=metadata)


# Mapeador para o Value Object Placa
class PlacaType(TypeDecorator):
    impl = String(10)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        # Se value for um objeto Placa, extrai a string interna (value.numero)
        if isinstance(value, Placa):
            return value.numero
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        # Ao ler do banco, reconstrói o Value Object Placa com a string limpa
        return Placa(value)


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
    Column("placa", PlacaType(), nullable=False),
    Column("tipo", String(50), nullable=False),
)


def start_mappers():
    mapper_registry.map_imperatively(Veiculo, veiculos_table)
    mapper_registry.map_imperatively(
        Cliente,
        clientes_table,
        properties={
            "veiculos": relationship(Veiculo, backref="cliente"),
        },
    )

    #Parcial do mapeamento ORM para o agregado Cliente