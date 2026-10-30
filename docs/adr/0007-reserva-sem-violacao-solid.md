# ADR-0007: Aplicar SOLID ao agregado Reserva (`Reserva` e `Ticket`)

- Status: Aceito (29/10/2026)
- Substitui: [ADR-0003](0003-reserva.md)

## Contexto
O ADR-0003 definiu as fronteiras do agregado: `Ticket` controla o próprio ciclo de vida (`horarioSaida` e `pago`), `Reserva` é um Value Object imutável (`@dataclass(frozen=True)`) e os repositórios isolam o domínio do banco. Essas decisões continuam válidas. A revisão SOLID encontrou três problemas que o ADR-0003 não tratou:
1. **SRP:** `Ticket` e `Reserva` tinham cada um sua cópia das mesmas regras: "id não pode ser negativo" e "uma data não pode ser anterior a uma referência". Mudar uma regra exigia lembrar de editar as duas entidades.
2. **ISP/DIP/LSP:** `list()` existia apenas em `SqlAlchemyReservaRepository`, `SqlAlchemyTicketRepository` e nos Fakes, e não em `AbstractReservaRepository` nem em `AbstractTicketRepository`. Quem dependia da abstração não podia listar sem passar a depender de uma implementação concreta, e uma nova implementação do repositório podia omitir `list()` sem que nada acusasse.
3. **Mapeamento inconsistente:** o domínio aceita `Ticket` sem saída (`horarioSaida: datetime | None`, o veículo ainda está no estacionamento), mas a coluna `tickets.horarioSaida` estava como `nullable=False`. Persistir um ticket recém-aberto violaria a restrição do banco, e os testes com Fake não detectavam isso.

## Decisão
1. **Validações compartilhadas em funções únicas (`domain/model.py`).** Extraímos `_validar_id_nao_negativo` e `_validar_nao_anterior`, e `Ticket` e `Reserva` passam a delegar a elas no `__post_init__` (e em `Ticket.updateSaida`). As mensagens de erro e as exceções (`ValueError`, `DataInvalida`) não mudam.

```python
def _validar_id_nao_negativo(valor: int) -> None:
    if valor < 0:
        raise ValueError("Valor não pode ser negativo.")

def _validar_nao_anterior(data: datetime, referencia: datetime, mensagem: str) -> None:
    if data < referencia:
        raise DataInvalida(mensagem)
```

2. **`list()` passa a fazer parte do contrato abstrato (`adapters/repository.py`).** Ele vira `@abc.abstractmethod` em `AbstractReservaRepository` e em `AbstractTicketRepository`. As implementações Sql e Fake já o tinham e não precisaram mudar.
3. **`horarioSaida` aceita `NULL` (`adapters/orm.py`).** A coluna passa a `nullable=True`, alinhada ao tipo `datetime | None` do domínio.

Não alteramos nomes de campos, assinaturas públicas (`idTicket`, `updateSaida`, `hoje`, `placa_veiculo_reserva`) nem a imutabilidade de `Reserva`, para não quebrar `services.py` nem `test_services.py`.

## Alternativas consideradas
- **Manter a validação duplicada em cada entidade (ADR-0003):** descartada porque a mesma regra ficava em dois lugares e podia divergir.
- **Classe base ou mixin de validação, ou uma lista de regras extensível (OCP):** descartada porque são só duas regras e uma abstração maior seria excesso de engenharia. Se surgirem novas regras de data, a decisão pode ser revista.
- **Manter `list()` só nas implementações concretas (estado anterior):** descartada porque deixa o contrato incompleto e permite implementações que o violam.
- **Interface de leitura separada (por exemplo, `AbstractReservaReader`):** descartada porque só existem dois métodos de leitura (`get` e `list`), e separar isso criaria mais tipos do que benefício.

## Consequências
- **Positivas:**
  - cada regra de id e de data tem um único lugar para mudar;
  - o comportamento observável das entidades não muda;
  - quem depende de `AbstractReservaRepository` ou `AbstractTicketRepository` pode listar sem conhecer a implementação;
  - uma subclasse sem `list()` não pode mais ser instanciada;
  - um `Ticket` sem saída passa a ser consistente entre domínio e esquema;
  - a suíte unitária (`test_model.py` e `test_repository.py`) passa com 53 testes: os novos cobrem as bordas das regras compartilhadas, `list()` nos Fakes e o contrato abstrato (checado por `__abstractmethods__`, sem depender do `pytest` em `test_repository.py`).
- **Negativas:**
  - qualquer outra subclasse dos repositórios abstratos sem `list()` passa a falhar ao ser instanciada (nenhuma existe hoje no código);
  - `Ticket` e `Reserva` passam a depender das mesmas funções, então alterar uma regra afeta as duas entidades;
  - as funções são privadas ao módulo `model.py`, e a mensagem de data é passada como texto por quem chama;
  - a proteção de datas, que o ADR-0003 descrevia como centralizada no `Ticket`, agora fica em funções compartilhadas (o `Ticket` continua dono do ciclo de vida);
  - `create_all` não altera tabelas já existentes, então um banco criado com `horarioSaida NOT NULL` precisa ser recriado ou migrado.
- **Em aberto:**
  - os testes passaram com repositórios Fake e uma sessão simulada, e o SQLAlchemy não foi executado, então a mudança no `orm.py` não foi validada contra um banco real. Falta um teste de integração que salve e recupere um `Ticket` com `horarioSaida=None`;
  - o ADR-0006 registra que `@dataclass(frozen=True)` bloqueia o `_sa_instance_state` e inviabiliza o `map_imperatively`, e `Reserva` usa `frozen=True` e é mapeada. É preciso confirmar com um teste de integração que ela persiste, e, se não persistir, rever a imutabilidade de `Reserva` (ADR-0003) com a mesma abordagem do `Pagamento`;
  - os testes importam o `model` por duas raízes (`src.estacionamento...` e `estacionamento...`), que geram classes de exceção distintas. Convém padronizar para uma só.
