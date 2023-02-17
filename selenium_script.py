import os
import time
from datetime import datetime, timedelta
from random import randint, choice

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def populate_python_anywhere():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    chromedriver_location = "drivers/chromedriver"
    driver = webdriver.Chrome(chromedriver_location, chrome_options=chrome_options)
    driver.maximize_window()
    a = ActionChains(driver)

    url = 'https://marcinfraszczak.eu.pythonanywhere.com/'
    driver.get(url)
    sleep_time = 2

    # username = os.environ.get('SEL_USERNAME')
    # email = os.environ.get('SEL_EMAIL')
    # password = os.environ.get('SEL_PASSWORD')
    username = 'user1'
    email = 'user1@gmail.com'
    password = 'Testpass123'

    categories = ["SPORT", "FOOD", "BICYCLE", "HOUSING", "TRANSPORT", "FUN", "HEALTH", "WORK"]
    counterparties = ["BIEDRONKA", "LIDL", "TESCO", "ŻABKA", "PKP", "CERVELO",
                      "STARA ROMANA", "MPK", "CASTORAMA", "MULTIKINO", "STALMET", "ITALINOX"]
    wallets = ["PERSONAL", "BUSINESS"]
    plans = [
        {"name": "Minimalistic", "goal": 4000, "initial": 1000, "curve": "Parabolic"},
        {"name": "Like no tomorrow", "goal": 8000, "initial": 500, "curve": "Logarithmic"},
    ]

    # XPATHS:
    sign_up = '//*[@id="navbarSupportedContent"]/ul/li[1]/a'
    sign_username_input = '//*[@id="id_username"]'
    sign_email_input = '//*[@id="id_email"]'
    sign_pass_input = '//*[@id="id_password1"]'
    sign_pass_conf_input = '//*[@id="id_password2"]'
    sign_submit = '/html/body/div[4]/form/button'

    first_login = '// *[ @ id = "navbarSupportedContent"] / ul / li[2] / a'
    username_input = '//*[@id="id_username"]'
    password_input = '//*[@id="id_password"]'
    login_submit = '/html/body/div[4]/form/button'

    cat_menu = '//*[@id="navbarSupportedContent"]/ul/li[2]/a'
    add_category = '//*[@id="navbarSupportedContent"]/ul/li[2]/div/a[1]'
    list_category = '//*[@id="navbarSupportedContent"]/ul/li[2]/div/a[2]'
    cat_name_input = '//*[@id="id_name"]'
    cat_desc_input = '//*[@id="id_description"]'
    add_cat_submit = '/html/body/div[4]/form/button'

    cntp_menu = '//*[@id="navbarSupportedContent"]/ul/li[3]/a'
    add_cntp = '//*[@id="navbarSupportedContent"]/ul/li[3]/div/a[1]'
    list_cntp = '//*[@id="navbarSupportedContent"]/ul/li[3]/div/a[2]'
    cntp_name_input = '//*[@id="id_name"]'
    cntp_desc_input = '//*[@id="id_description"]'
    add_cntp_submit = '/html/body/div[4]/form/button'

    wallet_menu = '//*[@id="navbarSupportedContent"]/ul/li[4]/a'
    add_wallet = '//*[@id="navbarSupportedContent"]/ul/li[4]/div/a[1]'
    list_wallet = '//*[@id="navbarSupportedContent"]/ul/li[4]/div/a[2]'
    wallet_name_input = '//*[@id="id_name"]'
    wallet_desc_input = '//*[@id="id_description"]'
    add_wallet_submit = '/html/body/div[4]/form/button'

    plan_menu = '//*[@id="navbarSupportedContent"]/ul/li[5]/a'
    add_plan = '//*[@id="navbarSupportedContent"]/ul/li[5]/div/a[1]'
    list_plan = '//*[@id="navbarSupportedContent"]/ul/li[5]/div/a[2]'
    plan_name_input = '//*[@id="id_name"]'
    plan_goal_input = '//*[@id="id_monthly_goal"]'
    plan_initial_input = '//*[@id="id_initial_value"]'
    plan_curve_list = '//*[@id="id_curve_type"]'
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
    add_trans_submit = '/html/body/div[4]/form/button'


    # register new user
    driver.find_element(By.XPATH, sign_up).click()
    driver.find_element(By.XPATH, sign_username_input).send_keys(username)
    driver.find_element(By.XPATH, sign_email_input).send_keys(email)
    driver.find_element(By.XPATH, sign_pass_input).send_keys(password)
    driver.find_element(By.XPATH, sign_pass_conf_input).send_keys(password)
    driver.find_element(By.XPATH, sign_submit).click()

    # login
    driver.find_element(By.XPATH, first_login).click()
    driver.find_element(By.XPATH, username_input).send_keys(username)
    driver.find_element(By.XPATH, password_input).send_keys(password)
    driver.find_element(By.XPATH, login_submit).click()

    # adding category
    for cat_name in categories:
        time.sleep(sleep_time)
        cat_menu_button = driver.find_element(By.XPATH, cat_menu)
        a.move_to_element(cat_menu_button).perform()
        driver.find_element(By.XPATH, add_category).click()
        driver.find_element(By.XPATH, cat_name_input).send_keys(cat_name)
        driver.find_element(By.XPATH, cat_desc_input).send_keys(cat_name + "desc")
        driver.find_element(By.XPATH, add_cat_submit).click()

    # removing default category
    time.sleep(sleep_time)
    cat_menu_button = driver.find_element(By.XPATH, cat_menu)
    a.move_to_element(cat_menu_button).perform()
    driver.find_element(By.XPATH, list_category).click()
    delete_category = '/html/body/div[4]/form[2]/button'
    default_category = driver.find_element(By.XPATH, "//a[contains(text(), 'DEFAULT CATEGORY')]")
    if default_category:
        default_category.click()
        driver.find_element(By.XPATH, delete_category).click()

    # adding counterparty
    for cntp_name in counterparties:
        time.sleep(sleep_time)
        cntp_menu_button = driver.find_element(By.XPATH, cntp_menu)
        a.move_to_element(cntp_menu_button).perform()
        driver.find_element(By.XPATH, add_cntp).click()
        driver.find_element(By.XPATH, cntp_name_input).send_keys(cntp_name)
        driver.find_element(By.XPATH, cntp_desc_input).send_keys(cntp_name + "desc")
        driver.find_element(By.XPATH, add_cntp_submit).click()

    # removing default counterparty
    time.sleep(sleep_time)
    cntp_menu_button = driver.find_element(By.XPATH, cntp_menu)
    a.move_to_element(cntp_menu_button).perform()
    driver.find_element(By.XPATH, list_cntp).click()
    delete_cntp = '/html/body/div[4]/form[2]/button'
    default_cntp = driver.find_element(By.XPATH, "//a[contains(text(), 'DEFAULT COUNTERPARTY')]")
    if default_cntp:
        default_cntp.click()
        driver.find_element(By.XPATH, delete_cntp).click()

    # adding wallet
    for wallet_name in wallets:
        time.sleep(sleep_time)
        wallet_menu_button = driver.find_element(By.XPATH, wallet_menu)
        a.move_to_element(wallet_menu_button).perform()
        driver.find_element(By.XPATH, add_wallet).click()
        driver.find_element(By.XPATH, wallet_name_input).send_keys(wallet_name)
        driver.find_element(By.XPATH, wallet_desc_input).send_keys(wallet_name + " expenses")
        driver.find_element(By.XPATH, add_wallet_submit).click()

    # removing default wallet
    time.sleep(sleep_time)
    wallet_menu_button = driver.find_element(By.XPATH, wallet_menu)
    a.move_to_element(wallet_menu_button).perform()
    driver.find_element(By.XPATH, list_wallet).click()
    delete_wallet = '/html/body/div[4]/form[2]/button'
    default_wallet = driver.find_element(By.XPATH, "//a[contains(text(), 'DEFAULT WALLET')]")
    if default_wallet:
        default_wallet.click()
        driver.find_element(By.XPATH, delete_wallet).click()

    # setting default wallet
    time.sleep(sleep_time)
    wallet_menu_button = driver.find_element(By.XPATH, wallet_menu)
    a.move_to_element(wallet_menu_button).perform()
    driver.find_element(By.XPATH, list_wallet).click()
    personal_wallet = driver.find_element(By.XPATH, "//div//div//a[contains(text(), 'PERSONAL')]")
    if personal_wallet:
        personal_wallet.find_element(By.XPATH, "//a[contains(text(), 'make default')]").click()

    # adding savings_plan
    for plan in plans:
        time.sleep(sleep_time)
        plan_menu_button = driver.find_element(By.XPATH, plan_menu)
        a.move_to_element(plan_menu_button).perform()
        driver.find_element(By.XPATH, add_plan).click()
        driver.find_element(By.XPATH, plan_name_input).send_keys(plan["name"])
        driver.find_element(By.XPATH, plan_goal_input).send_keys(plan["goal"])
        driver.find_element(By.XPATH, plan_initial_input).send_keys(plan["initial"])
        curve_select = Select(driver.find_element(By.XPATH, plan_curve_list))
        curve_select.select_by_visible_text(plan["curve"])
        driver.find_element(By.XPATH, add_plan_submit).click()

    # setting default plan
    time.sleep(sleep_time)
    plan_menu_button = driver.find_element(By.XPATH, plan_menu)
    a.move_to_element(plan_menu_button).perform()
    driver.find_element(By.XPATH, list_plan).click()
    personal_plan = driver.find_element(By.XPATH, "//div//div//a[contains(text(), 'MINIMALISTIC')]")
    if personal_plan:
        personal_plan.find_element(By.XPATH, "//a[contains(text(), 'make default')]").click()

    starting_date = datetime(year=2023, month=1, day=1).date()

    def get_days_till_today(start):
        # just today
        # stop = datetime.now().date()

        # arbitrary date
        stop = datetime(year=2023, month=3, day=1).date()
        return (stop - start).days

    def create_date_key(today):
        if int(today.month) <= 9:
            month = f"0{today.month}"
        else:
            month = today.month
        if int(today.day) <= 9:
            day = f"0{today.day}"
        else:
            day = today.day
        date_key = f"{month}-{day}-{today.year}"
        return date_key


    for i in range(get_days_till_today(starting_date)):
        today = starting_date + timedelta(days=i)

        # Salary
        if today.day == 10:
            time.sleep(sleep_time)
            trans_menu_button = driver.find_element(By.XPATH, trans_menu)
            a.move_to_element(trans_menu_button).perform()
            driver.find_element(By.XPATH, add_trans).click()
            time.sleep(0.5)
            driver.find_element(By.XPATH, trans_date_input).send_keys(create_date_key(today))
            driver.find_element(By.XPATH, trans_value_input).send_keys(4000)
            driver.find_element(By.XPATH, trans_is_profit_input).click()
            driver.find_element(By.XPATH, trans_desc_input).send_keys(f"salary")
            cat_select = Select(driver.find_element(By.XPATH, trans_cat_input))
            cat_select.select_by_visible_text("WORK")
            cntp_select = Select(driver.find_element(By.XPATH, trans_cntp_input))
            cntp_select.select_by_visible_text("MPK")
            wallet_select = Select(driver.find_element(By.XPATH, trans_wallet_input))
            wallet_select.select_by_visible_text("PERSONAL")
            driver.find_element(By.XPATH, add_trans_submit).click()

        no_of_transactions = randint(0, 3)

        # adding transaction
        for _ in range(no_of_transactions):
            time.sleep(sleep_time)
            trans_menu_button = driver.find_element(By.XPATH, trans_menu)
            a.move_to_element(trans_menu_button).perform()
            driver.find_element(By.XPATH, add_trans).click()
            time.sleep(0.5)
            driver.find_element(By.XPATH, trans_date_input).send_keys(create_date_key(today))
            driver.find_element(By.XPATH, trans_value_input).send_keys(randint(50, 100))
            is_profit = driver.find_element(By.XPATH, trans_is_profit_input)
            if randint(1, 5) == 1:
                is_profit.click()
            if randint(1, 10) == 1:
                driver.find_element(By.XPATH, trans_desc_input).send_keys(f"random desc")
            cat_select = Select(driver.find_element(By.XPATH, trans_cat_input))
            cat_select.select_by_visible_text(choice(categories))
            cntp_select = Select(driver.find_element(By.XPATH, trans_cntp_input))
            cntp_select.select_by_visible_text(choice(counterparties))
            wallet_select = Select(driver.find_element(By.XPATH, trans_wallet_input))
            if randint(1, 10) == 1:
                wallet_select.select_by_visible_text("BUSINESS")
            else:
                wallet_select.select_by_visible_text("PERSONAL")
            driver.find_element(By.XPATH, add_trans_submit).click()


if __name__ == '__main__':
    populate_python_anywhere()
