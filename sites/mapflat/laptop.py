import re

from stuffer import apt
from stuffer import content
from stuffer import debconf
from stuffer import files
from stuffer import pip
from stuffer import system
from stuffer import user
from stuffer import utils
from stuffer.contrib import java
from stuffer.contrib import jetbrains


# Does not work yet. Need to figure out a reuse model.
# from sites.mapflat import development


apt.KeyAdd("https://packages.cloud.google.com/apt/doc/apt-key.gpg")
apt.Install('lsb-release')
apt.SourceList('google-cloud-sdk',
               content.OutputOf('echo "deb http://packages.cloud.google.com/apt cloud-sdk-$(lsb_release -c -s) main"',
                                shell=True))

apt.KeyRecv("hkp://keyserver.ubuntu.com:80", "BBEBDCB318AD50EC6865090613B00F1FD2C19886")
apt.SourceList("spotify", "deb http://repository.spotify.com stable non-free")

apt.KeyAdd("https://dl.google.com/linux/linux_signing_key.pub")
apt.SourceList("google-chrome", "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main")

apt.KeyRecv('pgp.mit.edu', '5044912E')
apt.SourceList('dropbox',
               content.OutputOf('echo "deb http://linux.dropbox.com/ubuntu/ $(lsb_release -c -s) main"',
                                shell=True))

# Used to work, but no more?
# apt.SourceList("samsung", "deb http://www.bchemnet.com/suldr/ debian extra")
# apt.KeyAdd("http://www.bchemnet.com/suldr/suldr.gpg")

apt.Install(["apt-transport-https", "ca-certificates"])
apt.KeyRecv("hkp://p80.pool.sks-keyservers.net:80", "58118E89F3A912897C070ADBF76221572C52609D")
apt.SourceList("docker",
               content.OutputOf('echo "deb https://apt.dockerproject.org/repo ubuntu-$(lsb_release -c -s) main"',
                                shell=True))

apt.KeyAdd("https://download.01.org/gfx/RPM-GPG-KEY-ilg-3")

apt.KeyRecv("hkp://keyserver.ubuntu.com:80", "642AC823")
apt.SourceList("sbt", "deb https://dl.bintray.com/sbt/debian /")

apt.Install('google-chrome-stable')
apt.Install('libnss3-tools')

apt.Install(['emacs24'])

apt.Install('dropbox')

java.Jdk(8)

apt.Install('python3')
apt.Install("python3-pip")
pip.Install('pip', upgrade=True)
apt.Purge('python3-pip')

files.Content("/etc/resolvconf/resolv.conf.d/tail", "nameserver 8.8.8.8\n")

# For gsutil
apt.Install(['libffi-dev', 'libssl-dev'])
pip.Install('cryptography')

apt.Install("google-cloud-sdk")

# Development
apt.Install('git-core')
apt.Install("gradle")
apt.Install('groovy2')
apt.Install("jq")
apt.Install('kdiff3')
apt.Install('maven')
apt.Install('mercurial')
apt.Install('mysql-client')
apt.Install('pylint3')
apt.Install('python3-doc')
apt.Install('python3-mysqldb')
apt.Install('python3-venv')
pip.Install("restview")
apt.Install('ruby')
apt.Install("sbt")
apt.Install('scala')
apt.Install('scala-doc')
apt.Install('subversion')
apt.Install("tox")

apt.Install('docker.io')
user.AddToGroup(system.real_user(), 'docker')

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

pip.Install("awscli")

debconf.SetSelections('ttf-mscorefonts-installer', 'msttcorefonts/accepted-mscorefonts-eula',
                      'select', 'true')

apt.Install('ubuntu-session')

debconf.SetSelections('lightdm', 'shared/default-x-display-manager', 'select', 'sddm')
debconf.SetSelections('sddm', 'shared/default-x-display-manager', 'select', 'sddm')

# https://bugs.launchpad.net/ubuntu/+source/kaccounts-providers/+bug/1488909
system.ShellCommand("dpkg --remove account-plugin-google unity-scope-gdrive")
apt.Install("kubuntu-desktop")
apt.Install("konqueror")
debconf.SetSelections('ttf-mscorefonts-installer', 'msttcorefonts/accepted-mscorefonts-eula', 'select', 'true')
apt.Install('kubuntu-restricted-extras')

apt.Install('aspell-sv')
apt.Install('graphviz')
apt.Install('hugo')
apt.Install("pandoc")
apt.Install('ttf-xfree86-nonfree')
apt.Install("xclip")

apt.Install('gphoto2')
apt.Install('pinta')

apt.Install('kaffeine')
apt.Install(['mplayer', 'mplayer-skins', 'mplayer-fonts', 'smplayer'])

# apt.Install('skype')
# apt.Install('xpra=0.14.35-1')

apt.Install("spotify-client")

# development.DebugTools()
# development.NetDebugTools()
apt.Install("acpi")
apt.Install(['gkrellm', 'gkrelltop'])
apt.Install("htop")
apt.Install('httrack')
apt.Install("libmbim-utils")
apt.Install('lsof')
apt.Install('strace')
apt.Install('tree')

debconf.SetSelections('debconf', 'wireshark-common/install-setuid', 'select', 'true')
apt.Install('wireshark')
user.AddToGroup(system.real_user(), "wireshark")

# Needed for Intel graphics installer
apt.Install("ttf-ancient-fonts")

files.Transform("/usr/share/lightdm/lightdm.conf.d/50-ubuntu.conf",
                lambda c: re.sub(r"user-session=.*", "user-session=kde-plasma", c))

idea = jetbrains.IntelliJ("2016.1", "145")
files.Chown(system.real_user(), utils.DeferStr(idea.path), group=system.real_user(), recursive=True)

apt.Purge('thunderbird')
