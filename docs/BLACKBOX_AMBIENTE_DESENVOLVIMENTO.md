# Ambiente de Desenvolvimento Black-Box — Soberania do Código

**Objetivo:** Nenhuma telemetria ou código da Cara Core Informática deve sair do NOTEBOOK_TEO sem permissão expressa. VS Code/Cursor restrito a telemetria desligada e, opcionalmente, apenas localhost (Ollama).

---

## 1. Configurações no `settings.json` (telemetria e crash reporter)

**Arquivo (Cursor):** `%APPDATA%\Cursor\User\settings.json`  
**Arquivo (VS Code):** `%APPDATA%\Code\User\settings.json`

Adicione ou ajuste as chaves abaixo:

| Chave | Valor | Efeito |
|-------|--------|--------|
| `telemetry.telemetryLevel` | `"off"` | Desativa **toda** telemetria do núcleo (uso, erros, eventos). |
| `telemetry.enableCrashReporter` | `false` | Desativa envio de relatórios de crash. |
| `enable-crash-reporter` | `false` | Flag do Electron/crash reporter (redundante com o anterior). |
| `update.mode` | `"none"` | Opcional: não busca atualizações automaticamente (evita tráfego de update). |
| `extensions.autoCheckUpdates` | `false` | Opcional: não verifica atualizações de extensões. |
| `extensions.autoUpdate` | `false` | Opcional: não atualiza extensões automaticamente. |

**Cursor (específico):**

- **Privacy Mode:** em **Cursor Settings > General > Privacy Mode** ative **Privacy Mode**.  
  Isso reduz retenção de dados com provedores de modelo (prompts/código não usados para treino).  
  Se existir chave em `settings.json`, use: `"cursor.privacyMode": true` (conforme documentação atual do Cursor).

**Resumo mínimo no JSON:**

```json
{
  "telemetry.telemetryLevel": "off",
  "telemetry.enableCrashReporter": false,
  "enable-crash-reporter": false
}
```

Reinicie o editor após alterar. Mesmo com isso, o editor pode ainda fazer *DNS lookups* para domínios Microsoft; para bloquear de fato, use o arquivo **hosts** (seção 3).

---

## 2. Extensões que costumam enviar dados (e como limitar)

Estas extensões costumam ter telemetria ou envio de código/uso para nuvem. Limite-as conforme necessidade.

| Extensão / família | O que costumam fazer | Como limitar |
|--------------------|----------------------|--------------|
| **GitHub Copilot** | Envia trechos de código e contexto para nuvem. | Desative na extensão ou não use em repositórios sensíveis. Cursor: use apenas modelos locais (Ollama) e Privacy Mode. |
| **GitLens** | Uso e, em versões, telemetria. | `"gitlens.telemetry.enabled": false` (ou equivalente nas configurações da extensão). |
| **Red Hat (Java, YAML, etc.)** | Telemetria de uso. | `"redhat.telemetry.enabled": false` (você já pode forçar no settings). |
| **Docker** | Telemetria e analytics. | Desative em *Docker extension settings* (telemetry / usage data). |
| **Azure / MS SQL** | Telemetria e diagnóstico. | Desative telemetria nas configurações de cada extensão; evite abrir workspaces sensíveis com elas. |
| **Codeium / Tabnine / similares** | Enviam contexto de código para servidores. | Desative ou não instale em ambiente black-box. |
| **Qualquer extensão “AI” que use nuvem** | Envio de código/prompts. | Use apenas modelos locais (Ollama) e leia a política de privacidade. |

**Boas práticas:**

- Em **Extensions**, revise cada extensão: abra *Details* e procure por “Telemetry”, “Data”, “Privacy”.
- Desative telemetria por extensão quando houver opção em **Settings** ou em `settings.json` (chaves com nome da extensão).
- Para máxima soberania: use o mínimo de extensões e prefira as que não dependem de servidores externos para o seu código.

---

## 3. Script para bloquear domínios de telemetria no `hosts` (Windows)

O script adiciona entradas ao arquivo **hosts** do Windows para resolver domínios conhecidos de telemetria da Microsoft e do ecossistema VS Code para `0.0.0.0`, impedindo que o tráfego saia.

