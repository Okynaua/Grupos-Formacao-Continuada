import pandas as pd
import sys

#Cria o código do profissional
def code(pessoa):
    prof = dados_df.loc[dados_df['Nome'] == pessoa]
    cod = ''

    #Grupo
    cod += f'{g+1}'

    #Curso
    Curso = format(prof['Curso'])
    if 'Quimica e Biologia' in Curso: cod += 'D'
    elif 'Biologia' in Curso: cod += 'B'
    elif 'Ciências ' in Curso: cod += 'C'
    elif 'Engenharia de Pesca' in Curso: cod += 'E'
    elif 'Letras'  in Curso: cod += 'L'
    elif 'Farmacia' in Curso: cod += 'A'
    elif 'Normal Superior' in Curso: cod += 'N'
    elif 'Pedagogia' in Curso: cod += 'P'
    elif 'Química' in Curso: cod += 'Q'
    elif 'Física' in Curso: cod += 'F'

    #Escolaridade
    Esc = format(prof['Escolaridade'])
    if Esc == 'Graduação': cod += 'G'
    elif Esc == 'Mestrado': cod += 'M'
    elif Esc == 'Pós Graduação Latu Sensu': cod += 'P'
    elif Esc == 'Doutorado': cod += 'D'

    #Rede
    Rede = format(prof['Rede'])
    if Rede == 'Pública federal': cod += 'PF'
    elif Rede == 'Pública Municipal': cod += 'PM'
    elif Rede == 'Pública estadual': cod += 'PE'
    elif Rede == 'Privada': cod += 'PV'
    elif Rede == 'Pública estadual, e Pública municipal': cod += 'EM'
    elif Rede == 'Pública estadual, Pública federal': cod += 'EF'
    elif Rede == 'Pública estadual, Privada': cod += 'EP'
    elif Rede == 'Pública federal, Privada': cod += 'FP'
    elif Rede == 'Cursinho pré-vestibular voluntário' or Rede == 'Aulas particulares': cod += 'OT'
    else: cod += 'NA'

    #Tempo
    Temp = format(prof['Tempo'])
    if len(Temp) < 2: cod += f'0{Temp}'
    else: cod += Temp

    #Estado
    Num = format(prof['Número'])
    ddd = Num[:2]

    if len(Num) < 11: cod += 'ES'
    elif ddd == '27': cod += 'ES'
    elif ddd == '82': cod += 'AL'
    elif ddd == '32' or ddd == '34' or ddd == '31': cod += 'MG'
    elif ddd == '83': cod += 'PB'
    elif ddd == '49' or ddd == '48': cod += 'SC'
    elif ddd == '45': cod += 'PR'
    elif ddd == '21': cod += 'RJ'
    elif ddd == '96': cod += 'AP'
    elif ddd == '86': cod += 'PI'
    elif ddd == '66': cod += 'MT'
    elif ddd == '12': cod += 'SP' 
    elif ddd == '71': cod += 'BA'
    elif ddd == '79': cod += 'SE'
    elif ddd == '62': cod += 'GO'
    elif ddd == '87': cod += 'PE'
    
    return cod

#Remove o índice da Series transformada em String
def format(x):
    x = list(pd.Series.to_string(x))
    while x[0].isdigit(): x.pop(0)
    while x[0] == ' ': x.pop(0)

    y = ''
    for l in x: y += l
    return y

#Distribui os professores
def distribuir(prfs):
    professores = []

    #Pega os professores mestres ou doutores
    pmestres = prfs.loc[(prfs['Escolaridade'] == 'Mestrado') | (prfs['Escolaridade'] == 'Doutorado')]
    for p in pmestres['Nome']: professores.append(p)

    #Pega os professores com mais de 10 anos de atuação
    prfs_10 = prfs.loc[(dados_df['Tempo'] > 10) & (dados_df['Escolaridade'] != 'Mestrado') & (dados_df['Escolaridade'] != 'Doutorado')]
    for p in prfs_10['Nome']: professores.append(p)

    #Pega os professores com menos de 10 anos de atuação
    prfs_0 = prfs.loc[(dados_df['Tempo'] <= 10) & (dados_df['Escolaridade'] != 'Mestrado') & (dados_df['Escolaridade'] != 'Doutorado')]
    for p in prfs_0['Nome']: professores.append(p)

    global g

    #Distribui os professores entre os grupos
    while len(professores) != 0:
        grupos[g].append((professores[0], code(professores[0]))) #Adiciona ao determinado grupo o nome do professor e seu código

        g += 1 #Cicla o grupo
        if g >= 6: g = 0
        professores.pop(0) #Remove o professor adicionado  

#Importa a tabela excel
dados_df = pd.read_excel(r"C:\Users\samue\Desktop\Códigos\Pandas\Mamãe\inscrição2.xlsx")

#Formata o Tempo de Trabalho
for n, tempo in enumerate(dados_df['Tempo']):
    t = [l for l in str(tempo) if not l.isalpha() and l != ' ']
    tempo = ''.join(t)
    if tempo.isnumeric(): dados_df.loc[n, 'Tempo'] = int(tempo)
    else: dados_df.loc[n, 'Tempo'] = 0

#Formata o Número de Telefone
for n, num in enumerate(dados_df['Número']):
    nu = [l for l in str(num) if l.isnumeric()]
    num = ''.join(nu)
    dados_df.loc[n, 'Número'] = num


#Cria os grupos vazios
grupos = [[], [], [], [], [], []]

global g
g = 0

#Física
prfs = dados_df.loc[dados_df['Curso'] == 'Física']
distribuir(prfs)

#Biologia
prfs = dados_df.loc[dados_df['Curso'] == 'Biologia']
distribuir(prfs)

#Química
prfs = dados_df.loc[dados_df['Curso'] == 'Química']
distribuir(prfs)

#Letras
for curso in dados_df['Curso']: dados_df.loc[dados_df['Curso'] == curso, ['Curso']] = 'Letras' if 'Letras' in curso else curso #Padrozina o curso de Letras
prfs = dados_df.loc[dados_df['Curso'] == 'Letras']
distribuir(prfs)

#Pedagogia
prfs = dados_df.loc[dados_df['Curso'] == 'Pedagogia']
distribuir(prfs)

#Outros
prfs = dados_df.loc[(dados_df['Curso'] != 'Física') & (dados_df['Curso'] != 'Biologia') & (dados_df['Curso'] != 'Química') & (dados_df['Curso'] != 'Letras') & (dados_df['Curso'] != 'Pedagogia')]
distribuir(prfs)

#Salva os grupos
sys.stdout = open("grupos.txt", "w")

for g, grupo in enumerate(grupos):
    print(f'Grupo {g+1}: ({len(grupo)})')

    for prof, cod in grupo:
        print(f'({cod}) {prof}')
    print('\n')

sys.stdout.close()