**Pyvault**

install

`pip install -r requirements.txt`

utilisation

- creer un dossier "vault" dans le repertoire ou se trouve le playbook (a fixer)
puis
`python3 pyvault.py -d chemin/vers/le/dossier -f mon-playbook.yml (ou all)
`
ou -d est optionnel (si il n'y a rien il va chercher dans le repertoire ou est lance pyvault)
et -f soit le nom du playbook soit all pour crypter tous les playbook du repertoire

pour lancer le playbook

`ansible-playbook -vv -i hosts mon-playbook.yml --extra-vars="@/chemin/vers/fichier/vault' --ask-vault-pass`
