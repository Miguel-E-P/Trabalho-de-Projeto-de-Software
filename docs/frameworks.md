
# Frameworks do sistema - Versão 0
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
# Fim Versão 0

# Versão 1

# Análise e Classificação de Frameworks do Sistema

Este documento analisa os frameworks utilizados no sistema (**Flask/FastAPI**, **SQLAlchemy** e **pytest**), detalhando seus papéis arquiteturais, sua classificação teórica com base na Aula 9 - Frameworks (UFF - Prof. Troy Costa Kohwalter), pontos de inversão de controle (IoC), hot/frozen spots e padrões de projeto internos.

---

## 1. Papel dos Frameworks, Camadas de Atuação e Isolamento do Domínio

Um framework é uma *aplicação quase completa reutilizável que, quando especializada, produz aplicações personalizadas*[cite: 3], provendo reúso não só de código, mas também da arquitetura abstrata da aplicação[cite: 3]. 

Conforme a classificação formal da Aula 9, todos os frameworks utilizados são **frameworks horizontais (de aplicação)**[cite: 12], pois resolvem problemas genéricos e aplicáveis a múltiplos domínios sem dependência de regras de negócio específicas[cite: 12, 13].

| Framework | Camada de Atuação | Papel na Solução | Motivo do Não-Acoplamento com o Domínio |
| :--- | :--- | :--- | :--- |
| **Flask / FastAPI** | Apresentação / API (`src/estacionamento/entrypoints/`) | Roteamento HTTP, serialização/deserialização de JSON e manipulação de respostas HTTP. | O domínio não possui importações HTTP nem conhece a Web. As rotas apenas convertem requisições e delegam a execução aos serviços da aplicação. |
| **SQLAlchemy** | Infraestrutura / Persistência (`src/estacionamento/adapters/`) | Mapeamento Objeto-Relacional (ORM), gestão de sessões de banco de dados e controle de transações SQL. | O modelo de domínio utiliza `dataclasses` puras sem herdar de `db.Model`. O mapeamento é feito via *Data Mapper* na camada de infraestrutura. |
| **pytest** | Testes e Qualidade (`tests/`) | Automação e execução de testes unitários, de integração e end-to-end (E2E). | Os testes exercitam o domínio invocando diretamente métodos Python. O código de produção da regra de negócio não depende nem conhece o pytest. |

---

## 2. Inversão de Controle (IoC) vs. Biblioteca

### Diferença Conceitual
* **Biblioteca:** Um conjunto de classes instanciadas pelo cliente onde **o seu código chama a biblioteca** para executar funções específicas[cite: 18, 19]. O fluxo de controle é gerido pela aplicação[cite: 19].
* **Framework:** Estrutura abstrata que detém o controle do fluxo principal e executa a **Inversão de Controle (IoC)** — o *Princípio de Hollywood: "Não nos chame, nós chamaremos você"*[cite: 18, 19]. **O framework chama o código do grupo** nos pontos de extensão (*hot spots*) previstos no projeto[cite: 19, 24].

### Pontos de Inversão de Controle (IoC) no Sistema:

1. **Registro e Despacho de Rotas HTTP (Flask/FastAPI):**
   * *Funcionamento:* Ao utilizar decoradores (`@app.get("/clientes")`), o grupo registra ganchos de código (*hot spots*)[cite: 24]. O ciclo principal do servidor Web (infraestrutura fixa / *frozen spot*) escuta as requisições e **chama a função do grupo**[cite: 19, 24].
2. **Injeção de Fixtures (pytest):**
   * *Funcionamento:* O executor do pytest inspeciona a assinatura das funções de teste e **injeta/executa automaticamente as fixtures** anotadas com `@pytest.fixture` antes e depois dos testes, gerindo o ciclo de vida da suíte[cite: 19].
3. **Reconstituição de Entidades pelo ORM (SQLAlchemy):**
   * *Funcionamento:* Durante a execução de consultas SQL, o SQLAlchemy intercepta as tuplas do banco e **chama o construtor da classe `Cliente`** para reconstituir o objeto de domínio na memória.

---

## 3. Análise de Hot Spots e Frozen Spots (Aula 9 - Frameworks - UFF)

A arquitetura de um framework é definida pela combinação de seus *Hot Spots* (partes extensíveis) e *Frozen Spots* (infraestrutura fixa que coordena a execução)[cite: 24]:

* **Flask / FastAPI:**
  * **Frozen Spot:** O servidor WSGI/ASGI, o loop de recepção de pacotes HTTP e a desserialização inicial de requisições[cite: 24].
  * **Hot Spot:** As rotas registradas pelo grupo (`@app.get("/clientes")`), que definem a lógica específica dos endpoints[cite: 24].
* **pytest:**
  * **Frozen Spot:** O mecanismo automático de descoberta (*test discovery*) e o ciclo fixo de execução da suíte[cite: 24].
  * **Hot Spot:** As fixtures (`@pytest.fixture`) e os testes customizados do grupo[cite: 24].

---

## 4. Padrões de Projeto Internos dos Frameworks no Código do Grupo

Conforme abordado na Aula 9, frameworks são softwares concretos que utilizam diversos padrões de projeto (GoF) em sua estrutura interna[cite: 21]:

1. **Template Method (no `pytest`):**
   * *Onde aparece:* Na execução da suíte em `tests/unit/test_model.py`.
   * *Aplicação:* O pytest define o esqueleto fixo do ciclo de testes (*setup* -> *execution* -> *teardown*)[cite: 24], permitindo que o grupo preencha as etapas concretas via fixtures e asserções[cite: 15, 21].
2. **Data Mapper / Identity Map (no SQLAlchemy):**
   * *Onde aparece:* Na camada de adaptadores em `src/estacionamento/adapters/repository.py`.
   * *Aplicação:* O SQLAlchemy separa a tabela relacional da entidade `Cliente`, mantendo um *Identity Map* para evitar leitura duplicada de instâncias na mesma sessão sem poluir o domínio com comandos SQL[cite: 21].
3. **Decorator (no Flask / FastAPI):**
   * *Onde aparece:* Nos controladores de rota em `src/estacionamento/entrypoints/api.py`.
   * *Aplicação:* O framework utiliza decoradores em Python para envolver funções de manipulação de rotas com comportamentos transversais (tratamento de erros, serialização JSON e validações HTTP)[cite: 21].

---

## 5. Impacto da Adoção de um Framework Full-Stack (ex.: Django)

Se o grupo tivesse optado por um framework full-stack como o **Django**:

* **Violação do Isolamento do Domínio (*Active Record*):** As entidades de domínio teriam que herdar de `django.db.models.Model`, acoplando diretamente a lógica de negócio às bibliotecas de banco de dados e ao ORM do framework[cite: 19].
* **Perda da Arquitetura em Camadas Decouplada:** O Django impõe o padrão MVT (*Model-Template-View*)[cite: 9], o que dificultaria manter a separação estrita entre a camada de aplicação/serviços e os adaptadores de infraestrutura.
* **Degradação na Velocidade dos Testes Unitários:** Os testes unitários do domínio não poderiam ser executados isoladamente em memória em 0,61s, pois exigiriam o carregamento do ambiente completo e do banco de dados relacional orquestrado pelo Django.
# Fim Versão 1