from stuffer import apt
from stuffer.core import Action


class DebugTools(Action):
    def run(self):
        apt.Install(['lsof', 'strace']).execute()


class NetDebugTools(Action):
    def run(self):
        apt.Install(['bind9-host', 'dnsutils', 'iputils-ping', 'lsof', 'netcat-openbsd']).execute()

