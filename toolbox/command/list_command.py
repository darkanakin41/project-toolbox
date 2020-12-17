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
        only_active: bool = kwargs.get('only_active')
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
                self._display(projects=all_projects, only_active=only_active)
                time.sleep(10)
        else:
            self._display(projects=all_projects, only_active=only_active)

    def _display(self, projects: list, only_active: bool):
        """
        Display projects
        :param projects: the list of projects
        :param only_active: filter only on active projects
        :return: void
        """
        table = PrettyTable(['Project', 'Type', 'Mutagen Active'])
        table.align["Project"] = "l"
        table.align["Mutagen Active"] = "l"
        for p in projects:
            status = p.get_mutagen_status()
            if not only_active or len(status) > 0:
                table.add_row([p.name, p.type.name, p.get_mutagen_status()])
        table.title = 'Project Toolbox - ' + datetime.today().ctime()
        os.system('cls')
        print(table)
