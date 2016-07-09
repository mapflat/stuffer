from stuffer import apt
from stuffer.contrib import jetbrains

apt.Install('charon-cmd')
apt.Install('expect')
apt.Install(["strongswan-ike", "strongswan-starter"])
apt.Install("strongswan-plugin-xauth-generic")

jetbrains.IntelliJ("2016.1.3", "145", variant="IU")

apt.Install('libgeoip-dev')
apt.Install('python-lxml')
apt.Install(['postgresql-common', 'postgresql-server-dev-9.5'])


