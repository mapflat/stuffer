from stuffer import apt
from stuffer import files
from stuffer import system
from stuffer import utils
from stuffer.contrib import jetbrains


apt.Install('charon-cmd')
apt.Install('expect')
apt.Install(["strongswan-ike", "strongswan-starter"])
apt.Install("strongswan-plugin-xauth-generic")
apt.Install("strongswan-plugin-xauth-noauth")
apt.Install("strongswan-plugin-xauth-pam")

idea = jetbrains.IntelliJ("2016.1.4", "145", variant="IU")
files.Chown(system.real_user(), utils.DeferStr(idea.path), group=system.real_user(), recursive=True)

apt.Install('libgeoip-dev')
apt.Install('python-dev')
apt.Install('python-lxml')
apt.Install(['postgresql-common', 'postgresql-server-dev-9.5'])
