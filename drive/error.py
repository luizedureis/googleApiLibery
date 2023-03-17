class Error():
    '''
    move_files -> 143510
    move_file  -> 143509

    upload_file -> 602316
    upload_files -> 1028317

    delete_file -> 304317

    list_files -> 403317
    '''
    def __init__(self,id_func,type_error,case=None) -> None:
        self.case = case
        dic_type = {143510:{'len<1'           : self.move_file_len_low,
                            'folder_not_file' : self.not_file,
                            'no_file_found'   : self.not_find_file
                            },
                    143509:{'folder_not_file' : self.not_file,
                            'no_file_found'   : self.not_find_file
                            },
                    602316:{
                            },
                    1028317:{
                            },
                    304317:{'Del_file_error'  : self.del_error
                            },
                    403317:{'no_file_found'   : self.not_find_file}
                    }
        
        dic_type[id_func][type_error]()
        pass
    
    #####################################
    ## Error from function delete_file ##
    #####################################

    def del_error(self):
        print("ERROR")
        print("Erro to delete the file, the error can not be specified, maybe the code could not delete the file or didn't find the file")
        print(f"The fileId error was {self.case}")
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
        print(f"the mymetype of the item found is: {self.case}\n")

 
    ####################################
    ## Erros from function move_files ##
    ####################################
    def move_file_len_low(self):
        print("ERROR")
        print("the code expected to receive a list with one or more items and the key dest, but received a list with just one element that can not be specified")
        print(f'the element is: {self.case}\n')

    def not_find_file(self):
        print("ERROR")
        print("Item not find found")
        print('The code executed query function, but get no item match from google API\n')