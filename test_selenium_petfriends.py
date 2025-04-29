from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_petfriends(selenium):
    """Тест авторизации на PetFriends с валидными данными."""
    selenium.get("https://petfriends.skillfactory.ru/")

    try:
        # Переход на страницу входа
        btn_newuser = WebDriverWait(selenium, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]"))
        )
        btn_newuser.click()

        btn_exist_acc = WebDriverWait(selenium, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "У меня уже есть аккаунт"))
        )
        btn_exist_acc.click()

        # Ввод данных
        field_email = WebDriverWait(selenium, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        field_email.clear()
        field_email.send_keys("vagap007@gmail.com")

        field_pass = WebDriverWait(selenium, 10).until(
            EC.presence_of_element_located((By.ID, "pass"))
        )
        field_pass.clear()
        field_pass.send_keys("12345")

        # Отправка формы
        btn_submit = WebDriverWait(selenium, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        btn_submit.click()

        # Проверка успешной авторизации
        WebDriverWait(selenium, 10).until(
            EC.url_contains("all_pets")
        )

    except Exception as e:
        print(f"Тест упал с ошибкой: {e}")
        raise  # conftest.py сделает скриншот