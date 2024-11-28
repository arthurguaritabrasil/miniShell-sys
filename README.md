# **MiniShell**

Bem-vindo ao **MiniShell**, um sistema minimalista e intuitivo para gerenciamento de arquivos e diretórios. 

---

## **Comandos Disponíveis**

| Comando               | Descrição                                                                 |
|-----------------------|---------------------------------------------------------------------------|
| `listar [diretorio]` ou somente `listar`  | Lista os arquivos e pastas no diretório especificado ou no diretório atual. |
| `criar arquivo <nome>`| Cria um novo arquivo no diretório atual.                                  |
| `criar diretorio <nome>` | Cria um novo diretório no diretório atual.                             |
| `apagar arquivo <nome>`| Exclui o arquivo especificado.                                           |
| `apagar diretorio <nome> --force` | Remove o diretório especificado, mesmo se não estiver vazio (com `--force`). |
| `cd <diretorio>`      | Muda para o diretório especificado.
| `apagar diretorio <nome>` | Apaga o diretório especificado. Ele deve estar vazio.
| `exit` ou `sair`      | Sai do MiniShell.                                                        |
| `clear` ou `cls`      | Limpa a tela do console.  

---

## **Regras de Negócio**

1. **Segurança de Usuário**  
   - Usuários só podem manipular seus próprios arquivos e diretórios.  
   - Tentativas de acessar ou modificar dados de outros usuários resultam em erros.

2. **Identificação do Processo**  
   - Sempre que um comando for executado, o PID do processo será exibido para controle e auditoria.

3. **Metadados**  
   - Arquivos e diretórios possuem metadados (como dono, permissões e caminho) armazenados em arquivos `.meta`.

4. **Permissões Restritas**  
   - Apenas o dono pode modificar ou apagar arquivos e diretórios.  

---