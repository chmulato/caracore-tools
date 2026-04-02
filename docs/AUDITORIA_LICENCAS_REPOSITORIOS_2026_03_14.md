# Auditoria de Licencas dos Repositorios

Data: 2026-03-14
Escopo: pastas de repositorio em d:/dev (caracore-* e circuito*)

## Resumo executivo

- Arquivos LICENSE existentes: OK (sem placeholder real, sem arquivo vazio).
- Tipos encontrados: MIT, Apache-2.0 e Proprietario.
- Status final: cobertura de LICENSE na raiz regularizada para 100% dos repositorios auditados.

## Repositorios com LICENSE na raiz

- caracore-circuito (Proprietario)
- caracore-cso (MIT)
- caracore-ete (MIT)
- caracore-ete-releases (Proprietario)
- caracore-ink (MIT)
- caracore-mkt (MIT)
- caracore-mkt-releases (MIT)
- caracore-oidc (Proprietario)
- caracore-oidc-releases (MIT)
- caracore-pdv (MIT)
- caracore-seed-releases (MIT)
- caracore-site (MIT)

### Regularizados nesta execucao (LICENSE de raiz criado)

- caracore-area51 (Proprietario)
- caracore-area51-releases (Proprietario)
- caracore-circuito-releases (Proprietario)
- caracore-cso-releases (Proprietario)
- caracore-hub (Proprietario)
- caracore-hub-releases (Proprietario)
- caracore-ink-releases (Proprietario)
- caracore-pdv-releases (Proprietario)
- caracore-ru (Proprietario)
- caracore-ru-releases (Proprietario)
- caracore-seed (Proprietario)
- caracore-tools (Proprietario)

## Observacao importante

- caracore-hub possui subprojeto com licenca propria em `project_hub/LICENSE` (Apache-2.0). A raiz do repositorio foi regularizada com politica proprietaria institucional.

## Repositorios sem LICENSE na raiz (gap)

- Nenhum (0). Gap encerrado nesta execucao.

## Verificacao de qualidade dos LICENSE existentes

- Nenhum LICENSE existente esta vazio.
- Nao foi encontrado TODO/TBD/PENDING/PLACEHOLDER real em LICENSE (os matches iniciais eram falsos positivos por palavras como "Todos").

## Proximo passo natural (recomendado)

1. Atualizar cada README com secao "Licenca" e link para o LICENSE da raiz.
2. Definir, em documento de governanca, criterios objetivos para quando um repositorio deve ser MIT vs Proprietario.
3. Adicionar checagem automatica no CI para falhar se faltar arquivo LICENSE na raiz.
