# Gate de Publicacao Antiabutre - Ecossistema Cara Core

Data base: 2026-03-15
Escopo: todos os repositorios de produto, releases e site institucional
Objetivo: impedir exposicao, captura oportunista e incoerencia comercial antes de qualquer publicacao

---

## 1. Regra de Ouro

Nenhuma publicacao segue para ambiente publico sem aprovacao completa deste gate.

Aprovacao minima:
- Seguranca: APROVADO
- Propriedade e licenca: APROVADO
- Consistencia comercial e cronograma: APROVADO
- Evidencia de integridade: APROVADO

Se qualquer item critico falhar, status final = BLOQUEADO.

---

## 2. Checklist Obrigatorio (Go/No-Go)

### A. Seguranca e Exposicao

- [ ] Zero segredo em repositorios publicos (.env real, senha, token, chave privada)
- [ ] Zero artefato sensivel em lojas/releases (logs internos, dumps, backups)
- [ ] Dependencias e CVEs com status aceitavel para release
- [ ] Regras de protecao de credenciais validadas no build/revisao

Evidencias esperadas:
- Relatorio de seguranca atualizado
- Busca por padroes sensiveis sem achados criticos

### B. Propriedade Intelectual e Licenca

- [ ] Licenca coerente com politica do produto (proprietario, free, premium)
- [ ] Copyright e aviso de uso corretos
- [ ] Nenhuma contradicao entre README, loja e documento legal

Evidencias esperadas:
- Revisao de README e LICENSE
- Verificacao cruzada com paginas de release

### C. Consistencia Comercial e Cronograma

- [ ] Data oficial de publicacao alinhada em todos os documentos oficiais
- [ ] Nome do produto, versao e proposta comercial consistentes
- [ ] Sem mensagem ambigua sobre status (beta, producao, roadmap)

Evidencias esperadas:
- Lista de arquivos oficiais revisados
- Dif consolidado de alteracoes de cronograma/comercial

### D. Saude Tecnica

- [ ] Build principal sem erro bloqueante
- [ ] Suite de testes em nivel aceitavel para release
- [ ] Sem regressao funcional critica conhecida

Evidencias esperadas:
- Log de build/test
- Sumario de riscos tecnicos

### E. Integridade e Rastreabilidade

- [ ] Commit unico de release com mensagem clara
- [ ] Tag de checkpoint de seguranca criada e publicada
- [ ] Manifesto/hash dos arquivos criticos anexado
- [ ] Registro de aprovacao final (quem aprovou, quando, escopo)

Evidencias esperadas:
- Commit SHA
- Tag de seguranca
- SHA256 dos arquivos oficiais

---

## 3. Matriz de Severidade (Decisao)

Critica:
- Segredo exposto
- Inconsistencia de licenca/propriedade
- Divergencia de data oficial em material de publicacao
- Falha de build/test que compromete release

Alta:
- Risco de interpretacao comercial incorreta
- Evidencia de integridade incompleta

Media:
- Warnings nao bloqueantes com plano de correcao

Baixa:
- Ajustes editoriais sem impacto legal/comercial/tecnico

Regra de decisao:
- Qualquer Critica = BLOQUEADO
- Mais de 2 Altas = BLOQUEADO
- Somente Medias/Baixas = APROVADO COM RESSALVAS

---

## 4. Ata de Aprovacao de Release

Produto:
Versao:
Data oficial de publicacao:
Responsavel tecnico:
Responsavel comercial:

Resultado do Gate:
- Seguranca: APROVADO / BLOQUEADO
- Licenca e propriedade: APROVADO / BLOQUEADO
- Consistencia cronograma/comercial: APROVADO / BLOQUEADO
- Integridade/rastreabilidade: APROVADO / BLOQUEADO

Status final: APROVADO / APROVADO COM RESSALVAS / BLOQUEADO

Pendencias (se houver):
1.
2.
3.

Evidencias anexadas:
- Commit SHA:
- Tag de seguranca:
- Manifesto/hash:
- Relatorio de seguranca:

Aprovadores:
- Tecnico:
- Produto/Comercial:
- Data/hora:

---

## 5. Cadencia Recomendada Ate 08/11/2028

- Gate completo em toda release publica
- Revisao mensal de risco do ecossistema
- Auditoria trimestral de lojas e licencas
- Simulacao de incidente semestral (segredo vazado, conflito de data, erro de release)

---

## 6. Comando de Execucao Operacional (Resumo)

1. Rodar checklist A-E.
2. Coletar evidencias minimas.
3. Classificar severidade.
4. Decidir Go/No-Go.
5. Registrar ata.
6. Publicar somente com tag de seguranca.
