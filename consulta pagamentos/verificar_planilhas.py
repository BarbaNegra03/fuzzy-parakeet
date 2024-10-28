import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Definir o escopo de acesso
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(credentials)

# Listar todas as planilhas acessíveis
spreadsheet_list = client.openall()
print("Planilhas acessíveis:")
for spreadsheet in spreadsheet_list:
    print(spreadsheet.title)

# Tentar abrir a planilha específica
try:
    spreadsheet = client.open('Consultas pagamentos')  # Certifique-se de usar o nome correto da planilha
    sheet = spreadsheet.sheet1
    dados = sheet.get_all_records()
    print(dados)
except gspread.exceptions.SpreadsheetNotFound:
    print("Planilha não encontrada. Certifique-se de que o nome está correto e de que você compartilhou a planilha com a conta de serviço.")
