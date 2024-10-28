from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Nome do arquivo JSON com as credenciais da conta de serviço
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Carregar as credenciais da conta de serviço
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# IDs das planilhas do Google Sheets que você quer acessar
SPREADSHEET_IDS = [
    '1leCGpz6ZrUXqJ2wvkgVWJDsuqEEpmVsj',
    '1q-N5MeMK8hvuwpvzxYuyUFRi-fv5VWWe',
    '1U12RlkABwOh8ukipoakNf3cfIgCcgYcU'
]

# Nome da aba e intervalo de células que você quer acessar
RANGE_NAME = 'Sheet1!A1:D100'

# Inicializa o cliente do Google Sheets API com a API Key
API_KEY = 'AIzaSyD1gch0wWafxsgapYlo5lNozOsM4u7B2bA'
service = build('sheets', 'v4', developerKey=API_KEY)

# Função para ler dados de uma planilha
def ler_dados(spreadsheet_id):
    try:
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                     range=RANGE_NAME).execute()
        values = result.get('values', [])
        return values
    except HttpError as error:
        print(f"Erro ao acessar planilha {spreadsheet_id}: {error}")
        return None

# Ler e exibir dados de cada planilha
for spreadsheet_id in SPREADSHEET_IDS:
    print(f"Lendo dados da planilha com ID: {spreadsheet_id}")
    values = ler_dados(spreadsheet_id)
    if not values:
        print('Nenhum dado encontrado.')
    else:
        for row in values:
            print(row)
