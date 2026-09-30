from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


URL_DROPDOWN = "https://the-internet.herokuapp.com/dropdown"
URL_DYNAMIC = "https://the-internet.herokuapp.com/dynamic_loading/2"
URL_WIKI = "https://pt.wikipedia.org"


def abrir_nova_aba(driver, url):
    """Abre uma nova aba via window.open e só retorna após ela existir."""
    handles_antes = set(driver.window_handles)

    driver.execute_script("window.open(arguments[0], '_blank');", url)

    WebDriverWait(driver, 10).until(
        lambda d: len(set(d.window_handles) - handles_antes) >= 1
    )

    novos_handles = list(set(driver.window_handles) - handles_antes)
    if not novos_handles:
        raise RuntimeError(f"Não foi possível abrir uma nova aba: {url}")

    novo_handle = novos_handles[0]
    WebDriverWait(driver, 10).until(
        lambda d: novo_handle in d.window_handles
    )
    return novo_handle


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        # ============================================================
        # PARTE 1 - Headless, tamanho da janela e espera implícita
        # ============================================================
        driver.implicitly_wait(10)
        driver.set_window_size(1920, 1080)

        # ============================================================
        # PARTE 2 - Orquestração de abas
        # ============================================================
        driver.get(URL_DROPDOWN)
        aba0 = driver.current_window_handle
        handles_iniciais = set(driver.window_handles)

        aba1 = abrir_nova_aba(driver, URL_DYNAMIC)
        if len(driver.window_handles) <= len(handles_iniciais):
            raise RuntimeError("A segunda aba não foi reconhecida pelo Selenium.")

        aba2 = abrir_nova_aba(driver, URL_WIKI)
        if len(driver.window_handles) < 3:
            raise RuntimeError("A terceira aba não foi reconhecida pelo Selenium.")

        print(f"Abas abertas com sucesso: {len(driver.window_handles)}")

        # ============================================================
        # PARTE 3 - Dropdown na Aba 0
        # ============================================================
        driver.switch_to.window(aba0)

        select_element = driver.find_element(By.TAG_NAME, "select")
        select = Select(select_element)
        select.select_by_visible_text("Option 1")

        primeira_selecionada = select.first_selected_option
        valor_selecionado = primeira_selecionada.get_attribute("value")

        print(f"Dropdown selecionado: {primeira_selecionada.text}")
        print(f"Valor da opção selecionada: {valor_selecionado}")

        # ============================================================
        # PARTE 4 - Sincronização dinâmica na Aba 1
        # ============================================================
        driver.switch_to.window(aba1)

        start_button = driver.find_element(By.CSS_SELECTOR, "#start button")
        start_button.click()

        finish = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "finish"))
        )

        print(f"Texto encontrado na Aba 1: {finish.text}")

        # ============================================================
        # PARTE 5 - Extração de dados e evidência na Aba 2
        # ============================================================
        driver.switch_to.window(aba2)

        search = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "searchInput"))
        )
        search.clear()
        search.send_keys("Automação")

        # Qualquer link do menu lateral de navegação.
        # O seletor procura links dentro do painel de navegação.
        link_menu = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#vector-main-menu a")
            )
        )

        texto_link = link_menu.text.strip()
        href_link = link_menu.get_attribute("href")

        print(f"Texto visível do link: {texto_link}")
        print(f"Destino (href): {href_link}")

        driver.save_screenshot("evidencia_wiki.png")
        print("Screenshot salvo em: evidencia_wiki.png")

    except TimeoutException as exc:
        print(f"Tempo limite excedido durante a execução: {exc}")
        raise
    finally:
        # ============================================================
        # PARTE 6 - Encerramento
        # ============================================================
        driver.quit()
        print("Navegador encerrado com driver.quit().")


if __name__ == "__main__":
    main()
