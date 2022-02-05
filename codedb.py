
import sqlite3 as db
import hashlib
import keyring


class connection(): #conexão banco dados
    def __init__(self):
        try:
            self.conn = db.connect('passbank.db')
            self.cur = self.conn.cursor()
            print('Conexão bem sucedida')
        except Exception as e:
            print("Erro na conexão", e)

    def __enter__(self):
        return self

    def __exit__(self,exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
        return self.conn

    @property
    def cursor(self):
        return self.cur

    def commit(self):
        self.connection.commit()

    def fetchall(self):
        return self.cur.fetchall()
    
    def execute(self, sql, params=None):
        self.cur.execute(sql, params or ())

    def query(self, sql, params=None):
        self.cur.execute(sql, params or ())
        return self.fetchall()

class login(connection):
    def __init__(self):
        connection.__init__(self)
    def insert(self,botid,botuser,botsen,botgru): # Adicionar novos dados
        try:
            self.cur.execute(f"""
                    INSERT INTO login (id, usuario, senha, grupo) VALUES (?, ?, ?, ?)
                   ;""", (botid,botuser,botsen,botgru))
            self.commit()
        except Exception as e:
            print("Erro ",e, " ao atualizar o banco de dados")

    def delete(self,idele): # Deletar dados / procura pelo id
        try:
            self.cur.execute(f"""DELETE FROM login WHERE id = '{idele}'""")  
            self.commit()  
            print('Conta: ',idele,' deletada')
        except Exception as e:
            print("Erro ",e, " ao deletar no banco de dados")  

    def updateusu(self,upid, new_usu): # Editar usuario 
        try:
            self.execute(f"UPDATE login SET usuario = '{new_usu}' WHERE id= '{upid}'")  
            self.commit()
            print("Usuario alterado do id: ",upid)
        except Exception as e:
            print("Erro ",e, " ao atualizar o usuario")

    def updatesen(self,upid, new_sen): # Editar senha
        try:
            self.execute(f"UPDATE login SET senha = '{new_sen}' WHERE id= '{upid}'")  
            self.commit()
            print("Senha alterada do id: ",upid)
        except Exception as e:
            print("Erro ",e, " ao atualizar senha")

    def updategru(self,upid, new_gru): # Editar grupo
        try:
            self.execute(f"UPDATE login SET grupo = '{new_gru}' WHERE id= '{upid}'")  
            self.commit()
            print("Grupo alterado do id: ",upid)
        except Exception as e:
            print("Erro ",e, " ao atualizar o grupo")

    def procuraid(self,proid): # Pesquisa pelo id 
        apps = (self.query(f"""
                    SELECT usuario, senha,grupo FROM login WHERE id = '{proid}'
                  ;"""))
        if apps: 
            print (' Resultado da procura pelo id: ',proid)
            print('\n')
            for row in apps:
                print('USUARIO --> ',row[0])
                print(' SENHA  --> ',row[1])
                print(' GRUPO  --> ',row[2])
                print('\n')
        else: print('O id ', proid, ' não foi encontrado') 

    def procuragru(self,progru): # Pesquisa por grupo
        apps = (self.query(f"""
                    SELECT id, usuario, senha FROM login WHERE grupo = '{progru}'
                  ;"""))
        if apps: 
            print (' Resultado da procura pelo grupo: ',progru)
            print('\n')
            for row in apps:
                print('  ID    --> ',row[0])
                print('USUARIO --> ',row[1])
                print(' SENHA  --> ',row[2])
                print('\n')
        else: print('O grupo ', progru, ' não foi encontrado') 

    def main_menu(): # menu principal
        print('------------------------------')
        print('1- Inserir uma nova conta')
        print('2- Vizualizar as contas salvas')
        print('3- Pesquisar uma conta')
        print('4- Excluir uma conta')
        print('5- Editar uma conta')
        print('0- Sair')
        print('------------------------------')

    def menuzin(): #menu de edição
        print('------------------------------')
        print('1- Mudar o usuario')
        print('2- Mudar a senha')
        print('3- Mudar o grupo')
        print('4- Mudar usuario e senha')
        print('------------------------------\n')

    def continua(): # Continuar ou não a usar o banco de dados
        cc = input(' Deseja continuar? (S) (N)')
        if cc == 'S' or cc == 's':
            vano = True
        elif cc=='N' or cc=='n':
            vano =False
        return vano
        
    def clear_terminal():
        return print('\x1b[2J')


class autoriza(connection): # Intereção com o banco de dados
    def __init__(self):
            print('Bem-vindo Deus Grego')
                # Cadastro do admin pelo hash sha512 - padrão admin
            self.admin = '58b5444cf1b6253a4317fe12daff411a78bda0a95279b1d5768ebf5ca60829e78da944e8a9160a0b6d428cb213e813525a72650dac67b88879394ff624da482f'
                # Cadastro da senha pelo hash sha512 - padrão admin
            self.master = '58b5444cf1b6253a4317fe12daff411a78bda0a95279b1d5768ebf5ca60829e78da944e8a9160a0b6d428cb213e813525a72650dac67b88879394ff624da482f' 
            keyring.set_password('master', self.admin, self.master) # Armazenamento de credenciais pela biblioteca keyring
            pede_admin = input(' Admin: ')
            pede_master = input ('Senha Mestra: ')
                #Verificação em duas etapas - padrão 1
            salt = input('Verificação 2 etapas: ')
            cc = pede_admin + salt
            mm = pede_master + salt
            hm = hashlib.sha512(mm.encode())
            hashs = hm.hexdigest() # transformação do admin fornecido em hash sha512
            hc = hashlib.sha512(cc.encode())
            hashc = hc.hexdigest() # transformação da senha fornecida em hash sha512
            aa = keyring.get_password("master",hashc)

            if (aa == hashs): # Verificação de autenticidade
                connection.__init__(self)
                cont = True
                while cont == True:
                    login.main_menu()
                    xxx = input('Qual opção desejada:  ')
                    if xxx == '1': # ADD nova linha
                        login.clear_terminal()
                        print('Dados do novo cadastro')
                        botid_new = input('ID:  ')
                        botuser_new = input('Usuario:  ')
                        botsen_new = input('Senha:  ')
                        botgru_new = input('Grupo:  ')
                        login.insert(self,botid_new,botuser_new,botsen_new,botgru_new)
                        print('Banco de Dados atualizado')
                        print('\n')
                        cont = (login.continua())

                    elif xxx == '2': # Mostrar todo o banco de dados
                        login.clear_terminal()
                        apps = self.query("SELECT * FROM login")
                        for row in apps:
                            print('  ID    --> ',row[0])
                            print('USUARIO --> ',row[1])
                            print(' SENHA  --> ',row[2])
                            print(' GRUPO  --> ',row[3])
                            print('\n')
                        cont = (login.continua())

                    elif xxx== '3': #Pesquisar dentro do banco de dados
                        login.clear_terminal()
                        tipo = input('Pesquisa por id ou grupo?  ')
                        if tipo == 'id': # procura por id
                            ser_id = input('Qual id que procuras? ')
                            login.clear_terminal()
                            login.procuraid(self,ser_id)
                        else: # procura pelo grupo
                            ser_gru = input('Qual grupo que procuras? ')
                            login.clear_terminal()
                            login.procuragru(self,ser_gru)

                    elif xxx=='4': #excluir dados do banco
                        login.clear_terminal()
                        idsai = input('Qual conta deseja excluir: ')
                        login.delete(self,idsai)
                        print('\n')
                        cont = (login.continua())

                    elif xxx=='5': #Editar conta
                        login.clear_terminal()
                        idedi = input('Qual ID da conta deseja mudar? ')
                        print('\n')
                        login.procuraid(self,idedi)
                        login.menuzin()
                        temp = input('Sua escolha: ')
                        if temp == '1': # Alterar somente usuario
                            login.clear_terminal()
                            new_u = input(' Qual o novo usuario? ')
                            login.updateusu(self,idedi,new_u)
                            login.procuraid(self,idedi)
                            print('\n')
                            cont = (login.continua())
                        elif temp =='2': # Alterar somente senha
                            login.clear_terminal()
                            new_s = input(' Qual a nova senha? ')
                            login.updatesen(self,idedi,new_s)
                            login.procuraid(self,idedi)
                            print('\n')
                            cont = (login.continua())
                        elif temp =='3': # Alterar somente grupo
                            login.clear_terminal()
                            new_g = input(' Qual o novo grupo? ')
                            login.updategru(self,idedi,new_g)
                            login.procuraid(self,idedi)
                            print('\n')
                            cont = (login.continua())
                        elif temp =='4': # Alterar usuario e senha
                            login.clear_terminal()
                            new_u = input(' Qual o novo usuario? ')
                            login.updateusu(self,idedi,new_u)
                            new_s = input(' Qual a nova senha? ')
                            login.updatesen(self,idedi,new_s)
                            login.procuraid(self,idedi)
                            print('\n')
                            cont = (login.continua())
                        else: print('Digita serto parça')
                    elif xxx == '0':
                        cont = False
                connection.__exit__
                print(' Bye bye bitch ')
            else: 
                connection.__exit__
                print(' Tu não conhece meus segredos')

        
if __name__ == "__main__":
    banco = autoriza()



        
        

            
