from uuid import uuid4
from datetime import datetime
from sqlalchemy import text
from estacionamento.adapters.repository import SqlAlchemyRepository, SqlAlchemyPagamentoRepository
from estacionamento.domain.model import Cliente, Placa, Veiculo
from estacionamento.domain import model

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

#PAGAMENTO INI

def test_sqlalchemy_repository_salva_pagamento(session):
    repo = SqlAlchemyPagamentoRepository(session)
    dinheiro = 80.00
    pagamento = model.Pagamento(
        id_ticket=105,
        valor=dinheiro,
        tipo_pagamento=model.TipoPagamento.PIX,
        data_hora_pagamento=datetime(2023, 11, 10, 9, 15)
    )

    repo.add(pagamento)
    session.commit()

    rows = session.execute(
        text("SELECT id_ticket, valor, tipo_pagamento FROM pagamentos WHERE id_ticket = 105")
    ).fetchall()

    assert [tuple(row) for row in rows] == [(105, 80.00, "PIX")]


def test_sqlalchemy_repository_recupera_pagamento(session):
    session.execute(
        text(
            "INSERT INTO pagamentos (id_ticket, valor, tipo_pagamento, data_hora_pagamento) "
            "VALUES (202, 25.0, 'DEBITO', '2023-10-27 15:00:00.000000')"
        )
    )
    session.commit()

    repo = SqlAlchemyPagamentoRepository(session)
    pagamento_recuperado = repo.get(id_ticket=202)

    assert pagamento_recuperado is not None
    assert pagamento_recuperado.id_ticket == 202
    assert isinstance(pagamento_recuperado.valor, float)
    assert pagamento_recuperado.valor == 25.0
    assert pagamento_recuperado.tipo_pagamento == model.TipoPagamento.DEBITO