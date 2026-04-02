# Mapeamento Completo do Ecossistema CaraCore
Data: 27 de fevereiro de 2026
Total de Produtos: 11 produtos ativos

---

## Status: Ecossistema em Crescimento

O ecossistema CaraCore conta com 11 produtos proprietarios em diferentes estagios de desenvolvimento, cobrindo desde gestao empresarial ate educacao e simulacao cientifica.

---

## Produtos por Categoria

### Gestao de Negocios (4 produtos)

#### 1. CaraCore PDV - PDV Selo Verde
- Status: Producao - v1.1 (Releases disponiveis)
- Tipo: Sistema de Ponto de Venda Desktop (Windows)
- Stack: Java 21 + Spring Boot + SQLite + JavaFX
- Proposta: "O PDV que paga sua propria mensalidade"
- Diferenciais:
  - Funciona offline (localhost)
  - Banco SQLite local
  - Reforma Tributaria 2026-2033 compliance
  - Planos: Free e Premium
- Workspace: caracore-pdv/ + caracore-pdv-releases/
- Testes: 174/174 (100%)
- Site: [chmulato.github.io/caracore-pdv](https://chmulato.github.io/caracore-pdv/)

#### 2. CaraCore Hub - Hub Town (Gestao de Encomendas)
- Status: Em Desenvolvimento - v2.1 (Fase 5 concluida)
- Tipo: Sistema de Gestao Multi-Marketplace
- Stack: Jakarta EE 10 + Java 11 → migrando Java 21 + PostgreSQL → SQLite
- Proposta: Integracao automatizada com marketplaces
- Diferenciais:
  - Integracao Mercado Livre, Shopee, Temu
  - Webhooks em tempo real
  - Dashboard com Chart.js
  - Redis Cache + WebSocket
- Proximo Marco: Desktop SQLite EXE (06/04/2026)
- Workspace: caracore-hub/ + caracore-hub-releases/
- Site: [chmulato.github.io/caracore-hub](https://chmulato.github.io/caracore-hub/)

#### 3. Ink Agenda - Gestao para Estudios de Tatuagem
- Status: Em Desenvolvimento - v2.0.0 (Windows Desktop)
- Tipo: Sistema de Agendamento e Controle Financeiro
- Stack: Java 21 + JavaFX 21 + SQLite + Maven
- Proposta: Ferramenta profissional para tatuadores
- Diferenciais:
  - Agenda visual de sessoes
  - Controle financeiro completo
  - Painel de resultados
  - Temas claro/escuro
- Workspace: caracore-ink/ + caracore-ink-releases/
- Observacao: App Android v1.0 em producao (nao na matriz atual)

#### 4. CaraCore Seed - Controle de Licencas Empresariais
- Status: Producao (Pronto)
- Tipo: Sistema SaaS de Controle de Licencas
- Stack: Java + Spring Boot → migrando para Electron + SQLite
- Proposta: Licenciamento para CaraCore Hub e outros produtos
- Diferenciais:
  - Modelo SaaS recorrente
  - Gestao de licencas offline (Desktop)
  - Cobertura de testes: 89% (619 testes)
  - Testes E2E Selenium: 100%
- Workspace: caracore-seed/ + caracore-seed-releases/
- Site: [chmulato.github.io/caracore-seed](https://chmulato.github.io/caracore-seed/)

---

### Logistica e Entregas (1 produto)

#### 5. CaraCore CSO - Soberania Operacional (Protocolo Amarelinha)
- Status: Em Desenvolvimento - Sprint 1 (iniciando 06/04/2026)
- Tipo: Sistema de Rastreamento e Auditoria de Entregas
- Stack: Spring Boot + HSQLDB → migrando JavaFX 21 + SQLite
- Proposta: Auditoria inteligente de entregas com IA
- Diferenciais:
  - Protocolo Amarelinha (5 Atos):
    1. Geometria - Checkpoints obrigatorios
    2. Dinamica - Velocidade e consumo
    3. Sombra - Navegacao inercial (sem GPS)
    4. Massa - Detecao de perda de carga (Lei de Lavoisier)
    5. Ceu - Relatorios consolidados
  - Desktop Windows com JavaFX
- Lancamento Previsto: 08/11/2028
- Workspace: caracore-cso/ + caracore-cso-releases/
- Testes: 191/191 (100%)

---

### Educacao e Aprendizado (3 produtos)

#### 6. Circuito Ferradura - Curso de HTML Interativo
- Status: Producao (6 fases completas)
- Tipo: Plataforma Educacional Desktop/Web
- Stack: Python + HTML5/CSS3/JavaScript
- Proposta: Ensino de programacao web
- Diferenciais:
  - 6 fases completas de curso HTML
  - Instalador EXE Windows
  - Licenca proprietaria (gratuito para PF)
  - R$ 5,00/aluno/mes para escolas
- Workspace: caracore-circuito/ + caracore-circuito-releases/
- Site Loja: [chmulato.github.io/circuito-python-releases](https://chmulato.github.io/circuito-python-releases/)

#### 7. RU Free - Soberania RU - Dashboard Academico UFPR 1991
- Status: Em Desenvolvimento (migracao Python → Java 21 FX)
- Lancamento Previsto: 18/06/2026
- Tipo: Simulador Educacional Universitario
- Stack: Java 21 + JavaFX + Maven
- Proposta: Dashboard retro-futurista UFPR 1991
- Diferenciais:
  - Emulacao HP-48SX
  - Aula Prof. Soccol (balanco de massa)
  - Biorreator Simulator
  - Terminal CRT vintage
  - Soberania F10/F12
- Workspace: caracore-ru/ + caracore-ru-releases/
- Testes: 36/36 (100%)

#### 8. Reino OIDC - OAuth 2.1 Educacional
- Status: Producao
- Tipo: Plataforma Educacional de Autenticacao
- Stack: HTML5 + TypeScript + OIDC Client
- Proposta: Ensino de OAuth 2.1 e OpenID Connect
- Diferenciais:
  - 9 personagens canonicos (Lady OAuth, Lord OIDC, etc.)
  - Narrativa "O Trono da Identidade"
  - Upgrade: R$ 29,90
  - Integracao Google + Microsoft Entra
- Licenca: Proprietaria (convertida de MIT em 19/02/2026)
- Workspace: caracore-oidc/ + caracore-oidc-releases/
- Site Loja: [chmulato.github.io/reino-oidc-releases](https://chmulato.github.io/reino-oidc-releases/)

---

### Ciencia e Simulacao (1 produto)

#### 9. Minerador 4.0 (ETE) - Hidrometalurgia de Terras Raras
- Status: Producao
- Tipo: Simulador Cientifico Desktop
- Stack: Python + Tkinter/JavaFX
- Proposta: Simulacao de refino de terras raras
- Diferenciais:
  - Metodologia ETE aplicada a mineracao
  - "True Engine" - calculos quimicos reais
  - Vitrine web (conhecimento aberto)
  - Ferramenta desktop (execucao)
  - Validacao ambiental
- Workspace: caracore-ete/ + caracore-ete-releases/
- Sites: 
  - Vitrine: [chmulato.github.io/ETE](https://chmulato.github.io/ETE/)
  - Releases: [chmulato.github.io/ETE-releases](https://chmulato.github.io/ETE-releases/)

---

### Seguranca e Infraestrutura (2 produtos)

#### 10. Area 51 - Scripts OIDC para Empresas
- Status: Em Desenvolvimento - v0.1.0-dev
- Tipo: Pacote Python + Servico de Configuracao OIDC
- Stack: Python 3.14 + setuptools
- Proposta: Automacao de configuracao OIDC empresarial
- Diferenciais:
  - CLI: area51-config generate {google,microsoft}
  - Validacao PKCE e redirect_uri
  - Fabricas de config (.env, JSON)
  - Sem exposicao de client_secret
  - Servico de suporte (orcamento sob demanda)
- Lancamento Previsto: 02/08/2026
- Workspace: caracore-area51/ + caracore-area51-releases/
- Testes: 111/111 (100%)
- Site: [chmulato.github.io/caracore-area51-releases](https://chmulato.github.io/caracore-area51-releases/)

#### 11. CaraCore MKT - Sala de Noticias (Uso Interno)
- Status: Em Desenvolvimento (uso interno)
- Tipo: Automacao de Marketing e Comunicacao
- Stack: Python (Microsoft Store baseline)
- Proposta: Automacao de publicacao em canais sociais
- Diferenciais:
  - Scripts para Instagram, Facebook, Retro
  - Validacao automatica de entregas
  - Planilha de gestao de conteudo
  - Mensagens WhatsApp/Telegram/E-mail
- Licenca: MIT (uso interno apenas)
- Workspace: caracore-mkt/ + caracore-mkt-releases/
- Observacao: Nao e produto comercial - ferramenta interna

---

## Resumo por Status

| Status | Quantidade | Produtos |
|--------|------------|----------|
| Producao | 5 | PDV, Seed, Circuito, Reino OIDC, Minerador 4.0 |
| Desenvolvimento Ativo | 5 | Hub, CSO, Ink, RU, Area 51 |
| Interno/Ferramental | 1 | MKT |

---

## Produtos com Releases Prioritarios

| Produto | Data Prevista | Marco |
|---------|---------------|-------|
| Area 51 | 02/08/2026 | v0.1.0 |
| Hub (Desktop) | 06/04/2026 | Instalador SQLite EXE |
| RU Free | 18/06/2026 | v1.0 JavaFX |
| CSO (Amarelinha) | 08/11/2028 | Protocolo completo |

---

## Evolucoes Relevantes

Nao ha produtos totalmente novos no periodo. As evolucoes principais sao:

1. CSO com arquitetura Protocolo Amarelinha em 5 atos e foco desktop JavaFX.
2. Hub com entrega desktop SQLite em 06/04/2026.
3. Seed em migracao para desktop Electron com base local.
4. RU Free em migracao para Java 21 FX com lancamento em 18/06/2026.

---

## Modelo de Negocio por Produto

| Produto | Modelo | Preco/Licenca |
|---------|--------|---------------|
| PDV | Freemium | Free / Premium |
| Hub | SaaS (futuro) | Por centro de distribuicao |
| Seed | SaaS | Controle de licencas |
| Ink | Licenca | Desktop Windows |
| CSO | Licenca (futuro) | Empresas de logistica |
| Circuito | Gratuito PF / Licenca Escolar | R$ 5/aluno/mes |
| RU Free | Educacional | Gratuito |
| Reino OIDC | Freemium | Gratuito PF / R$ 29,90 upgrade |
| Minerador 4.0 | Educacional | Gratuito (conhecimento) / Desktop pago |
| Area 51 | Produto + Servico | Scripts + Consultoria sob orcamento |
| MKT | Interno | Nao comercializado |

---

## Stack Tecnologico Unificado

### Backend
- Java: 11 e 21 (migracao gradual para 21)
- Frameworks: Spring Boot e Jakarta EE 10
- Bancos: SQLite (padrao desktop) e PostgreSQL (legado web)

### Frontend Desktop
- JavaFX 21 como padrao dos aplicativos desktop
- Electron para Seed e futuras aplicacoes hibridas

### Frontend Web
- HTML5, CSS3 e JavaScript
- Bootstrap 5.3.3 local
- Chart.js 4.5.1 e Mermaid v11

### Python
- Versao 3.14+
- Uso em scripts, automacao e simuladores cientificos

---

## 📂 Estrutura do Workspace

```
D:\dev\
├── caracore-pdv/          + caracore-pdv-releases/
├── caracore-hub/          + caracore-hub-releases/
├── caracore-seed/         + caracore-seed-releases/
├── caracore-ink/          + caracore-ink-releases/
├── caracore-cso/          + caracore-cso-releases/
├── caracore-circuito/     + caracore-circuito-releases/
├── caracore-ru/           + caracore-ru-releases/
├── caracore-oidc/         + caracore-oidc-releases/
├── caracore-ete/          + caracore-ete-releases/
├── caracore-area51/       + caracore-area51-releases/
├── caracore-mkt/          + caracore-mkt-releases/
├── caracore-site/         (Matriz - portal principal)
└── caracore-tools/        (Ferramentas de desenvolvimento)
```

**Padrão**: Cada produto tem:
- Oficina (desenvolvimento privado)
- Releases (delivery público GitHub Pages)

---

## 🎓 Produtos por Público-Alvo

| Público | Produtos Recomendados |
|---------|----------------------|
| **Lojistas** | PDV |
| **E-commerce** | Hub |
| **Tatuadores** | Ink Agenda |
| **Transportadoras** | CSO |
| **Estudantes** | Circuito, RU, Reino OIDC, Minerador 4.0 |
| **Médias Empresas** | Área 51, Seed |
| **Desenvolvedores** | Reino OIDC, Área 51 |
| **Cientistas/Acadêmicos** | Minerador 4.0, RU |

---

## ✅ Certificação de Qualidade

### Produtos com 100% Testes ✅
1. **PDV**: 174/174 testes
2. **CSO**: 191/191 testes
3. **RU**: 36/36 testes
4. **Área 51**: 111/111 testes

### Produtos com Alta Cobertura
- **Seed**: 89% (619 testes unitários + E2E Selenium 100%)

---

## 🚀 Roadmap Estratégico

### 2026
- ✅ Q1: Consolidação PDV, Seed, Circuito
- 🔧 Q3: Lançamento Área 51 (agosto)
- 🔧 Q4: CSO Sprint 1-4

### 2027
- 🔧 Q2: Hub Desktop SQLite (abril)

### 2028
- 🔧 Q4: CSO Protocolo Amarelinha (novembro)

---

## 📞 Matriz e Contato

- **Site Principal**: [caracore.com.br](https://caracore.com.br)
- **CNPJ**: 23.969.028/0001-37
- **Suporte**: suporte@caracore.com.br
- **Modelo**: Matriz (delivery) + Filiais (lojas GitHub Pages)

---

**Gerado por**: CaraCore Product Mapping System  
**Última Atualização**: 27 de fevereiro de 2026  

---

## 🎯 Conclusão

O ecossistema CaraCore está **saudável e em crescimento**, com:
- ✅ **11 produtos ativos** (5 em produção, 5 em desenvolvimento, 1 interno)
- ✅ **100% de testes** nos produtos principais (PDV, CSO, RU, Área 51)
- ✅ **Migração unificada** para Java 21 + JavaFX + SQLite
- ✅ **Licenciamento proprietário** consolidado em todos os produtos
- ✅ **Roadmap claro** até 2028

**Não há produtos completamente novos**, mas há **evoluções arquiteturais significativas** em Hub, Seed e CSO (Protocolo Amarelinha).
