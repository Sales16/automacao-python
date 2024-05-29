import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def configurar_driver():
    options = Options()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def credenciais(arquivo):
    credenciais = pd.read_csv(arquivo)
    return credenciais.iloc[0]['username'], credenciais.iloc[0]['password']

def realizar_login(driver, url, username, password):
    driver.get(url)
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()

def adicionar_produtos_no_carrinho(driver, produtos):
    for produto in produtos:
        driver.find_element(By.XPATH, f"//div[text()='{produto}']/ancestor::div[@class='inventory_item']//button").click()

def realizar_checkout(driver, first_name, last_name, postal_code):
    driver.find_element(By.ID, "shopping_cart_container").click()
    driver.find_element(By.ID, "checkout").click()
    driver.find_element(By.ID, "first-name").send_keys(first_name)
    driver.find_element(By.ID, "last-name").send_keys(last_name)
    driver.find_element(By.ID, "postal-code").send_keys(postal_code)
    driver.find_element(By.ID, "continue").click()

def obter_valor_total(driver):
    return driver.find_element(By.CLASS_NAME, "summary_subtotal_label").text.split("$")[1]

def finalizar_compra(driver):
    driver.find_element(By.ID, "finish").click()
    driver.quit()

def main():
    url = "https://www.saucedemo.com"
    produtos = [
        "Test.allTheThings() T-Shirt (Red)",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Bike Light"
    ]
    usuario, senha = credenciais('users.csv')

    driver = configurar_driver()
    realizar_login(driver, url, usuario, senha)
    adicionar_produtos_no_carrinho(driver, produtos)
    realizar_checkout(driver, "Eduardo", "Sales", "99999999")
    preco_total = obter_valor_total(driver)
    finalizar_compra(driver)
    
    print(f'Valor total foi de: ${preco_total}')

if __name__ == "__main__":
    main()
