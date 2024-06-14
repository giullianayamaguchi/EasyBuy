from playwright.sync_api import Playwright, sync_playwright
import time
import csv 
import os
import ctypes as pes
import subprocess as proc
from datetime import datetime, timezone, timedelta

'''
=============================================================================
Importa Dados Csv
=============================================================================
'''
#=====================================Variaveis Globais====================================
#array
link = [] 
args = []
datas = ['','']
path= ["C:/Users/Drummond/Documents/FullStack/PYTHON/data/giulliana.json","C:/Users/Drummond/Documents/FullStack/PYTHON/data/ighordrummond.json"]
#String
horario = ""
formato = "%H:%M:%S"
formato_data = '%d/%m/%Y'
dir_bat = 'C:/Users/Drummond/Documents/FullStack/PYTHON/data/Temp.bat'
ponto = 'Esperando o Tempo'
#Numerico
nCont = 0
browse = 0
#boolean
lSai = False


'''
=============================================================================
Função: automatização do site Nike
Descrição: Abrir página web e automatizar cadastro de informações
Programador(a): Giulliana Yamaguchi
Data: 07/01/2024
Documentos: https://playwright.dev/python/docs/locators
            https://playwright.dev/docs/api/class-keyboard    
            https://thats-it-code.com/playwright/playwright__save-authentication-state-and-login-atuomatically/        
=============================================================================
'''

#=====================================Funções====================================
def SubtraiSegundos(string_horario):
    data = datetime.strptime(string_horario, "%H:%M:%S")
    ret = ''
    segundos_a_subtrair = 8

    delta = timedelta(seconds=segundos_a_subtrair)

    data = data - delta

    ret = str(data.hour) + ':'
    ret += str(data.minute) + ':'
    ret += str(data.second) 

    return ret
    

'''
'''
def informacao():
    link = []
    aRet = [] 
    dir = 'C:/Users/Drummond/Downloads/Itens.csv'

    with open(dir, 'r') as file:
        leitor = csv.reader(file)
        for linha in leitor:
            aRet += [linha[0].split(';')]
           
    return aRet
'''
'''
def configure_firefox_context(context):
    # Configurações do Firefox para melhorar o desempenho
    context.set_default_timeout(7000)# Ajuste o timeout conforme necessário
    context.clear_permissions()
    context.set_offline(False)
     # Pode ser alterado com base no seu cenário

