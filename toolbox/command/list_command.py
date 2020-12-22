import os
import time
from datetime import datetime

from prettytable import PrettyTable

from toolbox.command.abstract_command import AbstractCommand
from toolbox.config import config


class ListCommand(AbstractCommand):
    """
    Stop command
    """

    def exec(self, **kwargs):
        project: str = kwargs.get('project')
        project_type: str = kwargs.get('type')
        all: bool = kwargs.get('all')
        watch: bool = kwargs.get('watch')

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
