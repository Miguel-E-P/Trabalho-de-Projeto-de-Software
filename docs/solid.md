# Registros de Refatoração SOLID - Checkpoint 2

## Integrante: Kennedy Soares
**Módulo / Agregado:** Agregado Cliente (`Cliente`, `Veiculo`, `Placa`)

---

### 1. Princípios Violados e Trecho de Código ("Antes")
* **Princípios Violados:** 
  - **SRP** — *Single Responsibility Principle* (Princípio da Responsabilidade Única)
  - **OCP** — *Open-Closed Principle* (Princípio do Aberto/Fechado)
* **Hash do Commit "Antes":** `1564c18` em 29-09-26 *(Commit anterior a 06/10)*
* **Trecho do Código "Antes" (`src/estacionamento/domain/model.py`):**

```python
# Trecho do commit 1564c18 onde Placa agia apenas como contêiner de dados
@dataclass(frozen=True)
class Placa:
    numero: str
```

### 2. Problema Concreto
2.1 Violação do SRP: O Value Object Placa era um mero contêiner anêmico sem garantir suas próprias invariantes de formato (caracteres nulos, tamanho incorreto ou padrões fora do padrão nacional/Mercosul). Isso forçava a camada de aplicação (services.py) a efetuar validações imperativas externas, espalhando responsabilidades de validação.

2.2 Violação do OCP: Se o sistema precisasse passar a aceitar um novo formato de placa (ex.: padrão antigo ABC-1234 vs. padrão Mercosul ABC1D23), seria necessário modificar e adicionar estruturas condicionais (if/elif) nos chamadores e rotas, alterando código testado e correndo o risco de gerar regressões.

### 3. Refatoração e Código ("Depois")

Hash do Commit "Depois": 841bc73

Trecho do Código Refatorado (src/estacionamento/domain/model.py):

import re
from dataclasses import dataclass

@dataclass(frozen=True)
class Placa:
    numero: str

    def __post_init__(self):
        # Validação centralizada garantindo invariante e encapsulamento (SRP)
        if not self.numero or not self._validar_formato(self.numero):
            raise ValueError(f"Placa inválida: '{self.numero}' não atende ao formato esperado.")

    @staticmethod
    def _validar_formato(placa_str: str) -> bool:
        # Padrão flexível via Regex que estende o suporte ao formato antigo e Mercosul (OCP)
        padrao = r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$'
        return bool(re.match(padrao, placa_str.upper().replace("-", "")))

### 4. Garantia por Testes Automatizados

A suíte completa de testes unitários, de repositório e E2E da API REST foi executada com sucesso após a refatoração.

- Comando Executado: python -m pytest -o pythonpath=src

- Resultado: 48 passed in 1.43s (100% dos testes aprovados, garantindo retrocompatibilidade das rotas existentes e barrando a criação de placas sintaticamente inválidas).

### 5. Análise do Custo da Refatoração(Trade-offs)Custo:

 Inclusão da execução de expressões regulares no método __post_init__ do Value Object.   
 
 Por que compensa:
 
 Coesão (SRP): Torna impossível existir um objeto Placa em estado sintaticamente inválido na memória da aplicação.

 Extensibilidade (OCP): Permite aceitar novos formatos de placa (Mercosul e Tradicional) de forma transparente sem que nenhuma linha de código da camada de serviço ou da entidade Cliente precise ser editada ou retestada.

## Integrante: Pedro Quintaes
**Módulo / Agregado:** Agregado Pagamento (`Pagamento`)

---

### 1. Princípios Violados e Trecho de Código ("Antes")
* **Princípios Violados:**
  - **DIP** — *Dependency Inversion Principle* (Princípio da Inversão de Dependência)
* **Hash do Commit "Antes":** aa55b3ca5cb4bc0ca8aa6da7e53098cda9cd75e5

* **Trecho do Código "Antes" (`src/estacionamento/domain/model.py`):**

