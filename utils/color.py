class TextColors:
    def __init__(self):
        self.HEADER = "\033[95m"
        self.OKBLUE = "\033[94m"
        self.OKGREEN = "\033[92m"
        self.WARNING = "\033[93m"
        self.FAIL = "\033[91m"
        self.ENDC = "\033[0m"
        self.BOLD = "\033[1m"
        self.UNDERLINE = "\033[4m"

    def header(self, text):
        return self.HEADER + text + self.ENDC

    def blue(self, text):
        return self.OKBLUE + text + self.ENDC

    def green(self, text):
        return self.OKGREEN + text + self.ENDC

    def warning(self, text):
        return self.WARNING + text + self.ENDC

    def fail(self, text):
        return self.FAIL + text + self.ENDC

    def bold(self, text):
        return self.BOLD + text + self.ENDC

    def underline(self, text):
        return self.UNDERLINE + text + self.ENDC
