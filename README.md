**Pyvault**

install

`pip install -r requirements.txt`

utilisation

`python3 pyvault.py -d chemin/vers/le/dossier -f mon-playbook.yml (ou all)`

pour lancer le playbook

`ansible-playbook -vv -i hosts mon-playbook.yml --extra-vars="@/chemin/vers/fichier/vault' --ask-vault-pass`
