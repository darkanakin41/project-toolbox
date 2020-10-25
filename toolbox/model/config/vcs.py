class Vcs:
    """
    VCS Configuration
    """

    def __init__(self, name: str, base_url: str, user: str = None, password: str = None, token: str = None):
        self.name = name
        self.base_url = base_url
        self.user = user
        self.password = password
        self.token = token
