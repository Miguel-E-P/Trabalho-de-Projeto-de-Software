from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from estacionamento.adapters.orm import metadata, start_mappers
from estacionamento.adapters.repository import SqlAlchemyRepository
from estacionamento.service_layer import services

app = Flask(__name__)

# Configuração de Banco para In-Memory (pode ser sobrescrita nos testes)
engine = create_engine("sqlite:///:memory:")
metadata.create_all(engine)
try:
    start_mappers()
except Exception:
    pass  # Evita erro se os mappers já tiverem sido inicializados

get_session = sessionmaker(bind=engine)


@app.route("/clientes", methods=["POST"])
def endpoint_cadastrar_cliente():
    data = request.get_json()
    session = get_session()
    repo = SqlAlchemyRepository(session)

    try:
        id_cliente = services.cadastrar_cliente(
            nome=data["nome"],
            cpf=data["cpf"],
            telefone=data["telefone"],
            email=data["email"],
            repo=repo,
            session=session,
        )
        return jsonify({"id_cliente": id_cliente}), 201
    except KeyError as e:
        return jsonify({"message": f"Campo obrigatório ausente: {str(e)}"}), 400
    finally:
        session.close()


@app.route("/clientes/<id_cliente>/veiculos", methods=["POST"])
def endpoint_cadastrar_veiculo_cliente(id_cliente):
    data = request.get_json()
    session = get_session()
    repo = SqlAlchemyRepository(session)

    try:
        id_veiculo = services.cadastrar_veiculo_cliente(
            id_cliente_str=id_cliente,
            placa_str=data["placa"],
            tipo=data["tipo"],
            repo=repo,
            session=session,
        )
        return jsonify({"id_veiculo": id_veiculo}), 201
    except services.ClienteNaoEncontradoException as e:
        return jsonify({"message": str(e)}), 404
    except (ValueError, services.InvalidInputException) as e:
        return jsonify({"message": str(e)}), 400
    finally:
        session.close()


@app.route("/clientes/<id_cliente>", methods=["GET"])
def endpoint_buscar_cliente(id_cliente):
    session = get_session()
    repo = SqlAlchemyRepository(session)

    try:
        cliente_dict = services.buscar_cliente(id_cliente, repo)
        return jsonify(cliente_dict), 200
    except services.ClienteNaoEncontradoException as e:
        return jsonify({"message": str(e)}), 404
    finally:
        session.close()

#Fim do entrypoint para o agregado Cliente