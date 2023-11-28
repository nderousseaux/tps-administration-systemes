import pandas as pd
import hashlib

def hash_password(pswd):
	# On hash le mot de passe
	hash = hashlib.sha1(pswd.encode('utf-8'))
	return "{SSHA}" + hash.hexdigest()

# On ouvre le fichier cvs
df = pd.read_csv('usr.csv', sep=';')

# On crée un fichier ldif
fichier = open("usr.ldif", "w")n
# Pour chaque ligne de notre df
for i in range(len(df)):
	str = f"""
dn: cn={df.loc[i, "Login"]},ou=Group,dc=example,dc=com
cn: {df.loc[i, "Login"]}
objectclass: posixGroup
objectclass: top
gidnumber: {1000 + i}

dn: uid={df.loc[i, "Login"]},ou=People,dc=example,dc=com
objectclass: top
objectclass: inetOrgPerson
objectclass: person
objectclass: organizationalPerson
objectclass: posixAccount
objectclass: shadowAccount
cn: {df.loc[i, "Firstname"]} {df.loc[i, "Name"]}
sn: {df.loc[i, "Name"]}
uid: {df.loc[i, "Login"]}
givenName: {df.loc[i, "Firstname"]}
userpassword: {hash_password(df.loc[i, "Password"])}
loginshell: /bin/bash
gidnumber: {1000 + i}
uidnumber: {1000 + i}
homeDirectory: /home/{df.loc[i, "Login"]} !
"""

	fichier.write(str)
fichier.close()