# ADR-0006: Remover o conhecimento do ORM de `Pagamento.__setattr__`

- Status: Aceito(27/10/2026)
- Substitui: [ADR-0004](0004-pagamento.md)

## Contexto
O domínio (`domain/model.py`) é Python puro e independente do ORM (ADR-0001). `Pagamento` precisa ser imutável depois de criado, e o `@dataclass(frozen=True)` não funciona com `map_imperatively`, porque o SQLAlchemy grava `_sa_instance_state` em cada instância. O ADR-0004 resolveu isso com um `__setattr__` customizado que aceitava nomes começando com `_sa_`. Com isso, um detalhe interno do SQLAlchemy passou a fazer parte do domínio: um módulo de alto nível dependia de um detalhe de baixo nível, violando o DIP e o ADR-0001.

## Decisão
Removemos a verificação de `_sa_` e passamos a definir a regra pelos próprios campos do dataclass, com três regras:
1. campos do dataclass que ainda não existem em `__dict__` são aceitos, o que permite o `__init__` do dataclass;
2. reatribuir um campo do dataclass que já existe lança `FrozenInstanceError`;
3. nomes que não são campos, inclusive os internos do SQLAlchemy, são aceitos sem que o domínio precise conhecê-los.

```python
def __setattr__(self, name, value):
    if name in self.__dataclass_fields__ and name in self.__dict__:
        raise FrozenInstanceError("ERROR: Nao pode alterar pagamento")
    super().__setattr__(name, value)
```

## Alternativas consideradas
- **Manter a exceção `_sa_` (ADR-0004):** descartada porque acopla o domínio a um detalhe interno do SQLAlchemy, o que viola o DIP.
- **`@dataclass(frozen=True)`:** descartada porque bloqueia o `_sa_instance_state` e inviabiliza o mapeamento imperativo.

## Consequências
- **Positivas:** o domínio deixa de conhecer o prefixo `_sa_` e qualquer outro detalhe do SQLAlchemy; a regra de imutabilidade depende só dos campos da própria entidade; o comportamento dos campos não muda (a primeira atribuição funciona e a reatribuição lança `FrozenInstanceError`).
- **Negativas:**
  - Atributos que não são campos do dataclass passam a poder ser reatribuídos.
  - A regra usa `__dataclass_fields__`, então `Pagamento` precisa continuar sendo um `@dataclass`.
  - Código "mágico" e repetição: outra entidade imutável precisaria copiar essa lógica.
- **Em aberto:** extrair a lógica para uma classe base ou mixin se outras entidades precisarem.