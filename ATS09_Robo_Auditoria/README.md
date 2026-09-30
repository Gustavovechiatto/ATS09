# ATS09 — Robô de Auditoria Multitarefa com Selenium

Implementação do desafio prático do **Exercício ATS09**, utilizando Selenium com Chromium em modo Headless.

## O que foi implementado

### Parte 1 — Configuração inicial
- Chromium configurado com `--headless=new`.
- Janela configurada para `1920x1080`.
- Espera implícita global de **10 segundos**.
- Opções adicionais para execução em servidor Linux/Armbian sem interface gráfica:
  - `--no-sandbox`
  - `--disable-dev-shm-usage`
  - `--disable-gpu`

### Parte 2 — Orquestração de abas
O script abre:
1. `https://the-internet.herokuapp.com/dropdown`
2. `https://the-internet.herokuapp.com/dynamic_loading/2`
3. `https://pt.wikipedia.org`

A abertura das abas é feita com `window.open()`.

Antes de trocar para uma nova aba, o código verifica se o número de `window_handles` aumentou e aguarda o novo identificador. Isso evita o problema `IndexError: list index out of range`.

### Parte 3 — Dropdown
Na primeira aba:
- localiza o elemento `<select>`;
- utiliza `selenium.webdriver.support.ui.Select`;
- seleciona `Option 1` pelo texto visível;
- utiliza `first_selected_option`;
- imprime o texto e o atributo `value` da opção selecionada.

### Parte 4 — Carregamento dinâmico
Na segunda aba:
- localiza e clica em `Start`;
- utiliza espera explícita de até **15 segundos**;
- aguarda o elemento `#finish` ficar visível;
- imprime o texto encontrado.

Assim, o projeto demonstra a combinação entre:
- espera implícita global de 10 segundos;
- espera explícita de 15 segundos para uma situação específica.

### Parte 5 — Wikipédia e evidência
Na terceira aba:
- localiza a barra de pesquisa;
- digita `Automação`;
- localiza um link do menu lateral;
- imprime:
  - texto visível;
  - atributo `href`;
- salva uma captura da tela como:

`evidencia_wiki.png`

### Parte 6 — Encerramento
O `driver.quit()` fica dentro de `finally`, garantindo que o navegador seja encerrado mesmo se ocorrer uma exceção durante a execução.

---

# Como executar

## 1. Requisitos

É necessário ter instalado:

- Python 3.10 ou superior;
- Google Chrome ou Chromium;
- pip.

O Selenium 4 utiliza o gerenciamento automático do driver nas versões atuais.

## 2. Criar ambiente virtual — recomendado

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / Armbian

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

## 4. Executar

```bash
python robo_auditoria.py
```

## 5. Resultado esperado

No terminal serão exibidas informações semelhantes a:

```text
Abas abertas com sucesso: 3
Dropdown selecionado: Option 1
Valor da opção selecionada: 1
Texto encontrado na Aba 1: Hello World!
Texto visível do link: ...
Destino (href): ...
Screenshot salvo em: evidencia_wiki.png
Navegador encerrado com driver.quit().
```

Os textos do menu da Wikipédia podem variar conforme a versão atual da página.

## 6. Evidência

Depois da execução, o arquivo abaixo será criado na mesma pasta:

```text
evidencia_wiki.png
```

Ele comprova visualmente a interação realizada na Wikipédia.

---

# Estrutura

```text
ATS09_Robo_Auditoria/
├── robo_auditoria.py
├── requirements.txt
└── README.md
```

---

# Observação para execução em Armbian

O script foi preparado para execução sem interface gráfica. O modo:

```python
--headless=new
```

faz o Chromium funcionar em background.

As opções `--no-sandbox` e `--disable-dev-shm-usage` também ajudam na execução em ambientes Linux/servidores, conforme o cenário proposto no exercício.

