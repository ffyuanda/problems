import goody


def read_fa(file : open) -> {str:{str:str}}:
    pass


def fa_as_str(fa : {str:{str:str}}) -> str:
    pass

    
def process(fa : {str:{str:str}}, state : str, inputs : [str]) -> [None]:
    pass


def interpret(fa_result : [None]) -> str:
    pass




if __name__ == '__main__':
    # Write script here
              
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc3.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
