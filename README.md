# caracore-tools

Utilitários de desenvolvimento do ecossistema **Cara Core Informática**.

Ferramentas para soberania do ambiente de desenvolvimento local: bloqueio de telemetria, IA local via Ollama, validação de qualidade de repositórios e laboratório de features Java.

---

## Estrutura

```
caracore-tools/
├── java/                        # Laboratório Java
│   ├── Main.java                # Records e Switch Expressions (Java 21+)
│   └── TesteJava21.java         # Virtual Threads — 10.000 tarefas paralelas
├── python/                      # Scripts de ambiente Black-Box
│   ├── block-telemetry-hosts.py     # Bloqueia domínios de telemetria no hosts
│   ├── unblock-telemetry-hosts.py   # Remove o bloqueio de telemetria
│   ├── plugar-olloma-local.py       # Inicia servidor Ollama local
│   └── desplugar-olloma-local.py    # Para servidor Ollama local
├── scripts/                     # Scripts PowerShell de qualidade
│   └── check-readme-encoding.ps1   # Detecta e corrige mojibake em READMEs
├── docs/                        # Documentação técnica
│   └── BLACKBOX_AMBIENTE_DESENVOLVIMENTO.md
├── plano/                       # Rascunhos estratégicos internos
└── .github/workflows/
    └── readme-encoding-check.yml   # CI: valida encoding de READMEs
```

---

## Módulos

### `python/` — Soberania do Código (Black-Box)

Controle total sobre o que entra e sai do ambiente de desenvolvimento.

#### Bloqueio de telemetria

Bloqueia domínios de telemetria da Microsoft, VS Code e Cursor no arquivo `hosts` do Windows, impedindo envio de dados sem consentimento.

```powershell
# Executar como Administrador
python python/block-telemetry-hosts.py

# Simular sem escrever (não requer admin)
python python/block-telemetry-hosts.py --dry-run

# Remover o bloqueio
python python/unblock-telemetry-hosts.py
```

Após qualquer alteração:

```powershell
ipconfig /flushdns
```

#### IA local via Ollama

Liga e desliga o servidor Ollama em `http://localhost:11434` para uso de modelos de linguagem totalmente offline.

```powershell
# Iniciar Ollama
python python/plugar-olloma-local.py

# Parar Ollama
python python/desplugar-olloma-local.py
```

Configure o VS Code ou Cursor para usar `http://localhost:11434/v1` como endpoint de IA local.

---

### `scripts/` — Qualidade de Repositórios

#### `check-readme-encoding.ps1`

Detecta marcadores de *mojibake* (UTF-8 decodificado como CP1252/Latin1) nos arquivos `README.md` de todos os repositórios `caracore-*` e `circuito*` em `D:\dev`.

```powershell
# Apenas detectar problemas
.\scripts\check-readme-encoding.ps1

# Detectar e corrigir automaticamente
.\scripts\check-readme-encoding.ps1 -Fix

# Usar outro diretório raiz
.\scripts\check-readme-encoding.ps1 -RootPath "C:\projetos"
```

---

### `java/` — Laboratório Java

Sandbox para validar features modernas do Java antes de adotá-las nos produtos do ecossistema.

| Arquivo | Feature testada | Versão mínima |
|---|---|---|
| `Main.java` | Records + Switch Expressions | Java 21 |
| `TesteJava21.java` | Virtual Threads (`newVirtualThreadPerTaskExecutor`) | Java 21 |

Compilar e executar:

```powershell
cd java
javac Main.java ; java Main
javac TesteJava21.java ; java TesteJava21
```

---

### `.github/workflows/readme-encoding-check.yml`

CI que roda em todo `push` e `pull_request`, validando que nenhum `README.md` do repositório contém marcadores de *mojibake*. Falha o build se encontrar caracteres suspeitos.

---

### `docs/BLACKBOX_AMBIENTE_DESENVOLVIMENTO.md`

Guia completo de configuração do ambiente de desenvolvimento hermético:

- Desativar telemetria no VS Code e Cursor via `settings.json`
- Ativar Privacy Mode no Cursor
- Bloquear domínios Microsoft via arquivo `hosts`
- Usar Ollama como backend de IA local

---

## Pré-requisitos

| Ferramenta | Uso |
|---|---|
| Python 3.8+ | Scripts `python/` |
| Java 21+ | Laboratório `java/` |
| PowerShell 5.1+ | Script `scripts/` |
| Ollama | Scripts de IA local (opcional) |
| Privilégio de Administrador | Scripts de bloqueio de telemetria |

---

## Relacionado

- [caracore-cso](https://github.com/chmulato/caracore-cso) — Backend Java 21 + Quarkus
- [caracore-cso-releases](https://github.com/chmulato/caracore-cso-releases) — Loja e releases
- Portfólio: [caracore.com.br](https://caracore.com.br)

---

*Cara Core Informática — Soberania do Código.*
