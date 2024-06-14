#Bibliotecas
import PySimpleGUI as Ps
import pyodbc as bd
import smtplib as smt
import random
import os 
import time 
from datetime import date 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

TEMA_TELA = 'DarkRed2'

#Variaveis Globais
#string
driver = 'SQL Server Native Client 11.0'
server = 'DESKTOP-ENF1136\SQLEXPRESS'
database = 'OTTOBD'
username = None
password = None
trusted_connection = 'yes'
dir = 'C:/Logs'
arquivo = '/log-' + str(date.today()) + '.txt'
LoginSalvo = ''
#array
layout = []
tela_erro = []
tela_acesso = []
tela_senha = []
tela_codigo = []
Dados = [[''], [''], ['']]
#boolean
existe = False
existeEmail = False
ProgCancel = False
#objeto
arqlog = None
file = None
dados_conexao = None
conexao = None
cursor = None
servidor_email = None

#========================Funções====================
'''
=============================================================================
Função: RegistraLog(Operação, Descrição do Logger)
Descrição: Responsavel por acessar e escrever o logger 
Programador(a): Ighor Drummond
Data: 09/01/2024
=============================================================================
'''
def RegistraLog(opc, desc):
    #cria uma pasta temporaria para o log
    if opc == '1':
        try:
            os.mkdir(dir)
        except FileExistsError:
            arqlog = open(dir + arquivo, 'a') 
            desc = 'Sistema Acessado na Data: '
            arqlog.write(desc + time.asctime(time.localtime())  + '\n')    
            arqlog.close()
    else:
        #Abrir o arquivo Log
        arqlog = open(dir + arquivo, 'a') 
        arqlog.write('==============================Error=====================\n')
        arqlog.write( time.asctime(time.localtime()) + ' - ' + desc  + '\n')    
        arqlog.close()
        exit()

'''
=============================================================================
Função: ErrorTela(descrição, titulo)
Descrição: Responsavel por criar uma tela popup de erro 
Programador(a): Ighor Drummond
Data: 08/01/2024
=============================================================================
'''
def ErrorTela(details, title):
    Ps.theme(TEMA_TELA)
    Ps.popup(details, title=title)

'''
=============================================================================
Função: BDsenha(Nova Senha, Email)
Descrição: Responsavel por atualizar no banco a nova senha do usuario
Programador(a): Ighor Drummond
Data: 08/01/2024
=============================================================================
'''
def BDsenha(NovaSenha, Email):

    #cria a consulta para verificar existencia do email no banco
    Query = " UPDATE USERS "
    Query += " SET PASS_USER = '" + NovaSenha + "'"
    Query += " WHERE EMAIL_USER  = '" + Email + "'"

    try:
        #Recebe Conexão com o banco de dados
        cursor = conexao.cursor()
        #Executa Alteração contida na Query
        cursor.execute(Query)  
        cursor.commit()         
        cursor.close()
    except bd.ProgrammingError: 
        ErrorTela('Erro Imprevisto! Contate o suporte do sistema', 'Error_Fatal') 
        RegistraLog('2','(42000, "[42000] [Microsoft][SQL Server Native Client 11.0][SQL Server]Sintaxe incorreta  (SQLExecDirectW); [42000] [Microsoft][SQL Server Native Client 11.0][SQL Server]Aspas não fechadas depois da cadeia de caracteres ''.")')
'''
=============================================================================
Função: GeraCode()
Descrição: Responsavel por criar codigo de recuperação de senha
Programador(a): Ighor Drummond
Data: 08/01/2024
=============================================================================
'''
def GeraCode():
    GeraCod = ''

    #gera o codigo aleatoriamente
    for x in range(6):
        aleatorio = random.randint(0,9)
        GeraCod += str(aleatorio)

    return GeraCod    
