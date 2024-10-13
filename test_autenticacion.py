import pytest
from appium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

@pytest.fixture(scope="module")
def driver():
    capacidades_deseadas = {
        "platformName": "Android",
        "appium:platformVersion": "11",
        "appium:deviceName": "Small Phone API 35",
        "appium:appPackage": "com.coink.app",
        "appium:appActivity": "com.coink.app.MainActivity",
        "appium:automationName": "UIAutomator2",
        "appium:noReset": True,
        "appium:newCommandTimeout": 300
    }
    driver = webdriver.Remote("http://localhost:4723/wd/hub", capacidades_deseadas)
    yield driver
    driver.quit()

def test_autenticacion(driver):
    # Ingresar el número de teléfono
    driver.find_element(By.CLASS_NAME, "android.widget.EditText").send_keys("304 373 1112")
    
    # Pinchar en el botón INGRESAR
    driver.find_element(By.XPATH, "//android.widget.Button[@text='INGRESAR']").click()
    
    # Intento 1: Contraseña incorrecta
    driver.find_element(By.CLASS_NAME, "android.widget.EditText").send_keys("clave_invalida")
    driver.find_element(By.XPATH, "//android.widget.Button[@text='INGRESAR']").click()
    sleep(1)
    
    # Intento 2: Contraseña incorrecta
    driver.find_element(By.CLASS_NAME, "android.widget.EditText").send_keys("clave_invalida")
    driver.find_element(By.XPATH, "//android.widget.Button[@text='INGRESAR']").click()
    sleep(1)
    
    # Verificar mensaje de advertencia de 2 intentos restantes
    mensaje_advertencia = driver.find_element(By.CLASS_NAME, "android.view.View").text
    assert "quedan 2 intentos" in mensaje_advertencia
    
    # Intento 3: Contraseña incorrecta
    driver.find_element(By.CLASS_NAME, "android.widget.EditText").send_keys("clave_invalida")
    driver.find_element(By.XPATH, "//android.widget.Button[@text='INGRESAR']").click()
    sleep(1)
    
    # Verificar mensaje de bloqueo
    mensaje_bloqueo = driver.find_element(By.CLASS_NAME, "android.widget.TextView").text
    assert "Agotaste tus tres intentos para ingresar tu PIN por ahora. Intenta nuevamente en 14 minutos." in mensaje_bloqueo

def test_autenticacion_despues_espera(driver):
    # Esperar 15 minutos
    sleep(900)
    
    # Intentar autenticarse nuevamente con la contraseña correcta
    driver.find_element(By.CLASS_NAME, "android.widget.EditText").send_keys("304 373 1112")
    driver.find_element(By.XPATH, "//android.widget.Button[@text='INGRESAR']").click()
    driver.find_element(By.CLASS_NAME, "android.widget.EditText").send_keys("clave_valida")
    driver.find_element(By.XPATH, "//android.widget.Button[@text='INGRESAR']").click()
    
    # Verificar que la autenticación es posible
    mensaje_bienvenida = driver.find_element(By.CLASS_NAME, "android.widget.TextView").text
    assert "bienvenido" in mensaje_bienvenida