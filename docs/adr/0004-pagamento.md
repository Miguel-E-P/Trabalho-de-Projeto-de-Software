# ADR-0004: Imutabilidade de `Pagamento` com `__setattr__` customizado

- Status: Aceito(fase 1)

## Contexto
O domínio (`domain/model.py`) é Python puro e não importa o SQLAlchemy. `Pagamento` precisa ser imutável depois de criado: um pagamento registrado não pode ter valor, tipo ou data alterados. A primeira versão usava `@dataclass(frozen=True)`. Porém, ao mapear a classe com `map_imperatively`, o SQLAlchemy grava o atributo interno `_sa_instance_state` em cada instância. O `frozen=True` bloqueia qualquer atribuição, e o `FrozenInstanceError` impedia o ORM de funcionar (commit [hash]).

## Decisão
Removemos o `frozen=True` e implementamos `__setattr__` em `Pagamento` com três regras:
1. nomes que começam com `_sa_` (estado interno do SQLAlchemy) são aceitos;
2. atributos que ainda não existem em `__dict__` são aceitos, o que permite o `__init__` do dataclass;
3. reatribuir um atributo que já existe lança `FrozenInstanceError`.

```python
def __setattr__(self, name, value):
    if name.startswith("_sa_"):
        super().__setattr__(name, value)
        return
    if name not in self.__dict__:
        super().__setattr__(name, value)
    else:
        raise FrozenInstanceError("ERROR: Nao pode alterar pagamento")
```

## Alternativas consideradas
- **`@dataclass(frozen=True)`:** a versão original. Descartada porque bloqueia o `_sa_instance_state` e inviabiliza o mapeamento imperativo.

## Consequências
- **Positivas:** o domínio continua sem importar o SQLAlchemy (0 ocorrências no `grep`); a imutabilidade é verificada pelo teste [nome do teste]; os testes de integração do repositório deixaram de falhar.
- **Negativas:**
  - Código "mágico" e repetição: outra entidade imutável mapeada pelo ORM precisaria copiar essa lógica.
  - O domínio passa a conhecer o prefixo `_sa_`, um detalhe interno do SQLAlchemy que pode mudar. O `grep` por `sqlalchemy` não detecta esse acoplamento.
- **Em aberto:** extrair a lógica para uma classe base ou mixin se outras entidades precisarem; revisar o `expire_on_commit`.