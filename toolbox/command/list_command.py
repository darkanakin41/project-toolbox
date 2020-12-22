import os
import time
from datetime import datetime

import click
from prettytable import PrettyTable

from toolbox.command.abstract.command import Command
from toolbox.config import config, project_type_names


class ListCommand(Command):
    """
    List command
    """

    def __init__(self):
        super().__init__('list')
        self.help = 'List projects and status'
        self.params.append(click.Argument(['project'], required=False, default=None))
        self.params.append(click.Option(['--type'],
                                        required=False,
                                        type=click.Choice(project_type_names()),
                                        help='Display only given type'))
        self.params.append(click.Option(['--all'], default=False, is_flag=True, help='Display all projects'))
        self.params.append(click.Option(['--watch'], default=False, is_flag=True, help='Watch mode'))

    def _display(self, projects: list, all: bool):
        """
        Display projects
        :param projects: the list of projects
        :param all: filter only on active projects
        :return: void
        """
        table = PrettyTable(['Project', 'Type', 'Mutagen Active'])
        table.align["Project"] = "l"
        table.align["Mutagen Active"] = "l"
        for p in projects:
            status = p.get_mutagen_status()
            if all or len(status) > 0:
                table.add_row([p.name, p.type.name, p.get_mutagen_status()])
        table.title = 'Project Toolbox - ' + datetime.today().ctime()
        os.system('cls')
        print(table)

    def invoke(self, ctx: click.Context):
        project: str = ctx.params.get('project')
        project_type: str = ctx.params.get('type')
        all: bool = ctx.params.get('all')
        watch: bool = ctx.params.get('watch')

        ListCommand.validate_project_type(project_type)
        projects_type = map(lambda pt: pt[1], config.get('project_type').items())
        if project_type is not None:
            project_type_config = config.get('project_type').get(project_type)
            projects_type = [project_type_config]

        all_projects = []
        for pt in projects_type:
            all_projects += pt.get_projects()
        all_projects.sort(key=lambda x: x.type.name + x.name)

        if project is not None:
            all_projects = [p for p in all_projects if project == p.name]

        if watch:
            while True:
                for t in projects_type:
                    t.refresh_mutagen_entries()
                self._display(projects=all_projects, all=all)
                time.sleep(10)
        else:
            self._display(projects=all_projects, all=all)


command = ListCommand()
