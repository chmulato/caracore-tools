# Cara Core Informatica Tools

Manual tecnico e operacional das ferramentas de apoio ao ecossistema Cara Core Informatica.

## Objetivo

Este repositorio centraliza o portal estatico (`docs/`), a Sala de Operacoes, scripts de governanca/delivery e a pasta `sources/` como matriz editorial.

## Escopo funcional

1. Validacao automatica de encoding em README (CI e script local).
2. Registro documental de governanca tecnica e conformidade do ecossistema.
3. Publicacao canonica da Sala de Operacoes em `docs/sala/`, consumida pelo dominio `tools.caracore.com.br`.

## Estrutura do repositorio

```text
caracore-tools/
|-- .github/
|   `-- workflows/
|       `-- readme-encoding-check.yml
|-- docs/
|-- sources/
`-- scripts/
    |-- check_docs_html_only.py
    |-- check_readme_encoding.py
    |-- ecosystem_delivery.py
    |-- ecosystem_governance.py
    |-- ecosystem_branch_governance.py
    |-- subdomain_smoke_check.py
    `-- sync_delivery_site_to_releases_docs.py
```

## Catalogo de ferramentas

| Diretorio | Ferramenta | Funcao operacional |
|---|---|---|
| scripts | check_readme_encoding.py | Detecta marcas de mojibake em README (multi-repo ou `--root .` no CI) |
| scripts | check_docs_html_only.py | Audita `docs/` contra a politica HTML-only |
| scripts | ecosystem_delivery.py | Lista, valida e executa deliveries (`ecosystem-delivery-map.json`) |
| scripts | ecosystem_governance.py | Painel, roadmap, gate; relatorios Markdown em `reports/governance/` (gitignored, fora do site publico) |
| scripts | ecosystem_branch_governance.py | Estado e alinhamento de branches por app |
| scripts | subdomain_smoke_check.py | Verificacoes HTTP em subdominios publicos |
| scripts | sync_delivery_site_to_releases_docs.py | Copia `delivery/<app>` para `*-releases/docs` com git |
| scripts | run_delivery_ink.py | Wrapper: sync Ink matriz -> caracore-ink-releases |
| docs/sala | Sala de Operacoes | Hub canonico de documentacao operacional, campanhas e registos da sala |
| sources/sala | Matriz editorial | Textos e registos operacionais que alimentam a revisao antes de publicar em `docs/` |

## Procedimentos operacionais

### 1) Validacao de encoding de README

Ferramentas desta secao:

| Ferramenta | Arquivo | Responsabilidade |
|---|---|---|
| Verificador de codificacao de README | [scripts/check_readme_encoding.py](scripts/check_readme_encoding.py) | Detecta e opcionalmente corrige sinais de codificacao incorreta |
| Workflow de controle continuo | [.github/workflows/readme-encoding-check.yml](.github/workflows/readme-encoding-check.yml) | Executa validacao automatica em push e pull request |

Analise sem correcao (README na raiz do repo ou em `caracore-*` sob `--root`).

```bash
python scripts/check_readme_encoding.py --root .
```

Analise com correcao automatica.

```bash
python scripts/check_readme_encoding.py --root . --fix
```

Analise apontando outra raiz de repositorios (ex.: varios `caracore-*` lado a lado).

```bash
python scripts/check_readme_encoding.py --root "D:/dev"
```

### 2) Orquestracao de delivery do ecossistema

Ferramentas desta secao:

| Ferramenta | Arquivo | Responsabilidade |
|---|---|---|
| Orquestrador de delivery | [scripts/ecosystem_delivery.py](scripts/ecosystem_delivery.py) | Lista, valida e executa comandos de delivery cadastrados por aplicacao |
| Mapa central de comandos | [scripts/ecosystem-delivery-map.json](scripts/ecosystem-delivery-map.json) | Define calendario, status, repositorio e comando de cada aplicacao |

Listar o calendario e o status operacional dos comandos.

```bash
python scripts/ecosystem_delivery.py list
```

Validar caminhos locais, comandos e tokens necessarios antes da execucao.

```bash
python scripts/ecosystem_delivery.py validate
```

Executar um delivery especifico em modo simulacao.

```bash
python scripts/ecosystem_delivery.py run --app pdv --dry-run
```

Aplicacoes com wrapper automatico no orquestrador:

```text
pdv, oidc, seed, area51, ete, circuito, hub, ink-v2, ru, cso
```

Exemplos para as apps que antes eram manuais.

```bash
python scripts/ecosystem_delivery.py run --app ete --dry-run
python scripts/ecosystem_delivery.py run --app circuito --dry-run
python scripts/ecosystem_delivery.py run --app hub --dry-run
python scripts/ecosystem_delivery.py run --app ink-v2 --dry-run
python scripts/ecosystem_delivery.py run --app ru --dry-run
python scripts/ecosystem_delivery.py run --app cso --dry-run
```

