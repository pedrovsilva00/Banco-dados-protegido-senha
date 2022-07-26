
import sqlite3 as db
import hashlib
import keyring
import time
import getpass 
import random
import string
import time
from progressbar import Bar, AdaptiveETA, Percentage, ProgressBar,  RotatingMarker, FileTransferSpeed

def logo():
    print ('     ___________________________________________________________ ')
    print ('    |      _______   _______   _______   _______   _______      |')
    print ('    |     (  ____ ) (  ___  ) (  ____ \ (  ____ \ (  ___  )     |')
    print ('    |     | (    )| | (   ) | | (    \/ | (    \/ | (   ) |     |')
    print ('    |     | (____)| | (___) | | (_____  | (_____  | (___) |     |')
    print ('    |     |  _____) |  ___  | (_____  ) (_____  ) |  ___  |     |')
    print ('    |     | (       | (   ) |       ) |       ) | | (   ) |     |')
    print ('    |     | )       | )   ( | /\____) | /\____) | | )   ( |     |')
    print ('    |     |/        |/     \| \_______) \_______) |/     \|     |')
    print ('    |      _______   _______   _                   _______      |')
    print ('    |     (  ____ \ (  ____ \ ( (    /| |\     /| (  ___  )     |')
    print ('    |     | (    \/ | (    \/ |  \  ( | | )   ( | | (   ) |     |')
    print ('    |     | (_____  | (__     |   \ | | | (___) | | (___) |     |')
    print ('    |     (_____  ) |  __)    | (\ \) | |  ___  | |  ___  |     |')
    print ('    |           ) | | (       | | \   | | (   ) | | (   ) |     |')
    print ('    |     /\____) | | (____/\ | )  \  | | )   ( | | )   ( |     |')
    print ('    |     \_______) (_______/ |/    )_) |/     \| |/     \|     |')
    print ('    |___________________________________________________________|')
    time.sleep(2)
    print('\x1b[2J')

def barra():
    widgets = ['Carregando: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
               ' ', AdaptiveETA(), ' ', FileTransferSpeed(unit='J')]
    pbar = ProgressBar(widgets=widgets, maxval=10000000).start()
    for i in range(100000):
        # do something
        pbar.update(100*i+1)
    pbar.finish()

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

def cripto(s1, s2):
    return "".join([chr(ord(c1) ^ ord(c2)) for (c1, c2) in zip(s1,s2)])

