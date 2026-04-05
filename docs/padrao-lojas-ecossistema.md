# Padrao de Lojas do Ecossistema Cara Core Informatica

Este documento define o padrao tecnico para todas as lojas publicadas via repositorios `*-releases`.

## 1) Objetivos

- Garantir encoding consistente (UTF-8) em todas as paginas.
- Padronizar layout e componentes institucionais.
- Manter identidade visual por produto sem perder consistencia de ecossistema.
- Facilitar manutencao e evolucao das lojas.

## 2) Estrutura padrao

```text
docs/
  assets/
    caracore-core-typography.css
    caracore-institutional-components.css
    css/
      loja.css
      <produto>.css
    evolution-status/
      evolution-status.css
    js/
      loja.js
      <produto>.js
    images/
      favicon.ico
  index.html
  download.html
  canal-feedback.html
  tecnologia.html (ou equivalente)
  wiki/ (opcional)
  .nojekyll
  CNAME
  _config.yml
```

## 3) Regras de encoding

- Todos os arquivos HTML, CSS, JS e MD devem estar em UTF-8.
- `meta charset="UTF-8"` deve existir em todas as paginas HTML.
- Nao permitir texto corrompido (ex.: `Ã§`, `Ã£`, `â€”`, `â€“`, `â€`).

## 4) Regras de front-end

- `body` deve usar `class="cc-i-page"` para ativar componentes institucionais.
- Ordem recomendada de CSS no `<head>`:
  1. `assets/caracore-core-typography.css`
  2. `assets/caracore-institutional-components.css`
  3. `assets/css/loja.css`
  4. `assets/css/<produto>.css`
  5. `assets/evolution-status/evolution-status.css` (quando aplicavel)
- Evitar CDN externo para frameworks de layout; priorizar recursos locais versionados no repo.

## 5) Componentes obrigatorios por loja

- Breadcrumb institucional.
- Canal de feedback.
- Rodape com links para loja, repositorio e portfolio.
- Bloco de apresentacao do produto com CTA claro (download, demonstracao ou compra).

## 6) Checklist de revisao por loja

- [ ] `index.html` com `meta charset="UTF-8"`.
- [ ] Arquivos sem mojibake (`Ã`, `â€`, `�`).
- [ ] `body.cc-i-page` aplicado.
- [ ] Breadcrumb presente e funcional.
- [ ] Canal de feedback funcional.
- [ ] CSS padronizado (`loja.css` + `<produto>.css`).
- [ ] Dependencias externas de layout removidas ou justificadas.
- [ ] Links internos validados (sem 404).
- [ ] `CNAME`, `.nojekyll` e `_config.yml` corretos.

## 7) Ordem recomendada de revisita

1. caracore-oidc-releases
2. caracore-ete-releases
3. caracore-cso-releases
4. caracore-seed-releases
5. caracore-area51-releases
6. caracore-ru-releases
7. caracore-ink-releases
8. caracore-mkt-releases
9. caracore-pdv-releases
10. caracore-hub-releases
11. caracore-circuito-releases

## 8) Regra de commit

- Um commit por loja e por objetivo tecnico.
- Mensagem padrao sugerida:
  - `fix(loja): normaliza encoding utf-8`
  - `refactor(loja): padroniza css e layout institucional`
  - `feat(loja): adiciona componentes obrigatorios da loja`