```python
# Trecho do commit aa55b3ca5cb4bc0ca8aa6da7e53098cda9cd75e5 onde Pagamento conhecia o prefixo `_sa_` do SQLAlchemy
@dataclass
class Pagamento:
    id_ticket: int
    valor: float
    tipo_pagamento: TipoPagamento
    data_hora_pagamento: datetime

    def __post_init__(self):
        if self.valor < 0.0:
            raise ValueError("ERROR: Valor do pagamento NAO pode ser negativo")

    def __setattr__(self, name, value):
        if name.startswith("_sa_"):
            super().__setattr__(name, value)
            return
        if name not in self.__dict__:
            super().__setattr__(name, value)
        else:
            raise FrozenInstanceError("ERROR: Nao pode alterar pagamento")
```

### 2. Problema Concreto
2.1 Violação do DIP: `Pagamento`, uma entidade de domínio (módulo de alto nível), dependia de um detalhe de baixo nível: o prefixo `_sa_`, usado internamente pelo SQLAlchemy. A exceção `name.startswith("_sa_")` em `__setattr__` fazia o domínio conhecer o funcionamento interno do ORM, mesmo sem importá-lo, o que contraria a independência do domínio. Se o SQLAlchemy mudasse esse detalhe, seria necessário alterar uma entidade de domínio.

### 3. Refatoração e Código ("Depois")

Hash do Commit "Depois": 35bf78340a62e12fdeea281c816562c2b39627d3

Trecho do Código Refatorado (`src/estacionamento/domain/model.py`):

```python
@dataclass
class Pagamento:
    id_ticket: int
    valor: float
    tipo_pagamento: TipoPagamento
    data_hora_pagamento: datetime

    def __post_init__(self):
        if self.valor < 0.0:
            raise ValueError("ERROR: Valor do pagamento NAO pode ser negativo")

    def __setattr__(self, name, value):
        # Regra definida só pelos campos da própria entidade, sem conhecer o ORM (DIP)
        if name in self.__dataclass_fields__ and name in self.__dict__:
            raise FrozenInstanceError("ERROR: Nao pode alterar pagamento")
        super().__setattr__(name, value)
```

### 4. Garantia por Testes Automatizados

A suíte completa de testes unitários, de repositório e E2E da API REST foi executada após a refatoração. Nenhum erro foi detectado.

### 5. Análise do Custo da Refatoração (Trade-offs)

**Custo:** A imutabilidade passa a valer apenas para os campos declarados do dataclass (atributos que não são campos podem ser reatribuídos), e a regra depende de `__dataclass_fields__`, o que exige que `Pagamento` continue sendo um `@dataclass`.

**Por que compensa:**

- **Desacoplamento (DIP):** o domínio deixa de conhecer o prefixo `_sa_` e qualquer outro detalhe do SQLAlchemy; a regra de imutabilidade depende só dos campos da própria entidade, e a dependência passa a apontar apenas do ORM para o domínio.

- **Retrocompatibilidade:** o comportamento dos campos não muda (a primeira atribuição funciona e a reatribuição lança `FrozenInstanceError`).

# Integrante: Miguel Enne

Módulo / Agregado: Agregado Reserva (Reserva, Ticket, AbstractReservaRepository, AbstractTicketRepository e a tabela tickets no ORM)

Hash do Commit: 

### 1. Princípios Violados e Trecho de Código ("Antes")
Princípios Violados:
Princípio da Responsabilidade Única, Princípio da Inversão de Dependência e o Princípio da Substituição de Liskov no contrato dos repositórios

Trecho do Código antes das mudanças:

[cada entidade carrega a sua própria cópia das regras]
src/estacionamento/domain/model.py 

python
@dataclass
class Ticket:
    ...
    def __post_init__(self):
        if self.idTicket < 0:
            raise ValueError("Valor não pode ser negativo.")

    def updateSaida(self, horarioSaida: datetime) -> None:
        if horarioSaida < self.horarioEntrada:
            raise DataInvalida("Essa data está indisponível para a saída.")
        self.horarioSaida = horarioSaida

