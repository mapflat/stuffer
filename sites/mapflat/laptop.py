from stuffer import apt
from stuffer import pip

apt.Install("tox")

apt.Install("konqueror")

apt.Install("htop")
apt.Install("acpi")

# Needed for Intel graphics installer
apt.Install("ttf-ancient-fonts")

apt.KeyAdd("https://download.01.org/gfx/RPM-GPG-KEY-ilg-3")

# wget --no-check-certificate https://download.01.org/gfx/RPM-GPG-KEY-ilg-3 -O - | \
# sudo apt-key add -

# Create an environment variable for the correct distribution
#export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"

# Add the Cloud SDK distribution URI as a package source
#echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee /etc/apt/sources.list.d/google-cloud-sdk.list

# Import the Google Cloud public key
#curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

# Update and install the Cloud SDK
#sudo apt-get update && sudo apt-get install google-cloud-sdk

# For gsutil
apt.Install(['libffi-dev', 'libssl-dev'])
pip.Install('cryptography')


# Development
apt.Install("python3-pip")

pip.Install("awscli")

pip.Install("restview")


# sed s/user-session=.*/user-session=kde-plasma/g /usr/share/lightdm/lightdm.conf.d/50-ubuntu.conf

# Download IntelliJ


# Spotify

apt.Install("strongswan-ike")
apt.Install("strongswan-plugin-xauth-generic")
 