class login(connection):
    def __init__(self):
        connection.__init__(self)
    def insert(self,btu,btc,btg,bte,k): # Adicionar novos dados
        try:
            btu_cry = cripto(btu,k)
            btc_cry = cripto(btc,k)
            btg_cry = cripto(btg,k)
            bte_cry = cripto(bte,k)
            self.cur.execute(f"""
                    INSERT INTO aevr (uiop, cvbn, ghjk, erty) VALUES (?, ?, ?, ?)
                   ;""", [btu_cry,btc_cry,btg_cry,bte_cry])
            self.commit()
            barra()
            print('Banco de Dados atualizado')
        except Exception as e:
            print("Erro ",e, " ao atualizar o banco de dados")

    def delete(self,delu,k): # Deletar dados / procura pelo id
        try:
            delu_cry = cripto(delu,k)
            self.cur.execute(f"""DELETE FROM aevr WHERE uiop = '{delu_cry}'""")  
            self.commit()  
            print('Conta: ',delu,' deletada')
        except Exception as e:
            print("Erro ",e, " ao deletar no banco de dados")  

    def updatecv(self,upu, new_c,k): # Editar usuario 
        try:
            upu_cry = cripto(upu,k)
            new_cry = cripto(new_c,k)
            self.execute(f"UPDATE aevr SET cvbn = '{new_cry}' WHERE uiop= '{upu_cry}'")  
            self.commit()
            print("Usuario alterado da conta: ",upu)
        except Exception as e:
            print("Erro ",e, " ao atualizar o usuario")

    def updategh(self,upu, new_g,k): # Editar senha
        try:
            upu_cry = cripto(upu,k)
            new_cry = cripto(new_g,k)
            self.execute(f"UPDATE aevr SET ghjk = '{new_cry}' WHERE uiop= '{upu_cry}'")  
            self.commit()
            print("Senha alterada da conta: ",upu)
        except Exception as e:
            print("Erro ",e, " ao atualizar senha")

    def updateer(self,upu, new_e,k): # Editar grupo
        try:
            upu_cry = cripto(upu,k)
            new_cry = cripto(new_e,k)
            self.execute(f"UPDATE aevr SET erty = '{new_cry}' WHERE uiop= '{upu_cry}'")  
            self.commit()
            print("Grupo alterado da conta: ",upu)
        except Exception as e:
            print("Erro ",e, " ao atualizar o grupo")

    def procuraui(self,prou,k): # Pesquisa pelo id
        if prou == 'all':
            apps = self.query("SELECT uiop FROM aevr")
            print('\nTodas Contas: \n')
            x =''
            for row in apps:
                um = cripto(row[0],k)
                print(' ID  --> ',um)
                print('\n')
        else:
            pu = cripto(prou,k)
            apps = (self.query(f"""
                    SELECT cvbn, ghjk ,erty FROM aevr WHERE uiop = '{pu}'
                  ;"""))
            if apps: 
                print (' Resultado da procura pela conta: ',prou)
                print('\n')
                for row in apps:
                    um = cripto(row[0],k) 
                    dos = cripto(row[1],k)
                    tre = cripto(row[2],k)
                    print('USUARIO --> ',um)
                    print(' SENHA  --> ',dos)
                    print(' GRUPO  --> ',tre)
                    print('\n')
            else: x = ('O id ', prou, ' não foi encontrado')
        return print (x) 

    def procuraer(self,proe,k): # Pesquisa por grupo
        if proe == 'all':
            apps = self.query("SELECT erty FROM aevr")
            print('\nTodos os grupos: \n')
            x =''
            for row in apps:
                um = cripto(row[0],k)
                print(' GRUPO  --> ',um)
                print('\n')
        else:
            pe = cripto(proe,k)
            apps = (self.query(f"""
                    SELECT uiop, cvbn, ghjk FROM aevr WHERE erty = '{pe}'
                  ;"""))
            if apps: 
                print (' Resultado da procura pelo grupo: ',proe)
                print('\n')
                for row in apps:
                    um = cripto(row[0],k) 
                    dos = cripto(row[1],k)
                    tre = cripto(row[2],k)
                    print('  ID    --> ',um)
                    print('USUARIO --> ',dos)
                    print(' SENHA  --> ',tre)
                    print('\n')
            else:  x = ('O grupo ', proe ,' não foi encontrado') 
        return print (x)

    def main_menu(): # menu principal
        print('------------------------------')
        print('1- Inserir uma nova conta')
        print('2- Procurar conta por id')
        print('3- Procurar conta por grupo')
        print('4- Excluir uma conta')
        print('5- Editar uma conta')
        print('6- Gerador de senhas')
        print('0- Sair')
        print('------------------------------\n')
        z =input('Qual opção desejada:  ')
        return z

    def menuzin(): #menu de edição
        print('------------------------------')
        print('1- Mudar o usuario')
        print('2- Mudar a senha')
        print('3- Mudar o grupo')
        print('4- Mudar usuario e senha')
        print('------------------------------\n')
        z =input('Sua escolha: ')
        return z


    def continua(): # Continuar ou não a usar o banco de dados
        cc = input(' Deseja continuar? (S) (N) ')
        if cc == 'S' or cc == 's' or cc == '1':
            vano = True
        elif cc=='N' or cc=='n' or cc == '0':
            vano =False
        return vano
        
    def clear_terminal():
        return print('\x1b[2J')
    
    def gerador (x):
        xxx = 0
        senha = ''
        for xxx in range(x):
            senha += random.choice((string.ascii_letters) + (string.digits) + "#$%&*^?@_!-ç=]}{[")
        return senha



