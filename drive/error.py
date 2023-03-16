class Error():
    '''
    move_files -> 143510
    move_file  -> 143509

    upload_file -> 602316
    '''
    def __init__(self,id_func,type_error,case=None) -> None:
        self.case = case
        dic_type = {143510:{'len<1':self.move_file_len_low,
                            'folder_not_file' : self.not_file,
                            'no_file_found'   : self.not_find_file
                            },
                    143509:{'folder_not_file' : self.not_file,
                            'no_file_found'   : self.not_find_file
                            },
                    602316:{
                    }
                    
                    }
        dic_type[id_func][type_error]()
        pass
    
    ###################################
    ## Erros from function move_file ##
    ###################################
    def not_file(self):
        '''
        this error can be seeing in the functions:
        move_files -> 143510
        move_file  -> 143509
        '''
        print("ERROR")
        print("the item found was not a file")
        print(f"the mymetype of the item found is: {self.case}")

 
    ####################################
    ## Erros from function move_files ##
    ####################################
    def move_file_len_low(self):
        print("ERROR")
        print("the code expected to receive a list with one or more items and the key dest, but received a list with just one element that can not be specified")
        print(f'the element is: {self.case}')

    def not_find_file(self):
        print("ERROR")
        print("Item not find found")
        print('The code executed query function, but get no item match from google API')