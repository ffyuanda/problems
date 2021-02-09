class bcolors:
    """
    This color class is cited and modified from
    https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
    for color coded text.
    """

    def __init__(self):
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKCYAN = '\033[96m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'

    def color_code(self, string: str, ctype: str) -> str:
        """
        To return a color-coded string.
        :param string: the original string without color
        :param ctype: the type of color you want to encode
        :return: a color-coded string

        Example usage:
        color_mod = color.bcolors()
        print(color_mod.color_code("sad", 'ok'))
        """
        if ctype == 'ok':
            output = "{}{}{}".format(self.OKGREEN, string, self.ENDC)
            return output
        elif ctype == 'warning':
            output = "{}{}{}".format(self.WARNING, string, self.ENDC)
            return output
        elif ctype == 'error':
            output = "{}{}{}".format(self.FAIL, string, self.ENDC)
            return output
