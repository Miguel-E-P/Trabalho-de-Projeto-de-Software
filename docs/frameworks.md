# Frameworks do sistema

O sistema usa três frameworks: **Flask** (API), **SQLAlchemy** (persistência) e **pytest** (testes). Esta análise mostra o papel de cada um, a camada em que aparece, onde ele chama o código do grupo, quais padrões de projeto ele usa por dentro e o que mudaria com o Django.

## Flask
Papel: Recebe as requisições HTTP, converte entrada e saída (JSON e código de status), cria o repositório e garante o fechamento da sessão do banco. <br>
Camada: Entrypoints: `entrypoints/flask_app.py`, testado em `tests/e2e/test_api.py`.  <br>
Por que o domínio não depende dele:  Só o `flask_app.py` o importa. Ele chama a camada de serviço com parâmetros Python simples, e `service_layer/services.py` e `domain/model.py` não conhecem HTTP.  <br>