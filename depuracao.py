from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Inicializar o WebDriver
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

print("WebDriver inicializado")

# Abrir o site desejado
driver.get('https://consultcpf-devaprender.netlify.app/')
print("Site de consulta aberto")

# Tentar interagir com o campo de pesquisa
try:
    # Usar WebDriverWait para esperar até que o campo de pesquisa esteja presente
    campo_pesquisa = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='cpfinput']"))
    )
    print("Campo de pesquisa encontrado pelo ID 'cpfinput'")
except:
    try:
        campo_pesquisa = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "cpfinput"))
        )
        print("Campo de pesquisa encontrado pelo NAME 'cpfinput'")
    except:
        try:
            campo_pesquisa = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='cpfinput']"))
            )
            print("Campo de pesquisa encontrado pelo CSS 'input[id=\"cpfinput\"]'")
        except Exception as e:
            print(f"Erro ao interagir com o site: {e}")
else:
    campo_pesquisa.send_keys("123.456.789-00")
    print("CPF preenchido")

# Fechar o WebDriver
driver.quit()
print("WebDriver fechado")
