from playwright.sync_api import Playwright, sync_playwright
import csv
import time 

link = [] 

'''
Salva Json após Login
'''

def informacao():
    aRet = [] 
    dir = 'C:/Users/Drummond/Downloads/Itens.csv'

    with open(dir, 'r') as file:
        leitor = csv.reader(file)
        for linha in leitor:
            aRet += [linha[0].split(';')]
           
    return aRet

def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.pinterest.com/
    page.goto("https://www.nike.com.br/")

    page.get_by_role("button", name="Entrar").click()

    page.locator('//*[@id="username"]').fill(str(link[2][0]))
         #page.locator('//*[@id="username"]').fill("ighordrummond2001@gmail.com")
    page.get_by_role("button", name="continue").click()
    print('inserindo email')
        
    page.locator('//*[@id="password"]').fill(link[2][1])
    #page.locator('//*[@id="password"]').fill("Dh357676#")
    page.get_by_role("button", name="Entrar").click()
    print('inserindo senha')
        
    #adicionando codigo de verificação
    Cod = input("Digite o codigo de verificação: ")
    page.locator('//*[@id="send-code"]').fill(Cod)
    page.get_by_role("button", name="Continuar").click()
    print('inserindo codigo de verificação')

    time.sleep(5)
    # Save storage state into the file.
    context.storage_state(path="C:/Users/Drummond/Documents/FullStack/PYTHON/data/ighordrummond.json")

    # ---------------------
    context.close()
    browser.close()


link = informacao()

with sync_playwright() as playwright:
    run(playwright)