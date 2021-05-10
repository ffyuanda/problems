import re, traceback, keyword


def pnamedtuple(type_name, field_names, mutable = False,  defaults =  {}):
    def show_listing(s):
        for ln_number, text_of_ln in enumerate(s.split('\n'),1):     
            print(f' {ln_number: >3} {text_of_ln.rstrip()}')

    def check_name_legit(name: str) -> bool:
        """
        Check if the name is legit.
        :param name: input str
        :return: True if legit otherwise False
        """
        pattern = "^([a-zA-Z])([a-zA-Z]|[0-9]|_)*$"
        return (re.match(pattern, name) is not None) and (name not in keyword.kwlist)

    def convert_field_names(s: str or list or set) -> list:
        """
        Convert the field_names (either str or list) into a
        correctly split list.
        :param s: the field_names
        :return: a correctly split list
        """
        if type(s) == list:
            return s
        elif type(s) == str:
            s_comma_split = s.split(',')
            if len(s_comma_split) == 1:  # no commas in s
                s_space_split = s_comma_split[0].split(' ')
                s_split = [i for i in s_space_split if i != '']
                return s_split
            else:  # comma-split s
                s_split = [i.strip() for i in s_comma_split]
                return s_split
        else:
            raise SyntaxError("type_name is illegal")

    fields = convert_field_names(field_names)

    def combined_input_checker() -> None:
        try:
            if not check_name_legit(type_name):
                raise SyntaxError("type_name is illegal")
        except:
            raise SyntaxError("type_name is illegal")

        try:
            for name in fields:
                if not check_name_legit(name):
                    raise SyntaxError("type_name is illegal")
        except:
            raise SyntaxError("type_name is illegal")

    def gen_repr() -> str:
        within_brace1 = ""
        within_brace2 = ""
        for name in fields:
            within_brace1 += "{}={}{}{},".format(name, '{', name, '}')
            within_brace2 += "{}=self.{},".format(name, name)
        within_brace1 = within_brace1.rstrip(',')
        within_brace2 = within_brace2.rstrip(',')
        base_func = "def __repr__(self):\n" \
                    "        return '{type_name}({within_brace1})'.format({within_brace2})".format(type_name=type_name,
                                                                                              within_brace1=within_brace1,
                                                                                              within_brace2=within_brace2)
        return base_func

    def gen_init() -> str:
        within_brace1 = ""
        init_content = ""
        for name in fields:
            within_brace1 += "{}, ".format(name)
            init_content += "        self.{} = {}\n".format(name, name)

        within_brace1 = within_brace1.rstrip(", ")
        init_content = init_content.rstrip()
        base_func = """def __init__(self, {within_brace1}):
{init_content}""".format(within_brace1=within_brace1, init_content=init_content)
        return base_func

    def gen_get() -> str:
        base_func = ""
        for name in fields:
            base_func += "    def get_{}(self):\n" \
                         "        return self.{}\n\n".format(name, name)
        base_func = base_func.strip()
        return base_func

    def gen_getitem() -> str:
        base_func = """def __getitem__(self,index):
        if type(index) == int:
            try:
                i = self._fields[index]
                return eval('self.get_' + i + '()')
            except:
                raise IndexError("invalid index")
        elif type(index) == str:
            try:
                return eval("self.{{}}".format(index))
            except:
                raise IndexError("invalid index")
        else:
            raise IndexError("invalid index")
            """.format(str(fields))
        base_func = base_func.strip()
        return base_func

    def gen_eq() -> str:
        base_func = """def __eq__(self, other):
        if self.__class__.__name__ != other.__class__.__name__:
            return False
        for i in range(len(self._fields)):
            if self[i] != other[i]:
                return False
        return True"""
        return base_func

    def gen_asdict() -> str:
        base_func = """def _asdict(self):
        return_dict = dict()
        for field in self._fields:
            return_dict[field] = self[field]
        return return_dict"""
        return base_func

    def gen_make() -> str:
        base_func = """def _make(iterable):
        within_brace = ''
        for i in iterable:
            within_brace += str(i) + ','
        within_brace = within_brace.rstrip(',')            
        return eval('{}({{}})'.format(within_brace))""".format(type_name)
        return base_func

    def gen_replace() -> str:
        base_func = """def _replace(self, **kwargs):
        pass"""
        return base_func

    # put your code here
    # bind class_definition (used below) to the string constructed for the class
    repr_str = gen_repr()
    init_str = gen_init()
    get_str = gen_get()
    getitem = gen_getitem()
    eq = gen_eq()
    asdict = gen_asdict()
    make = gen_make()
    replace = gen_replace()

    combined_input_checker()

    class_template = """class {type_name}:
    _fields = {field_names} 
    _mutable = {mutable}

    {init_str}
    
    {repr_str}
    
    {get_str}
    
    {getitem}
    
    {eq}
    
    {asdict}
    
    {make}
    
    {replace}
"""
    class_definition = class_template.format(type_name=type_name,
                                             field_names=fields,
                                             mutable=mutable,
                                             init_str=init_str,
                                             repr_str=repr_str,
                                             get_str=get_str,
                                             getitem=getitem,
                                             eq=eq,
                                             asdict=asdict,
                                             make=make,
                                             replace=replace)
    show_listing(class_definition)

    name_space = dict( __name__ = f'pnamedtuple_{type_name}')
    try:
        exec(class_definition, name_space)
        name_space[type_name].source_code = class_definition
    except (TypeError,SyntaxError):                  
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]


if __name__ == '__main__':
    # driver tests
    Point = pnamedtuple('Point', 'x,y')
    Triple1 = pnamedtuple('Triple1', 'a b c')
    t1 = Triple1._make([1, 2, 3])
    print(t1)
    # TestPoint = pnamedtuple('TestPoint', 'x,y,z,c')
    import driver  
    driver.default_file_name = 'bscp3S21.txt'
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