'''
=============================================================================
Função: HostBd()
Descrição: Responsavel por criar conexão com o banco de dados
Programador(a): Ighor Drummond
Data: 07/01/2024
=============================================================================
'''
def HostBd():
    #faz conexão com o banco de dados
    dados_conexao = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TRUSTED_CONNECTION={trusted_connection}"
    #executa conexão
    try:
        return bd.connect(dados_conexao)
    except bd.OperationalError:
        ErrorTela('Erro Imprevisto! Contate o suporte do sistema', 'Error_Fatal')
        RegistraLog('2', '(08001, "[08001] [Microsoft][SQL Server Native Client 11.0]Valor inválido especificado para atributo da cadeia de conexão TRUSTED_CONNECTION (0) (SQLDriverConnect)") variavel trusted está sem o yes')
    except bd.InterfaceError: 
        ErrorTela('Erro Imprevisto! Contate o suporte do sistema', 'Error_Fatal')
        RegistraLog('2', 'IM002 [IM002] [Microsoft][ODBC Driver Manager] Nome da fonte de dados não encontrado e nenhum driver padrão especificado (0) (SQLDriverConnect)')
'''
=============================================================================
Função: HostEmail(Recebe o Email confirmado)
Descrição: Responsavel por criar conexão com o email
Programador(a): Ighor Drummond
Data: 08/01/2024
=============================================================================
'''
def HostEmail(Email):
    remetente = 'giullianaTavares@outlook.com'
    destinatario = [Email]
    conteudo = ''

    #prepara o conteúdo como codigo que sera enviado ao email
    CodGerado = GeraCode()
    conteudo = 'Seu Codigo de Verifição para troca de senha é: ' + CodGerado

    #Construção da Mensagem a ser enviada
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = Email
    msg['Subject'] = 'Não Responda - Codigo Gerado!'
    msg.attach(MIMEText(conteudo))    
    #mensagem para erros
    try:
        #estabelece a conexão com o email
        servidor_email = smt.SMTP('smtp-mail.outlook.com', 587)
        servidor_email.ehlo()

        if servidor_email.starttls() != None:
            #verifica conexão com o email
            #envia o email para o cliente informado
            servidor_email.login(remetente,'Drummond-1208')
            servidor_email.sendmail(remetente, destinatario[0], msg.as_string().encode('utf-8'))
        #finaliza a conexão com o servidor email
        servidor_email.quit()    
    except smt.SMTPServerDisconnected:  
        ErrorTela('Erro Imprevisto! Contate o suporte do sistema', 'Error_Fatal')
        RegistraLog('2', 'please run connect() first, O email para SMTP está invalido ou inativo!')
    except smt.SMTPNotSupportedError:
        ErrorTela('Erro Imprevisto! Contate o suporte do sistema', 'Error_Fatal')
        RegistraLog('2', 'SMTP AUTH extension not supported by server. Starttls Está com problemas ou falta do mesmo')
    except UnicodeEncodeError:
        ErrorTela('Erro Imprevisto! Contate o suporte do sistema', 'Error_Fatal')
        RegistraLog('2', 'ascii codec can t encode characters in position x-x: ordinal not in range(128), Modo UTF-8 Não está ativo na mensagem do email' )
    #retorna o codigo gerado
    return CodGerado

''' 
=============================================================================
Função: VerificaEmail(Recebe o Email Informado)
Descrição: Verifica se o Email informado existe no BD e se a conta está ativa
Programador(a): Ighor Drummond
Data: 08/01/2024
=============================================================================
'''
def VerificaEmail(Email):
    Query = ''
    valores2 = None
    ret = False

    #cria a consulta para verificar existencia do email no banco
    Query = " SELECT EMAIL_USER, ACTIVE_USER FROM USERS "
    Query += " WHERE EMAIL_USER = '" + Email +"' AND ACTIVE_USER = 'Y ' "

    #Recebe Conexão com o banco de dados
    cursor = conexao.cursor()
    #recebe o valor da consulta do banco
    try:
        valores2 = cursor.execute(Query).fetchall() 
    except bd.OperationalError:
        ErrorTela('Erro Imprevisto! Contate o suporte do sistema', 'Error_Fatal')
        RegistraLog('2', '(08001, "[08001] [Microsoft][SQL Server Native Client 11.0]Valor inválido especificado para atributo da cadeia de conexão TRUSTED_CONNECTION (0) (SQLDriverConnect)") variavel trusted está sem o yes' )

    if len(valores2) == 0:
        return ret
   
    if valores2[0][0] == Email and valores2[0][1] == 'Y ':
        ret = True

    return ret
    