class autoriza(connection): # Intereção com o banco de dados
    def __init__(self):
            logo()
                # Cadastro do admin pelo hash sha512 - padrão admin
            self.admin = '58b5444cf1b6253a4317fe12daff411a78bda0a95279b1d5768ebf5ca60829e78da944e8a9160a0b6d428cb213e813525a72650dac67b88879394ff624da482f'
                # Cadastro da senha pelo hash sha512 - padrão admin
            self.master = '58b5444cf1b6253a4317fe12daff411a78bda0a95279b1d5768ebf5ca60829e78da944e8a9160a0b6d428cb213e813525a72650dac67b88879394ff624da482f' 
            keyring.set_password('master', self.admin, self.master) # Armazenamento de credenciais pela biblioteca keyring
            pede_admin = getpass.getpass('User: ')
            pede_master = getpass.getpass ('Password: ')
                #Verificação em duas etapas - padrão 1
            salt = getpass.getpass('Lucky Number: ')
            cc = pede_admin + salt
            mm = pede_master + salt
            hm = hashlib.sha512(mm.encode())
            hashs = hm.hexdigest() # transformação do senha fornecido em hash sha512
            hc = hashlib.sha512(cc.encode())
            hashc = hc.hexdigest() # transformação da admin fornecida em hash sha512
            aa = keyring.get_password("master",hashc)
            barra()

            if (aa == hashs): # Verificação de autenticidade
                connection.__init__(self)
                cont = True
                while cont == True:
                    xxx = login.main_menu()
                    if xxx == '1': # ADD nova linha
                        login.clear_terminal()
                        print('Dados do novo cadastro')
                        pdu = input('ID:  ')
                        pdc = input('Usuario:  ')
                        pdg = input('Senha:  ')
                        pde = input('Grupo:  ')
                        login.insert(self,pdu,pdc,pdg,pde,aa)
                        print('\n')
                        cont = (login.continua())

                    elif xxx == '2': # Procurar por id
                        login.clear_terminal()
                        seru = input('Qual id que procuras? ')
                        login.clear_terminal()
                        barra()
                        login.procuraui(self,seru,aa)
                        cont = (login.continua())

                    elif xxx== '3':  # procura pelo grupo
                        login.clear_terminal()
                        sere = input('Qual grupo que procuras? ')
                        login.clear_terminal()
                        barra()
                        login.procuraer(self,sere,aa)
                        cont = (login.continua())

                    elif xxx=='4': #excluir dados do banco
                        login.clear_terminal()
                        delui = input('Qual conta deseja excluir: ')
                        login.delete(self,delui,aa)
                        print('\n')
                        cont = (login.continua())

                    elif xxx=='5': #Editar conta
                        login.clear_terminal()
                        muu = input('Qual ID da conta deseja mudar? ')
                        print('\n')
                        login.procuraui(self,muu,aa)
                        temp = login.menuzin()
                        if temp == '1': # Alterar somente usuario
                            login.clear_terminal()
                            new_c = input(' Qual o novo usuario? ')
                            login.updatecv(self,muu,new_c,aa)
                            barra()
                            login.procuraui(self,muu,aa)
                            print('\n')
                            cont = (login.continua())
                        elif temp =='2': # Alterar somente senha
                            login.clear_terminal()
                            new_g = input(' Qual a nova senha? ')
                            login.updategh(self,muu,new_g,aa)
                            barra()
                            login.procuraui(self,muu,aa)
                            print('\n')
                            cont = (login.continua())
                        elif temp =='3': # Alterar somente grupo
                            login.clear_terminal()
                            new_g = input(' Qual o novo grupo? ')
                            login.updateer(self,muu,new_g,aa)
                            barra()
                            login.procuraui(self,muu,aa)
                            print('\n')
                            cont = (login.continua())
                        elif temp =='4': # Alterar usuario e senha
                            login.clear_terminal()
                            new_c = input(' Qual o novo usuario? ')
                            login.updatecv(self,muu,new_c,aa)
                            new_g = input(' Qual a nova senha? ')
                            login.updategh(self,muu,new_g,aa)
                            barra()
                            login.procuraui(self,muu,aa)
                            print('\n')
                            cont = (login.continua())
                        else: print('Digita serto parça')
                    elif xxx == '6':
                        login.clear_terminal()
                        print ('Gerador de Senhas\n')
                        temp = int(input('Tamanho desejado: \n'))
                        print (login.gerador(temp))
                        cont = login.continua()

                    elif xxx == '0':
                        cont = False
                connection.__exit__
                print(' Bye ')
                time.sleep(1)
            else: 
                connection.__exit__
                print(' Tu não conhece meus segredos')
                time.sleep(1)
        
if __name__ == "__main__":
    banco = autoriza()
