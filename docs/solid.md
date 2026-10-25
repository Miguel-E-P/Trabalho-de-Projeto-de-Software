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
