import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configuração do driver
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Define as credenciais e a URl
credenciais = pd.read_csv('users.csv')
username = credenciais.iloc[0]['username']
password = credenciais.iloc[0]['password']
url = "https://www.saucedemo.com"

# Acessa o site
driver.get(url)

# Realiza o login com as credenciais contidas no cvs
driver.find_element(By.ID, "user-name").send_keys(username)
driver.find_element(By.ID, "password").send_keys(password)
driver.find_element(By.ID, "login-button").click()

# Adiciona os produtos no carrinho
produtos = [
    "Test.allTheThings() T-Shirt (Red)",
    "Sauce Labs Bolt T-Shirt",
    "Sauce Labs Bike Light"
]
for produto in produtos:
    driver.find_element(By.XPATH, f"//div[text()='{produto}']/ancestor::div[@class='inventory_item']//button").click()

# Vai para o carrinho e faz o checkout
driver.find_element(By.ID, "shopping_cart_container").click()
driver.find_element(By.ID, "checkout").click()

# Preenche as informações de checkout
driver.find_element(By.ID, "first-name").send_keys("Eduardo")
driver.find_element(By.ID, "last-name").send_keys("Sales")
driver.find_element(By.ID, "postal-code").send_keys("99999999")
driver.find_element(By.ID, "continue").click()

# Pega o vlaor totol
preco_total = driver.find_element(By.CLASS_NAME, "summary_subtotal_label").text.split("$")[1]

# Finaliza a compra
driver.find_element(By.ID, "finish").click()

# Fecha o navegador
driver.quit()

# Mostra o valor total
print(f'Valor total foi de: ${preco_total}')


