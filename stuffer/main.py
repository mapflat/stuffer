import logging

import click

from . import apt
from .core import Action


@click.command()
@click.option("--dry-run/--no-dry-run", default=False)
@click.argument("operations", nargs=-1)
def cli(dry_run, operations):
    full_command = "\n".join(operations) + "\n"
    action_namespace = {'apt': apt}
    exec full_command in action_namespace, action_namespace

    def extract_actions(action_obj):
        if isinstance(action_obj, Action):
            return [action_obj]
        return []

    actions = list(Action.registered())
    logging.info("Loaded {} actions: {}".format(len(actions), ', '.join(map(repr, actions))))
    for act in actions:
        act.execute(dry_run)
