import os as oo 
import cx_Oracle

# Inserção de dados para conexão com banco de dados
host = input("Informe o nome do host: ")
port = input("Informe o número da porta: ")
service_name = input("Informe o nome do serviço do banco de dados: ")
username = input("Informe o nome do usuário: ")
password = input("Informe a senha do usuário: ")

# Cria uma conexão com o banco de dados
dsn_tns = cx_Oracle.makedsn(host, port, service_name=service_name)

conn = cx_Oracle.connect(username, password, dsn_tns)

cur = conn.cursor()

oo.system('cls')

# Leitura das amostras armazenadas com seus respectivo rótulos, além da leitura da média dos parâmetros

# Seleciona as colunas da tabela
sqlSelect= 'select mp10, mp25, o3, co, no2, so2 from qualidade_ar'
cur.execute(sqlSelect)
    
nomeC = [desc[0] for desc in cur.description]
print("\n",nomeC)

# Mostra o valor dos dados
rows = cur.fetchall()

for row in rows:
    print(row)
    
# Calcula a media de cada coluna
for i in range(len(nomeC)):
    cur.execute(f"SELECT AVG({nomeC[i]}) FROM qualidade_ar")
    med = cur.fetchone()[0]
    print(f"[\nMédia de {nomeC[i]}: {med}")
        
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

# Fecham-se o cursor do sql e sua conexão
cur.close()

conn.close()

# Validação dos valores informados
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


    