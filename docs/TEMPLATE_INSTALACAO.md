# [NomeProduto] - Instalacao (Windows)

Arquivos desta entrega:
- [Executavel].exe
- checksum.sha256
- checksum.md5
- INSTALACAO.md (este arquivo)

## Validacao de integridade

No PowerShell, na pasta de artefatos:

```powershell
Get-FileHash -Path .\[Executavel].exe -Algorithm SHA256
Get-FileHash -Path .\[Executavel].exe -Algorithm MD5
```

Compare os valores com os arquivos `checksum.sha256` e `checksum.md5`.

## Requisitos

- Windows 10 ou superior (64 bits)
- [Requisitos extras, ex: 4 GB RAM, 500 MB de espaço livre]
- Conexao com internet: [sim / nao / somente ativacao]

## Execucao

1. Execute `[Executavel].exe` como usuario local do Windows.
2. Conclua o assistente de instalacao (nao requer privilegio de administrador para apps standalone).
3. [Instrucao de acesso, ex: abra o navegador em localhost:8080 / clique no atalho criado]

[Login de degustacao, se aplicavel:]
- usuario: [usuario_padrao]
- senha: [senha_padrao]

## Desinstalacao

[Instrucoes de remocao, ex: Painel de Controle > Programas > desinstalar [NomeProduto] / excluir pasta de instalacao]

## Canal oficial

- Pagina de download: [../download.html ou URL pública]
- Licenca: [LICENCA.txt ou URL da licenca]
- Suporte: [email ou URL de suporte]

---

> Versao: [versao], Lancamento: [data]
> Cara Core Informatica — https://caracore.com.br