@dataclass(frozen=True)
class Reserva:
    ...
    def __post_init__(self):
        if self.id_reserva < 0:
            raise ValueError("Valor não pode ser negativo.")

        if self.data_reserva < self.hoje:
            raise DataInvalida("Essa data está indisponível para reserva.")

[o contrato abstrato só declara add e get, mas as implementações concretas têm list]
src/estacionamento/adapters/repository.py 

python
class AbstractReservaRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, reserva: model.Reserva) -> None: ...
    @abc.abstractmethod
    def get(self, id_reserva: int) -> Optional[model.Reserva]: ...

class SqlAlchemyReservaRepository(AbstractReservaRepository):
    ...
    def list(self):          # fora do contrato
        return self.session.query(model.Reserva).all()

src/estacionamento/adapters/orm.py:

python
Column("horarioSaida", DateTime, nullable=False),

### 2. Problema Concreto

2.1 Violação do SRP: Ticket e Reserva repetiam as mesmas regras dentro de si: "o id não pode ser negativo" (com a mesma mensagem) e "uma data não pode ser anterior a uma referência" (Ticket.updateSaida e Reserva). Cada regra tinha duas casas, então alterar uma delas (mensagem, tipo de exceção, etc) exigia editar as duas entidades e lembrar de manter as duas iguais.

2.2 Violação do DIP (e do contrato do LSP): AbstractReservaRepository e AbstractTicketRepository não declaravam list, embora as quatro implementações concretas (Sql e Fake, de cada um) a tivessem. Quem recebe a abstração não pode listar; para usar list teria de depender de SqlAlchemyReservaRepository ou do Fake, e a troca de uma implementação por outra deixava de ser segura.

2.3 Inconsistência de persistência (correção de bug, não é violação de princípio): o domínio aceita Ticket sem saída (horarioSaida=None, veículo ainda estacionado), mas a coluna horarioSaida era NOT NULL. Salvar um ticket de entrada falharia no banco real. Foi corrigido aqui por estar no mesmo agregado.

### 3. Refatoração e Código 

src/estacionamento/domain/model.py — cada regra tem uma única casa e as entidades só delegam:

python
def _validar_id_nao_negativo(valor: int) -> None:
    if valor < 0:
        raise ValueError("Valor não pode ser negativo.")


def _validar_nao_anterior(data: datetime, referencia: datetime, mensagem: str) -> None:
    if data < referencia:
        raise DataInvalida(mensagem)


@dataclass
class Ticket:
    ...
    def __post_init__(self):
        _validar_id_nao_negativo(self.idTicket)

    def updateSaida(self, horarioSaida: datetime) -> None:
        _validar_nao_anterior(
            horarioSaida, self.horarioEntrada, "Essa data está indisponível para a saída."
        )
        self.horarioSaida = horarioSaida


@dataclass(frozen=True)
class Reserva:
    ...
    def __post_init__(self):
        _validar_id_nao_negativo(self.id_reserva)
        _validar_nao_anterior(
            self.data_reserva, self.hoje, "Essa data está indisponível para reserva."
        )

src/estacionamento/adapters/repository.py — list passa a fazer parte do contrato (o mesmo vale para AbstractTicketRepository):

python
class AbstractReservaRepository(abc.ABC):
    ...
    @abc.abstractmethod
    def list(self) -> "list[model.Reserva]":
        "retorna todas as reservas do repositório"
        raise NotImplementedError

src/estacionamento/adapters/orm.py:

python
[ O domínio aceita Ticket sem saída (veículo ainda estacionado): a coluna precisa aceitar NULL.]
Column("horarioSaida", DateTime, nullable=True),

