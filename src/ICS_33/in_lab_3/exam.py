from ile3helper  import hide, nth, nth_for_m, randoms
            

def max_skip_ties(*iterables):
    if len(iterables) == 0:
        return
    else:
        agree_list = [False] * len(iterables)  # when a slot equals True, then do not go __next__()
        value_list = [None] * len(iterables)
        while True:
            try:
                for i in range(len(iterables)):
                    if not agree_list[i]:
                        value = next(iterables[i])
                    else:
                        value = value_list[i]
                        agree_list[i] = False
                    value_list[i] = value

                max_v = max(value_list)

                if value_list.count(max_v) == 1:
                    yield max_v
                    agree_list = [False] * len(iterables)  # release all holds
                else:
                    for i, v in enumerate(value_list):
                        if v != max_v:
                            agree_list[i] = True

            except StopIteration:
                break


def can_sum_to(pool : {int}, value : int) -> bool:

    if value == 0:
        return True
    else:
        for p in pool:
            pool_copy = pool.union()
            pool_copy.remove(p)
            re1 = can_sum_to(pool_copy, value - p)
            if re1:
                return True
        return False


class sorted_dict(dict):
    def __init__(self):
        super().__init__()
        self._temporal_index = 0
        self._temporal_keys = {}

        self._sorter_key = None
        self._sorter_reverse = False

    def show_info(self):
        return f'  temporal_index/_temporal_keys = {self._temporal_index}/{self._temporal_keys}\n'\
              +f'  keys/values in dict order     = {dict.__str__(self)}'        

    def set_sorting(self,*,key = None, reverse = False):
        if key != None:
            self._sorter_key = key
        self._sorter_reverse = reverse

    def __str__(self):
        pass
                                                              
    def __setitem__(self,key,value):
        if key not in self._temporal_keys.keys():
            self._temporal_index += 1
            self._temporal_keys[key] = self._temporal_index
        super().__setitem__(key, value)
    
# By not defining __iter__ sorted_dict inherites dict's __iter__.
# Uncomment the code below when you are ready to write __iter__
# and provide a body for it; if you just write pass for its body
# it will override the inherited __iter__ but not return an object
# that next can be called on, which will break all sorts of things.
#     def __iter__(self):

                            
if __name__ == '__main__':

    print('\n\nTesting sorted_dict. Feel free to test other cases')
    print('  sd = sorted_dict(); print(sd.show_info())')
    sd = sorted_dict()
    print(sd.show_info())

    print("\n  sd['a'] = 10; print(sd.show_info())")
    sd['a'] = 10
    print(sd.show_info())
    #
    print("\n  sd['c'] = 30; print(sd.show_info())")
    sd['c'] = 30
    print(sd.show_info())
    #
    print("\n  sd['b'] = 20; print(sd.show_info())")
    sd['b'] = 20
    print(sd.show_info())
    #
    # print("\n  print(sd)")
    print(sd)
    #
    # print("\n  sd.set_sorting(key  = (lambda x : x[1]), reverse = True); print(sd)")
    # sd.set_sorting(key  = (lambda x : x[1]), reverse = True)
    # print(sd)
    #
    # print("\n  sd.set_sorting(key  = (lambda x : x[2]), reverse = False); print(sd)")
    # sd.set_sorting(key  = (lambda x : x[2]), reverse = False)
    # print(sd)
    #
    # print("\n  del sd['c']; print(sd.show_info()); print(sd)")
    # del sd['c']
    # print(sd.show_info())
    # print(sd)
    #
    # print("\n  sd['c'] = -7; print(sd.show_info()); print(sd)")
    # sd['c'] = -7
    # print(sd.show_info())
    # print(sd)
    #
    # print("\n  sd.set_sorting(key  = (lambda x : x[0])); print(sd)")
    # sd.set_sorting(key  = (lambda x : x[0]))
    # print(sd)
    
    print()
    import driver
    #Uncomment the following lines to see MORE details on exceptions
    driver.default_file_name = 'bscile3W21.txt'
    #But better to debug putting testing code above
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
    driver.driver()
