class Error():
    def __init__(self,id_func,type_error,case=None) -> None:
        self.case = case
        dic_type = {143509:{'len<1':self.move_file_len_low}}
        dic_type[id_func][type_error]()
        pass
    
    ###################################
    ## Erros from function move_file ##
    ###################################
    def move_file_len_low(self):
        print("ERROR")
        print("the code expected to receive a list with one or more items and the key dest, but received a list with just one element that can not be specified")
        print(f'the element is: {self.case}')