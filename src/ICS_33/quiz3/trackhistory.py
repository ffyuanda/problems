from collections import defaultdict
import re


class TrackHistory:
    def __init__(self):
        super().__setattr__("his_dict", defaultdict(list))
        super().__setattr__("pattern", "^([a-z]+)(_prev)([0-9]*?)$")

    def __setattr__(self, key, value):
        if '_prev' in key:
            raise NameError("key of attribute cannot contain \"_prev\"")
        else:
            self.his_dict[key].append(value)
            super().__setattr__(key, value)

    def __getattr__(self, name):
        m = re.match(self.pattern, name)
        if m is not None:
            real_name = m.group(1)
            if real_name not in self.his_dict.keys():
                raise NameError(real_name + " does not exist as a key")

            if m.group(3) != '':  # has an index after _prev
                ver_int = -int(m.group(3)) - 1
                try:
                    return self.his_dict[real_name][ver_int]
                except IndexError:  # the index ver_int does not exist
                    return None
            else:  # has no index after _prev
                try:
                    return self.his_dict[real_name][-2]
                except IndexError:  # the index ver_int does not exist
                    return None
        else:
            raise NameError("The format of " + name + " is not right")

    def __getitem__(self, index):
        return_dict = defaultdict(int)
        if index > 0:
            raise IndexError
        for value, versions in self.his_dict.items():
            try:
                return_dict[value] = versions[index-1]
            except IndexError:
                return_dict[value] = None
        return dict(return_dict)


if __name__ == '__main__':
    # Put in simple tests for TrackHistory before allowing driver to run
    # Debugging is easier in script code than in bsc tests

    print('Start simple testing')
    print()
    # x = TrackHistory()
    # x.six = 6
    # x.six = 5
    # x.six = 4
    # x.six = 3

    import driver
    driver.default_file_name = 'bscq32S21.txt'
#     driver.default_show_traceback=True
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
    driver.driver()
