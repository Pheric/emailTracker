import utils


class Account:
    def __init__(self, username, password, email):
        self.id = username
        self.salt = utils.genSalt()
        self.secret = utils.hashPasswd(password, self.salt)
        self.tracker = None
        self.email = email
