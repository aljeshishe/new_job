from glassdoor import constants


class State:
    def __init__(self):
        self.headers = constants.HEADERS.copy()

    def set_csrf_token(self, csrf_token):
        self.headers["gd-csrf-token"] = csrf_token