Executar um delivery especifico com argumentos extra (exemplo com tag no OIDC).

```bash
python scripts/ecosystem_delivery.py run --app oidc -- --tag v1.0.0
```

Regra operacional do Ink Agenda:

- A sincronizacao feita por `run_delivery_ink.py` / `sync_delivery_site_to_releases_docs.py` atualiza apenas o conteudo institucional da loja `caracore-ink-releases` a partir da matriz.
- Os artefatos RC1 de `Windows (.zip)`, `macOS (.dmg)` e `Linux (.deb)` sao publicados pelo repositorio `caracore-ink`, usando scripts e workflows dedicados por plataforma.
- A branch oficial do repositorio `caracore-ink-releases` e `master`.

Regra operacional do PDV:

- Publicar EXE e checksums exclusivamente em `https://github.com/chmulato/caracore-pdv-releases`.
- Nao publicar EXE do PDV na matriz `caracore-site`.

Regra geral do ecossistema:

- Cada app com artefato de release deve usar sua loja dedicada `*-releases`.
- O site matriz deve conter apenas conteudo institucional, documentacao e links para as lojas.

### 3) Governanca de releases, roadmap e lojas

Ferramentas desta secao:

| Ferramenta | Arquivo | Responsabilidade |
|---|---|---|
| Dashboard e gate de governanca | [scripts/ecosystem_governance.py](scripts/ecosystem_governance.py) | Exibe saude do ecossistema, janela de roadmap, decisao Go/No-Go e gera Markdown local de evidencia |
| Catalogo oficial de apps | [scripts/ecosystem-governance-catalog.json](scripts/ecosystem-governance-catalog.json) | Define caminhos fonte/release/matriz e status de roadmap por app |
| Manual operacional de governanca | [docs/sistema_governanca_ecossistema.html](docs/sistema_governanca_ecossistema.html) | Politica de execucao e evidencias obrigatorias |

Dashboard de governanca do ecossistema.

```bash
python scripts/ecosystem_governance.py dashboard
```

Janela de marcos do roadmap.

```bash
python scripts/ecosystem_governance.py roadmap --window-days 180
```

Gate por aplicacao com bloqueio estrito.

```bash
python scripts/ecosystem_governance.py gate --app pdv --strict
```

Geracao de evidencia formal do gate.

```bash
python scripts/ecosystem_governance.py report --app pdv
```

### 4) Governanca de branches por aplicacao

Ferramentas desta secao:

| Ferramenta | Arquivo | Responsabilidade |
|---|---|---|
| Auditoria e alinhamento de branches | [scripts/ecosystem_branch_governance.py](scripts/ecosystem_branch_governance.py) | Verifica branch atual vs branch alvo e executa alinhamento seguro |
| Politica de branch por app | [scripts/ecosystem-governance-catalog.json](scripts/ecosystem-governance-catalog.json) | Define `sourceBranchTarget` e `releaseBranchTarget` |

Status de alinhamento de branches.

```bash
python scripts/ecosystem_branch_governance.py status
```

Alinhamento de branches com seguranca (nao troca branch em repo sujo).

```bash
python scripts/ecosystem_branch_governance.py align
```

Simulacao de alinhamento sem alterar repositorios.

```bash
python scripts/ecosystem_branch_governance.py align --dry-run
```

## Documentacao de governanca

| Documento | Finalidade |
|---|---|
| [mapeamento_ecossistema_productos.html](docs/mapeamento_ecossistema_productos.html) | Mapa tecnico dos produtos e dependencias |
| [relatorio_seguranca_ecossistema.html](docs/relatorio_seguranca_ecossistema.html) | Consolidado de postura de seguranca do ecossistema |
| [auditoria_licencas_repositorios_2026_03_14.html](docs/auditoria_licencas_repositorios_2026_03_14.html) | Verificacao de conformidade de licenciamento |
| [auditoria_seguranca_lojas_releases.html](docs/auditoria_seguranca_lojas_releases.html) | Analise de seguranca para repositorios de releases |
| [gate_publicacao_antiabutre_ecossistema.html](docs/gate_publicacao_antiabutre_ecossistema.html) | Criterios obrigatorios antes de publicacao |

## Pre-requisitos

| Dependencia | Versao recomendada |
|---|---|
| Python | 3.10 ou superior (scripts em `scripts/` usam apenas biblioteca padrao) |
| Git | Necessario para delivery sync e governanca de branches |

## Licenciamento

Este repositorio e distribuido sob a Licenca MIT.
Os termos completos de uso, modificacao e distribuicao estao no arquivo [LICENSE](LICENSE).

## Politica editorial deste manual

Este README deve permanecer em padrao institucional, com linguagem tecnica, objetiva e foco operacional.
Nao utilizar emojis, icones visuais informais, excesso de marcacao tipografica ou recursos narrativos nao tecnicos.
