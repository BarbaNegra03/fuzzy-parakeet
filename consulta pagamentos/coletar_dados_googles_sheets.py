import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

# Configurar a API do Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(credentials)

# Abrir a planilha de dados
spreadsheet = client.open('consultas_pagamentos')  # Substitua pelo nome da sua planilha
sheet = spreadsheet.sheet1

# Inicializar o WebDriver
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

print("WebDriver inicializado")

# Ler os dados dos clientes do Google Sheets
dados_clientes = sheet.get_all_records()

# Lista para armazenar os resultados
resultados = []

# 1 - Entrar na planilha e extrair os dados do cliente
for cliente in dados_clientes:
    nome = cliente['Nome']
    valor = cliente['Valor']
    cpf = cliente['CPF']
    vencimento = cliente['Vencimento']
    print(f"Processando: {nome}, {cpf}")
    print(valor)
    print(cpf)
    print(vencimento)

    # Abrir o site para cada CPF
    print("Abrindo site de consulta")
    driver.get('https://consultcpf-devaprender.netlify.app/')
    sleep(5)

    print("Site aberto")

    # Preencher o campo de pesquisa
    print("Preenchendo campo de pesquisa")
    campo_pesquisa = driver.find_element(By.XPATH, "//input[@id='cpfinput']")
    sleep(1)
    campo_pesquisa.send_keys(cpf)
    sleep(1)

    # Clicar no botão de pesquisa
    print("Clicando no botão de pesquisa")
    botao_pesquisar = driver.find_element(By.XPATH, "//button[@class='btn btn-custom btn-block mt-3']")
    sleep(1)
    botao_pesquisar.click()
    sleep(4)

    # Verificar o status
    print("Verificando status")
    status = driver.find_element(By.XPATH, "//span[@id='statusLabel']").text
    print(f"Status: {status}")

    if status == 'em dia':
        try:
            # 4 - Se estiver "em dia", pegar a data do pagamento e o método de pagamento
            data_pagamento = driver.find_element(By.XPATH, "//p[@id='paymentDate']").text
            metodo_pagamento = driver.find_element(By.XPATH, "//p[@id='paymentMethod']").text
        except:
            data_pagamento = "Não encontrado"
            metodo_pagamento = "Não encontrado"
        resultados.append([nome, valor, cpf, vencimento, 'em dia', data_pagamento, metodo_pagamento])
    else:
        # 5 - Caso contrário (se estiver atrasado), colocar o status como pendente
        resultados.append([nome, valor, cpf, vencimento, 'pendente', '', ''])

# Fechar o WebDriver no final do loop
driver.quit()
print("WebDriver fechado")

# Atualizar os resultados no Google Sheets
sheet.append_row(['Nome', 'Valor', 'CPF', 'Vencimento', 'Status', 'Data Pagamento', 'Método Pagamento'])
for resultado in resultados:
    print(f"Salvando resultado: {resultado}")
    sheet.append_row(resultado)

print("Resultados salvos no Google Sheets")
print("Dados Salvos:")
for resultado in resultados:
    print(resultado)
