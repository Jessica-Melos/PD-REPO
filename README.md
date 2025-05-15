Projeto destinado a automatização e controle de dados do PA.

Sinalizações referente ao erro de exibição do template change_password.html:
- Possível conflito entre a view que determina a exibição da popup com o javascript dessa página ou
- Possível erro no Javascript que exibe a popup.

Views utilizadas nessa popup:
- form_log: Ao efetuar o login, serve para determinar se a popup será exibida com base na busca pelo valor False na coluna Changed_password no banco de dados.
- change_password: É a view da popup, que autentica o e-mail do banco para saber quem está tentando logar, e seta no banco a senha nova no banco.
