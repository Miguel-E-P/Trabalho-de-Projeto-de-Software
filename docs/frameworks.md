# Frameworks do sistema
Como fomos orientados pelo professor na Fase 1, usamos três frameworks pra desenvolver nosso sistema: **Flask** (API), **SQLAlchemy** (persistência) e **pytest** (testes). Esta análise mostra o papel de cada um, a camada em que aparece, onde ele chama o código do grupo, quais padrões de projeto ele usa por dentro e o que mudaria com o Django.

## Flask
Papel: Recebe as requisições HTTP, converte entrada e saída (JSON e código de status), cria o repositório e garante o fechamento da sessão do banco. <br>
Camada: Entrypoints: `entrypoints/flask_app.py`, testado em `tests/e2e/test_api.py`.  <br>
Por que o domínio não depende dele:  Só o `flask_app.py` o importa. Ele chama a camada de serviço com parâmetros Python simples, e `service_layer/services.py` e `domain/model.py` não conhecem HTTP.  <br>

## SQLAlchemy
**Papel**: É responsável pela persistência dos dados, além de gerenciar as sessões e transações com o banco de dados. Ele usa o ORM (Object Relational Mapper) pra mapear objetos Python em tabelas do banco e vice-versa, permitindo realizar operações básicas como consulta, inserção, atualização e exclusão sem precisar escrever todo o SQL manualmente.

**Camada**: aparece na camada de infraestrutura (adapters), nos repositórios concretos responsáveis pela comunicação com o banco de dados. Essa camada implementa os contratos definidos pelo domínio e utiliza o SQLAlchemy para executar as operações de persistência.

**Por que o domínio não depende dele**: O domínio não importa nem conhece o SQLAlchemy, ele só define as regras de negócio e as abstrações dos repositórios, enquanto os adapters implementa essas abstrações utilizando o ORM. Assim, podemos substituir o SQLAlchemy por outra tecnologia de persistência sem precisar modificar as regras de negócio.

### Pytest

Papel: Descobre e executa todos os testes do sistema (114 unitários, 7 de integração e 2 e2e), entrega aos testes os recursos de que precisam (banco em memória, cliente HTTP) e relata o resultado. Também oferece pytest.raises e parametrize, que usamos para checar as exceções de domínio e repetir um teste com várias entradas. <br> 
Camada: Fica fora de src/, em tests/, com uma pasta por camada: unit/ testa domain/ e service_layer/ com os repositórios Fake, integration/ testa adapters/ com SQLite em memória e e2e/ testa entrypoints/ pela API. A configuração está em tests/pytest.ini e o banco dos testes, em tests/conftest.py. <br> 
Por que o domínio não depende dele: A dependência vai só dos testes para o código: tests/ importa domain, adapters e service_layer, e nenhum arquivo de src/ importa o pytest. O comando grep -rnE "sqlalchemy|flask|pytest|django" src/estacionamento/domain/ retorna 0 ocorrências. Como os testes unitários usam Fakes no lugar do banco, a suíte unitária roda em cerca de 0,1 s. <br>