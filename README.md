# Cara Core Informatica Tools

Manual tecnico e operacional das ferramentas de apoio ao ecossistema Cara Core Informatica.

## Objetivo

Este repositorio centraliza utilitarios para padronizacao de ambiente, validacao de qualidade tecnica e experimentacao controlada de tecnologias.

## Escopo funcional

1. Controle local de telemetria e privacidade no ambiente de desenvolvimento.
2. Operacao de endpoint local para modelos de linguagem com Ollama.
3. Validacao automatica de encoding em arquivos README.
4. Laboratorio de recursos modernos do Java para uso futuro em produtos.
5. Registro documental de governanca tecnica e conformidade do ecossistema.

## Estrutura do repositorio

```text
caracore-tools/
|-- .github/
|   `-- workflows/
|       `-- readme-encoding-check.yml
|-- docs/
|-- java/
|   |-- Main.java
|   `-- TesteJava21.java
|-- plano/
|-- python/
|   |-- block-telemetry-hosts.py
|   |-- unblock-telemetry-hosts.py
|   |-- plugar-olloma-local.py
|   `-- desplugar-olloma-local.py
`-- scripts/
    `-- check-readme-encoding.ps1
```

## Catalogo de ferramentas

| Diretorio | Ferramenta | Funcao operacional |
|---|---|---|
| python | block-telemetry-hosts.py | Adiciona regras no arquivo hosts para bloqueio de dominios de telemetria |
| python | unblock-telemetry-hosts.py | Remove regras de bloqueio adicionadas no hosts |
| python | plugar-olloma-local.py | Inicializa servidor local do Ollama |
| python | desplugar-olloma-local.py | Interrompe servidor local do Ollama |
| scripts | check-readme-encoding.ps1 | Detecta e corrige codificacao incorreta em README.md |
| java | Main.java | Exercicios de records e switch expressions |
| java | TesteJava21.java | Teste de virtual threads com alta concorrencia |

## Procedimentos operacionais

### 1) Bloqueio de telemetria

Ferramentas desta secao:

| Ferramenta | Arquivo | Responsabilidade |
|---|---|---|
| Aplicacao de bloqueios no hosts | [python/block-telemetry-hosts.py](python/block-telemetry-hosts.py) | Insere entradas de bloqueio de dominios de telemetria |
| Reversao de bloqueios no hosts | [python/unblock-telemetry-hosts.py](python/unblock-telemetry-hosts.py) | Remove entradas adicionadas para restaurar estado anterior |

Executar em terminal com privilegio administrativo.

```powershell
python python/block-telemetry-hosts.py
```

Modo de simulacao, sem alterar o hosts.

```powershell
python python/block-telemetry-hosts.py --dry-run
```

Remocao das regras aplicadas.

```powershell
python python/unblock-telemetry-hosts.py
```

Atualizacao de cache DNS apos mudancas.

```powershell
ipconfig /flushdns
```

### 2) Operacao de IA local com Ollama

Ferramentas desta secao:

| Ferramenta | Arquivo | Responsabilidade |
|---|---|---|
| Inicializacao do endpoint local | [python/plugar-olloma-local.py](python/plugar-olloma-local.py) | Inicia o servico Ollama para uso local |
| Encerramento do endpoint local | [python/desplugar-olloma-local.py](python/desplugar-olloma-local.py) | Interrompe o servico Ollama em execucao |

Inicializacao do endpoint local.

```powershell
python python/plugar-olloma-local.py
```

Parada do endpoint local.

```powershell
python python/desplugar-olloma-local.py
```

Endpoint esperado para integracao em IDEs: `http://localhost:11434/v1`.

### 3) Validacao de encoding de README

Ferramentas desta secao:

| Ferramenta | Arquivo | Responsabilidade |
|---|---|---|
| Verificador de codificacao de README | [scripts/check-readme-encoding.ps1](scripts/check-readme-encoding.ps1) | Detecta e opcionalmente corrige sinais de codificacao incorreta |
| Workflow de controle continuo | [.github/workflows/readme-encoding-check.yml](.github/workflows/readme-encoding-check.yml) | Executa validacao automatica em push e pull request |

Analise sem correcao.

```powershell
.\scripts\check-readme-encoding.ps1
```

Analise com correcao automatica.

```powershell
.\scripts\check-readme-encoding.ps1 -Fix
```

Analise apontando outra raiz de repositorios.

```powershell
.\scripts\check-readme-encoding.ps1 -RootPath "C:\projetos"
```

### 4) Laboratorio Java

Ferramentas desta secao:

| Ferramenta | Arquivo | Responsabilidade |
|---|---|---|
| Exemplo de records e switch expressions | [java/Main.java](java/Main.java) | Validar sintaxe e comportamento de recursos modernos da linguagem |
| Exemplo de virtual threads | [java/TesteJava21.java](java/TesteJava21.java) | Avaliar concorrencia baseada em virtual threads |

Compilacao e execucao dos exemplos.

```powershell
Set-Location java
javac Main.java
java Main
javac TesteJava21.java
java TesteJava21
```

## Documentacao de governanca

| Documento | Finalidade |
|---|---|
| [BLACKBOX_AMBIENTE_DESENVOLVIMENTO.md](docs/BLACKBOX_AMBIENTE_DESENVOLVIMENTO.md) | Diretrizes do ambiente local com foco em privacidade |
| [MAPEAMENTO_ECOSSISTEMA_PRODUCTOS.md](docs/MAPEAMENTO_ECOSSISTEMA_PRODUCTOS.md) | Mapa tecnico dos produtos e dependencias |
| [RELATORIO_SEGURANCA_ECOSSISTEMA.md](docs/RELATORIO_SEGURANCA_ECOSSISTEMA.md) | Consolidado de postura de seguranca do ecossistema |
| [AUDITORIA_LICENCAS_REPOSITORIOS_2026_03_14.md](docs/AUDITORIA_LICENCAS_REPOSITORIOS_2026_03_14.md) | Verificacao de conformidade de licenciamento |
| [AUDITORIA_SEGURANCA_LOJAS_RELEASES.md](docs/AUDITORIA_SEGURANCA_LOJAS_RELEASES.md) | Analise de seguranca para repositorios de releases |
| [GATE_PUBLICACAO_ANTIABUTRE_ECOSSISTEMA.md](docs/GATE_PUBLICACAO_ANTIABUTRE_ECOSSISTEMA.md) | Criterios obrigatorios antes de publicacao |

## Pre-requisitos

| Dependencia | Versao recomendada |
|---|---|
| Python | 3.8 ou superior |
| Java | 21 ou superior |
| PowerShell | 5.1 ou superior |
| Ollama | Instalacao local valida para operacao offline |
| Permissao administrativa | Necessaria para alteracao do arquivo hosts |

## Politica editorial deste manual

Este README deve permanecer em padrao institucional, com linguagem tecnica e foco operacional.
Nao utilizar emojis, icones visuais infantis ou elementos de destaque informais.
