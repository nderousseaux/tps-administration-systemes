# TP2 - Utilisateurs et stockage

```c
sudo qemu-system-x86_64 \
  -m 2048 \
  -M accel=hvf \
	-drive file=tp2.qcow2,media=disk,if=virtio \
  -nic vmnet-bridged,ifname=en0
```

## Cartographie, LDAP

L'ip de `SRV` est `10.0.0.2` et l'ip de `PC1` est `10.0.0.5`. 

Pour configurer correctement la résolution de nom il suffit de changer le DNS dans le fichier `/etc/resolv.conf` pour l'ip de notre serveur de nom : `10.0.0.2`. 

Pour se brancher sur le serveur ldap, la commande est `lxc-attach srv`. 

## Import des utilisateurs

 Ce script python permet de passer du CSV au LDIF :

```python
# dn: cn=jdoe,ou=Group,...
# cn: jdoe
# objectclass: posixGroup
# objectclass: top
# gidnumber: 1000

# dn: uid=jdoe,ou=People,...
# objectclass: top
# objectclass: inetOrgPerson
# objectclass: person
# objectclass: organizationalPerson
# objectclass: posixAccount
# objectclass: shadowAccount
# cn: John Doe
# sn: Doe
# uid: jdoe
# givenName: John
# userpassword: {SSHA}H/YPhEO5YT/REoiFFsoCCT6q34c+fBJp
# loginshell: /bin/bash
# gidnumber: 1000
# uidnumber: 1000
# homeDirectory: /home/jdoe !

import pandas as pd
import hashlib

def hash_password(pswd):
	# On hash le mot de passe
	hash = hashlib.sha1(pswd.encode('utf-8'))
	return "{SSHA}" + hash.hexdigest()

# On ouvre le fichier cvs
df = pd.read_csv('usr.csv', sep=';')

# On crée un fichier ldif
fichier = open("usr.ldif", "w")
# Pour chaque ligne de notre df
for i in range(len(df)):
	str = f"""
dn: cn={df.loc[i, "Login"]},ou=Group,dc=example,dc=com
cn: {df.loc[i, "Login"]}
objectclass: posixGroup
objectclass: top
gidnumber: {1000 + i}

dn: uid={df.loc[i, "Login"]},ou=People, dc=example,dc=com
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
homeDirectory: /home/{df.loc[i, "Login"]} !"""

	fichier.write(str)
fichier.close()
```

Ensuite on importe avec :

```shell
$ldapadd -H ldap://127.0.0.1 -D cn=admin,dc=example,dc=com -x -w secret1234 -f usr.ldif
```

