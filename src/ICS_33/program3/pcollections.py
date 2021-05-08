import re, traceback, keyword

def pnamedtuple(type_name, field_names, mutable = False,  defaults =  {}):
    def show_listing(s):
        for ln_number, text_of_ln in enumerate(s.split('\n'),1):     
            print(f' {ln_number: >3} {text_of_ln.rstrip()}')

    # put your code here
    # bind class_definition (used below) to the string constructed for the class



    # Debugging aid: uncomment show_listing here so always display source code
    # show_listing(class_definition)
    
    # Execute class_definition's str inside name_space; followed by binding the
    #   attribute source_code to the class_definition; after the try/except then
    #   return the created class object; if any syntax errors occur, show the
    #   listing of the class and also show the error in the except clause
    name_space = dict( __name__ = f'pnamedtuple_{type_name}' )              
    try:
        exec(class_definition,name_space)
        name_space[type_name].source_code = class_definition
    except (TypeError,SyntaxError):                  
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]


    
if __name__ == '__main__':
    # Test simple pnamedtuple below in script: Point=pnamedtuple('Point','x,y')

    #driver tests
    import driver  
    driver.default_file_name = 'bscp3S21.txt'
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
