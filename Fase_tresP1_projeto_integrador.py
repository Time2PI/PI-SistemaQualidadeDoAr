import os as oo 
import cx_Oracle
import getpass

#Utilização da biblioteca getpass para mascarar da senha da conexão
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

# Criação da tabela em background para inserção dos parâmetros
sqlParam= 'create table qualidade_ar (mp10 integer, mp25 integer, o3 integer, co integer, no2 integer, so2 integer)'

cur.execute(sqlParam)

conn.commit()

oo.system('cls')

flag=True

# Definição do Menu principal

while flag==True:
    print("\nBem vindo ao sistema! Selecione uma opção para continuar: ")
    print("\n Opção 1. Inserir Amostras")
    print("\n Opção 2. Alterar Amostras")
    print("\n Opção 3. Apagar Amostras")
    print("\n Opção 4. Classificar Amostras")
    print("\n Opção 0. Sair do Sistema")

    opt=(int)(input("Selecione uma opção para continuar: "))

    while opt!=0:
            # Inserção dos valores de uma amostra
        if opt==1:
            oo.system('cls')
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
            
            break

        
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
            # Usuário escolhe a coluna que deseja alterar por rótulo e valor anterior
            columnname=str(input("Qual coluna deseja alterar?: "))
            
            if columnname=="mp10":    
                mp10 = float(input("Informe o novo valor de MP10: "))
                mp10old=float(input("Infrome o antigo valor de MP10: "))

                sqlupdate0="update qualidade_ar set mp10 = :mp10new where mp10 = :mp10old"
                data0={'mp10new':mp10, 'mp10old':mp10old}
                cur.execute(sqlupdate0,data0)
                conn.commit()

                print("\nValores da amostra atualizados!")
                print("\n")
                break
            
            if columnname=="mp25":
                mp25 = float(input("Informe o novo valor de MP2,5: "))
                mp25old=float(input("Informe o valor antigo de mp2,5: "))
                sqlupdate1="update qualidade_ar set mp25 = :mp25new where mp25 = :mp25old"
                data1={'mp25new':mp25, 'mp25old':mp25old}
                cur.execute(sqlupdate1,data1)
                conn.commit()

                print("\nValores da amostra atualizados!")
                print("\n")
                break

            if columnname=="o3":
                o3 = float(input("Informe o novo valor de O3: "))
                o3old=float(input("Informe o valor antigo de O3: "))
                sqlupdate2="update qualidade_ar set o3 = :o3new where o3 = :o3old"
                data2={'o3new':o3, 'o3old':o3old}
                cur.execute(sqlupdate2,data2)
                conn.commit()

                print("\nValores da amostra atualizados!")
                print("\n")
                break

            if columnname=="co":
                co = float(input("Informe o novo valor de CO: "))
                coold=float(input("Informe o valor antigo de CO: "))
                sqlupdate3="update qualidade_ar set co = :conew where co = :coold"
                data3={'conew':co, 'coold':coold}
                cur.execute(sqlupdate3,data3)
                conn.commit()

                print("\nValores da amostra atualizados!")
                print("\n")
                break

            if columnname=="no2":
                no2 = float(input("Informe o novo valor de NO2: "))
                no2old= float(input("Informe o valor antigo de NO2: "))
                sqlupdate4="update qualidade_ar set no2 = :no2new where no2 = :no2old"
                data4={'no2new':no2, 'no2old':no2old}
                cur.execute(sqlupdate4,data4)
                conn.commit()

                print("\nValores da amostra atualizados!")
                print("\n")
                break

            if columnname=="so2":
                so2 = float(input("Informe o novo valor de SO2: "))
                so2old= float(input("Informe o valor antigo de SO2: "))
                sqlupdate5="update qualidade_ar set so2 = :so2new where so2 = :so2old"
                data5={'so2new':so2, 'so2old':so2old}
                cur.execute(sqlupdate5,data5)
                conn.commit()
                
                print("\nValores da amostra atualizados!")
                print("\n")
                break
        
        if opt==3:
            oo.system('cls')
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
                no2deletecomm={'no2delete':no2deletecomm}
                cur.execute(sqldeleteno2,no2deletecomm)
                conn.commit()

            elif sampledelete==("so2"):
                sqldeleteso2='update qualidade_ar set so2 = 0 where so2 = :so2delete'
                so2deletecomm={'so2delete':so2deletecomm}
                cur.execute(sqldeleteso2,so2deletecomm)
                conn.commit()
            print("\nAmostra apagada!")
            print("\n")
            break

        if opt==4:
            oo.system('cls')
            print("\n")

            sqlSelect2= 'select mp10, mp25, o3, co, no2, so2 from qualidade_ar'
            cur.execute(sqlSelect2)
    
            nomeC2 = [desc[0] for desc in cur.description]
            print("\n",nomeC2)

# Mostra o valor dos dados
            rows = cur.fetchall()

            for row in rows:
                print("\n",row)
    
# Calcula a media de cada coluna
            for i in range(len(nomeC2)):
                cur.execute(f"SELECT AVG({nomeC2[i]}) FROM qualidade_ar")
                med = cur.fetchone()[0]
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
    
                print("\nQualidade do ar: Boa")
                print ("\n\n")
                    

            elif (50 < mp10 <= 100) or (25 < mp25 <= 50) or (100 < o3 <= 130) or (9 < co <= 11) or (200 < no2 <= 240) or (20 < so2 <= 40):
    
                print("\nQualidade do ar: Moderada")
                print ("\n")
                print ("Pessoas de grupos sensíveis(crianças, idosos e pessoas com doenças respiratórias e cardíacas) podem apresentar sintomas como tosse seca e cansaço. A populaçao em geral nao é afetada")
                print ("\n")
                    
                
            elif (100 < mp10 <= 150) or (50 < mp25 <= 75) or (130 < o3 <= 160) or (11 < co <= 13) or  (240 < no2 <= 320) or (40 < so2 <= 365):
    
                print("\nQualidade do ar: Ruim")
                print ("\n\n")
                print ("Toda a população pode apresentar sintomas como tosse seca, cansaço, ardor nos olhos, nariz e garganta. Pessoas de grupos sensíveis(crianças, idosos e pessoas com doenças resiratórias e cardíacas) podem apresentar efeitos mais sérios na saúde")
                print ("\n")
                    
                
            elif (150 < mp10 <= 250) or (75 < mp25 <= 125) or (160 < o3 <= 200) or (13 < co <= 15) or (320 < no2 <= 1130) or (365 < so2 <= 800):
    
                print("\nQualidade do ar: Muito ruim")
                print ("\n\n")
                print ("Toda a população pode aresentar sintomas como tosse seca, cansaço, ardor nos olhos, nariz, e garganta e ainda falta de ar e respiração ofegante. Efeitos ainda mais graves à saúde de grupos sensíveis(crianças, idosos e pessoas com doenças respiratórias e cardíacas)")
                print ("\n")
                      
                
            elif (250 < mp10) or (125 < mp25) or (200 < o3) or (15 < co) or (1130 < no2) or (800 < so2):
    
                print("\nQualidade do ar: Pessima")
                print ("\n\n")
                print ("Toda a população pode apresentar sérios risco de manifestações de doenças respiratórias e cardiovasculares. Aumento de mortes prematuras em pessoas de rupos sensíveis")
                print ("\n")
                
            break

    if opt==0:
        print("\nObrigado por utilizar o sistema! Nos vemos em breve!")
        break
    
if opt==0:
    flag==False
    
    cur.close()
    conn.close()
    
                    



