from uuid import uuid4
from estacionamento.adapters.repository import SqlAlchemyRepository
from estacionamento.domain.model import Cliente, Placa, Veiculo

#Teste de integração real com o SQLite/SQLAlchemy garante a 
# persistência do Agregado Cliente completo 
# (incluindo a lista de Veiculo).

def test_repository_pode_salvar_e_buscar_cliente_com_veiculos(session):
    repo = SqlAlchemyRepository(session)

    id_cliente = str(uuid4())
    cliente = Cliente(
        id_cliente=id_cliente,
        nome="Carlos",
        cpf="98765432100",
        telefone="21988887777",
        email="carlos@email.com",
    )
    veiculo = Veiculo(id_veiculo=str(uuid4()), placa=Placa("ABC1D23"), tipo="Carro")
    cliente.cadastrar_veiculo(veiculo)

    # 1. Adiciona e realiza commit
    repo.add(cliente)
    session.commit()

    # 2. Limpa a sessão para garantir que a consulta virá do banco SQLite (round-trip)
    session.expire_all()

    # 3. Busca do banco real
    cliente_recuperado = repo.get(id_cliente)

    assert cliente_recuperado is not None
    assert cliente_recuperado.nome == "Carlos"
    assert len(cliente_recuperado.veiculos) == 1
    assert cliente_recuperado.veiculos[0].placa == Placa("ABC1D23")