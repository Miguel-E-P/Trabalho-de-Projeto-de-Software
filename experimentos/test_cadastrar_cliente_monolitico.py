import pytest
import experimentos.cadastrar_cliente_monolitico as mono


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Configura um banco SQLite temporário e retorna o test_client do Flask."""
    db_file = tmp_path / "test_monolitico.db"
    monkeypatch.setattr(mono, "DB_PATH", str(db_file))
    mono.init_db()
    mono.app.config["TESTING"] = True

    with mono.app.test_client() as client:
        yield client


def test_deve_cadastrar_cliente_e_veiculo_com_sucesso(client):
    payload = {
        "nome": "João Silva",
        "cpf": "12345678900",
        "telefone": "21999998888",
        "email": "joao@email.com",
        "placa": "ABC1D23",
        "tipo": "CARRO",
    }

    resp = client.post("/clientes", json=payload)
    dados = resp.get_json()

    assert resp.status_code == 201
    assert dados["nome"] == "João Silva"
    assert dados["veiculo"]["placa"] == "ABC1D23"
    assert dados["veiculo"]["tipo"] == "CARRO"


@pytest.mark.parametrize("placa_invalida", ["", "ABC", "1234567", "AB123CD", "@@@-1234"])
def test_deve_rejeitar_placas_invalidas_via_http(client, placa_invalida):
    payload = {
        "nome": "Maria Souza",
        "cpf": "98765432100",
        "placa": placa_invalida,
        "tipo": "MOTO",
    }

    resp = client.post("/clientes", json=payload)
    assert resp.status_code == 400
    assert "Placa inválida" in resp.get_json()["erro"]


def test_deve_barrar_cpf_ou_placa_duplicados_no_banco(client):
    payload = {
        "nome": "Carlos Lima",
        "cpf": "11122233344",
        "placa": "XYZ-9876",
        "tipo": "CARRO",
    }

    resp1 = client.post("/clientes", json=payload)
    assert resp1.status_code == 201

    resp2 = client.post("/clientes", json=payload)
    assert resp2.status_code == 409
    assert "Conflito de dados" in resp2.get_json()["erro"]