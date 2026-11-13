# Caso de uso escolhido: Cadastrar cliente e veículo em arquivo único (monolítico):



**Cálculo por teste**:

Arquitetura Atual (tests/unit/test_model.py): 57 testes em 0.61s $\rightarrow$ ~10,7 ms por teste (execução pura na memória, sem I/O de disco ou HTTP).   Experimento Monolítico (experimentos/): 7 testes em 0.59s – 0.91s $\rightarrow$ ~84,3 ms a 130 ms por teste (cerca de 8x a 12x mais lento por caso de teste, pois exige instanciar o test_client() do Flask e criar tabelas SQLite no disco a cada execução).


**Foram realizados dois testes no experimentos**:

- Primeiro teste ou teste frio no experimento monolítico, utilizando o comando: 'python -m pytest experimentos/test_cadastrar_cliente_monolitico.py -v', obeteve o resultado '7 passed in 0.91s'. Nota: Na primeira execução a frio existe custo com criação de cache/arquivos temporários;

- No segundo teste no experimento monolítico, utilizando o comando:
'python -m pytest experimentos/ -v', obeteve o resultado '7 passed in 0.59s'.


# Experimento Opcional: Comparação Concreta de Arquitetura

Este documento apresenta o experimento empírico conduzido no diretório `experimentos/` para fundamentar a análise de trade-offs entre a **Arquitetura em Camadas (Clean Architecture / DDD Light)** adotada no projeto e uma abordagem alternativa baseada no modelo **Monolítico de Rota Única (Script Único / SQL Direto)**.

---

## 1. Estrutura do Experimento

* **Caso de Uso Avaliado:** Cadastro de Cliente com Veículo e Validação Sintática de Placa.
* **Arquivos Implementados:**
  * `experimentos/cadastrar_cliente_monolitico.py` (rota HTTP Flask, validação via regex e queries SQLite acopladas em um único script).
  * `experimentos/test_cadastrar_cliente_monolitico.py` (suíte de 7 testes utilizando `app.test_client()` e banco SQLite temporário por fixture).

---

## 2. Evidência de Execução dos Testes Experimentais

```text
PS F:\2026 2\projeto_de_software\trabalhoProjeto\Trabalho-de-Projeto-de-Software> python -m pytest experimentos/ -v
============================ test session starts =============================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
collected 7 items

experimentos/test_cadastrar_cliente_monolitico.py::test_deve_cadastrar_cliente_e_veiculo_com_sucesso PASSED [ 14%]
experimentos/test_cadastrar_cliente_monolitico.py::test_deve_rejeitar_placas_invalidas_via_http[] PASSED [ 28%]
experimentos/test_cadastrar_cliente_monolitico.py::test_deve_rejeitar_placas_invalidas_via_http[ABC] PASSED [ 42%]
experimentos/test_cadastrar_cliente_monolitico.py::test_deve_rejeitar_placas_invalidas_via_http[1234567] PASSED [ 57%]
experimentos/test_cadastrar_cliente_monolitico.py::test_deve_rejeitar_placas_invalidas_via_http[AB123CD] PASSED [ 71%]
experimentos/test_cadastrar_cliente_monolitico.py::test_deve_rejeitar_placas_invalidas_via_http[@@@-1234] PASSED [ 85%]
experimentos/test_cadastrar_cliente_monolitico.py::test_deve_barrar_cpf_ou_placa_duplicados_no_banco PASSED [100%]

============================= 7 passed in 0.59s ==============================


4. Conclusão Empírica

A comparação quantitativa entre os dois modelos comprovou na prática:

1. Custo Oculto de Testabilidade: Embora o script monolítico dispense arquivos intermediários inicialmente, o acoplamento entre regra de negócio, HTTP e banco de dados torna cada teste unitário de validação de 8 a 12 vezes mais lento[cite: 19]. Em uma suíte com 123 testes (como a do projeto oficial), esse padrão levaria mais de 10 a 15 segundos para rodar, contra 1.43s da arquitetura em camadas atual.

2. Rigidez para Evolução: No script alternativo, não existe Value Object Placa nem Factory Method para Veiculo — tudo trafega como strings e dicionários primitivos, impossibilitando o reúso seguro das regras fora da rota HTTP.   


Essas evidências empíricas fundamentam a decisão final registrada em docs/retrospectiva.md: manter a Arquitetura em Camadas com Domínio Isolado é a escolha técnica mais escalável e sustentável[cite: 19].


Nota: 

As ocorrências de 'cite: xx' são para a referência 'Aula 9 - Frameworks'.   