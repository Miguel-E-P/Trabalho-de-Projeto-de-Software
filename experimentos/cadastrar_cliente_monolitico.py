import re
import sqlite3
from uuid import uuid4
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_PATH = "estacionamento_monolitico.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                telefone TEXT,
                email TEXT,
                categoria TEXT DEFAULT 'AVULSO'
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS veiculos (
                id TEXT PRIMARY KEY,
                cliente_id TEXT NOT NULL,
                placa TEXT NOT NULL UNIQUE,
                tipo TEXT NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            )
        """)


@app.route("/clientes", methods=["POST"])
def cadastrar_cliente_e_veiculo():
    dados = request.get_json(silent=True) or {}

    nome = dados.get("nome")
    cpf = dados.get("cpf")
    placa_raw = dados.get("placa", "")
    tipo_veiculo = dados.get("tipo", "CARRO").upper()

    # 1. Validações imperativas acopladas à rota HTTP
    if not nome or not cpf:
        return jsonify({"erro": "Nome e CPF são obrigatórios"}), 400

    placa_limpa = placa_raw.upper().replace("-", "").strip()
    if not re.match(r"^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$", placa_limpa):
        return jsonify({"erro": f"Placa inválida: {placa_raw}"}), 400

    if tipo_veiculo not in ("CARRO", "MOTO"):
        return jsonify({"erro": "Tipo de veículo inválido"}), 400

    # 2. Persistência SQL direta misturada com regras de negócio
    cliente_id = str(uuid4())
    veiculo_id = str(uuid4())

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO clientes (id, nome, cpf, telefone, email) VALUES (?, ?, ?, ?, ?)",
                (cliente_id, nome, cpf, dados.get("telefone"), dados.get("email")),
            )
            conn.execute(
                "INSERT INTO veiculos (id, cliente_id, placa, tipo) VALUES (?, ?, ?, ?)",
                (veiculo_id, cliente_id, placa_limpa, tipo_veiculo),
            )
    except sqlite3.IntegrityError as e:
        return jsonify({"erro": f"Conflito de dados (CPF ou Placa já cadastrado): {e}"}), 409

    return jsonify({
        "id_cliente": cliente_id,
        "nome": nome,
        "cpf": cpf,
        "veiculo": {
            "id_veiculo": veiculo_id,
            "placa": placa_limpa,
            "tipo": tipo_veiculo,
        }
    }), 201


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5001)