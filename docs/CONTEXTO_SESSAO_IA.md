# Contexto de Sessão — Cara Core Informática
**Última atualização:** 22/02/2026  
**Propósito:** Memória de sessão para continuidade entre IAs colaboradoras.

## Classificação e proteção de contexto (obrigatório)

- Classificação deste documento: `USO INTERNO - ECOSSISTEMA CARA CORE`.
- Este conteúdo não deve ser publicado em blog, loja, release notes públicas, redes sociais ou prompts externos.
- É proibido registrar aqui segredo real: senha, token, chave privada, `client_secret`, credencial de produção ou dado pessoal sensível.
- Quando necessário, usar apenas placeholders (ex.: `<senha_bootstrap_local>`, `<token_interno>`).
- Antes de compartilhar qualquer trecho fora da infra, aplicar revisão de sanitização e mascaramento.

---

## 1. Empresa e Ecossistema

- **Empresa:** Cara Core Informática — CNPJ 23.969.028/0001-37
- **Site matriz:** `https://caracore.com.br` → workspace local: `D:\dev\caracore-site\`
- **Modelo:** Matriz (delivery) + Filiais (loja GitHub Pages por produto)
- **Contato suporte:** suporte@caracore.com.br · WhatsApp/Telegram · sem atendimento por telefone

---

## 2. Regra de licenciamento — DECISÃO FIRMADA (19/02/2026)

**TODOS os produtos da Cara Core Informática são PROPRIETÁRIOS. Nenhum é MIT ou open source.**

| Produto | Gratuidade | Licença paga |
|---------|-----------|-------------|
| Circuito Ferradura | Pessoas físicas (uso pessoal e estudo) | R$ 5,00/aluno/mês para escolas de ensino médio |
| Reino OIDC | Pessoas físicas (uso pessoal e estudo) | Licença comercial para empresas/instituições |
| Área 51 (scripts OIDC) | — | Serviço contratável, orçamento via canal de feedback |

**⚠️ Nunca usar "MIT", "open source" ou "licença livre" em nenhum material da Cara Core. Sempre usar:**
- "Licença proprietária — não é MIT, não é open source."
- "Gratuito para pessoas físicas (uso pessoal e estudo)."

---

## 3. Arquitetura de arquivos — onde fica o quê

### Matriz (`D:\dev\caracore-site\delivery\`)
| Caminho | Produto |
|---------|---------|
| `delivery/circuito/` | Circuito Ferradura — delivery matriz |
| `delivery/circuito/curso/` | Curso HTML 6 fases (copiado de `caracore-circuito\pages_ferradura\`) |
| `delivery/oidc/` | Reino OIDC — delivery matriz |
| `delivery/area51/` | Área 51 — delivery matriz |

### Filiais / Lojas (GitHub Pages)
| Workspace local | GitHub Pages | Produto |
|----------------|-------------|---------|
| `D:\dev\caracore-circuito-releases\docs\` | `chmulato.github.io/circuito-python-releases/` | Circuito Ferradura loja |
| `D:\dev\caracore-circuito-releases\docs\curso\` | (relativo à loja) | Curso HTML 6 fases na loja |
| `D:\dev\caracore-oidc-releases\docs\` | `chmulato.github.io/reino-oidc-releases/` | Reino OIDC loja |
| `D:\dev\caracore-area51-releases\docs\` | `chmulato.github.io/caracore-area51-releases/` | Área 51 loja |

### Oficinas (repositórios privados de desenvolvimento)
| Workspace local | Produto |
|----------------|---------|
| `D:\dev\caracore-circuito\` | Circuito Ferradura — oficina (PROPRIETÁRIO) |
| `D:\dev\caracore-oidc\` | Reino OIDC — oficina (PROPRIETÁRIO — convertido de MIT em 19/02/2026) |
| `D:\dev\caracore-area51\` | Área 51 — oficina |

---

## 4. Circuito Ferradura — estado atual

- **Licença:** PROPRIETÁRIA (`caracore-circuito/LICENSE` = "LICENÇA PROPRIETÁRIA - TODOS OS DIREITOS RESERVADOS")
- **Curso HTML:** 6 fases completas em HTML (Fase 1 → Fase 6 + Conclusão + Mundo do Conhecimento + Apresentação)
- **CTAs corretos:**
  - Primary: `curso/index.html` (relativo, interno)
  - Secondary: Download .exe → GitHub releases
- **Curso disponível em dois lugares:**
  - Matriz: `delivery/circuito/curso/index.html`
  - Loja: `caracore-circuito-releases/docs/curso/index.html`
- **Selo Seed:** presente na loja em todos os HTMLs (`.evo-beta-badge`, FAB WhatsApp, `evo-roadmap-footer`)
- **Mensagem de licença em destaque nas duas páginas principais:**  
  `"Licença proprietária — não é MIT, não é open source."`

---

## 5. Reino OIDC — estado atual

- **Licença:** PROPRIETÁRIA (convertida de MIT em 19/02/2026)
- **Arquivos atualizados:**
  - `caracore-oidc/LICENSE` → licença proprietária Cara Core
  - `caracore-oidc/LICENSING.md` → reescrito, "não é MIT, não é open source"
  - `caracore-oidc/CONTEXTO_COLABORACAO_IA.md` → seção 5 atualizada com aviso da decisão
  - `caracore-oidc-releases/docs/index.html` → footer corrigido (sem MIT), span→link para matriz
  - `caracore-oidc-releases/docs/licenca-uso.html` → título, meta, header e bloco FREE → proprietário
  - `caracore-site/delivery/oidc/index.html` → hero, footer, span Circuito Python → link real
  - `caracore-area51-releases/docs/index.html` → "produto MIT" → "produto proprietário Cara Core" (3 ocorrências)
- **Upgrade:** "O Trono da Identidade" — R$ 29,90, PIX (permanece inalterado)
- **9 personagens canônicos:** Lady OAuth, Lord OIDC, Alex Client, Pixie PKCE, IDA Token, Ace Token, Rex Token, Seraph Resource, Devia (ver `caracore-oidc/CONTEXTO_COLABORACAO_IA.md`)

---

## 6. Área 51 — estado atual

### 6.1 Produto e serviço
- **Produto:** Pacote Python `area51-config` — scripts de configuração OIDC para médias empresas
- **Versão atual:** `0.1.0.dev0` (em desenvolvimento). Lançamento previsto: 02/08/2026
- **Modelo comercial:** Produto (scripts proprietários) + Serviço (Suporte Área 51, orçamento via canal)
- **Narrativa Cara↔Crachá:**
  - Cara = Reino das Entidades Federadas (narrativa, personagens, scripting — **proprietário Cara Core**)
  - Crachá = OpenID Connect (padrão de mercado, especificação pública — não é propriedade da Cara Core)

### 6.2 Oficina (`D:\dev\caracore-area51\`) — pacote Python

| Módulo | O que entrega |
|--------|---------------|
| `area51_config.oidc_validation` | Validação PKCE, redirect_uri, authorization request |
| `area51_config.exceptions` | `Area51ConfigError`, `OIDCProtocolError` com `protocol_item` e `step` |
| `area51_config.logging_config` | Logs estruturados (fix Python 3.14: `_Area51Formatter` — evita `setLogRecordFactory`) |
| `area51_config.baseline_validation` | `validate_baseline()` — início obrigatório do processo |
| `area51_config.config_generator` | `OIDCConfigGenerator` — fábricas `.google()` e `.microsoft()`, `.build()`, `.validate()`, `.export_env()`, `.export_json()` |
| `area51_config.__main__` | CLI `area51-config generate {google,microsoft}` e `area51-config validate {google,microsoft}` |

**Arquivos de saída do CLI:**
- `.env.google.example` / `.env.microsoft.example`
- `oidc_config_google.json` / `oidc_config_microsoft.json`
- Nenhum arquivo de saída contém `client_secret`

**Regra de HTTPS no `build()`:** `_assert_redirect_uri()` sempre rejeita HTTP não-localhost, independente do flag `--allow-http`. O `--allow-http` relaxa apenas o `validate_baseline()`; como `build()` executa antes, o efeito prático de `--allow-http` é somente para localhost (que já é aceito por padrão).

**Testes:** 111 testes passando (Fevereiro/2026): `python -m pytest tests/ -v`
- `tests/unit/test_config_generator.py` — 44 testes do gerador
- `tests/unit/test_cli.py` — 34 testes da CLI
- `tests/unit/test_oidc_validation.py` — validação OIDC
- `tests/validation_oidc/` — testes de protocolo (PKCE, authorization request)

**pyproject.toml:** `build-backend = "setuptools.build_meta"` (não `setuptools.backends.legacy:build` — incompatível com Python 3.14). Instalação: `python -m pip install -e .`

**Documentação da oficina:**
- `docs/ALINHAMENTO_PRODUTO_AREA51.md` — documento canônico (criado 20/02/2026): define produto, serviço, IP, Cara↔Crachá, o que não mudar sem consenso
- `docs/ESTRATEGIA_DESENVOLVIMENTO_AREA51.md` — estratégia técnica e estrutura
- `docs/EXEMPLO_INICIO_PROCESSO.md` — exemplo de uso da baseline
- `docs/DOCUMENTACAO.txt` — regras da documentação da oficina (somente MD e TXT, sem HTML)

### 6.3 Loja (`D:\dev\caracore-area51-releases\docs\`) — correções aplicadas (20/02/2026)
- `licenca-uso.html`: "produto MIT" → "produto proprietário Cara Core Informática" + "Licença proprietária — não é MIT"
- `licenca-uso.html`, `download.html`, `canal-feedback.html`: breadcrumb "Cara Core" corrigido de `href="index.html"` para `href="https://caracore.com.br/"`
- `VERSION`: `0.1.0` → `0.1.0-dev` (alinhado com `0.1.0.dev0` do pyproject.toml)

### 6.4 Site (20/02/2026) — migração CDN → local (`D:\dev\caracore-site\`)
- **Bootstrap 5.3.3:** todos os HTMLs migrados de CDN para `/css/vendor/bootstrap.min.css` e `/js/vendor/bootstrap/bootstrap.bundle.min.js`
- **Bootstrap Icons:** CDN → `/css/vendor/bootstrap-icons/bootstrap-icons.min.css`
- **Mermaid v11:** CDN → `/js/vendor/mermaid/mermaid.esm.min.mjs`
- **Chart.js v4.5.1:** CDN → `/js/vendor/chartjs/chart.umd.min.js`
- **Resultado:** 0 referências CDN ativas em todos os HTMLs do site
- **OIDC site:** auditado e confirmado funcional — `oidc-client-ts.js` e `msal-browser.min.js` já eram locais; fluxo PKCE com Google (default) e Microsoft Entra

---

## 7. Padrões técnicos das lojas (filiais)

- **Todos os links internos:** referências relativas (`curso/index.html`, `download.html`, etc.)
- **Links externos legítimos:** GitHub (`github.com/chmulato/...`), outros domínios (`caracore.com.br`)
- **Breadcrumb padrão:**
  ```html
  <a href="https://caracore.com.br/">Cara Core Informática</a> · 
  <a href="https://caracore.com.br/portfolio.html#produto">Portfólio</a> · 
  <span>Nome do Produto — Filial</span>
  ```
- **Span morto → link real:** CTAs secundários "Ver apresentação (matriz)" devem ser `<a href="https://caracore.com.br/delivery/produto/">` nunca `<span disabled>`
- **Selo Seed (obrigatório em toda loja):**
  ```html
  <div class="evo-beta-wrap" aria-hidden="true"><span class="evo-beta-badge">Seed<span class="evo-beta-tooltip">...</span></span></div>
  <footer class="evo-roadmap-footer">...</footer>
  <div class="evo-feedback-fab">...</div>
  ```
  CSS: `assets/evolution-status/evolution-status.css`

---

## 8. Convenções de conteúdo

- Gratuidade: sempre "gratuito para pessoas físicas (uso pessoal e estudo)"
- Licença: sempre "licença proprietária — não é MIT, não é open source"
- Escolas Circuito: "R$ 5,00/aluno/mês obrigatório — uso sem licença pode responder legalmente"
- OIDC upgrade: "R$ 29,90 (valor único) — PIX"
- Sede da empresa: nunca linkar `index.html` (auto-referência) como "Cara Core" — usar `https://caracore.com.br/`
- Footer de loja: nunca `href="index.html"` para Cara Core — sempre `href="https://caracore.com.br/"`

