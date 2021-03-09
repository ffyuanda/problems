from color import bcolors
color_mode = bcolors()


def print_ok(msg: str):
    print(color_mode.color_code(msg, 'ok'))


def print_error(msg: str):
    try:
        raise AssertionError(msg)
    except AssertionError as e:
        print(color_mode.color_code(e, 'error'))


def print_warning(msg: str):
    print(color_mode.color_code(msg, 'warning'))


if __name__ == '__main__':
    print_error('something')
    print_ok('something')
    print_warning('something')
