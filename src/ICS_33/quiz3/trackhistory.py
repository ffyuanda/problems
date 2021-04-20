from collections import defaultdict


class TrackHistory:
    def __init__(self):
        pass

    
    def __getattr__(self,name):
        pass


    def __getitem__(self,index):
        pass

    
#    def __setattr__(self,name,value):
#        pass





if __name__ == '__main__':
    # Put in simple tests for TrackHistory before allowing driver to run
    # Debugging is easier in script code than in bsc tests

    print('Start simple testing')
    print()
    
    import driver
    driver.default_file_name = 'bscq32S21.txt'
#     driver.default_show_traceback=True
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
    driver.driver()