'''
=============================================================================
Função: TrocaSenha()
Descrição: Responsavel por trocar a senha após validar a existencia do email
Programador(a): Ighor Drummond
Data: 08/01/2024
=============================================================================
'''
def TrocaSenha():
    CodGerado = ''
    Email = ''
    janela2 = None
    eventos2 = None
    valores2 = None
    lRet = False
    

    #Tema
    Ps.theme('DarkBrown1')
    #Tela Layout
    tela_senha = [
        [Ps.Text('Insira o Email: '), Ps.Input(key='ConfirmaEmail')],
        [Ps.Button('Confirmar'), Ps.Button('Cancelar')]
    ]
    #Janela
    janela2 = Ps.Window('Recupere a Senha:', tela_senha)

    while True:
        eventos2, valores2 = janela2.read() 

        #Caso o Usuario aperte em Cancelar       
        if eventos2 == 'Cancelar':
            janela2.close()
            janela2 = None
            return None
        
        #verifica se o usuario existe no bd
        if eventos2 == 'Confirmar' and valores2['ConfirmaEmail'] != '':
            lRet = VerificaEmail(valores2['ConfirmaEmail'])
        else: 
            ErrorTela('Informe o Email para prosseguir!',"Dados Faltando!")
            continue    
            
        if lRet == True:
            #Dispara codigo para o email
            CodGerado = HostEmail(valores2['ConfirmaEmail'])
            Email = valores2['ConfirmaEmail']
            break
        else:
            ErrorTela('Email Não Existe ou está inativado!' ,'Email Incorreto!')

    janela2.close()#fecha a janela   
    janela2 = None # Reseta a variavel para criar a tela de recuperação
    
    # tela pós envio do codigo -----------------------------------
    Ps.theme('DarkBrown1')
    #layout
    tela_codigo = [
        [Ps.Text('Insira o codigo informado via Email:'), Ps.Input(key='Codigo')],
        [Ps.Button('Prosseguir'), Ps.Button('Cancelar')]
    ]
    #Gera Tela
    janela2 = Ps.Window('Insira Codigo: ', tela_codigo)

    while True:
        eventos2, valores2 = janela2.read()
        
        #operação de cancelamento
        if eventos2 == 'Cancelar':
            janela2.close()
            janela2 = None
            return None  
        if  valores2['Codigo']  == CodGerado:
            break
        else: 
            ErrorTela('Codigo Errado! Tente Novamente' ,'Codigo Incorreto!') 
            continue   
    #fecha a janela e limpa variavel
    janela2.close()
    janela2 = None

    # tela para recuperar senha -----------------------------------
    Ps.theme('DarkBrown1')
    #Layout
    tela_senha = [
        [Ps.Text('Insira a Nova Senha: '), Ps.Input(key='NovaSenha', password_char='*')],
        [Ps.Text('Confirme a Nova Senha: '), Ps.Input(key='ConNovaSenha', password_char='*')],
        [Ps.Button('Finalizar'), Ps.Button('Cancelar')]
    ]
    #Janela
    janela2 = Ps.Window('Recupere a Senha:', tela_senha)

    while True:
        eventos2, valores2 = janela2.read()
        #Cancela Operação
        if eventos2 == 'Cancelar':
            janela2.close()
            janela2 = None
            return None                

        if valores2['NovaSenha'] == valores2['ConNovaSenha']:
            BDsenha(valores2['NovaSenha'], Email)
            break
        else:
            ErrorTela('Senhas não se correspondem!', 'As senhas não batem')

    #fecha a janela e limpa variavel
    janela2.close()
    janela2 = None            

'''
=============================================================================
Função: MontaQuery(Recebe o Email, Recebe a Senha)
Descrição: Responsavel por criar a query para busca e consulta
Programador(a): Ighor Drummond
Data: 07/01/2024
=============================================================================
'''
def MontaQuery(valor, valor2):
    Query = ''

    Query += " SELECT EMAIL_USER, PASS_USER, ACTIVE_USER FROM USERS "
    Query += " WHERE EMAIL_USER = '" + valor +"' AND PASS_USER = '" + valor2 +"' AND ACTIVE_USER = 'Y ' " 
    return Query
