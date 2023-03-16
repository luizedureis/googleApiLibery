from drive.google_main import Google
from drive.error import Error
import ast

class file_sheet(Google):
    def __init__(self,*file_name) -> None:
        super().__init__()
        # puxando nome do arquivo que será substituido
        self.__file = file_name
        self.service = self.generate_service()

    def generate_service(self):
        #Keys para capturar pastas drive
        SCOPES = ['https://www.googleapis.com/auth/drive']
        CLIENT_SECRET_FILE = self.chromedriver
        API_NAME = 'drive'
        API_VERSION = 'V3'
        return self.Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)

   ####################################
   ####################################
   #### Processo de mover arquivos ####
   ####################################
   ####################################
   
    def move_file(self,
                  folder_id=str,
                  folder_target=str,
                  returnblob=False):
        '''
        To change a file to another folder first of all we need to find you file and to do 
        this the function has differents methods:
        \nFind item by name -> To find an item by name, you can use the function like this:\n
        >>> obj = file('namefile')
        >>> obj.move_file(folder_id,folder_target)\n

        The function has the method return blob, if you call this by True, the function will return the item blob in drive.
        '''
        self.__id = 143509
        # checando se realmente estamos recebendo o nome str de um arquivo
        if type(self.__file[0]) == str:
            # query para filtrar a pasta pai e o nome do arquivo target
            query = f"parents = '{folder_id}' and name = '{self.__file[0]}'"
            # localizando file, pelo correto irá retornar apenas um item
            file = self.service.files().list(q=query).execute()
            if len(file['files'])==0:
                Error(self.__id,'no_file_found')
                return
            # checando se localizamos um item e não uma pasta
            if file['files'][0]['mimeType'] == 'application/vnd.google-apps.folder':
                # se sim enviamos a mensagem de erro
                Error(self.__id,'folder_not_file',file['files']['mimeType'])
                return
            else:
                # se não podemos seguir com a modificação
                self.service.files().update(
                    fileId       = file['files'][0]['id'],
                    addParents    = folder_target,
                    removeParents = folder_id
                ).execute()
            if returnblob==True:
                return file


    def move_files(self,folder_id=None,folder_target=None,diferent_upload=False):
        '''
            For this method you can move an indeterminate number of files.
            \n
            The function operate with two diferents ways:\n
        Send more than one file to the same folder:\n
            The code receive how many files name you want, you will have to call the function like:
            >>> obj = files(file1,file2,file3)
            >>> obj.move_files(folder_id,folder_target)
            OBS: this method do not return if the code do not find any item.
        \n
        Send more than one life to diferents folders:\n
            to call this metod you will call the function like:
            >>> obj = files(file1,folder_dest1,file2,folder_dest2,file3,folder_dest3)
            >>> obj.move_files(folder_id,diferent_upload=True)
        '''
        self.__id=143510

        # se diferent upload = False consideramos que todos os arquivos vão para uma pasta em comum, então vamos considerar o folder_target como o local pradrão para subir os arquivos
        if diferent_upload==True:
            #############################################################################################################################################################################
            ## a proxima ideia para otimizar esse processo seria fazer a query puxar os itens dessa parte de uma vez só, ou seja, precisamos entrar com um dic e ralacionar os valores ##
            #############################################################################################################################################################################
            name_file=None
            for i in range(len(self.__file)):
                # puxando nome do arquivo
                if i%2==0:
                    name_file = self.__file[i]
                    continue
                
                # puxando pasta de destino
                folder_dest = self.__file[i]

                # gerando query
                query = f"parents = '{folder_id}' and name = '{name_file}'"
                file = self.service.files().list(q=query).execute()
                # checando se encontramos algum retorno
                if len(file['files'])==0:
                    Error(self.__id,'no_file_found')
                    continue
                # checando se é um file
                if file['files'][0]['mimeType'] == 'application/vnd.google-apps.folder':
                    # se sim enviamos a mensagem de erro
                    Error(self.__id,'folder_not_file',file['files']['mimeType'])
                    print(f'item {name_file} Error, doing next item or ending the function')
                else:
                    self.service.files().update(
                        fileId       = file['files'][0]['id'],
                        addParents    = folder_dest,
                        removeParents = folder_id
                    ).execute()

        elif diferent_upload==False:

            ##############################################################
            ##esse processo ñ identifica se o item foi encontrado ou nn ##
            ##############################################################
            
            query = self.create_query(folder_id)
            files = self.service.files().list(q=query).execute()
            # checando se encontramos algum retorno
            if len(files['files'])==0:
                Error(self.__id,'no_file_found')
                return
            for file in files['files']:
                # erro caso os arquivo encontrado seja uma pasta
                if file['mimeType'] == 'application/vnd.google-apps.folder':
                    # se sim enviamos a mensagem de erro
                    Error(self.__id,'folder_not_file',file['files']['mimeType'])
                    print(f'item {name_file} Error, doing next item or ending the function')
                else:
                    self.service.files().update(
                        fileId       = file['id'],
                        addParents    = folder_target,
                        removeParents = folder_id
                    ).execute()

    # criando query geral para puxar todos os itens de uma vez
    def create_query(self,folder_id):
        query = f"parents = '{folder_id}'"
        inicial=False
        for name in self.__file:
            if inicial == True:
                query = f"{query} or name = '{name}'"
            else:
                query = f"{query} and name = '{name}'"
                inicial = True
        return query
    