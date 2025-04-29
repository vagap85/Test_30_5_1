import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def driver_1():
    # Настройка драйвера с неявным ожиданием
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver_path = r'C:\Users\dublk\PycharmProjects\Selena\chromedriver\chromedriver-win64\chromedriver.exe'
    service = webdriver.chrome.service.Service(driver_path)

    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)  # Неявное ожидание для всех элементов

    # Явные ожидания для авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.ID, 'email'))
    ).send_keys('vasya@mail.com')

    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.ID, 'pass'))
    ).send_keys('12345')

    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
    ).click()

    yield driver
    driver.quit()


def test_pet_cards(driver_1):
    """Тест проверяет карточки питомцев с комбинацией ожиданий"""

    # Явное ожидание заголовка
    WebDriverWait(driver_1, 15).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), "PetFriends")
    )

    # Неявное ожидание (implicitly_wait) для загрузки карточек
    cards = driver_1.find_elements(By.CSS_SELECTOR, '.card-deck .card')
    assert len(cards) > 0, "На странице нет карточек питомцев"

    photos_count = 0
    names = set()
    pets_data = set()

    for i, card in enumerate(cards, 1):
        try:
            # Фото (неявное ожидание через implicitly_wait)
            img = card.find_element(By.CSS_SELECTOR, '.card-img-top')
            img_src = img.get_attribute('src') or ''

            if img_src.strip() and not img_src.endswith(('.svg', '.png')):
                photos_count += 1

            # Имя (явное ожидание)
            name = WebDriverWait(card, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.card-title'))
            ).text.strip()
            assert name, f"У питомца {i} нет имени"

            # Описание (возраст и порода - явное ожидание)
            description = WebDriverWait(card, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.card-text'))
            ).text.strip()

            parts = description.split(', ')
            assert len(parts) == 2, f"Неверный формат описания у питомца {i}"
            breed, age = parts[0].strip(), parts[1].strip()

            assert breed and age, f"Неполные данные у питомца {i}"

            # Проверка уникальности
            assert name not in names, f"Повтор имени: {name}"
            names.add(name)

            pet_id = (name, breed, age)
            assert pet_id not in pets_data, f"Дубликат питомца: {pet_id}"
            pets_data.add(pet_id)

        except Exception as ex:
            print(f"Ошибка в карточке {i}: {str(ex)}")
            continue

    print(f"\nСтатистика:\nВсего: {len(cards)}\nС фото: {photos_count}")
    assert photos_count > 0, "Не найдено ни одного фото питомца"