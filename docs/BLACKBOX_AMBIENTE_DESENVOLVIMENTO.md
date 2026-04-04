# Ambiente de Desenvolvimento Black-Box

Objetivo: garantir que codigo, dados e telemetria do ambiente de desenvolvimento nao saiam do equipamento sem autorizacao explicita.

## 1. Configuracao obrigatoria de telemetria

Arquivos de configuracao:

- Cursor: `%APPDATA%\Cursor\User\settings.json`
- VS Code: `%APPDATA%\Code\User\settings.json`

Chaves recomendadas:

| Chave | Valor | Finalidade |
|---|---|---|
| `telemetry.telemetryLevel` | `"off"` | Desativa telemetria de uso e eventos |
| `telemetry.enableCrashReporter` | `false` | Desativa envio de relatorios de falha |
| `enable-crash-reporter` | `false` | Redundancia de seguranca para crash reporter |
| `update.mode` | `"none"` | Opcional: desativa busca automatica de atualizacoes |
| `extensions.autoCheckUpdates` | `false` | Opcional: desativa verificacao automatica de extensoes |
| `extensions.autoUpdate` | `false` | Opcional: desativa atualizacao automatica de extensoes |

Exemplo minimo:

```json
{
  "telemetry.telemetryLevel": "off",
  "telemetry.enableCrashReporter": false,
  "enable-crash-reporter": false
}
```

No Cursor, ativar tambem o modo de privacidade nas configuracoes gerais.

## 2. Politica para extensoes

Diretriz: minimizar extensoes com envio de dados para nuvem em workspaces sensiveis.

| Grupo de extensao | Acao recomendada |
|---|---|
| Assistentes de codigo em nuvem | Desativar em repositorios sensiveis |
| Ferramentas com telemetria propria | Desativar telemetria por configuracao da extensao |
| Integracoes de cloud providers | Usar apenas quando necessario no escopo da tarefa |

Checklist de revisao:

1. Revisar configuracoes de privacidade de cada extensao instalada.
2. Desativar telemetria por extensao quando houver chave dedicada.
3. Manter somente extensoes estritamente necessarias para o fluxo operacional.

## 3. Bloqueio de dominios por hosts

Script oficial do repositorio:

- `python/block-telemetry-hosts.py`

Uso:

```powershell
python python/block-telemetry-hosts.py
```

Simulacao sem alteracao de arquivo:

```powershell
python python/block-telemetry-hosts.py --dry-run
```

Apos alteracao efetiva do hosts:

```powershell
ipconfig /flushdns
```

## 4. Firewall e endpoint local de modelo

Diretrizes:

1. Priorizar uso de endpoint local de modelo em `localhost:11434`.
2. Evitar bloqueio global de HTTPS no editor para nao interromper Git, dependencias e servicos necessarios.
3. Preferir bloqueio por hosts para dominios de telemetria.
4. Regras de firewall por processo/IP devem ser usadas apenas com inventario de destinos validado e mantido.

## 5. Checklist de conformidade do ambiente

- [ ] Telemetria do editor desativada.
- [ ] Relatorio de falhas desativado.
- [ ] Modo de privacidade do Cursor ativado.
- [ ] Politica de extensoes revisada.
- [ ] Bloqueio de hosts aplicado quando exigido.
- [ ] Endpoint local de modelo validado para operacao offline.

## 6. Regra operacional

Sem aprovacao explicita, nao utilizar configuracao que permita envio de codigo proprietario para servicos externos.