### 4. Garantia por Testes Automatizados
Comando Executado: python -m pytest -o pythonpath=src tests/unit/test_model.py tests/unit/test_repository.py
Resultado: 33 passed antes da refatoração; 44 passed depois (11 testes novos).
O que os testes novos garantem: 2 deles (test_list_faz_parte_do_contrato_abstrato_de_reserva e ..._de_ticket) falham contra o repository.py anterior e passam agora. Os outros 9 são testes de caracterização das bordas (id zero, saída igual à entrada, saída inválida que não altera o horário anterior, reserva para o próprio dia, list nos Fakes, cópia da lista devolvida, implementações concretas honrando o contrato). Eles passam antes e depois, e provam que extrair as regras não mudou o comportamento.
Limites desta verificação: a execução foi feita sem o SQLAlchemy instalado, com um stub mínimo de sqlalchemy.orm.Session só para importar o repository.py. Os testes de integração, os E2E e test_services.py não foram executados, e a mudança no orm.py foi verificada apenas por compilação do arquivo. [pendente: rodar python -m pytest -o pythonpath=src completo e colar aqui o resultado]

### 5. Análise do Custo da Refatoração(Trade-offs)Custo:

Duas funções privadas a mais em model.py (uma indireção a mais para ler uma validação) e uma quebra de compatibilidade: qualquer subclasse de AbstractReservaRepository ou AbstractTicketRepository que não implemente list deixa de poder ser instanciada.

Coesão (SRP): cada regra de validação do agregado tem um único lugar para mudar, e Ticket e Reserva não podem divergir sem querer.

Substituibilidade (DIP/LSP): código escrito contra a abstração pode listar, e Sql e Fake passam a ser trocáveis por contrato, o que sustenta a testabilidade com FakeRepository descrita em arquitetura.md.

## Integrante: Gustavo Teixeira
**Módulo/Agregado:** Agregado Estacionamento

### 1. Princípios Violados
**Princípio**: OCP — Open/Closed Principle (Princípio Aberto/Fechado)

```python
class TipoVaga(Enum):
    CARRO = "carro"
    MOTO = "moto"
    CARRO_ELETRICO = "carro elétrico"

```

```python
@dataclass
class Vaga:
    id_vaga: int
    tipo: TipoVaga
    status: StatusVaga = StatusVaga.LIVRE

    def ocupar(self) -> None:
        if self.status != StatusVaga.LIVRE:
            raise VagaIndisponivel(f"Vaga {self.id_vaga} indisponível.")

        self.status = StatusVaga.OCUPADA
```

```python
@dataclass
class Estacionamento:
    id_estacionamento: int
    vagas: list[Vaga]

    def buscar_vaga(self, id_vaga: int) -> Vaga:
        for vaga in self.vagas:
            if vaga.id_vaga == id_vaga:
                return vaga

        raise VagaNaoEncontrada(f"Vaga {id_vaga} não encontrada.")

    def ocupar_vaga(self, id_vaga: int) -> None:
        vaga = self.buscar_vaga(id_vaga)
        vaga.ocupar()
```

(faa6fd6) **feat: Trabalhando nas classes de domínio Vaga e Estacionamento**
(1537c2f) **feat: Implementando mecanismos de ocupar Vaga em Estacionamento**
(2f8bc1e) **refact: Explicitando exceções de domínio (VagaIndisponivel e VagaNaoEncontrada)**

### 2. Problema Concreto
Hoje, a regra de negócio definida para a ocupação de vagas é bem simples: uma vaga só pode ser ocupada se estiver livre. Isso acontece porque não adicionamos restrições de acordo com o tipo de vaga. Uma modificação plausível no escopo do nosso projeto é que o cliente precise de algum tipo de autorização pra ocupar a vaga. 

Por exemplo, vamos supor que carros a combustível não possam ocupar vagas para carro elétrico. Teríamos que adicionar uma condicional ao método responsável pela ocupação. A princípio, parece uma alteração inocente, mas surge uma nova regra: carros não podem ocupar vagas de moto. E se passassemos a tratar políticas de inclusão, agora teríamos um novo tipo de vaga, reservadas pra gestantes, idosos, etc...

