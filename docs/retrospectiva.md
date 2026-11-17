# Relatório de Retrospectiva
Mesmo depois de implementar os casos de uso, refatorar os agregados e aplicar princípios SOLID e padrões GoF, decidimos manter a Arquitetura Hexagonal Monolítica, mas usando suas abstrações de forma proporcional à complexidade de cada fluxo. 

A separação entre domínio, serviços e infraestrutura trouxe benefícios concretos, de testabilidade e organização, e também revelou custos de indireção e manutenção que nem todo caso de uso exige. Vimos que fazia sentido com nosso contexto, compreendendo a escolha do professor e dos autores do livro-texto que usamos nessa disciplina. 

Ainda assim, tivemos sorte em ver outras arquiteturas com os professores nessa segunda fase do projeto. É muito melhor tomar uma decisão sabendo das alternativas e consideramos elas ao decorrer do projeto.


## 1. Nossas Previsões
A previsão mais acertada foi a de testabilidade: o domínio permaneceu independente dos frameworks (Flask, SQLAlchemy e pytest), logo, os testes unitários puderam rodar sem iniciar a API ou o banco. O uso de repositórios Fake permitiu validar rapidamente regras e contratos durante as refatorações.


## 2. Revisitação da Análise do Checkpoint 1: Previsões vs. Realidade

| Previsão / Hipótese Inicial (CP1) | Confirmação na Prática | Trade-offs que Pesaram na Prática |
| :--- | :--- | :--- |
| *O isolamento do domínio facilitaria os testes unitários.* | **Confirmada com Louvor.** | A suíte de 57 testes unitários do modelo roda isoladamente na memória em apenas **0.61s**, sem necessidade de mockar o banco de dados ou subir servidores HTTP[cite: 19]. |
| *Haveria um custo maior de escrita de código boilerplate.* | **Confirmada.** | A necessidade de escrever repositórios, DTOs e mapeadores imperativos exigiu mais arquivos e linhas de código do que uma abordagem tradicional de Active Record. |
| *A arquitetura permitiria evoluir o domínio sem quebrar a API.* | **Confirmada.** | A refatoração do Value Object `Placa` (commit `841bc73`) e a introdução dos padrões GoF ocorreram de forma transparente, sem alterar as assinaturas dos endpoints HTTP. |

---

## 3. Evidências da Fase 2: Facilitadores vs. Obstáculos nas Refatorações e Padrões

As camadas isoladas atuaram como facilitadores diretos nas alterações realizadas na Fase 2 no Agregado Cliente:

### A. Refatoração SOLID (Checkpoint 2) — Value Object `Placa`
* **Situação "Antes" (Commit `1564c18` em 29-09-26):** A classe `Placa` era um contêiner anêmico (`@dataclass(frozen=True) class Placa: numero: str`), violando o **SRP** (não garantia suas invariantes) e o **OCP** (exigia condicionais externas para novos formatos).
* **Solução "Depois" (Commit `841bc73`):** Encapsulamento da validação no `__post_init__` com regex flexível (`r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$'`).
* **Impacto das Camadas:** A mudança ficou contida 100% dentro do arquivo do modelo de domínio (`model.py`). Nenhuma linha da camada de serviço (`services.py`) ou dos controladores HTTP (`api.py`) precisou ser modificada.

### B. Aplicação dos Padrões GoF (Checkpoint 3) — Agregado Cliente
* **Strategy (Comportamental):** A interface `EstrategiaDesconto` (`SemDesconto`, `DescontoMensalista`, `DescontoVIP`) foi acoplada à raiz `Cliente`. A alteração da política de preços foi implementada sem impactar a estrutura de persistência[cite: 21].
* **Factory Method (Criacional):** Aplicado à criação de `Veiculo` através de `CriadorVeiculo` (`CriadorCarro`, `CriadorMoto`), padronizando o atributo `tipo` e a criação de UUIDs sem alterar os repositórios[cite: 21].

### C. Evidência Consolidada da Suíte de Testes
A eficácia do isolamento e a ausência de regressões foram comprovadas pela execução automatizada:
* **Testes Unitários de Modelo (`tests/unit/test_model.py`):** `57 passed in 0.61s` (verificando validações de placas antigas/Mercosul, exceções para entradas nulas/inválidas, trocas dinâmicas de Strategy e geração via Factory Method).
* **Suíte Completa do Sistema (`python -m pytest -o pythonpath=src`):** `123 passed in 1.43s` (abrangendo testes de API E2E, repositórios de integração, modelo, serviços, Facade e Observers).

---

## 4. Justificativa da Decisão Arquitetural

Conforme analisado na Aula 9 sobre os custos e benefícios de frameworks[cite: 22, 23], o custo inicial de abstração e escrita de código de infraestrutura[cite: 23] é largamente compensado pelo reúso de projeto, manutenibilidade e alta velocidade de suíte de testes[cite: 3, 23]. 

A capacidade de rodar a suíte completa de 123 testes em 1.43s e refatorar invariantes de domínio complexas com zero regressão confirma que **manter a Arquitetura em Camadas com Domínio Isolado é a solução mais robusta e sustentável.**
