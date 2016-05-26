import re

from stuffer import apt
from stuffer import content
from stuffer import debconf
from stuffer import files
from stuffer import pip


apt.Install('lsb-release')
apt.SourceList('google-cloud-sdk',
               content.OutputOf('echo "deb http://packages.cloud.google.com/apt cloud-sdk-$(lsb_release -c -s) main"',
                                shell=True))

apt.KeyAdd("https://packages.cloud.google.com/apt/doc/apt-key.gpg")

apt.SourceList("spotify", "deb http://repository.spotify.com stable non-free")
apt.KeyRecv("hkp://keyserver.ubuntu.com:80", "BBEBDCB318AD50EC6865090613B00F1FD2C19886")

apt.SourceList("google-chrome", "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main")
apt.KeyAdd("https://dl.google.com/linux/linux_signing_key.pub")

apt.SourceList("samsung", "deb http://www.bchemnet.com/suldr/ debian extra")
apt.KeyAdd("http://www.bchemnet.com/suldr/suldr.gpg")

apt.KeyRecv("hkp://p80.pool.sks-keyservers.net:80", "58118E89F3A912897C070ADBF76221572C52609D")
apt.SourceList("docker",
               content.OutputOf('echo "deb https://apt.dockerproject.org/repo ubuntu-$(lsb_release -c -s) main"',
                                shell=True))

apt.KeyAdd("https://download.01.org/gfx/RPM-GPG-KEY-ilg-3")

apt.SourceList("sbt", "deb https://dl.bintray.com/sbt/debian /")
apt.KeyRecv("hkp://keyserver.ubuntu.com:80", "642AC823")


# For gsutil
apt.Install(['libffi-dev', 'libssl-dev'], update_first=True)
pip.Install('cryptography')

apt.Install("google-cloud-sdk")

apt.Install("tox")

# Development
apt.Install("python3-pip")

pip.Install("awscli")
apt.Install("jq")
pip.Install("restview")

debconf.SetSelections('ttf-mscorefonts-installer', 'msttcorefonts/accepted-mscorefonts-eula',
                      'true')

apt.Install('ubuntu-session')

apt.Install("kubuntu-desktop")

apt.Install("konqueror")
apt.Install("spotify-client")

apt.Install("htop")
apt.Install("acpi")

# Needed for Intel graphics installer
apt.Install("ttf-ancient-fonts")

files.Transform("/usr/share/lightdm/lightdm.conf.d/50-ubuntu.conf",
                lambda c: re.sub(r"user-session=.*", "user-session=kde-plasma", c))

# Download IntelliJ


# Spotify

apt.Install("strongswan-ike")
apt.Install("strongswan-plugin-xauth-generic")
