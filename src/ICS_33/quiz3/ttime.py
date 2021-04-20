from goody import type_as_str


class Time:
    def __init__(self, hour=0, minute=0, second=0):
        if type(hour) is not int:
            raise AssertionError(self.__class__.__name__ + " hour is not of type int")
        if hour > 23 or hour < 0:
            raise AssertionError(self.__class__.__name__ + " hour out of range")
        if type(minute) is not int:
            raise AssertionError(self.__class__.__name__ + " minute is not of type int")
        if minute > 59 or minute < 0:
            raise AssertionError(self.__class__.__name__ + " minute out of range")
        if type(second) is not int:
            raise AssertionError(self.__class__.__name__ + " second is not of type int")
        if second > 59 or second < 0:
            raise AssertionError(self.__class__.__name__ + " second out of range")

        self.hour = hour
        self.minute = minute
        self.second = second

    def __getitem__(self, item):

        item_list = [self.hour, self.minute, self.second]
        if type(item) is int:
            if item not in [1, 2, 3]:
                raise IndexError(self.__class__.__name__ + " item index not valid")
            return item_list[item-1]
        elif type(item) is tuple:
            return_list = list()
            for i in item:
                if i not in [1, 2, 3]:
                    raise IndexError(self.__class__.__name__ + " item index not valid")
                return_list.append(item_list[i-1])
            return tuple(return_list)
        else:
            raise IndexError(self.__class__.__name__ + " item should be int or tuple")

    def __repr__(self):
        return "Time({},{},{})".format(self.hour, self.minute, self.second)

    def __str__(self):
        am_pm = ''
        format_hour, format_minute, format_second = 0, 0, 0
        return_str = ''
        if self.hour < 12:
            am_pm = 'am'
            if self.hour == 0:
                format_hour = 12
            else:
                format_hour = self.hour
        else:
            am_pm = 'pm'
            if self.hour == 12:
                format_hour = 12
            else:
                format_hour = self.hour - 12

        if self.minute < 10:
            format_minute = '0' + str(self.minute)
        else:
            format_minute = self.minute

        if self.second < 10:
            format_second = '0' + str(self.second)
        else:
            format_second = self.second

        return_str = '{}:{}:{}{}'.format(format_hour, format_minute, format_second, am_pm)
        return return_str

    def __bool__(self):
        return False if self.hour == 0 and self.minute == 0 and self.second == 0 else True

    def __len__(self):
        return self.hour * 3600 + self.minute * 60 + self.second

    def __eq__(self, other):
        if other.__class__.__name__ != self.__class__.__name__:
            return False
        elif other.hour != self.hour or other.minute != self.minute or other.second != self.second:
            return False
        else:
            return True

    def __lt__(self, other):
        if other.__class__.__name__ == "Time":
            if self.hour < other.hour:
                return True

            elif self.hour == other.hour and self.minute < other.minute:
                return True

            elif self.hour == other.hour and self.minute == other.minute\
                    and self.second < other.second:
                return True
            else:
                return False
        elif other.__class__.__name__ == "int":
            if len(self) < other:
                return True
            else:
                return False
        else:
            raise TypeError("NotImplemented")

    def __add__(self, other):
        return_Time = Time(self.hour, self.minute, self.second)
        if other.__class__.__name__ != "int":
            raise TypeError("NotImplemented")
        else:
            len_second = len(self) + other
            return_Time.hour = len_second // 3600
            return_Time.minute = (len_second - return_Time.hour * 3600) // 60
            return_Time.second = len_second - return_Time.hour * 3600 - return_Time.minute * 60
            return_Time.hour = return_Time.hour % 24
        return return_Time

    def __radd__(self, other):
        return self.__add__(other)


if __name__ == '__main__':
    # Put in simple tests for Time before allowing driver to run
    # Debugging is easier in script code than in bsc tests

    print('Start simple testing')
    print()

    test_Time1 = Time(13, 10, 20)
    test_Time2 = Time(13, 10, 20)
    print(test_Time1)
    # print(test_Time1 == test_Time2)
    print(str(test_Time1 + 370090))


    import driver
    driver.default_file_name = 'bscq31S21.txt'
#     driver.default_show_traceback=True
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
    driver.driver()



        
        
        
        
        
