import os as oo 
import cx_Oracle
import getpass
import sys
import time
import numpy as np
from sympy import Matrix, Mod

def encrypt_hill(plaintext, key):
    plaintext = plaintext.lower().replace(" ", "")
    plaintext_len = len(plaintext)
    key_size = len(key)

    if plaintext_len % key_size != 0:
        padding_len = key_size - (plaintext_len % key_size)
        plaintext += "x" * padding_len

    ciphertext = ""

    plaintext_blocks = [plaintext[i : i + key_size] for i in range(0, len(plaintext), key_size)]

    for block in plaintext_blocks:
        block_indices = [ord(char) - ord("a") for char in block]
        block_vector = np.array(block_indices)

        encrypted_block = np.dot(key, block_vector) % 26

        encrypted_chars = [chr(index + ord("a")) for index in encrypted_block]
        ciphertext += "".join(encrypted_chars)

    return ciphertext

def decrypt_hill(ciphertext, key):
    ciphertext = ciphertext.lower().replace(" ", "")
    ciphertext_len = len(ciphertext)
    key_size = len(key)

    if ciphertext_len % key_size != 0:
        raise ValueError("Ciphertext length is not divisible by key size")

    plaintext = ""

    ciphertext_blocks = [ciphertext[i : i + key_size] for i in range(0, len(ciphertext), key_size)]

    key_inverse = Matrix(key).inv_mod(26)

    key_inverse_np = np.array(key_inverse.tolist(), dtype=int)

    for block in ciphertext_blocks:
        block_indices = [ord(char) - ord("a") for char in block]
        block_vector = np.array(block_indices)

        decrypted_block = np.dot(key_inverse_np, block_vector) % 26

        decrypted_chars = [chr(int(index) + ord("a")) for index in decrypted_block]
        plaintext += "".join(decrypted_chars)

    return plaintext.rstrip("x")  # Remover caracteres de padding 'x'

# Utilização de uma função que caso usuário digitar um string, apareça uma mensagem e peça novamente a informação
def obt_inpt(men):
    while True:
        entry = input(men)
        if entry.isdigit():
            return int(entry)
        else:
            print("Valor inválido. Digite uma das opções do menu: ")
            time.sleep(0.5)

# Utilização da biblioteca getpass para mascarar da senha da conexão
def masked_input(prompt=''):
    password=[]
    while True:
        key= getpass.getpass(prompt='',stream=None)
        if not key:
            break
        password.append(key)
        print('*'*len(key),end='',flush=True)
    print()
    return ''.join(password)

# Verificação da pré existênia da tabela
def table_exists(conn, table_name):
    cursor = conn.cursor()
    try:
        # Tenta executar um SELECT na tabela
        cursor.execute(f"SELECT 1 FROM {table_name} WHERE ROWNUM = 1")
    except cx_Oracle.DatabaseError:
        # Caso ocorrer um erro, a tabela não existe
        return False
    else:
        # Caso não ocorrer erro, a tabela existe
        return True
    finally:
        cursor.close()

