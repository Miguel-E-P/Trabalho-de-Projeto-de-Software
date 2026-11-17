# Relatório de Retrospectiva
Mesmo depois de implementar os casos de uso, refatorar os agregados e aplicar princípios SOLID e padrões GoF, decidimos manter a Arquitetura Hexagonal Monolítica, mas usando suas abstrações de forma proporcional à complexidade de cada fluxo. 

A separação entre domínio, serviços e infraestrutura trouxe benefícios concretos, de testabilidade e organização, e também revelou custos de indireção e manutenção que nem todo caso de uso exige. Vimos que fazia sentido com nosso contexto, compreendendo a escolha do professor e dos autores do livro-texto que usamos nessa disciplina. 

Ainda assim, tivemos sorte em ver outras arquiteturas com os professores nessa segunda fase do projeto. É muito melhor tomar uma decisão sabendo das alternativas e consideramos elas ao decorrer do projeto.


## 1. Nossas Previsões
A previsão mais acertada foi a de testabilidade: o domínio permaneceu independente dos frameworks (Flask, SQLAlchemy e pytest), logo, os testes unitários puderam rodar sem iniciar a API ou o banco. O uso de repositórios Fake permitiu validar rapidamente regras e contratos durante as refatorações.

A modificabilidade foi melhorando a medida que progredimos nos checkpoints, já que conhecer os princípios SOLID, principalmente o SRP e OCP, melhoraram muito nossa forma de desenvolver. Por exemplo, a validação de formato foi transferida para o ValueObject Placa, que passou a proteger sua própria invariante e a aceitar os formatos antigo e Mercosul sem espalhar condicionais pelos serviços. Também usamos padrões de projeto como Strategy e State, que nos ajudaram a garantir mais facilidade de manutenção.

Sobre a segurança, disponibilidade e desempenho, a arquitetura que usamos nos dá flexibilidade pra implementar mecanismos mais avançados e complexos que nos ofereçam essas características, sem afetar em nada nossas regras de negócio, que estão muito bem isoladas.

## 2. Quais trade-offs pesaram na prática?
O principal trade-off foi testabilidade e isolamento versus simplicidade. Repositórios abstratos e Fake permitiram testar serviços sem banco, mas aumentaram a quantidade de classes e exigiram manter contratos e implementações coerentes. O mapeamento imperativo preservou o domínio sem herança do ORM, porém transferiu complexidade para adapters/orm.py: foi necessário manter conversores como GUID e PlacaType, e arquitetura.md registra 128 linhas dedicadas ao mapeamento e aos tradutores.

O atrito mais claro entre pureza do domínio e persistência apareceu em Pagamento. O @dataclass(frozen=True) impedia o SQLAlchemy de gravar seu estado interno; a primeira solução passou a reconhecer o prefixo _sa_, fazendo o domínio conhecer um detalhe do ORM. O ADR-0006 corrigiu isso ao definir a imutabilidade com base nos próprios campos do dataclass. A solução, porém, ainda usa lógica especial em __setattr__ e depende de Pagamento continuar sendo um dataclass.

Também aprendemos que Fake não substitui integração real. O Fake de pagamentos aceitava duplicatas que a chave primária do banco rejeitaria. A refatoração alinhou a regra de unicidade, embora o tipo e o momento da exceção ainda sejam diferentes entre Fake e SQLAlchemy. Em Reserva e Ticket, os testes unitários ajudaram a corrigir o contrato de list() e a alinhar horarioSaida com a possibilidade de NULL, mas o ADR-0007 deixa pendente validar essas mudanças com o SQLAlchemy real.

Os padrões GoF trouxeram benefícios localizados, mas aumentaram a indireção. Strategy separou políticas de desconto e tarifas; Factory Method centralizou a criação de veículos; State organizou os estados da vaga; e Facade reuniu os fluxos de reserva, entrada e saída, com 22 testes unitários. O Observer desacoplou o registro do pagamento de suas reações, mas tornou a ordem dos observadores relevante: se um deles falhar, os seguintes não são chamados e o chamador precisa tratar o rollback. Os padrões compensam quando há variação ou responsabilidades a coordenar, não apenas por acrescentarem abstrações.


---

## 3. Evidências Empíricas do Módulo `CalculadoraTarifa` e Trade-offs na Prática

A decisão de manter a Arquitetura Hexagonal é sustentada pelas evidências observadas durante a refatoração e evolução do serviço `CalculadoraTarifa`:

1. **Isolamento das regras de precificação (`service_layer/services.py`):**
   Quando refatoramos o cálculo de tarifas usando o padrão Strategy (commit 672cbf4), trocamos condicionais rígidas por estratégias independentes (TarifaCarro, TarifaMoto, TarifaSUV e TarifaCarroEletrico) com registro dinâmico (registrar_estrategia). Tudo isso ficou contido na camada de serviço. Para suportar novas categorias de veículos, não precisamos mexer em nenhuma rota HTTP nem no banco de dados, que prova na prática a separação entre a regra de negócio e a infraestrutura.
2. **Testes isolados e sem regressão (tests/unit/test_services.py):**
   Com as responsabilidades bem divididas, conseguimos rodar os testes antigos e validar o cadastro dinâmico de novas tarifas direto pelo pytest (pytest tests/unit/test_services.py), sem depender de banco de dados rodando.
3. **Mais classes e indireção no código:**
   O lado negativo dessa arquitetura junto do padrão Strategy foi o aumento na quantidade de classes e níveis de indireção, já que criamos a interface EstrategiaTarifa e suas respectivas implementações. Ainda assim, o custo valeu a pena pela segurança de conseguir adicionar novas regras na CalculadoraTarifa sem precisar alterar código que já estava testado e funcionando.

---

## 4. Evidências da Fase 2: Facilitadores vs. Obstáculos nas Refatorações e Padrões

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

## 5. Conclusão - manter, com aplicação seletiva

Nossa decisão é manter o monólito hexagonal, em vez de migrar para microsserviços. Para uma equipe de quatro pessoas, no prazo de um semestre e com o escopo atual, microsserviços acrescentariam infraestrutura e problemas de comunicação e consistência sem benefício demonstrado. A arquitetura atual já permitiu testar o domínio isoladamente e evoluir regras sem misturá-las à API ou ao ORM.

Manter não significa preservar toda abstração automaticamente. Continuaríamos com as fronteiras entre domínio, serviços e adaptadores, os contratos de repositório e os testes em diferentes níveis. Aplicaríamos padrões GoF quando houvesse necessidade concreta; para fluxos simples, preferiríamos a solução direta. Como próximos cuidados, priorizaríamos testes de integração com SQLAlchemy real para Reserva e Ticket, a uniformização dos erros entre Fake e banco e a validação dos requisitos ainda não demonstrados de segurança, disponibilidade e desempenho. A arquitetura se mostrou adequada para organizar e testar o projeto, mas precisa ser acompanhada da implementação e verificação explícitas dos requisitos operacionais.