import glob
import re
import argparse
from ansible_vault import Vault
import os
#########CONSTANTES######
VAULT_PWD = "bidules"               #vault password

MARIA_PWD = "pwd_mariadb"           #string for search and var Name
PROFTP_PWD = "pwd_proftpd"
SQL_MDP = "bdd_mdp"
FTP_MDP = "ftp_mdp"
vault = Vault(VAULT_PWD)
CWD = os.getcwd()

##########PARSER#########
parser = argparse.ArgumentParser()
parser.add_argument('-f','--file', dest="filename")
parser.add_argument('-d','--directory', dest="directory")
args = parser.parse_args()

if args.directory:
    CWD = args.directory
    if args.filename == "all":
        YML_FILES = glob.glob(args.directory+"/"+"*.yml")
    else:
        YML_FILES = [str(args.directory+"/"+args.filename)]
else:
    if args.filename == "all":
        YML_FILES = glob.glob("*.yml")
    else:
        YML_FILES = [args.filename]

#########le prog le vrai#######
for files in YML_FILES:
    VaultName = files.split(".yml")
    VaultName = str(VaultName[0])
    VaultName = VaultName.split("/")
    VaultName = str(VaultName[-1])
    with open(files, "r") as search:
        data = search.readlines()
    vault_text = ": !vault |\n          $ANSIBLE_VAULT;1.1;AES256\n          "
    VAR_NAME = ""
    C_COUNT = 0
    C_MARIA = 0
    C_PROFTP = 0
    C_SQL = 0
    C_FTP = 0
    vault_file = ""
    for line in data:
        if re.match("(.*)pwd_mariadb(.*)", line):
            C_MARIA += 1
            Raw_Pwd_Line = line.split(":")
            PWD_CLEAN = Raw_Pwd_Line[-1].strip()
            MDP_VAULT = vault.dump_raw(PWD_CLEAN)
            VAR_NAME = MARIA_PWD
            # C_COUNT = C_MARIA
            MDP_VAULT = MDP_VAULT.decode("ASCII")
            MDP_VAULT_CLEAN = MDP_VAULT.split("\n")
            MDP_VAULT_CLEAN = "".join(MDP_VAULT_CLEAN[1:])
            MDP_VAULT= MDP_VAULT_CLEAN
            INDEX = data.index(line)
            C_COUNT +=1
            data[INDEX] = line.replace(PWD_CLEAN,"\"{{"+VAR_NAME+str(C_COUNT)+"}}\"")
            vault_file += (VAR_NAME+str(C_COUNT)+vault_text+MDP_VAULT+"\n")
        if re.match("(.*)pwd_proftpd(.*)", line):
            C_PROFTP += 1
            Raw_Pwd_Line = line.split(":")
            PWD_CLEAN = Raw_Pwd_Line[-1].strip()
            MDP_VAULT = vault.dump_raw(PWD_CLEAN)
            MDP_VAULT = MDP_VAULT.decode("utf-8")
            MDP_VAULT_CLEAN = MDP_VAULT.split("\n")
            MDP_VAULT_CLEAN = "".join(MDP_VAULT_CLEAN[1:])
            MDP_VAULT= MDP_VAULT_CLEAN
            VAR_NAME = PROFTP_PWD
            # C_COUNT = C_PROFTP
            INDEX = data.index(line)
            C_COUNT += 1
            data[INDEX] = line.replace(PWD_CLEAN,"\"{{"+VAR_NAME+str(C_COUNT)+"}}\"")
            vault_file += (VAR_NAME+str(C_COUNT)+vault_text+MDP_VAULT+"\n")
        if re.match("(.*)bdd_mdp(.*)", line):
            C_SQL += 1
            Raw_Pwd_Line = line.split(":")
            PWD_CLEAN = Raw_Pwd_Line[-1].strip()
            MDP_VAULT = vault.dump_raw(PWD_CLEAN)
            MDP_VAULT = MDP_VAULT.decode("utf-8")
            MDP_VAULT_CLEAN = MDP_VAULT.split("\n")
            MDP_VAULT_CLEAN = "".join(MDP_VAULT_CLEAN[1:])
            MDP_VAULT= MDP_VAULT_CLEAN
            VAR_NAME = SQL_MDP
            # C_COUNT = C_SQL
            C_COUNT += 1
            INDEX = data.index(line)
            data[INDEX] = line.replace(PWD_CLEAN,"\"{{"+VAR_NAME+str(C_COUNT)+"}}\"")
            vault_file += (VAR_NAME+str(C_COUNT)+vault_text+MDP_VAULT+"\n")
        if re.match("(.*)ftp_mdp(.*)", line):
            C_FTP += 1
            Raw_Pwd_Line = line.split(":")
            PWD_CLEAN = Raw_Pwd_Line[-1].strip()
            MDP_VAULT = vault.dump_raw(PWD_CLEAN)
            MDP_VAULT = MDP_VAULT.decode("utf-8")
            MDP_VAULT_CLEAN = MDP_VAULT.split("\n")
            MDP_VAULT_CLEAN = "".join(MDP_VAULT_CLEAN[1:])
            MDP_VAULT= MDP_VAULT_CLEAN
            VAR_NAME = FTP_MDP
            # C_COUNT = C_FTP
            C_COUNT+=1
            INDEX = data.index(line)
            data[INDEX] = line.replace(PWD_CLEAN,"\"{{"+VAR_NAME+str(C_COUNT)+"}}\"")
            vault_file += (VAR_NAME+str(C_COUNT)+vault_text+MDP_VAULT+"\n")
    clean =""
    for L in data:
        clean += L
    with open(files, "w") as search:
        search.write(clean)
    with open(CWD+"/vault/"+VaultName+"vault.yml", "w") as file_vault:
        file_vault.write(str(vault_file))
