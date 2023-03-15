class Error():
    '''
    move_files -> 143510
    move_file  -> 143509
    '''
    def __init__(self,id_func,type_error,case=None) -> None:
        self.case = case
        dic_type = {143510:{'len<1':self.move_file_len_low},
                    143509:{'folder_not_file' :  self.not_file,}
                    }
        dic_type[id_func][type_error]()
        pass
    
    ###################################
    ## Erros from function move_file ##
    ###################################
    def not_file(self):
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