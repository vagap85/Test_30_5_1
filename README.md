Файл для запуска теста- test_30_5_1.py

Тесты для проверки карточек питомцев и таблицы питомцев (явные и неявные ожидания элементов страницы)

Для запуска необходимо установить библиотеки: 
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

В терминале ввести: m pytest -v --driver Chrome --driver-path "Ваш путь до WebDriver"