---

## 9. Sessões anteriores (resumo das decisões acumuladas)

| Data | Decisão |
|------|---------|
| 19/02/2026 | Circuito Ferradura: MIT → proprietário (12 ocorrências em 2 arquivos) |
| 19/02/2026 | Curso HTML Circuito copiado para matriz (`delivery/circuito/curso/`) |
| 19/02/2026 | Curso HTML Circuito copiado para loja (`circuito-releases/docs/curso/`) |
| 19/02/2026 | CTAs loja Circuito: GitHub Pages → `curso/index.html` relativo |
| 19/02/2026 | Fixes técnicos Área 51 loja: breadcrumb, CTA spam→link, footer |
| 19/02/2026 | OIDC loja: span→link "Apresentação (matriz)" |
| 19/02/2026 | Reino OIDC: MIT → proprietário (LICENSE, LICENSING.md, loja, matriz, Área 51 — 9 arquivos) |
| 19/02/2026 | Matriz OIDC: span Circuito Python → link real para `delivery/circuito/` |
| 20/02/2026 | Matriz Circuito: nav-card licença + "não é MIT, não é open source" |
| 20/02/2026 | Site: Bootstrap, Mermaid, Chart.js — CDN → local (todos os HTMLs; 0 CDN ativas) |
| 20/02/2026 | Site OIDC: auditado e confirmado funcional (PKCE, Google + MS Entra, tudo local) |
| 20/02/2026 | Área 51 oficina: `OIDCConfigGenerator` (Google + MS Entra), `__main__.py` CLI, `pyproject.toml` |
| 20/02/2026 | Área 51 oficina: 111 testes passando; fix Python 3.14 logging (`_Area51Formatter`) |
| 20/02/2026 | Área 51 oficina: `pyproject.toml` — `build-backend = "setuptools.build_meta"` (fix Python 3.14) |
| 20/02/2026 | Área 51 oficina: `docs/ALINHAMENTO_PRODUTO_AREA51.md` criado — documento canônico de IP |
| 20/02/2026 | Área 51 loja: `licenca-uso.html` — "produto MIT" → "produto proprietário" (erro factual corrigido) |
| 20/02/2026 | Área 51 loja: breadcrumbs de 3 páginas corrigidos (`index.html` → `https://caracore.com.br/`) |
| 20/02/2026 | Área 51 loja: `VERSION` — `0.1.0` → `0.1.0-dev` (alinhado com pyproject.toml) |
| 22/02/2026 | **Personal blog validação:** Ollama local confirmado conectado (`codellama` via `http://localhost:11434`) |
| 22/02/2026 | **Personal blog:** `feed.xml` — removido artigo duplicado `2026_05_09`, mantido `2026_05_10` |
| 22/02/2026 | **Personal blog:** `index.html` — card de maio atualizado: `2026_05_09` → `2026_05_10`, data `09/05` → `10/05` |
| 22/02/2026 | **Personal blog:** validação de cobertura — índice e feed consistentes (98 artigos) |
| 22/02/2026 | **Personal blog:** auditoria de links quebrados — 131 referências locais não resolvidas |