**Arquivo:** `D:\dev\block-telemetry-hosts.py` (Python 3)

**Uso:** Executar **como Administrador** (terminal/Prompt de Comando elevado):

```bash
python D:\dev\block-telemetry-hosts.py
```

Para **testar sem alterar o hosts** (não exige admin): `python D:\dev\block-telemetry-hosts.py --dry-run`

Depois de executar de fato: `ipconfig /flushdns`.

---

## 4. Firewall do Windows: Ollama (localhost:11434) permitido e restrição a telemetria

**Objetivo:** Garantir que o Cursor/VS Code possa falar com o Ollama em `localhost:11434` e, na medida do possível, não alcançar servidores de telemetria (sem quebrar Git, npm, etc.).

### 4.1 Permitir apenas localhost:11434 (Ollama)

O tráfego para `127.0.0.1:11434` já é local; o Firewall do Windows normalmente não bloqueia conexões de loopback. Se você tiver regras restritivas:

- **Permitir entrada em 11434:** apenas se o Ollama estiver vinculado a `0.0.0.0` e você quiser regra explícita.
- **Permitir saída para 127.0.0.1:** normalmente já permitida por padrão.

Não é necessário criar regra especial só para “VS Code → localhost:11434” a menos que você tenha bloqueado tudo e esteja liberando exceções.

### 4.2 Bloquear saída para servidores de telemetria (porta 443)

A abordagem mais prática é **não bloquear toda a porta 443** para o editor (senão quebra atualizações, extensões, Git, etc.), e sim:

1. **Bloquear por nome de host:** usar o arquivo **hosts** (script da seção 3) para que os domínios de telemetria resolvam para `0.0.0.0`. Assim, mesmo que o processo tente conexão HTTPS (443), o destino será inválido.
2. **Opcional – regras de Firewall por processo:**  
   Se quiser bloquear **por destino** (IP), seria necessário manter uma lista de IPs de telemetria (que mudam) e criar regras “Block outbound” para o executável do Cursor/VS Code. Isso é avançado e de manutenção custosa; o bloqueio via **hosts** é mais simples e eficaz.

**Exemplo conceitual (apenas se você tiver lista de IPs):**

- Abrir **Windows Defender Firewall with Advanced Security**.
- **Outbound Rules** → New Rule → Custom → Program: `%LOCALAPPDATA%\Programs\cursor\Cursor.exe` (ou o caminho do `Code.exe`).
- Scope: Remote IP addresses = lista dos IPs de telemetria (não recomendado como única medida).
- Action: Block.

Recomendação: **rely no hosts + telemetry desligada no settings**; use firewall apenas se precisar de política extra (ex.: rede corporativa).

### 4.3 Resumo firewall

| Ação | Como |
|------|------|
| Ollama (localhost:11434) | Já permitido em loopback; sem regra extra na maioria dos casos. |
| Telemetria (443) | Bloquear domínios via **hosts** (script). Opcional: regras de bloqueio por IP se tiver lista estável. |
| Não bloquear 443 globalmente para o editor | Evita quebrar atualizações, extensões e Git. |

---

## 5. Checklist rápido — NOTEBOOK_TEO

- [ ] `telemetry.telemetryLevel`: `"off"` e `telemetry.enableCrashReporter`: `false` em `settings.json`.
- [ ] Cursor: **Privacy Mode** ativado em Settings > General.
- [ ] Extensões: telemetria desligada (Red Hat, GitLens, Docker, etc.); evitar extensões “AI” em nuvem em projeto Cara Core.
- [ ] Script `block-telemetry-hosts.ps1` executado **como Administrador**; `ipconfig /flushdns` após.
- [ ] Ollama em `localhost:11434` para uso de modelos locais sem vazamento.
- [ ] Opcional: `update.mode`: `"none"` e desativar auto-update de extensões se quiser mínimo tráfego.

---

*Soberania do Código — Cara Core Informática. Nada sai do NOTEBOOK_TEO sem sua permissão expressa.*
