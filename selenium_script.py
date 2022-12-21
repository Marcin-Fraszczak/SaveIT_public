import os

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def connect():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    chromedriver_location = "drivers/chromedriver"
    driver = webdriver.Chrome(chromedriver_location, chrome_options=chrome_options)
    driver.maximize_window()
    a = ActionChains(driver)

    url = 'https://marcinfraszczak.eu.pythonanywhere.com/'
    driver.get(url)

    username = os.environ.get('SEL_USERNAME')
    password = os.environ.get('SEL_PASSWORD')
    categories = ["SPORT", "FOOD", "BICYCLE", "HOUSING", "TRANSPORT", "FUN", "HEALTH"]
    counterparties = ["Biedronka", "LIDL", "TESCO", "ŻABKA", "PKP", "CERVELO",
                      "STARA ROMANA", "MPK", "CASTORAMA", "MULTIKINO", "DREWBUD"]
    wallets = ["PERSONAL", "BUSINESS"]
    plans = [
        {"name": "Minimalistic", "goal": 4000, "initial": 1000, "curve": "Parabolic"},
        {"name": "Like no tomorrow", "goal": 8000, "initial": 500, "curve": "Logarithmic"},
    ]

    # XPATHS:
    first_login = '// *[ @ id = "navbarSupportedContent"] / ul / li[2] / a'
    username_input = '//*[@id="id_username"]'
    password_input = '//*[@id="id_password"]'
    login_submit = '/html/body/div[4]/form/button'

    cat_menu = '//*[@id="navbarSupportedContent"]/ul/li[2]/a'
    add_category = '//*[@id="navbarSupportedContent"]/ul/li[2]/div/a[1]'
    cat_name_input = '//*[@id="id_name"]'
    cat_desc_input = '//*[@id="id_description"]'
    add_cat_submit = '/html/body/div[4]/form/button'

    cntp_menu = '//*[@id="navbarSupportedContent"]/ul/li[3]/a'
    add_cntp = '//*[@id="navbarSupportedContent"]/ul/li[3]/div/a[1]'
    cntp_name_input = '//*[@id="id_name"]'
    cntp_desc_input = '//*[@id="id_description"]'
    add_cntp_submit = '/html/body/div[4]/form/button'

    wallet_menu = '//*[@id="navbarSupportedContent"]/ul/li[4]/a'
    add_wallet = '//*[@id="navbarSupportedContent"]/ul/li[4]/div/a[1]'
    wallet_name_input = '//*[@id="id_name"]'
    wallet_desc_input = '//*[@id="id_description"]'
    add_wallet_submit = '/html/body/div[4]/form/button'

    plan_menu = '//*[@id="navbarSupportedContent"]/ul/li[5]/a'
    add_plan = '//*[@id="navbarSupportedContent"]/ul/li[5]/div/a[1]'
    plan_name_input = '//*[@id="id_name"]'
    plan_goal_input = '//*[@id="id_monthly_goal"]'
    plan_initial_input = '//*[@id="id_initial_value"]'
    plan_curve_list = '//*[@id="id_curve_type"]'
    plan_curve_option = ''
    add_plan_submit = '/html/body/div[4]/form/button'

    trans_menu = '//*[@id="navbarSupportedContent"]/ul/li[1]/a'
    add_trans = '//*[@id="navbarSupportedContent"]/ul/li[1]/div/a[1]'
    trans_date_input = '//*[@id="id_date"]'
    trans_value_input = '//*[@id="id_value"]'
    trans_is_profit_input = '//*[@id="id_is_profit"]'
    trans_desc_input = '//*[@id="id_description"]'
    trans_cat_input = '//*[@id="id_category"]'
    trans_cntp_input = '//*[@id="id_counterparty"]'
    trans_wallet_input = '//*[@id="id_wallet"]'


    # login
    driver.find_element(By.XPATH, first_login).click()
    driver.find_element(By.XPATH, username_input).send_keys(username)
    driver.find_element(By.XPATH, password_input).send_keys(password)
    driver.find_element(By.XPATH, login_submit).click()

    # # adding category
    # for cat_name in categories:
    #     cat_menu_button = driver.find_element(By.XPATH, cat_menu)
    #     a.move_to_element(cat_menu_button).perform()
    #     driver.find_element(By.XPATH, add_category).click()
    #     driver.find_element(By.XPATH, cat_name_input).send_keys(cat_name)
    #     driver.find_element(By.XPATH, cat_desc_input).send_keys(cat_name + "desc")
    #     driver.find_element(By.XPATH, add_cat_submit).click()

    # # adding counterparty
    # for cntp_name in counterparties:
    #     cntp_menu_button = driver.find_element(By.XPATH, cntp_menu)
    #     a.move_to_element(cntp_menu_button).perform()
    #     driver.find_element(By.XPATH, add_cntp).click()
    #     driver.find_element(By.XPATH, cntp_name_input).send_keys(cntp_name)
    #     driver.find_element(By.XPATH, cntp_desc_input).send_keys(cntp_name + "desc")
    #     driver.find_element(By.XPATH, add_cntp_submit).click()

    # # adding wallet
    # for wallet_name in wallets:
    #     wallet_menu_button = driver.find_element(By.XPATH, wallet_menu)
    #     a.move_to_element(wallet_menu_button).perform()
    #     driver.find_element(By.XPATH, add_wallet).click()
    #     driver.find_element(By.XPATH, wallet_name_input).send_keys(wallet_name)
    #     driver.find_element(By.XPATH, wallet_desc_input).send_keys(wallet_name + " expenses")
    #     driver.find_element(By.XPATH, add_wallet_submit).click()

    # adding savings_plan
    for plan in plans:
        plan_menu_button = driver.find_element(By.XPATH, plan_menu)
        a.move_to_element(plan_menu_button).perform()
        driver.find_element(By.XPATH, add_plan).click()
        driver.find_element(By.XPATH, plan_name_input).send_keys(plan["name"])
        driver.find_element(By.XPATH, plan_goal_input).send_keys(plan["goal"])
        driver.find_element(By.XPATH, plan_initial_input).send_keys(plan["initial"])
        curve_select = Select(driver.find_element(By.XPATH, plan_curve_list))
        curve_select.select_by_visible_text(plan["curve"])
        driver.find_element(By.XPATH, add_plan_submit).click()

    # adding transaction
    for plan in plans:
        trans_menu_button = driver.find_element(By.XPATH, trans_menu)
        a.move_to_element(trans_menu_button).perform()
        driver.find_element(By.XPATH, add_trans).click()


