# 0001. Consolidação e Validação E2E do Agregado Cliente com Apoio de IA

* **Status:** Aceito (Fase 1)[cite: 31] (slide aula)
* **Data:** 16/10/2026
* **Autor:** Kennedy Soares

---

## 1. Contexto

Durante a finalização do *checkpoint* da Fase 1, foi necessário assegurar que o **Agregado Cliente** (`Cliente`, `Veiculo` e `Placa`) estivesse totalmente funcional e integrado antes de avançar para a Fase 2 do projeto. 

Identificou-se uma sequência de falhas nos testes de integração e End-to-End (E2E) decorrentes do mapeamento imperativo do SQLAlchemy com o banco SQLite. As falhas eram causadas por:
1. Erros de *binding* e conversão do tipo nativo `UUID` para a coluna de chave estrangeira (`id_cliente`) no SQLite.
2. Incompatibilidade nos acessos aos atributos do Value Object `Placa` (acesso direto vs. atributo `.numero`).
3. Falta de validação completa do fluxo API HTTP dos casos de uso UC01 (Cadastrar Cliente) e UC02 (Cadastrar Veículo).

---

## 2. Declarativo do Uso de Inteligência Artificial

Para diagnosticar e corrigir os erros recorrentes dos testes de integração sem violar o isolamento do domínio, foi utilizada assistência de Inteligência Artificial. A IA auxiliou em:
- Implementação da classe customizada `GUID` estendendo `TypeDecorator` no SQLAlchemy (`adapters/orm.py`) para tratar a conversão bi-direcional de UUID/string no SQLite.
- Ajuste no alinhamento do DTO e acesso aos atributos do Value Object `Placa` na camada de serviço (`service_layer/services.py`).
- Refatoração dos scripts de testes E2E do endpoint REST (`tests/e2e/test_api.py`).

---

## 3. Decisão

1. **Priorizar a Estabilização do Agregado Cliente:** Concluir o checkpoint da Fase 1 focando na consolidação e aprovação integral de 100% dos testes unitários, de repositório e E2E do Agregado Cliente, estabelecendo uma base confiável para o projeto.
2. **Manter Mapeamento Imperativo:** Corrigir os conectores de persistência através de `TypeDecorator` customizado (`GUID`), mantendo a classe `Cliente` do modelo de domínio estritamente desacoplada do SQLAlchemy (Python puro)[cite: 31] (slide aula).
3. **Validação E2E do Fluxo Principal:** Cobrir via testes automatizados em `test_api.py` as três operações fundamentais do agregado:
   - **UC01:** Cadastrar Cliente via API (`POST /clientes`).
   - **UC02:** Cadastrar Veículo para o Cliente (`POST /clientes/{id}/veiculos`).
   - **Validação E2E:** Consultar Cliente e verificar a correta persistência e relacionamento dos veículos inseridos (`GET /clientes/{id}`).

---

## 4. Alternativas Consideradas

* **Migrar para Mapeamento Declarativo (Herança do ORM):**
  - *Abordagem:* Fazer a classe `Cliente` herdar de `Base` do SQLAlchemy.
  - *Por que foi descartada:* Viola o princípio do *Cosmic Python* e da Arquitetura Hexagonal, acoplando a camada de domínio à biblioteca de persistência e prejudicando a testabilidade limpa sem banco[cite: 31] (slide aula).
* **Avançar para a Fase 2 sem cobrir o E2E do Agregado Cliente:**
  - *Abordagem:* Deixar os testes de integração para a fase posterior.
  - *Por que foi descartada:* Traaria alto risco técnico ao acumular dívidas técnicas e falhas de persistência para as etapas com novos frameworks/tecnologias.

---

## 5. Consequências e Trade-offs

* **(+) Alta Confiabilidade:** Garantia de funcionamento ponta a ponta do Agregado Cliente (48 testes aprovados em ~1.05s no `pytest`).
* **(+) Preservação do Isolamento do Domínio:** A camada `domain/` continua com 0 dependências de infraestrutura/ORM[cite: 31, 35] (slide aula).
* **(+) Segurança para a Fase 2:** Transição para novas demandas, frameworks ou refatorações arquiteturais com suporte de uma suíte de testes E2E regressiva.
* **(-) Complexidade em `orm.py`:** Necessidade de escrever e manter conversores manuais de tipo (`GUID`, `PlacaType`) no mapeamento imperativo (128 linhas de código em `adapters/orm.py`)[cite: 31, 35] (slide aula).

---

## 6. Evidências do Repositório

* **Suíte de Testes:** `python -m pytest -o pythonpath=src`
  - *Resultado:* **48 passed in 1.05s** (suíte 100% verde).
* **Isolamento de Domínio:** `grep -rn "sqlalchemy" src/estacionamento/domain/`
  - *Resultado:* **0 ocorrências**[cite: 35] (slide aula).
* **Arquivos do Agregado Impactados:**
  - `src/estacionamento/domain/model.py`
  - `src/estacionamento/adapters/orm.py`
  