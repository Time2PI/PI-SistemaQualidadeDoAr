import os as oo 

oo.system('cls')
# Leitura dos valores das amostras (Entradas)
mp10 = float(input("Informe o valor de MP10: "))
mp25 = float(input("Informe o valor de MP2,5: "))
o3 = float(input("Informe o valor de O3: "))
co = float(input("Informe o valor de CO: "))
no2 = float(input("Informe o valor de NO2: "))
so2 = float(input("Informe o valor de SO2: "))



#Validação dos valores informados
if (mp10 < 0) and (mp25 <= 0) and (o3 <= 0) and (co <= 0) and (no2 <= 0) and (so2 <= 0):
  
    print("Valores inválidos!")

# Verificação da qualidade do ar com base nos valores informados
# Exemplo: Se todos os valores da linha estiverem de acordo com a classificação de boa então imprime "Qualidade do ar: Boa"!
# Porém se algum valor estourar o limite, passa para a qualidade seguinte adequada.
if (0 <= mp10 <= 50) and (0 <= mp25 <= 25) and (0<= o3 <= 100) and (0<= co <= 9) and (0<= no2 <= 200) and (0<= so2 <= 20):
    
    print("Qualidade do ar: Boa")
    print ("\n\n")

elif (50 < mp10 <= 100) or (25 < mp25 <= 50) or (100 < o3 <= 130) or (9 < co <= 11) or (200 < no2 <= 240) or (20 < so2 <= 40):
    
    print("Qualidade do ar: Moderada")
    print ("\n")
    print ("Pessoas de grupos sensíveis(crianças, idosos e pessoas com doenças respiratórias e cardíacas) podem apresentar sintomas como tosse seca e cansaço. A populaçao em geral nao é afetada")
    print ("\n")

elif (100 < mp10 <= 150) or (50 < mp25 <= 75) or (130 < o3 <= 160) or (11 < co <= 13) or  (240 < no2 <= 320) or (40 < so2 <= 365):
    
    print("Qualidade do ar: Ruim")
    print ("\n\n")
    print ("Toda a população pode apresentar sintomas como tosse seca, cansaço, ardor nos olhos, nariz e garganta. Pessoas de grupos sensíveis(crianças, idosos e pessoas com doenças resiratórias e cardíacas) podem apresentar efeitos mais sérios na saúde")
    print ("\n")

elif (150 < mp10 <= 250) or (75 < mp25 <= 125) or (160 < o3 <= 200) or (13 < co <= 15) or (320 < no2 <= 1130) or (365 < so2 <= 800):
    
    print("Qualidade do ar: Muito ruim")
    print ("\n\n")
    print ("Toda a população pode aresentar sintomas como tosse seca, cansaço, ardor nos olhos, nariz, e garganta e ainda falta de ar e respiração ofegante. Efeitos ainda mais graves à saúde de grupos sensíveis(crianças, idosos e pessoas com doenças respiratórias e cardíacas)")
    print ("\n")

elif (250 < mp10) or (125 < mp25) or (200 < o3) or (15 < co) or (1130 < no2) or (800 < so2):
    
    print("Qualidade do ar: Pessima")
    print ("\n\n")
    print ("Toda a população pode apresentar sérios risco de manifestações de doenças respiratórias e cardiovasculares. Aumento de mortes prematuras em pessoas de rupos sensíveis")
    print ("\n")
    
