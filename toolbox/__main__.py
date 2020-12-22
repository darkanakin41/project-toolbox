import os

from click import Group

plugin_folder = os.path.join(os.path.dirname(__file__), 'command')


class MainCommands(Group):
    """
    List of main commands
    """

    # def __init__(self, **attrs):
    #     super().__init__(**attrs)
    #     self.params.append(Option(['-v', '--verbose'],
    #                               default=False,
    #                               is_flag=True,
    #                               help='Add more output'))
    #     self.params.append(Option(['-s', '--silent'],
    #                               default=False,
    #                               is_flag=True,
    #                               help='Not output at all'))

    # def invoke(self, ctx: Context):
    #     if not ctx.params.get('silent'):
    #         print('Silent mode is off')
    #         root = logging.getLogger()
    #         if ctx.params.get('verbose'):
    #             print('Verbose mode is on')
    #             root.setLevel(logging.DEBUG)
    #         else:
    #             print('Verbose mode is off')
    #             root.setLevel(logging.INFO)
    #
    #         handler = logging.StreamHandler(sys.stdout)
    #         handler.setLevel(logging.DEBUG)
    #         formatter = logging.Formatter('[%(levelname)s] %(message)s')
    #         handler.setFormatter(formatter)
    #         root.addHandler(handler)

    def list_commands(self, ctx):
        return ['create', 'start', 'stop', 'list']

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(plugin_folder, name + '_command.py')
        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)
        return ns['command']


main = MainCommands()

if __name__ == '__main__':
    main()