```python
@dataclass
class Vaga:
    id_vaga: int
    tipo: TipoVaga
    status: StatusVaga = StatusVaga.LIVRE

    def ocupar(self, veiculo) -> None:
        if self.status != StatusVaga.LIVRE:
            raise VagaIndisponivel(
                f"Vaga {self.id_vaga} indisponível."
            )

        if self.tipo == TipoVaga.CARRO_ELETRICO:
            if veiculo.tipo != "carro elétrico":
                raise VagaIndisponivel(
                    "Esta vaga é exclusiva para carros elétricos."
                )

        if self.tipo == TipoVaga.MOTO:
            if veiculo.tipo != "moto":
                raise VagaIndisponivel(
                    "Esta vaga é exclusiva para motos."
                )

        # ...
```

Nesse cenário, o método nosso método poderia crescer descontroladamente, mais e mais condicionais aninhadas ou duplicadas, um bad smell fortíssimo.

### 3. Refatoração do Código
Pra resolver o problema do OCP, isto é, a necessidade de alterar o método sempre que uma regra de negócio for introduzida, pensei em implementar um padrão de projeto que vimos com o professor Paulo no início do período: o Strategy Pattern.

A ideia foi retirar as regras específicas de autorização de dentro da classe Vaga e encapsulá-las em estratégias independentes, que chamei de políticas:

```python
class PoliticaOcupacao(ABC):
    @abstractmethod
    def validar(self, vaga, veiculo) -> bool:
        pass

class PoliticaCarroEletrico(PoliticaOcupacao):
    def validar(self, vaga, veiculo) -> bool:
        return veiculo.tipo == "carro elétrico"


class PoliticaVagaMoto(PoliticaOcupacao):
    def validar(self, vaga, veiculo) -> bool:
        return veiculo.tipo == "moto"
```

E passar essas políticas, junto com o veículo, na chamada dos métodos de ocupação:

```python
# Em Vaga
def ocupar(self, veiculo: Veiculo=None, politica: PoliticaOcupacao=None) -> None:
    if self.status != StatusVaga.LIVRE:
        raise VagaIndisponivel(f"Vaga {self.id_vaga} indisponível.")

    if veiculo and not politica.validar(self, veiculo):
        raise VagaIndisponivel(f"Veículo não autorizado para a vaga {self.id_vaga}.")

    self.status = StatusVaga.OCUPADA

# Em Estacionamento
def ocupar_vaga(self, id_vaga: int, veiculo: Veiculo=None, politica: PoliticaOcupacao=None) -> None:
    vaga = self.buscar_vaga(id_vaga)
    vaga.ocupar(veiculo, politica)
```

(b1d317b) **refact: Alterações SOLID em Estacionamento**
(ac1a7b1) **refact: Simplificando política de carros elétricos**

### 4. Garantia por Testes Automatizados
Para garantir que o comportamento anterior foi preservado, precisei levar em consideração um fator importante. Como agora `Vaga.ocupar` e `Estacionamento.ocupar_vaga` conhecem veiculo e política, as chamadas a esses métodos quebraria, caso não permitíssimos que `veiculo` e `politica` fossem opcionais.

Isso foi resolvido atribuindo o valor `None` como padrão para ambos os parâmetros. Feito isso, todos os testes da aplicação, inclusive dos demais agregados, continuam passando.  

### 5. Análise do Custo da Refatoração
Implementando o Strategy Pattern, os custos de refatoração ficam consideravelmente baixos. As responsabilidades estão bem mais divididas e adicionar uma nova política de ocupação de vaga é simples, não afeta o restante do código.

É evidente que, como a implementação de qualquer outro padrão de projeto, a solução cria uma complexidade a mais na base de código. Mas outras alternativas mais simples, como criar uma classe responsável por concentrar as regras de ocupação, apenas mascara o problema, porque ela próprio passaria a violar o OCP.