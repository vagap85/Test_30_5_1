from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


service = Service('C:/Users/dublk/PycharmProjects/Selena/chromedriver/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service)

driver.get('https://petfriends.skillfactory.ru/')

email_field = driver.find_element(By.XPATH, "//input[@name='email']")
email_field.send_keys("your_email@example.com")


driver.quit()