---

## 10. Sessão 22/02/2026 — Personal Blog (Christian Mulato Dev Blog)

### 10.1 Correções realizadas

**Feed.xml (`caracore-site/personal/feed.xml`)**
- Removida entrada duplicada: `2026_05_09_o_legado_e_a_matriz_o_que_a_engenharia_herda_do_cuidado.html`
- Mantém entrada corrigida: `2026_05_10_o_legado_e_a_matriz_o_que_a_engenharia_herda_do_cuidado.html`
- Data publicação corrigida: `Sat, 09 May 2026` → `Sun, 10 May 2026`

**Index.html (`caracore-site/personal/index.html`)**
- Card de maio 2026 atualizado: link `2026_05_09_...html` → `2026_05_10_...html`
- Meta data do card: `09/05/2026` → `10/05/2026`

### 10.2 Validações confirmadas

| Validação | Status |
|-----------|--------|
| Feed vs. pasta `articles/` | ✅ consistente (98 artigos, sem redundância) |
| Index vs. pasta `articles/` | ✅ consistente (links resolvem, sem órfãos) |
| Index vs. feed | ✅ coerentes (mesmas datas, mesmos títulos) |

### 10.3 Links quebrados encontrados (não-crítico)

**Quebrados por falta de arquivo:**
- `assets/css/highlight.css` — 106 refs (alguns artigos importam CSS inexistente)
- `assets/img/favicon.ico` — 20 refs (favicon não existe)
- Imagens específicas faltando de poucos artigos:
  - `2024_03_06_IMAGE_001.png` (1 artigo)
  - `2024_03_20_IMAGE_003.png` (1 artigo)
  - `2026_03_30_IMAGE_001.png` (1 artigo)