while True:
    try:
        # Inserção de dados para conexão com banco de dados
        host = input("Informe o nome do host: ")
        port = input("Informe o número da porta: ")
        service_name = input("Informe o nome do serviço do banco de dados: ")
        username = input("Informe o nome do usuário: ")
        print("\nInforme a senha do usuário:")
        password = masked_input("Informe a senha do usuário: ")

        # Cria uma conexão com o banco de dados
        dsn_tns = cx_Oracle.makedsn(host, port, service_name=service_name)
        conn = cx_Oracle.connect(username, password, dsn_tns)

        cur = conn.cursor()
        
        oo.system('cls')

        if table_exists(conn, 'qualidade_ar'):
            print()
        else:
            # Criação da tabela
            sqlParam = 'CREATE TABLE qualidade_ar (mp10 INTEGER, mp25 INTEGER, o3 INTEGER, co INTEGER, no2 INTEGER, so2 INTEGER)'
            cursor = conn.cursor()
            cursor.execute(sqlParam)
            cursor.close()
            conn.commit()
        
        flag=True

        # Definição do Menu principal

        while flag==True:
            print("\nBem vindo ao sistema! Selecione uma opção para continuar: ")
            print("\n Opção 1. Inserir Amostras")
            time.sleep(0.2)

            print("\n Opção 2. Alterar Amostras")
            time.sleep(0.2)

            print("\n Opção 3. Apagar Amostras")
            time.sleep(0.2)

            print("\n Opção 4. Classificar Amostras")
            time.sleep(0.2)

            print("\n Opção 0. Sair do Sistema")
            time.sleep(0.2)

            opt=obt_inpt("\nSelecione uma opção para continuar: ")
            
            if opt>=5:
                print("Valor inválido. Digite uma das opções do menu: ")
                opt=obt_inpt("\nSelecione uma opção para continuar: ")

            while opt!=0:
                # Inserção dos valores de uma amostra
                if opt==1:   
                    try: 
                        print("\nPor favor, insira as amostras:")
                        mp10 = float(input("Informe o valor de MP10: "))
                        mp25 = float(input("Informe o valor de MP2,5: "))
                        o3 = float(input("Informe o valor de O3: "))
                        co = float(input("Informe o valor de CO: "))
                        no2 = float(input("Informe o valor de NO2: "))
                        so2 = float(input("Informe o valor de SO2: "))
                
                        sqlInsert = 'insert into qualidade_ar (mp10, mp25, o3, co, no2, so2) VALUES (:mp10, :mp25, :o3, :co, :no2, :so2)'
                
                        dados= {'mp10': mp10, 'mp25':mp25, 'o3':o3, 'co':co, 'no2':no2, 'so2':so2}
                
                        cur.execute(sqlInsert,dados)
                
                        conn.commit()
                        print("\nValores Inseridos!")
                        
                        time.sleep(0.7)

                        oo.system('cls')
                        
                        break
                    except ValueError:
                        oo.system('cls')
                        print("\nPor favor insira um valor valido:")
                        
            
                if opt==2:
                    oo.system('cls')
                    # Atualização dos valores de uma amostra
                    print("\n")
                    sqlSelect= 'select mp10, mp25, o3, co, no2, so2 from qualidade_ar'
                    cur.execute(sqlSelect)
        
                    nomeC = [desc[0] for desc in cur.description]
                    print("\n",nomeC)

                    # Mostra o valor dos dados
                    rows = cur.fetchall()

                    for row in rows:
                        print("\n",row)

                    conn.commit()
                    print("\n")
                    print("Valores não incluídos na tabela não serão alterados!")
                    print("\n")
                    # Usuário escolhe a coluna que deseja alterar por rótulo e valor anterior
                    columnname=str(input("Qual coluna deseja alterar?: "))
                
                    if columnname=="mp10":    
                        try: 
                            mp10 = float(input("Informe o novo valor de MP10: "))
                            mp10old=float(input("Infrome o antigo valor de MP10: "))

                            sqlupdate0="update qualidade_ar set mp10 = :mp10new where mp10 = :mp10old"
                            data0={'mp10new':mp10, 'mp10old':mp10old}
                            cur.execute(sqlupdate0,data0)
                            conn.commit()

                            print("\nValores da amostra atualizados!")
                            print("\n")
                            time.sleep(0.8)
                            oo.system('cls')
                            break
                        
                        except ValueError: 
                            time.sleep(0.5)

                    if columnname=="mp25":
                        try:
                            mp25 = float(input("Informe o novo valor de MP2,5: "))
                            mp25old=float(input("Informe o valor antigo de mp2,5: "))
                            sqlupdate1="update qualidade_ar set mp25 = :mp25new where mp25 = :mp25old"
                            data1={'mp25new':mp25, 'mp25old':mp25old}
                            cur.execute(sqlupdate1,data1)
                            conn.commit()

                            print("\nValores da amostra atualizados!")
                            print("\n")
                            time.sleep(0.8)
                            oo.system('cls')
                            break
                        
                        except ValueError:
                            time.sleep(0.5)

                    if columnname=="o3":
                        try:
                            o3 = float(input("Informe o novo valor de O3: "))
                            o3old=float(input("Informe o valor antigo de O3: "))
                            sqlupdate2="update qualidade_ar set o3 = :o3new where o3 = :o3old"
                            data2={'o3new':o3, 'o3old':o3old}
                            cur.execute(sqlupdate2,data2)
                            conn.commit()

                            print("\nValores da amostra atualizados!")
                            print("\n")
                            time.sleep(0.8)
                            oo.system('cls')
                            break
                        
                        except ValueError:
                            time.sleep(0.5)

                    if columnname=="co":
                        try:
                            co = float(input("Informe o novo valor de CO: "))
                            coold=float(input("Informe o valor antigo de CO: "))
                            sqlupdate3="update qualidade_ar set co = :conew where co = :coold"
                            data3={'conew':co, 'coold':coold}
                            cur.execute(sqlupdate3,data3)
                            conn.commit()

                            print("\nValores da amostra atualizados!")
                            print("\n")
                            time.sleep(0.8)
                            oo.system('cls')
                            break
                        
                        except ValueError:
                            time.sleep(0.5)

                    if columnname=="no2":
                        try:
                            no2 = float(input("Informe o novo valor de NO2: "))
                            no2old= float(input("Informe o valor antigo de NO2: "))
                            sqlupdate4="update qualidade_ar set no2 = :no2new where no2 = :no2old"
                            data4={'no2new':no2, 'no2old':no2old}
                            cur.execute(sqlupdate4,data4)
                            conn.commit()

                            print("\nValores da amostra atualizados!")
                            print("\n")
                            time.sleep(0.8)
                            oo.system('cls')
                            break
                        
                        except ValueError:
                            time.sleep(0.5)

                    if columnname=="so2":
                        try:
                            so2 = float(input("Informe o novo valor de SO2: "))
                            so2old= float(input("Informe o valor antigo de SO2: "))
                            sqlupdate5="update qualidade_ar set so2 = :so2new where so2 = :so2old"
                            data5={'so2new':so2, 'so2old':so2old}
                            cur.execute(sqlupdate5,data5)
                            conn.commit()
                        
                            print("\nValores da amostra atualizados!")
                            print("\n")
                            time.sleep(0.8)
                            oo.system('cls')
                            break
                        
                        except ValueError:
                            time.sleep(0.5)

                    if columnname!=float:
                        print("\nPor favor insira um válido:")
                        time.sleep(1)

                if opt==3:
                    try:
                        print("\n")
                        # Atualização dos valores de uma amostra
                        print("\n")
                        sqlSelect= 'select mp10, mp25, o3, co, no2, so2 from qualidade_ar'
                        cur.execute(sqlSelect)
        
                        nomeC = [desc[0] for desc in cur.description]
                        print("\n",nomeC)

                        # Mostra o valor dos dados
                        rows = cur.fetchall()

                        for row in rows:
                            print("\n",row)

                        conn.commit()
                        # Seleção das amostras por rótulo e valor antigo
                        print("\n")  
                        print("Valores não incluídos na tabela não serão apagados!")
                        print("\n")
                        sampledelete=str(input("Qual amostra deseja apagar?: "))
                        dataname=float(input("\nQual dado da coluna deseja apagar?: "))
                        if sampledelete==("mp10"):
                            sqldeletemp10='update qualidade_ar set mp10 = 0 where mp10 = :mp10delete'
                            mp10deletecomm={'mp10delete':dataname}
                            cur.execute(sqldeletemp10,mp10deletecomm)
                            conn.commit()

                        elif sampledelete==("mp25"):
                            sqldeletemp25='update qualidade_ar set mp25 = 0 where mp25 = :mp25delete'
                            mp25deletecomm={'mp25delete':dataname}
                            cur.execute(sqldeletemp25,mp25deletecomm)
                            conn.commit()

                        elif sampledelete==("o3"):
                            sqldeleteo3='update qualidade_ar set o3 = 0 where o3 = :o3delete'
                            o3deletecomm={'o3delete':dataname}
                            cur.execute(sqldeleteo3,o3deletecomm)
                            conn.commit()

                        elif sampledelete==("co"):
                            sqldeleteco='update qualidade_ar set co = 0 where co = :codelete'
                            codeletecomm={'codelete':dataname}
                            cur.execute(sqldeleteco,codeletecomm)
                            conn.commit()

                        elif sampledelete==("no2"):
                            sqldeleteno2='update qualidade_ar set no2 = 0 where no2 = :no2delete'
                            no2deletecomm={'no2delete':dataname}
                            cur.execute(sqldeleteno2,no2deletecomm)
                            conn.commit()

                        elif sampledelete==("so2"):
                            sqldeleteso2='update qualidade_ar set so2 = 0 where so2 = :so2delete'
                            so2deletecomm={'so2delete':dataname}
                            cur.execute(sqldeleteso2,so2deletecomm)
                            conn.commit()
                        
                        elif sampledelete!=str or dataname!=float:
                            print("Por favor insira um valor válido:")
                            time.sleep(0.5)
                            break

                        print("\nAmostra apagada!")
                        print("\n")
                        time.sleep(0.8)
                        oo.system('cls')
                        break
                                               
                    except ValueError:
                        print("\nPor favor insira valor válido:")
                        time.sleep(1)
                        oo.system('cls')

                # Seleciona a tabela e organiza seus valores
                if opt==4:
                    oo.system('cls')
                    print("\n")

                    sqlSelect2= 'select mp10, mp25, o3, co, no2, so2 from qualidade_ar'
                    cur.execute(sqlSelect2)
        
                    nomeC2 = [desc[0] for desc in cur.description]
                    print(nomeC2)

                    # Mostra o valor dos dados
                    rows = cur.fetchall()

                    for row in rows:
                        print("\n",row)
        
                    # Calcula a media de cada coluna
                    for i in range(len(nomeC2)):
                        cur.execute(f"SELECT AVG({nomeC2[i]}) FROM qualidade_ar")
                        med = cur.fetchone()[0]
                        time.sleep(0.5)
                        print(f"[\nMédia de {nomeC2[i]}: {med}")

                        conn.commit()

                        # Leitura dos valores das amostras (Entradas)
                        cur.execute('select avg(mp10) from qualidade_ar')
                        mp10 = cur.fetchone()[0]

                        cur.execute('select avg(mp25) from qualidade_ar')
                        mp25 = cur.fetchone()[0]

                        cur.execute('select avg(o3) from qualidade_ar')
                        o3 = cur.fetchone()[0]

                        cur.execute('select avg(co) from qualidade_ar')
                        co = cur.fetchone()[0]

                        cur.execute('select avg(no2) from qualidade_ar')
                        no2 = cur.fetchone()[0]

                        cur.execute('select avg(so2) from qualidade_ar')
                        so2 = cur.fetchone()[0]

                    
                    if (mp10 < 0) and (mp25 <= 0) and (o3 <= 0) and (co <= 0) and (no2 <= 0) and (so2 <= 0):
    
                        print("Valores inválidos!")
                        

                        # Verificação da qualidade do ar com base nos valores informados
                        # Exemplo: Se todos os valores da linha estiverem de acordo com a classificação de boa então imprime "Qualidade do ar: Boa"!
                        # Porém se algum valor estourar o limite, passa para a qualidade seguinte adequada.
                    
                    if (0 <= mp10 <= 50) and (0 <= mp25 <= 25) and (0<= o3 <= 100) and (0<= co <= 9) and (0<= no2 <= 200) and (0<= so2 <= 20):
                        try:  
                            plaintext0 = "Qualidade do ar Boa"
                            key = [[9, 4], [5, 7]]
                            
                            ciphertext0 = encrypt_hill(plaintext0, key)
                            
                            print("\nClassificação criptografada:", ciphertext0)
                            
                            time.sleep(0.5)
                            criptopt=int(input("Digite 1 para descriptografar a mensagem, ou 0 para voltar ao menu: "))
                            if criptopt==1:
                                decrypted_text = decrypt_hill(ciphertext0, key)
                                print("\nClassificação descriptografada:", decrypted_text)
                                time.sleep(0.8)
                                print("\nClassificação organizada: Qualidade do ar: Boa")
                            if criptopt==0:
                                break

                        except ValueError:
                            print("Por favor digite um valor válido:")
                        

                    elif (50 < mp10 <= 100) or (25 < mp25 <= 50) or (100 < o3 <= 130) or (9 < co <= 11) or (200 < no2 <= 240) or (20 < so2 <= 40):
                        try:  
                            plaintext = "Qualidade do ar Moderada"
                            key = [[9, 4], [5, 7]]
                            ciphertext = encrypt_hill(plaintext, key)
                            
                            print("\nClassificação criptografada:", ciphertext)
                            time.sleep(0.5)
                            
                            plaintext2 = "Pessoas de grupos sensiveis criancas idosos e pessoas com doenças respiratorias e cardiacas podem apresentar sintomas como tosse seca e cansaco A populacao em geral nao e afetada"
                            ciphertext2 = encrypt_hill(plaintext2, key)
                            print("\nRecomendação criptografada:", ciphertext)
                            
                            time.sleep(0.5)
                            criptopt=int(input("Digite 1 para descriptografar a mensagem, ou 0 para voltar ao menu: "))
                            if criptopt==1:
                                decrypted_text = decrypt_hill(ciphertext, key)
                                
                                print("\nClassificação descriptografada:", decrypted_text)
                                time.sleep(0.8)
                                print("\nClassificação organizada: Qualidade do ar: Moderada")
                                
                                decrypted_text = decrypt_hill(ciphertext2, key)
                                
                                print("\nRecomendação descriptografada:", decrypted_text)
                                time.sleep(0.8)
                                print("\nRecomendação organizada: Pessoas de grupos sensíveis crianças idosos e pessoas com doenças respiratórias e cardiacas podem apresentar sintomas como tosse seca, e ,cansaço. A populacao em geral não e afetada ")
                            
                            if criptopt==0:
                                break

                        except ValueError:
                            print("Por favor digite um valor válido:")
                        
                    
                    elif (100 < mp10 <= 150) or (50 < mp25 <= 75) or (130 < o3 <= 160) or (11 < co <= 13) or  (240 < no2 <= 320) or (40 < so2 <= 365):
                        try:
                            plaintext3 = "Qualidade do ar Ruim"
                            key = [[9, 4], [5, 7]]
                            ciphertext3 = encrypt_hill(plaintext3, key)
                            
                            print("\nClassificação criptografada:", ciphertext3)
                            
                            time.sleep(0.5)
                            
                            plaintext4 = "toda a populacao pode apresentar sintomas como tosse seca cansaço ardor nos olhos nariz e garganta Pessoas de grupos sensiveis criancas idosos e pessoas com doencas resiratorias e cardiacas podem apresentar efeitos mais serios na saude"
                            ciphertext4 = encrypt_hill(plaintext4, key)   
                            print("\nRecomendação criptografada:", ciphertext4)
                            
                            time.sleep(0.5)
                            
                            criptopt=int(input("Digite 1 para descriptografar a mensagem, ou 0 para voltar ao menu: "))
                            if criptopt==1:
                                
                                decrypted_text = decrypt_hill(ciphertext3, key)
                                
                                print("\nClassificação descriptografada:", decrypted_text)
                                
                                time.sleep(0.5)
                                
                                print("\nClassificação organizada: Qualidade do ar: Ruim")
                                
                                decrypted_text = decrypt_hill(ciphertext4, key)
                                
                                
                                print("\nRecomendação descriptografada:", decrypted_text)
                                
                                time.sleep(0.5)
                                
                                print("\nRecomendação organizada: Toda a população pode apresentar sintomas como tosse seca, cansaço, ardor nos olhos, nariz e garganta. Pessoas de grupos sensíveis(crianças, idosos e pessoas com doenças resiratórias e cardíacas) podem apresentar efeitos mais sérios na saúde")
                            if criptopt==0:
                                break
                               
                        except ValueError:
                            print("Por favor digite um valor válido:")
                        
                    
                    elif (150 < mp10 <= 250) or (75 < mp25 <= 125) or (160 < o3 <= 200) or (13 < co <= 15) or (320 < no2 <= 1130) or (365 < so2 <= 800):
                        try:
                            plaintext5 = "Qualidade do ar Muito ruim"
                            key = [[9, 4], [5, 7]]
                            ciphertext5 = encrypt_hill(plaintext5, key)
                           
                            print("\nClassificação criptografada:", ciphertext5)
                            
                            time.sleep(0.5)
                            
                            plaintext6 = "Toda a populacao pode apresentar sintomas como tosse seca cansaco ardor nos olhos nariz e garganta e ainda falta de ar e respiracao ofegante Efeitos ainda mais graves a saude de grupos sensiveis criancas idosos e pessoas com doencas respiratorias e cardiacas"
                            ciphertext6 = encrypt_hill(plaintext6, key)
                            
                            print("\nRecomendação criptografada:", ciphertext6)
                            
                            time.sleep(0.5)
                            
                            criptopt=int(input("Digite 1 para descriptografar a mensagem, ou 0 para voltar ao menu: "))
                            if criptopt==1:
                                decrypted_text = decrypt_hill(ciphertext5, key)
                                
                                print("\nClassificação descriptografada:", decrypted_text)
                                
                                time.sleep(0.5)
                                
                                print("\nClassificação organizada: Qualidade do ar: Muito ruim")
                                decrypted_text = decrypt_hill(ciphertext6, key)
                                
                                print("\nRecomendação descriptografada:", decrypted_text)
                                
                                time.sleep(0.5)
                                
                                print("\nRecomendação organizada: Toda a população pode apresentar sintomas como tosse seca, cansaço, ardor nos olhos, nariz, e garganta e ainda falta de ar e respiração ofegante. Efeitos ainda mais graves à saúde de grupos sensíveis(crianças, idosos e pessoas com doenças respiratórias e cardíacas)")
                            
                            if criptopt==0:
                                break

                        except ValueError:
                            print("Por favor digite um valor válido:")
                        
                    
                    elif (250 < mp10) or (125 < mp25) or (200 < o3) or (15 < co) or (1130 < no2) or (800 < so2):
                        try:
                            plaintext7 = "Qualidade do ar Pessima"
                            key = [[9, 4], [5, 7]]
                            ciphertext7 = encrypt_hill(plaintext7, key)
                            
                            print("\nClassificação criptografada:", ciphertext7)
                            
                            time.sleep(0.5)
                            
                            plaintext8 = "Toda a populacao pode apresentar serios risco de manifestacoes de doencas respiratorias e cardiovasculares Aumento de mortes prematuras em pessoas de grupos sensiveis"
                            ciphertext8 = encrypt_hill(plaintext8, key)
                            
                            print("\nRecomendação criptografada:", ciphertext8)
                            
                            time.sleep(0.5)
                            
                            criptopt=int(input("Digite 1 para descriptografar a mensagem, ou 0 para voltar ao menu: "))
                            if criptopt==1:
                                decrypted_text = decrypt_hill(ciphertext7, key)
                                
                                print("\nClassificação descriptografada:", decrypted_text)
                                
                                time.sleep(0.5)
                                
                                print("\nClassificação organizada: Qualidade do ar: Pessima")
                                decrypted_text = decrypt_hill(ciphertext8, key)
                                
                                print("\nRecomendação descriptografada:", decrypted_text)
                                
                                time.sleep(0.5)
                                
                                print("\nRecomendação organizada: Toda a população pode apresentar sérios risco de manifestações de doenças respiratórias e cardiovasculares. Aumento de mortes prematuras em pessoas de rupos sensíveis")
                            
                            if criptopt==0:
                                break
                        
                        except ValueError:
                            print("Por favor digite um valor válido:")
                        
                    time.sleep(10)
                    oo.system('cls')
                    break

            if opt==0:
                print("\nObrigado por utilizar o sistema! Nos vemos em breve!")
                break
        
        if opt==0:
            flag==False
        
            cur.close()
            conn.close()
            time.sleep(1)
            sys.exit()           
    
    except cx_Oracle.DatabaseError as e:
        oo.system('cls')
        print("Erro ao conectar ao banco de dados:")
        print(e)
        print("Por favor tente novamente. ")
        print()
# ------------------------------------------------------------------------------------------------------------
# Programadores: 
# ------------------------------------------------------------------------------------------------------------
# João Víctor Francetto Xavier - Backend, integração de criptografia, integração com banco de dados e frontend
# Bruna Barbour Fernandes - Frontend, organização do programa e auxilio no backend
# Gabriel Cardoso lima - Backend nas classificações dos dados e Frontend                    
# ------------------------------------------------------------------------------------------------------------ 
# Agradecimentos:
# ------------------------------------------------------------------------------------------------------------
# Professor André Mendeleck - Instruções gerais em python
# Professor José Marcelo Traina Chacon - Organização do projeto
# Aluno João Gabriel Biazon Ferreira - Auxilio com o projeto e apresentação
# ------------------------------------------------------------------------------------------------------------
# Integrantes do Grupo:
# ------------------------------------------------------------------------------------------------------------  
# João Víctor Francetto Xavier - Back End, Front End, integração de criptografia e integração com banco de dados
#
# Bruna Barbour Fernandes - Front End, organização do programa, organização do projeto e Back End
#
# Gabriel Cardoso Lima - Front End, developer do sistema de classificações e front end
#
#
#
#
# ------------------------------------------------------------------------------------------------------------
# Obrigado!
