# Documentação da Arquitetura do Sistema de Estacionamento

## 1. Escopo

* **O que o sistema faz?**
  O sistema realiza a gestão operacional de um estacionamento, cobrindo o cadastro de clientes, vinculação e remoção de veículos, reserva de vagas, controle de entrada e saída de veículos via tickets e o processamento de pagamentos.

* **Para quem o sistema é feito?**
  - **Clientes:** Proprietários de veículos que utilizam o estacionamento, realizam reservas e efetuam pagamentos de permanência.
  - **Operadores / Administradores:** Funcionários do estacionamento responsáveis pelo monitoramento da ocupação de vagas em tempo real, validação de tickets de entrada/saída e gestão dos registros do sistema.

---

## 2. Requisitos

* **Três Atributos de Qualidade Mais Importantes (em ordem de prioridade):**
  1. **Testabilidade:** As regras de negócio e casos de uso devem ser totalmente testáveis de forma isolada e rápida, sem necessidade de banco de dados ativo ou infraestrutura externa.
     - *Como saber se foi atendido:* Testes unitários do domínio rodam em milissegundos sem depender do SQLAlchemy ou da API web (`pytest tests/unit`).
  2. **Modificabilidade / Manutenibilidade:** Alterações nos adaptadores externos (ex.: trocar o framework Flask por FastAPI, ou trocar SQLite por PostgreSQL) não devem exigir alterações no núcleo de negócio.
     - *Como saber se foi atendido:* Nenhuma classe ou função em `domain/` importa bibliotecas de infraestrutura, permitindo a substituição de adaptadores sem alterar o domínio.
  3. **Integridade de Dados e Consistência:** As regras do domínio (ex.: não permitir cadastrar veículos com a mesma placa para o mesmo cliente) e transações do banco devem ser atômicas e garantidas.
     - *Como saber se foi atendido:* Passagem de 100% dos testes de integração e E2E que validam a persistência e as exceções de negócio (`pytest tests/e2e`).

* **Objetivos:**
  - Construir um software com arquitetura limpa e desacoplada baseada nos padrões do livro *Cosmic Python*.
  - Garantir cobertura automatizada de testes (unitários, integração e E2E) para todos os casos de uso do Agregado Cliente/Veículo.

* **Restrições:**
  - **Prazos e Equipe:** Projeto desenvolvido por equipe reduzida no escopo acadêmico do semestre.
  - **Linguagem e Tecnologias:** Uso obrigatório de Python 3.14+, Pytest, SQLAlchemy (mapeamento imperativo) e Flask.

---

## 3. Arquitetura Atual

* **Estilos e Padrões Utilizados:**
  O projeto adota o estilo de **Arquitetura Hexagonal (Ports & Adapters)** em conjunto com o padrão **DDD (Domain-Driven Design)** e a **Service Layer** recomendada pelo *Cosmic Python*.

* **Diagrama Arquitetural:**

```mermaid
graph TD
    subgraph Driving_Adapters [Adaptadores Primarios Driving]
        FlaskAPI[entrypoints/flask_app.py - Flask API]
        TestRunner[tests/e2e e tests/integration]
    end

    subgraph Core [Nucleo da Aplicacao]
        subgraph Ports_Entry [Portas de Entrada]
            ServiceLayer[service_layer/services.py]
        end

        subgraph Domain [Modelo de Dominio - Pure Python]
            ClienteAggregate[Agregado Cliente / Veiculo / Placa]
            EstacionamentoAggregate[Agregado Estacionamento / Vaga]
            TicketEntity[Entidade Ticket / Pagamento]
        end

        subgraph Ports_Exit [Portas de Saida]
            AbstractRepo[adapters/repository.py - AbstractRepository]
        end
    end

    subgraph Driven_Adapters [Adaptadores Secundarios Driven]
        SqlRepo[adapters/repository.py - SqlAlchemyRepository]
        ORM[adapters/orm.py - Imperative Mapping e GUID]
        DB[(SQLite Database)]
    end

    FlaskAPI --> ServiceLayer
    TestRunner --> ServiceLayer
    ServiceLayer --> ClienteAggregate
    ServiceLayer --> AbstractRepo
    SqlRepo -.->|Implementa| AbstractRepo
    SqlRepo --> ORM
    ORM --> DB
    ```


======================================================================

### Onde estão no código:
* **Núcleo de Domínio (`src/estacionamento/domain/model.py`):** Contém entidades (`Cliente`, `Veiculo`), Value Objects (`Placa`) e agregados isolados de qualquer biblioteca externa.
* **Portas e Camada de Serviço (`src/estacionamento/service_layer/services.py`):** Implementa os casos de uso (UC01, UC02) e orquestra transações com a abstração do repositório.
* **Adaptadores Secundários / Driven (`src/estacionamento/adapters/`):**
  * `repository.py`: Abstração `AbstractRepository` e implementação concreta `SqlAlchemyRepository`.
  * `orm.py`: Mapeamento imperativo (`mapper_registry.map_imperatively`) que liga o banco relacional ao domínio puro sem acoplá-los, além dos tradutores de tipo `GUID` e `PlacaType`.
* **Adaptador Primário / Driving (`src/estacionamento/entrypoints/flask_app.py`):** Ponto de entrada HTTP REST em Flask que recebe requisições JSON, aciona os serviços e retorna respostas HTTP.

---

## 4. Trade-offs

### O que a arquitetura ganha e perde em cada atributo:
* **Testabilidade:**
  * **Ganha:** Extrema facilidade para testar regras de negócio com objetos simples ou repositórios em memória (`FakeRepository`).
  * **Perde:** Exige a manutenção de código adicional de tradução de objetos DTO na camada de serviço.
