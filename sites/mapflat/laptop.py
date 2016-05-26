import re

from stuffer import apt
from stuffer import content
from stuffer import debconf
from stuffer import files
from stuffer import pip


apt.Install('lsb-release')
apt.SourceList('google-cloud-sdk',
               content.OutputOf('echo "deb http://packages.cloud.google.com/apt cloud-sdk-$(lsb_release -c -s) main"',
                                shell=True), update=False)

apt.KeyAdd("https://packages.cloud.google.com/apt/doc/apt-key.gpg")

# For gsutil
apt.Install(['libffi-dev', 'libssl-dev'])
pip.Install('cryptography')

apt.Install("google-cloud-sdk")

apt.Install("tox")

debconf.SetSelections('ttf-mscorefonts-installer', 'msttcorefonts/accepted-mscorefonts-eula',
                      'true')

apt.Install("kubuntu-desktop")

apt.Install('ubuntu-session')

apt.Install("konqueror")

apt.Install("htop")
apt.Install("acpi")

# Needed for Intel graphics installer
apt.Install("ttf-ancient-fonts")

apt.KeyAdd("https://download.01.org/gfx/RPM-GPG-KEY-ilg-3")

# Development
apt.Install("python3-pip")

pip.Install("awscli")
apt.Install("jq")
pip.Install("restview")

files.Transform("/usr/share/lightdm/lightdm.conf.d/50-ubuntu.conf",
                lambda c: re.sub(r"user-session=.*", "user-session=kde-plasma", c))

# Download IntelliJ


# Spotify

apt.Install("strongswan-ike")
apt.Install("strongswan-plugin-xauth-generic")
