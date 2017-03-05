from stuffer import files
from stuffer import system
from stuffer import utils
from stuffer.contrib import jetbrains

idea = jetbrains.IntelliJ("2016.1.4", "145")
files.Chown(system.real_user(), utils.DeferStr(idea.path), group=system.real_user(), recursive=True)
