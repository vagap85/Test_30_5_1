import pytest
import uuid
import os


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless=new")  # Для CI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return chrome_options


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture
def web_browser(request, selenium):
    browser = selenium
    browser.set_window_size(1400, 1000)

    yield browser

    if request.node.rep_call.failed:
        try:
            if not os.path.exists("screenshots/failures"):
                os.makedirs("screenshots/failures")

            screenshot_path = f"screenshots/failures/{request.node.name}_{uuid.uuid4()}.png"
            browser.save_screenshot(screenshot_path)
            print(f"\nСкриншот ошибки: {screenshot_path}")

            # Логирование
            with open("test_errors.log", "a") as f:
                f.write(f"\nТест {request.node.name} упал:\n")
                f.write(f"URL: {browser.current_url}\n")
                for log in browser.get_log("browser"):
                    f.write(f"{log}\n")
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")


def get_test_case_docstring(item):
    if not item._obj.__doc__:
        return item.nodeid

    docstring = item._obj.__doc__.strip()
    first_line = docstring.split("\n")[0].strip()

    if hasattr(item, "callspec"):
        params = item.callspec.params
        params_str = ", ".join([f'{k}="{v}"' for k, v in params.items()])
        first_line += f" [Параметры: {params_str}]"

    return first_line


def pytest_itemcollected(item):
    if item._obj.__doc__:
        item._nodeid = get_test_case_docstring(item)


def pytest_collection_finish(session):
    if session.config.option.collectonly:
        for item in session.items:
            print(get_test_case_docstring(item))
        pytest.exit("Done!")