- Placeholder não resolvido: `{video_path}` (1 artigo, `2026_03_03_...html`)

**Status:** Links internos (cross-article, breadcrumbs) — 100% funcional. Faltam só recursos estáticos (CSS de highlight, favicon, imagens pontuais).

### 10.4 Notas técnicas

- **Ollama local:** confirmado respondendo em `http://localhost:11434` com modelo `codellama:latest` ativo
- **Continue extension:** configurado em VS Code (`continue.models` aponta para `http://localhost:11434`)
- **Prompt customizado:** criado `caracore-site/personal/prompt_img.txt` para newsletter image generation
- **Artigos atuais:** 98 publicados (março 2024 — agosto 2026), organizados por ano/mês em HTML estruturado
- **RSS funcional:** feed.xml gerável automaticamente via script ou CI (não há CI em produção, feed edição manual)

### 10.5 Próximas ações (não urgent, pq site funcional)

- [ ] Criar/restaurar `highlight.css` se necessário (ou remover refs dos artigos se não usado)
- [ ] Gerar favicon.ico ou remover refs (baixa prioridade)
- [ ] Restaurar 3 imagens pontuais se edição de artigos planejada
- [ ] Substituir `{video_path}` em artigo 2026_03_03 com URL real ou remover tag
- [ ] Considerar automatizar feed.xml via script Python (opcional, atualmente manual)