'''
'''
def auto(x):    
    lRet = True

    def run(playwright: Playwright, x) -> None:
        lRet = True
        #abrir navegador Firefox
        browser =  playwright.firefox.launch(args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-extensions',
                '--disable-software-rasterizer',
                '--disable-gpu',
                '--disable-breakpad',
                '--disable-ipc-flooding-protection',
                '--disable-client-side-phishing-detection',
                '--no-remote',
                '--disable-background-networking',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-databases',
                '--disable-offline-load-stale-cache',
                '--dns-prefetch-disable',
                '--no-pings',
                '--disable-prompt-on-repost',
                '--enable-async-updates',
                '--disable-popup-blocking',
                '--disable-restore-session-state',
                '--disable-search-geolocation-disclosure',
                '--disable-session-crashed-bubble',
                '--disable-session-restore',
                '--disable-startup-window-tracking',
                '--disable-sync',
                '--disable-web-security',
                '--disable-remote-fonts',
                '--disable-hang-monitor',
                '--disable-newtab-tile',
                '--disable-service-worker',
                '--disable-offline-mode',
                # Adicione argumentos específicos do Firefox aqui
            ],
            firefox_user_prefs={
                'browser.tabs.remote.autostart': False,
                'dom.ipc.processCount': 4,  # Ajuste o número de processos conforme necessário
                'network.http.pipelining': True,
                'network.http.proxy.pipelining': True,
                'network.http.pipelining.maxrequests': 8,
                'network.dns.disableIPv6': True,
                'browser.cache.memory.enable': True,
                'browser.cache.disk.enable': False,
                'browser.sessionhistory.max_total_viewers': 0,
                 # Adicione preferências específicas do Firefox aqui
            },
            headless= False)


        context = browser.new_context(storage_state=path[browse])
        configure_firefox_context(context)
        page_One = context.new_page()

        '''
        page.goto('https://www.nike.com.br/nav?sorting=DescReleaseDate')
        #login na conta
        page.get_by_role("button", name="Entrar").click()

        page.locator('//*[@id="username"]').fill(str(link[x][0]))
         #page.locator('//*[@id="username"]').fill("ighordrummond2001@gmail.com")
        page.get_by_role("button", name="continue").click()
        print('inserindo email')
        
        page.locator('//*[@id="password"]').fill(link[x][1])
        #page.locator('//*[@id="password"]').fill("Dh357676#")
        page.get_by_role("button", name="Entrar").click()
        print('inserindo senha')
        
        #adicionando codigo de verificação
        Cod = input("Digite o codigo de verificação: ")
        page.locator('//*[@id="send-code"]').fill(Cod)
        page.get_by_role("button", name="Continuar").click()
        print('inserindo codigo de verificação')
        '''
        #time.sleep(1800)
        #style='display: none !important;'
        #recarregar pagina 
        start_automa = time.time()
        #acessar tenis escolhido 
        page_One.goto(link[x][2])
        print('acessando link de compra')
        #Selecionar tamanho do tenis e adicionar ao carrinho
      
        page_One.get_by_test_id("product-size-"+link[x][3]).check()
            
        page_One.get_by_text('Compra rápida').click()
        #page_One.locator('//*[@id="__next"]/div[2]/div/div/div[3]/div[3]/div/button[2]').click()     
        page_One.close()
        page_Two = context.new_page()
        print('Acionando compra rápida \n')
              
        #start_automa = time.time()
        page_Two.goto('https://www.nike.com.br')
        page_Two.get_by_test_id('BagIcon').click()
        page_Two.get_by_text('Continuar').click()
        
        
        #acessando checkout
        #page_Two.goto('https://www.nike.com.br/checkout')
        
        #confirmar identificação''
        page_Two.get_by_test_id('checkout-continue-button').click()
        print('confirmando identificação \n')
        
        #confirmar pagamento
        
        page_Two.locator('//*[@id="cardNumber"]').fill(link[x][4])
        print('adicionando cartão \n')

        page_Two.get_by_placeholder("Nome impresso").fill(link[x][5])
        print('adicionando nome \n')

        page_Two.get_by_placeholder("MM/AA").fill(link[x][6])
        print('adicionando vencimento \n')

        page_Two.get_by_placeholder("CVV").fill(link[x][7])
        print('adicinando CVV \n')

        page_Two.get_by_test_id('ArrowDownIcon').click()
        

        page_Two.keyboard.press(link[x][8]+'+Enter')
        print('selecionando opção de parcelamento \n')
        
        end_automa = time.time()
        
        #confirmar finalização da compra
        print(end_automa - start_automa)
        #page.get_by_role("button", name="Finalizar compra").click()
        print('Compra finalizada com sucesso')
        #fechar janela de navegador

        # Save storage state into the file.
        context.close()
        browser.close()

        return True

    #chama def Run
    with sync_playwright() as playwright:
        lRet = run(playwright, x)

        if(lRet == False):
            return None

#=======================================Escopo===============================
#chamando funções
link = informacao()

for x in range(len(link)):

    if x == 0:
        continue
    
    if x > 1: 
        if link[x][0] == link[x-1][0]:
            browse += 1
            
    #limpa temp
    proc.run(dir_bat, shell=True)

    #formata o dia
    horario = datetime.now()
    dia = horario.strftime(formato_data)

    #valida se está no mesmo dia que drop
    if link[x][10] != dia:
        print('data não é do mesmo dia')
        exit()
    else:
        horario = datetime.now()
        drop =  horario.strftime(formato)
    '''
    if drop > link[x][9] :
        print('Horario do Item ' + str(x) + 'não está mais disponivel!')
        continue
    '''
    link[x][9] = SubtraiSegundos(link[x][9])

    while(drop >= link[x][9]):
               
        horario = datetime.now()
        drop =  horario.strftime(formato)

        if nCont == 3:
            nCont = 0
            ponto = 'Esperando dar Horario de Drop'

        os.system('cls') 
        ponto += '.' 
        print(ponto)    
        nCont +=1 

    auto(x)   