'''
=============================================================================
Função: VerificaLogin(Email, Senha)
Descrição: Responsavel por validar se a senha e o email está correto no banco
Programador(a): Ighor Drummond
Data: 07/01/2024
=============================================================================
'''
def VerificaLogin(email, senha):
    #Recebe Conexão com o banco de dados
    cursor = conexao.cursor()
    #recebe o valor da consulta do banco
    valores2 = cursor.execute(MontaQuery(email, senha)).fetchall() 

    #verifica se tem valores no vetor
    if len(valores2) == 0:
        return False
    #verifica se os dados estão corretos e o email ativo
    if valores2[0][0] == email and valores2[0][1] == senha and valores2[0][2] == 'Y ':
        return True  
'''
=============================================================================
Função: LeiaEmail(Linha que será lida)
Descrição: Responsavel por ler a linha e recuperar o login salvo
Programador(a): Ighor Drummond
Data: 07/01/2024
=============================================================================
'''    
def LeiaEmail(linha):
    #declaração de variaveis
    #string
    aux = ''
    #numerico
    cont2 = 0

    #verifica se a linha está vazia
    if linha != '':
        for x in linha:
            if x != ';':
                aux += x
            else:
                Dados[cont2] = aux
                aux = ''
                cont2 += 1  
    return None                      
'''
=============================================================================
Função: TelaLogin()
Descrição: Responsavel por construir e Recuperar os valores do Email e Senha
Programador(a): Ighor Drummond
Data: 07/01/2024
=============================================================================
'''
def TelaLogin():
    #declaração de variavies
    #string
    check = ''
    #abre o arquivo de logins salvos
    file = open('C:/Users/Drummond/Documents/FullStack/PYTHON/Src/src.pwd')
    LoginSalvo = file.read()
    file.close()#fecha arquivo após leitura  

    #verifica se há logins salvos
    if LoginSalvo != '':
        LeiaEmail(LoginSalvo)
        check = 'x'
    else:
        Dados[0] = ''
        Dados[1] = '' 
            
    #Layou da Janela
    Ps.theme('DarkBrown2')
    layout = [  
        [Ps.Text('Email'), Ps.Input(key='Email',default_text=Dados[0])],
        [Ps.Text('Senha'),Ps.Input(key='Senha', password_char='*',default_text=Dados[1])],
        [Ps.Checkbox('Salvar Login?', default=check)],
        [Ps.Button('Entrar'), Ps.Button('Mudar Senha')]
    ]

    #Janela
    janela = Ps.Window('Tela de Login', layout)

    #Recupera Valores
    while True:
        eventos, valores = janela.read()
        if eventos == Ps.WINDOW_CLOSED:
            ProgCancel = True
            break
        if eventos == 'Entrar':
            existeEmail = VerificaLogin(valores['Email'], valores['Senha'])

        if eventos == 'Mudar Senha':
            TrocaSenha()#troca senha 
            continue

        #cria um popup de erro caso o email estiver errado ou senha ou se a conta não está ativa
        if existeEmail == False:
            ErrorTela('Senha ou Email Incorretos, Por favor Insira Novamente!' ,"Dados Incorretos!")
            continue
        else: 
            #verifica se o usuario quer guardar o login salvo para proxima sessão
            file = open('C:/Users/Drummond/Documents/FullStack/PYTHON/Src/src.pwd', 'w')#abre o arquivo para reescrever

            if valores[0] == True:
                file.write(valores['Email'] + ';' + valores['Senha'] + ';') 
            else:
                file.write('') 
                
            file.close()    
            break
    #Fecha Janela Após Operação    
    janela.close()    
#=====================Função Pricipal===================    
'''
=============================================================================
Função: Função Principal
Descrição: Executará o Codigo de acordo com as ocorrências 
Programador(a): Ighor Drummond
Data: 07/01/2024
=============================================================================
'''  
#Abre Logger do Programa
RegistraLog('1', '')

#Cria conexão com o banco  
conexao = HostBd()

if conexao == None:
    ErrorTela('Não Foi Possivel Conectar ao Banco! Verifique a Internet e Tente Mais Tarde.' ,'Impossivel Conectar')
    #fecha arquivo log
    exit()#Finaliza o Programa

TelaLogin()#exibe a tela login

#Irá Contruir a Tela de Acesso
if ProgCancel == False:#se o programa não for cancelado, entrará na tela do tema
    print('')