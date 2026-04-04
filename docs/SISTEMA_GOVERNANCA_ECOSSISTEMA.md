# Sistema de Governanca do Ecossistema Cara Core

Este documento define o `caracore-tools` como nucleo operacional de governanca para:
- releases
- roadmap
- automacao de delivery
- sincronizacao matriz/lojas por aplicacao

## Objetivo

Reduzir estresse operacional com um fluxo unico, rastreavel e reproduzivel.

## Componentes

1. Orquestracao de delivery:
- `scripts/ecosystem-delivery.ps1`
- `scripts/ecosystem-delivery-map.json`

2. Governanca e gate:
- `scripts/ecosystem-governance.ps1`
- `scripts/ecosystem-governance-catalog.json`

3. Governanca de branches:
- `scripts/ecosystem-branch-governance.ps1`
- campos `sourceBranchTarget` e `releaseBranchTarget` no catalogo

3. Wrappers por aplicacao:
- `scripts/run_delivery_ete_to_releases.ps1`
- `scripts/run_delivery_circuito_to_releases.ps1`
- `scripts/run_delivery_hub_to_releases.ps1`
- `scripts/run_delivery_ink_to_releases.ps1`
- `scripts/run_delivery_ru_to_releases.ps1`
- `scripts/run_delivery_cso_to_releases.ps1`
- suporte comum: `scripts/sync_delivery_site_to_releases_docs.ps1`

## Fluxo recomendado por release

1. Dashboard de governanca:

```powershell
.\scripts\ecosystem-governance.ps1 -Action dashboard
```

2. Janela de calendario (proximos marcos):

```powershell
.\scripts\ecosystem-governance.ps1 -Action roadmap -WindowDays 180
```

2.5. Alinhamento de branch por app (fonte e releases):

```powershell
.\scripts\ecosystem-branch-governance.ps1 -Action status
.\scripts\ecosystem-branch-governance.ps1 -Action align -DryRun
```

3. Gate por aplicacao (No-Go/Go):

```powershell
.\scripts\ecosystem-governance.ps1 -Action gate -App pdv -Strict
```

4. Geracao de evidencia formal do gate:

```powershell
.\scripts\ecosystem-governance.ps1 -Action report -App pdv
```

5. Simulacao de delivery:

```powershell
.\scripts\ecosystem-delivery.ps1 -Action run -App pdv -DryRun
```

6. Delivery efetivo:

```powershell
.\scripts\ecosystem-delivery.ps1 -Action run -App pdv
```

## Criticidade do gate

O gate avalia quatro eixos:
- Seguranca (tokens/credenciais de publicacao)
- Consistencia Delivery-Matriz-Loja
- Automacao (comando de release existente)
- Integridade Git (repos limpos)

Regra:
- Falha critica => `BLOQUEADO`
- Sem falha critica e com ressalvas => `APROVADO COM RESSALVAS`
- Sem ressalvas => `APROVADO`

## Evidencias

Relatorios sao gerados em:
- `docs/governance-reports/`

Padrao de arquivo:
- `GATE_<app>_<timestamp>.md`

## Politica operacional

- Sempre executar `dashboard` e `gate` antes de publicar.
- Sempre executar `-DryRun` antes de delivery efetivo.
- Usar commits atomicos por app e por repositorio.
- Publicar somente com trilha de evidencia do gate.
