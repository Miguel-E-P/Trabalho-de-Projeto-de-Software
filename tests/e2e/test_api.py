import pytest
from estacionamento.entrypoints.flask_app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_api_uc01_e_uc02_fluxo_completo_cliente(client):
    # 1. UC01 - Cadastrar Cliente via API
    payload_cliente = {
        "nome": "Mariana Lima",
        "cpf": "12345678900",
        "telefone": "21988887777",
        "email": "mariana@email.com",
    }
    res_cliente = client.post("/clientes", json=payload_cliente)
    assert res_cliente.status_code == 201
    id_cliente = res_cliente.get_json()["id_cliente"]

    # 2. UC02 - Cadastrar Veículo para o Cliente
    payload_veiculo = {
        "placa": "ABC1D23",
        "tipo": "Carro",
    }
    res_veiculo = client.post(f"/clientes/{id_cliente}/veiculos", json=payload_veiculo)
    assert res_veiculo.status_code == 201
    assert "id_veiculo" in res_veiculo.get_json()

    # 3. Validação E2E - Consultar Cliente e verificar veiculo inserido
    res_busca = client.get(f"/clientes/{id_cliente}")
    assert res_busca.status_code == 200
    dados = res_busca.get_json()
    assert dados["nome"] == "Mariana Lima"
    assert len(dados["veiculos"]) == 1
    assert dados["veiculos"][0]["placa"] == "ABC1D23"


def test_api_retorna_404_para_cliente_inexistente(client):
    id_fake = "00000000-0000-0000-0000-000000000000"
    payload_veiculo = {"placa": "XYZ9Y88", "tipo": "Moto"}
    res = client.post(f"/clientes/{id_fake}/veiculos", json=payload_veiculo)
    assert res.status_code == 404

#Fim do test end 2 end (e2e) para agregado Cliente