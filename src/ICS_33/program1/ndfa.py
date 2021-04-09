import goody


def read_ndfa(file : open) -> {str:{str:{str}}}:
    pass


def ndfa_as_str(ndfa : {str:{str:{str}}}) -> str:
    pass

       
def process(ndfa : {str:{str:{str}}}, state : str, inputs : [str]) -> [None]:
    pass


def interpret(result : [None]) -> str:
    pass





if __name__ == '__main__':
    # Write script here
              
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc4.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
