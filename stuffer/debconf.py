from stuffer import apt
from stuffer.core import Action


class SetSelections(Action):
    def __init__(self, section, template, value):
        self.section = section
        self.template = template
        self.value = value
        super(SetSelections, self).__init__()

    def prerequisites(self):
        return [apt.Install('debconf-utils')]

    def use_shell(self):
        return True

    def command(self):
        return "echo {} {} select {} | debconf-set-selections".format(self.section, self.template, self.value)