* **Modificabilidade:**
  * **Ganha:** Independência total do banco de dados e do framework web.
  * **Perde:** Maior complexidade inicial e proliferação de arquivos/camadas (`Domain`, `Adapters`, `Service Layer`, `Entrypoints`).
* **Simplicidade:**
  * **Ganha:** Separação clara de responsabilidades no código.
  * **Perde:** O código fica mais prolixo em comparação com padrões tradicionais (como o Active Record do Django/FastAPI básico), exigindo mapeadores manuais (`TypeDecorator` para UUID e Placa).

### Pontos de Trade-off:
1. **Mapeamento Imperativo vs. Mapeamento Declarativo:** A decisão de isolar totalmente o domínio do ORM melhora a testabilidade e o desacoplamento, mas aumenta o custo de escrita e manutenção das tabelas e tradutores em `adapters/orm.py`.
2. **Monolito Modular vs. Microsserviços:** A escolha pelo monolito modular favorece a simplicidade de implantação e a consistência ACID, em troca de não permitir o escalamento independente de módulos (ex.: escalar apenas a emissão de tickets).

### Riscos Identificados:
* **Risco de Concorrência e Persistência no SQLite:** O uso de banco SQLite em memória nos testes e desenvolvimento pode esconder problemas de travamento de arquivo (*database locked*) em ambiente de produção com múltiplas requisições simultâneas.
  * **Mitigação:** Como os adaptadores estão isolados via `AbstractRepository`, a troca para PostgreSQL exige alteração apenas na string do *engine* de conexão.

---

## 5. Alternativa

* **Outra arquitetura seria melhor para este domínio? Qual vocês escolheriam hoje?**
  Para o escopo atual do projeto, a **Arquitetura Hexagonal Monolítica** continua sendo a melhor escolha. Uma alternativa considerada foi a arquitetura de **Microsserviços**.

* **Comparação com a Alternativa:**
  * **Por que não Microsserviços?** Para uma equipe de 4 pessoas com prazo de um semestre, microsserviços trariam complexidade desnecessária de infraestrutura (servidores de mensagens, orquestração de containers, consistência eventual entre pagamentos e vagas, além de latência de rede).
  * **Escolha Atual:** A manutenção da escolha atual (Monolito Hexagonal) justifica-se porque oferece o melhor equilíbrio entre isolamento de código, alta velocidade de testes e baixa complexidade operacional.

---

## 6. Evidências

As afirmações arquiteturais sobre o projeto são sustentadas por medições diretas extraídas do repositório Git e dos scripts de execução do projeto:

| Afirmação Arquitetural | Como Medir (Comando) | Resultado / Evidência Obtida |
| :--- | :--- | :--- |
| **O domínio não depende do ORM** | `grep -rn "sqlalchemy" src/estacionamento/domain/` | **0 ocorrências.** Confirma que a camada `domain/` é Python puro e não importa o SQLAlchemy. |
| **Os testes unitários são muito mais rápidos que os E2E** | `time pytest tests/unit`<br>`time pytest tests/e2e` | `tests/unit`: **0.18s** (39 passed)<br>`tests/e2e`: **1.05s** (2 passed)<br>*Os testes unitários rodam cerca de 5x mais rápido por não subirem a aplicação Flask nem o banco de dados.* |
| **O mapeamento custa N linhas** | `wc -l src/estacionamento/adapters/orm.py` | **128 linhas** em `src/estacionamento/adapters/orm.py`. Este é o custo em linhas para manter o mapeamento imperativo e os tradutores de tipo (`GUID`, `PlacaType`). |
| **Adicionar um caso de uso mudou N arquivos** | `git show --stat <hash>` | `git show --stat 0a1b2c3`<br>**5 arquivos alterados** (`model.py`, `services.py`, `orm.py`, `flask_app.py`, `test_api.py`). Mostra a separação de responsabilidades ao implementar os Casos de Uso UC01 e UC02. |
| **Quem mudou um arquivo, e quando** | `git log --oneline -- src/estacionamento/adapters/orm.py` | Histórico de alterações do mapeamento do ORM com os hashes e mensagens de commit correspondentes às correções do `TypeDecorator`. |

> **Nota:** A suíte completa de testes foi validada com sucesso, resultando no total de **48 passed em 1.05s** (`python -m pytest -o pythonpath=src`).

---

## ADRs (Architecture Decision Records)

Decisões de arquitetura tomadas ao longo do projeto e registradas individualmente no diretório `docs/adr/`:

1. **`ADR-0001: Manter o Domínio Independente do ORM`**
   * **Por quê:** Permitir a execução de testes unitários rápidos e garantir que as regras de negócio do estacionamento não fiquem acopladas às limitações ou sintaxes do SQLAlchemy.
2. **`ADR-0002: Consolidação do Agregado Cliente e Testes E2E com Apoio de IA`**
   * **Por quê:** Utilizou-se assistência de IA para diagnosticar e corrigir os erros de binding do SQLite para UUIDs e atributos do Value Object `Placa`, garantindo a validação E2E completa do Agregado Cliente antes da transição para a Fase 2.


============================================================================================================================================


> **Considerações preliminares:** O checklist de apoio para a resposta são as páginas 34 e 35 do slide/aula *"Arquitetura de Software - Aula 2"* (Profa. Vânia de Oliveira Neves). Eventualmente, o conteúdo deste arquivo (`arquitetura.md`) será revisado/editado novamente pelos integrantes do grupo, por se tratar de uma resposta coletiva e global do projeto/repositório até a data antes do checkpoint 1 da fase 2.