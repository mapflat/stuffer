import getpass
import os
import re

from stuffer import apt
from stuffer import content
from stuffer import debconf
from stuffer import files
from stuffer import pip
from stuffer import user
from stuffer.contrib import java
from stuffer.contrib import jetbrains


# Does not work yet. Need to figure out a reuse model.
# from sites.mapflat import development


apt.Install('lsb-release')
apt.SourceList('google-cloud-sdk',
               content.OutputOf('echo "deb http://packages.cloud.google.com/apt cloud-sdk-$(lsb_release -c -s) main"',
                                shell=True))

apt.KeyAdd("https://packages.cloud.google.com/apt/doc/apt-key.gpg")

apt.SourceList("spotify", "deb http://repository.spotify.com stable non-free")
apt.KeyRecv("hkp://keyserver.ubuntu.com:80", "BBEBDCB318AD50EC6865090613B00F1FD2C19886")

apt.SourceList("google-chrome", "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main")
apt.KeyAdd("https://dl.google.com/linux/linux_signing_key.pub")

# Used to work, but no more?
# apt.SourceList("samsung", "deb http://www.bchemnet.com/suldr/ debian extra")
# apt.KeyAdd("http://www.bchemnet.com/suldr/suldr.gpg")

apt.Install(["apt-transport-https", "ca-certificates"])
apt.KeyRecv("hkp://p80.pool.sks-keyservers.net:80", "58118E89F3A912897C070ADBF76221572C52609D")
apt.SourceList("docker",
               content.OutputOf('echo "deb https://apt.dockerproject.org/repo ubuntu-$(lsb_release -c -s) main"',
                                shell=True))

docker_compose = "/usr/local/bin/docker-compose"
docker_compose_version = "1.6.2"
files.DownloadFile("https://github.com/docker/compose/releases/download/{}/docker-compose-Linux-x86_64".format(
    docker_compose_version),
    docker_compose)
files.Chmod(0o755, docker_compose)
docker_compose_complete = "/etc/bash_completion.d/docker-compose"
files.DownloadFile("https://raw.githubusercontent.com/docker/compose/{}/contrib/completion/bash/docker-compose".format(
    docker_compose_version),
    docker_compose_complete)
files.Chmod(0o644, docker_compose_complete)

apt.KeyAdd("https://download.01.org/gfx/RPM-GPG-KEY-ilg-3")

apt.SourceList("sbt", "deb https://dl.bintray.com/sbt/debian /")
apt.KeyRecv("hkp://keyserver.ubuntu.com:80", "642AC823")

java.Jdk(8)

# For gsutil
apt.Install(['libffi-dev', 'libssl-dev'])
pip.Install('cryptography')

apt.Install("google-cloud-sdk")
apt.Install("gradle")
apt.Install("tox")

# Development
apt.Install("python3-pip")
apt.Install("sbt")

pip.Install("awscli")
apt.Install("jq")
pip.Install("restview")

debconf.SetSelections('ttf-mscorefonts-installer', 'msttcorefonts/accepted-mscorefonts-eula',
                      'select', 'true')

apt.Install('ubuntu-session')

apt.Install("kubuntu-desktop")
apt.Install("konqueror")
apt.Install("pandoc")
apt.Install("xclip")

apt.Install("spotify-client")

# development.DebugTools()
# development.NetDebugTools()
apt.Install("libmbim-utils")
apt.Install("htop")
apt.Install("acpi")
debconf.SetSelections('debconf', 'wireshark-common/install-setuid', 'select', 'true')
apt.Install('wireshark')
user.AddToGroup(os.environ.get('SUDO_USER', getpass.getuser()), "wireshark")

# Needed for Intel graphics installer
apt.Install("ttf-ancient-fonts")

files.Transform("/usr/share/lightdm/lightdm.conf.d/50-ubuntu.conf",
                lambda c: re.sub(r"user-session=.*", "user-session=kde-plasma", c))

jetbrains.IntelliJ("2016.1", "145")

# Spotify

apt.Install(["strongswan-ike", "strongswan-starter"])
apt.Install("strongswan-plugin-xauth-generic")
