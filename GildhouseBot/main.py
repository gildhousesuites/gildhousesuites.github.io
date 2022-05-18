import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import shutil
from git import Repo
import os
from collections import OrderedDict
from datetime import datetime

# Arrowleaf Hair Studio = "https://www.schedulicity.com/scheduling/AHSHAE/services"
# Ashley Cleo Hair Studio = "https://www.vagaro.com/ashleycleohairstudio/book-now"
# Chroma = "https://www.vagaro.com/chromabzn/book-now"
# Embellish Hair Studio = "https://www.schedulicity.com/scheduling/EHS4EQ/services"
# Fringe = "https://www.vagaro.com/fringehairstudio406/book-now"
# Hyalite_Studio = "https://hyalitestudio.com/stylists/"
# KW_Studio = "https://www.schedulicity.com/scheduling/KSBEET7/services"
# Meraki_Hair_Styling = "https://www.schedulicity.com/scheduling/MHSB2B/services"
# R2 = "https://randirammell.glossgenius.com/services"
# Salon_South = "https://www.vagaro.com/salonsouth2/book-now"
# Studio_Souss = "https://www.schedulicity.com/scheduling/FSSDSZ/services"
# Thairapy = "https://www.schedulicity.com/scheduling/HMS5CW/services"
# Velvet = "https://www.vagaro.com/velvetstudio/book-now"
# Slicks_Wax_Skin = "https://square.site/book/06680NG66P1E5/slicks-wax-skin-bozeman-mt"
# Align_Skin_Massage = "https://www.schedulicity.com/scheduling/ASMDJU/services"
# Faze_Higher_Beauty = "https://www.schedulicity.com/scheduling/FSS6RM/services"
# Jamie_Burleigh_Permanent_Makeup = "https://jamie-burleigh-pmu.square.site/"
# Jenna_Bella = "https://www.schedulicity.com/scheduling/JBSXQL/services"
# Waxed_and_Tamed = "https://bookings.gettimely.com/waxedandtamed/book?uri=https%3A%2F%2Fbook.gettimely.com%2FBooking%2FLocation%2F128669%3Fmobile%3DTrue%26params%3D%25253fclient-login%25253dtrue"
# Good Karma Nail Studio = "https://www.schedulicity.com/scheduling/NASSMP/services"
# Wildflower = "https://www.schedulicity.com/scheduling/WNACSP/services"
# Jenna Bella Skin Care = "https://www.schedulicity.com/scheduling/JBSXQL/services"
# Vibrant_Life_Therapy = "https://vibrantlifetherapy.com/"
# American_Treasure_Barbershop = "https://www.schedulicity.com/scheduling/TBA9TC/services"
# INQ = "https://square.site/book/KX0RR40A42H7X/inq-bozeman-mt"


# Sapphire_Medical_Aesthetics = "https://sapphiremedicalaesthetics.myaestheticrecord.com/book/appointments" \
#                               "/MV8xMjU5Ml9jbGluaWNz"
# Shiloh_Medical_Clinic = "https://shilohmedicalclinic.com/"

def scrape_r2():
    from datetime import date

    tenants_dict = {
        "Randi Rammell": "https://randirammell.glossgenius.com/services"
    }

    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    # get today's date
    date = str(date.today())
    cur_month_num = str(datetime.now().month)

    datetime_object = datetime.strptime(cur_month_num, "%m")

    month_name = datetime_object.strftime("%b")
    print("Short name: ", month_name)

    # get just the day
    today = date[-2:]

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    availability = []

    for tenant, link in tenants_dict.items():
        driver.get(link)

        time.sleep(3)
        try:
            driver.find_element(By.XPATH, "/html/body/div/div/div[3]/div/div[2]/ul/li[1]/div/div[2]/button").click()
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        try:
            driver.find_element(By.XPATH, "/html/body/div/div/div[3]/div/div[2]/div[1]/a").click()
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        try:
            calendar_day = driver.find_element(By.XPATH, "//*[text()='{0}']".format(today))
            x = calendar_day.get_attribute("aria-disabled")
            if x == "false":
                print(tenant + " has availability!")
                availability.append(tenant)
            else:
                print(tenant + " has no availability :(")

        except (Exception,) as e:
            print(e)
            send_email()

    print(availability)
    update_html(availability, tenants_dict)


def scrape_leighann_schreiber():
    from datetime import date

    tenants_dict = {
        "Leighann Schreiber": "https://square.site/appointments/book/E19YCCAZSMB66/leighann-schreiber-bozeman-mt",
    }

    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    # get today's date
    date = str(date.today())
    cur_month_num = str(datetime.now().month)

    datetime_object = datetime.strptime(cur_month_num, "%m")

    month_name = datetime_object.strftime("%b")
    print("Short name: ", month_name)

    # get just the day
    today = date[-2:]

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    availability = []

    for tenant, link in tenants_dict.items():
        driver.get(link)

        time.sleep(3)

        if "Closed today" in driver.page_source:
            print(tenant + " has no availability :(")
            continue

        time.sleep(3)

        try:
            driver.find_element(By.XPATH, "/html/body/div/section/section/main/div/section[1]/a[2]/div/h5").click()
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        try:
            driver.find_element(By.XPATH, "//*[text()='Continue']").click()
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        try:
            if month_name not in driver.page_source:
                print(tenant + " has no availability :(")
                continue
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        try:
            calendar_day = driver.find_element(By.XPATH, "//*[text()='{0}']".format(today))
            x = calendar_day.get_attribute("class")
            if "--highlighted" in x:
                availability.append(tenant)
                print(tenant + " has availability!")
            else:
                print(tenant + " has no availability :(")
        except (Exception,) as e:
            print(e)
            send_email()

    print(availability)
    update_html(availability, tenants_dict)


# select shortest appointment slot for maximum availability
def scrape_haley_walsh():
    from datetime import date

    tenants_dict = {
        "Haley Walsh": "https://square.site/book/7041X3ZARVWF0/haley-bozeman-mt"
    }

    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    # get today's date
    date = str(date.today())
    cur_month_num = str(datetime.now().month)

    datetime_object = datetime.strptime(cur_month_num, "%m")

    month_name = datetime_object.strftime("%b")
    print("Short name: ", month_name)

    # get just the day
    today = date[-2:]

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    availability = []

    for tenant, link in tenants_dict.items():
        driver.get(link)

        time.sleep(3)

        if "Closed today" in driver.page_source:
            print(tenant + " has no availability :(")
            continue

        time.sleep(3)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(1)

        try:
            driver.find_element(By.XPATH,
                                "/html/body/div/section/section/main/div/section[1]/a[27]/div/h5/span").click()
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        time.sleep(3)

        try:
            if month_name not in driver.page_source:
                print(tenant + " has no availability :(")
                continue
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        try:
            calendar_day = driver.find_element(By.XPATH, "//*[text()='{0}']".format(today))
            x = calendar_day.get_attribute("class")
            if "--highlighted" in x:
                availability.append(tenant)
                print(tenant + " has availability!")
            else:
                print(tenant + " has no availability :(")
        except (Exception,) as e:
            print(e)
            send_email()

    print(availability)
    update_html(availability, tenants_dict)


# select shortest appointment slot for maximum availability
def scrape_tara_ashley():
    from datetime import date

    tenants_dict = {
        "Tara Ashley": "https://hairbytara-108877.square.site/"
    }

    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    # get today's date
    date = str(date.today())
    cur_month_num = str(datetime.now().month)

    datetime_object = datetime.strptime(cur_month_num, "%m")

    month_name = datetime_object.strftime("%b")
    print("Short name: ", month_name)

    # get just the day
    today = date[-2:]

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    availability = []

    for tenant, link in tenants_dict.items():
        driver.get(link)

        time.sleep(6)

        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[1]/div/div/div[2]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div[13]/div/div/div[2]/div/div[1]/div/button/span").click()
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(6)

        frame = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/div/div/div/div[1]/div/iframe")
        driver.switch_to.frame(frame)

        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/nav/div/button").click()

        time.sleep(3)

        try:
            if month_name not in driver.page_source:
                print(tenant + " has no availability :(")
                continue
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        try:
            calendar_day = driver.find_element(By.XPATH, "//*[text()='{0}']".format(today))
            x = calendar_day.get_attribute("class")
            if "--highlighted" in x:
                availability.append(tenant)
                print(tenant + " has availability!")
            else:
                print(tenant + " has no availability :(")
        except (Exception,) as e:
            print(e)
            send_email()

    print(availability)
    update_html(availability, tenants_dict)


# select shortest appointment slot for maximum availability
def scrape_slicks():
    from datetime import date

    tenants_dict = {
        "Wax & Skin Studio": "https://square.site/book/06680NG66P1E5/slicks-wax-skin-bozeman-mt"
    }

    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    # get today's date
    date = str(date.today())
    cur_month_num = str(datetime.now().month)

    datetime_object = datetime.strptime(cur_month_num, "%m")

    month_name = datetime_object.strftime("%b")
    print("Short name: ", month_name)

    # get just the day
    today = date[-2:]

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    availability = []

    for tenant, link in tenants_dict.items():
        driver.get(link)

        time.sleep(3)

        if "Closed today" in driver.page_source:
            print(tenant + " has no availability :(")
            continue

        time.sleep(3)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(1)

        try:
            # wax - chin
            driver.find_element(By.XPATH, "/html/body/div/section/section/main/div/section[1]/a[42]/div/h5/span").click()
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/nav/div/button").click()
        except (Exception,) as e:
            print(e)
            send_email()

        try:
            if month_name not in driver.page_source:
                print(tenant + " has no availability :(")
                continue
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        try:
            calendar_day = driver.find_element(By.XPATH, "//*[text()='{0}']".format(today))
            x = calendar_day.get_attribute("class")
            if "--highlighted" in x:
                availability.append(tenant)
                print(tenant + " has availability!")
            else:
                print(tenant + " has no availability :(")
        except (Exception,) as e:
            print(e)
            send_email()

    print(availability)
    update_html(availability, tenants_dict)


def scrape_vagaro():
    from datetime import date

    vagaro_dict = {
        "Ashley Cleo Hair Studio": "https://www.vagaro.com/ashleycleohairstudio/book-now"
        # "CHROMA": "https://www.vagaro.com/chromabzn/book-now",  # defaults to tomorrow's date?
        #  "Fringe": "https://www.vagaro.com/fringehairstudio406/book-now", defaults to tomorrow's date, probably
        # does not want same-day appointments
    }

    chrome_options = Options()

    # can't use headless as it breaks move_to_element_with_offset
    # chrome_options.add_argument("--headless")

    # get today's date
    date = str(date.today())

    # get just the day
    today = date[-2:]

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()

    availability = []

    for tenant, link in vagaro_dict.items():
        driver.get(link)

        time.sleep(3)
        el = driver.find_element(By.XPATH,
                                 "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div[3]/ul/li/input")
        driver.find_element(By.XPATH,
                            "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div[3]/ul/li/input").click()

        time.sleep(3)

        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(el, 60, 100)
        action.click()
        action.perform()

        time.sleep(3)
        driver.find_element(By.XPATH,
                            "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[2]/div[1]/div/div[2]/a").click()

        time.sleep(3)
        sorry = driver.find_element(By.XPATH,
                                    "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[3]/div[5]/div/div[3]")

        if "Sorry" not in sorry.text:
            # they have availability
            availability.append(tenant)
            print(tenant + " has availability!")
        else:
            print(tenant + " has no availability :(")

    print(availability)
    update_html(availability, vagaro_dict)


def scrape_libby_hendrix():
    from datetime import date

    vagaro_dict = {
        "Libby Hendrix": "https://www.vagaro.com/velvetstudio/book-now"
    }

    chrome_options = Options()

    # can't use headless as it breaks move_to_element_with_offset
    # chrome_options.add_argument("--headless")

    # get today's date
    date = str(date.today())

    # get just the day
    today = date[-2:]

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()

    availability = []

    for tenant, link in vagaro_dict.items():
        driver.get(link)

        time.sleep(3)
        el = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div[3]/ul/li/input")
        driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div[3]/ul/li/input").click()

        time.sleep(3)

        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(el, 60, 210)
        action.click()
        action.perform()

        time.sleep(3)

        driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/span/span[1]/span/span[1]/li/input").click()
        el = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/span/span[1]/span/span[1]/li/input")

        time.sleep(3)

        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(el, 60, 140)
        action.click()
        action.perform()

        time.sleep(3)

        driver.find_element(By.XPATH, "//*[text()='Search']").click()

        time.sleep(5)

        driver.find_element(By.XPATH, "//*[text()='Search']").click()

        time.sleep(5)

        sorry = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[3]/div[5]/div/div[3]")

        if "Sorry" not in sorry.text:
            # they have availability
            availability.append(tenant)
            print(tenant + " has availability!")
        else:
            print(tenant + " has no availability :(")

    print(availability)
    update_html(availability, vagaro_dict)


def scrape_jenn_sarchet():
    from datetime import date

    vagaro_dict = {
        "Jenn Sarchet": "https://www.vagaro.com/velvetstudio/book-now"
    }

    chrome_options = Options()

    # can't use headless as it breaks move_to_element_with_offset
    # chrome_options.add_argument("--headless")

    # get today's date
    date = str(date.today())

    # get just the day
    today = date[-2:]

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()

    availability = []

    for tenant, link in vagaro_dict.items():
        driver.get(link)

        time.sleep(3)
        el = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div[3]/ul/li/input")
        driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div[3]/ul/li/input").click()

        time.sleep(3)

        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(el, 60, 210)
        action.click()
        action.perform()

        time.sleep(3)

        driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/span/span[1]/span/span[1]/li/input").click()
        el = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/span/span[1]/span/span[1]/li/input")

        time.sleep(3)

        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(el, 60, 183)
        action.click()
        action.perform()

        time.sleep(3)

        driver.find_element(By.XPATH, "//*[text()='Search']").click()

        time.sleep(5)

        driver.find_element(By.XPATH, "//*[text()='Search']").click()

        time.sleep(5)

        sorry = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[3]/div[5]/div/div[3]")

        if "Sorry" not in sorry.text:
            # they have availability
            availability.append(tenant)
            print(tenant + " has availability!")
        else:
            print(tenant + " has no availability :(")

    print(availability)
    update_html(availability, vagaro_dict)


def scrape_jodi_griffith():
    from datetime import date

    vagaro_dict = {
        "Jodi Griffith": "https://www.vagaro.com/salonsouth2/book-now"
    }

    chrome_options = Options()

    # can't use headless as it breaks move_to_element_with_offset
    # chrome_options.add_argument("--headless")

    # get today's date
    date = str(date.today())

    # get just the day
    today = date[-2:]

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()

    availability = []

    for tenant, link in vagaro_dict.items():
        driver.get(link)

        time.sleep(3)
        el = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div[3]/ul/li/input")
        driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div[3]/ul/li/input").click()

        time.sleep(3)

        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(el, 60, 210)
        action.click()
        action.perform()

        time.sleep(3)

        driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/span/span[1]/span/span[1]/li/input").click()
        el = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/span/span[1]/span/span[1]/li/input")

        time.sleep(3)

        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(el, 60, 140)
        action.click()
        action.perform()

        time.sleep(3)

        driver.find_element(By.XPATH, "//*[text()='Search']").click()

        time.sleep(5)

        driver.find_element(By.XPATH, "//*[text()='Search']").click()

        time.sleep(5)

        sorry = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[3]/div[5]/div/div[3]")

        if "Sorry" not in sorry.text:
            # they have availability
            availability.append(tenant)
            print(tenant + " has availability!")
        else:
            print(tenant + " has no availability :(")

    print(availability)
    update_html(availability, vagaro_dict)


def scrape_cheree_ryan():
    from datetime import date

    vagaro_dict = {
        "Cheree Ryan": "https://www.vagaro.com/salonsouth2/book-now"
    }

    chrome_options = Options()

    # can't use headless as it breaks move_to_element_with_offset
    # chrome_options.add_argument("--headless")

    # get today's date
    date = str(date.today())

    # get just the day
    today = date[-2:]

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()

    availability = []

    for tenant, link in vagaro_dict.items():
        driver.get(link)

        time.sleep(3)
        el = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div[3]/ul/li/input")
        driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div[3]/ul/li/input").click()

        time.sleep(3)

        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(el, 60, 170)
        action.click()
        action.perform()

        time.sleep(3)

        driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/span/span[1]/span/span[1]/li/input").click()
        el = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/span/span[1]/span/span[1]/li/input")

        time.sleep(3)

        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(el, 60, 183)
        action.click()
        action.perform()

        time.sleep(3)

        driver.find_element(By.XPATH, "//*[text()='Search']").click()

        time.sleep(5)

        driver.find_element(By.XPATH, "//*[text()='Search']").click()

        time.sleep(5)

        sorry = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[1]/vg-custom-component/div/div[1]/div/div[3]/div[5]/div/div[3]")

        if "Sorry" not in sorry.text:
            # they have availability
            availability.append(tenant)
            print(tenant + " has availability!")
        else:
            print(tenant + " has no availability :(")

    print(availability)
    update_html(availability, vagaro_dict)


def scrape_jamie_burleigh():
    from datetime import date

    tenants_dict = {
        "Jamie Burleigh Permanent Makeup": "https://jamie-burleigh-pmu.square.site/"
    }

    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    # get today's date
    date = str(date.today())
    cur_month_num = str(datetime.now().month)

    datetime_object = datetime.strptime(cur_month_num, "%m")

    month_name = datetime_object.strftime("%b")
    print("Short name: ", month_name)

    # get just the day
    today = date[-2:]

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    availability = []

    for tenant, link in tenants_dict.items():
        driver.get(link)

        time.sleep(3)

        if "Closed today" in driver.page_source:
            print(tenant + " has no availability :(")
            continue

        time.sleep(3)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(1)

        try:
            # lip wax
            driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div[1]/div/div/div[2]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div[17]/div/div/div[2]/div/div[1]/div/button/span/span[1]").click()
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(6)

        frame = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/div/div/div/div[1]/div/iframe")
        driver.switch_to.frame(frame)

        time.sleep(1)

        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/nav/div/button").click()
        except (Exception,) as e:
            print(e)
            send_email()

        try:
            if month_name not in driver.page_source:
                print(tenant + " has no availability :(")
                continue
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        try:
            calendar_day = driver.find_element(By.XPATH, "//*[text()='{0}']".format(today))
            x = calendar_day.get_attribute("class")
            if "--highlighted" in x:
                availability.append(tenant)
                print(tenant + " has availability!")
            else:
                print(tenant + " has no availability :(")
        except (Exception,) as e:
            print(e)
            send_email()

    print(availability)
    update_html(availability, tenants_dict)


def scrape_waxed_and_tamed():
    from datetime import date

    tenants_dict = {
        "Waxed & Tamed": "https://bookings.gettimely.com/waxedandtamed/book?uri=https%3A%2F%2Fbook.gettimely.com%2FBooking%2FLocation%2F128669%3Fmobile%3DTrue%26params%3D%25253fclient-login%25253dtrue"
    }

    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    # get today's date
    date = str(date.today())
    cur_month_num = str(datetime.now().month)

    datetime_object = datetime.strptime(cur_month_num, "%m")

    month_name = datetime_object.strftime("%b")
    print("Short name: ", month_name)

    # get just the day
    today = date[-2:]

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    availability = []

    for tenant, link in tenants_dict.items():
        driver.get(link)

        time.sleep(3)

        frame = driver.find_element(By.XPATH, "/html/body/div/main/div/div/iframe")
        driver.switch_to.frame(frame)

        try:
            # lip wax
            driver.find_element(By.XPATH, "/html/body/div[1]/form/div[1]/div/div[1]/div[3]/div/div[2]/div/div/label[7]/label/span").click()
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/form/div[2]/button").click()
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        try:
            if month_name not in driver.page_source:
                print(tenant + " has no availability :(")
                continue
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        try:
            calendar_day = driver.find_element(By.XPATH, "//*[text()='{0}']".format(today))
            # get parent element since the class attribute we're looking for is stored there
            parent_element = calendar_day.find_element(By.XPATH, "..")
            x = parent_element.get_attribute("class")

            if "unselectable" not in x:
                availability.append(tenant)
                print(tenant + " has availability!")
            else:
                print(tenant + " has no availability :(")
        except (Exception,) as e:
            print(e)
            send_email()

    print(availability)
    update_html(availability, tenants_dict)


def scrape_sapphire():
    from datetime import date

    tenants_dict = {
        "Sapphire Medical Aesthetics": "https://sapphiremedicalaesthetics.myaestheticrecord.com/book/appointments/MV8xMjU5Ml9jbGluaWNz"
    }

    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    # get today's date
    date = str(date.today())
    cur_month_num = str(datetime.now().month)

    datetime_object = datetime.strptime(cur_month_num, "%m")

    month_name = datetime_object.strftime("%b")
    print("Short name: ", month_name)

    # get just the day
    today = date[-2:]

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    availability = []

    for tenant, link in tenants_dict.items():
        driver.get(link)

        time.sleep(3)

        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div/input").click()
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div[1]/h4/a").click()
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/div[3]/div[1]/label").click()
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[2]/button").click()
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[3]/input[2]").click()
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div[3]/button").click()
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        if month_name not in driver.page_source:
            print(tenant + " has no availability :(")
            continue

        time.sleep(3)

        try:
            calendar_day = driver.find_element(By.XPATH, "//*[text()='{0}']".format(today))
            x = calendar_day.get_attribute("aria-disabled")
            if x == "true":
                print(tenant + " has no availability :(")
            else:
                availability.append(tenant)
                print(tenant + " has availability!")
        except (Exception,) as e:
            print(e)
            send_email()

    print(availability)
    update_html(availability, tenants_dict)


def scrape_inq():
    from datetime import date

    tenants_dict = {
        "INQ": "https://squareup.com/appointments/book/keivpp56cj87hu/KX0RR40A42H7X/services"
    }

    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    # get today's date
    date = str(date.today())
    cur_month_num = str(datetime.now().month)

    datetime_object = datetime.strptime(cur_month_num, "%m")

    month_name = datetime_object.strftime("%b")
    print("Short name: ", month_name)

    # get just the day
    today = date[-2:]

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    availability = []

    for tenant, link in tenants_dict.items():
        driver.get(link)

        time.sleep(3)

        try:
            # tattoo touch up
            driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/section/section/div/div[2]/div/div[2]/div/div/input").click()
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/nav/div/button").click()
        except (Exception,) as e:
            print(e)
            send_email()

        time.sleep(3)

        # if month_name not in driver.page_source:
        #     print(tenant + " has no availability :(")
        #     continue

        time.sleep(3)

        try:
            calendar_day = driver.find_element(By.XPATH, "//*[text()='{0}']".format(today))
            x = calendar_day.get_attribute("aria-disabled")
            if x == "true":
                print(tenant + " has no availability :(")
            else:
                availability.append(tenant)
                print(tenant + " has availability!")
        except (Exception,) as e:
            print(e)
            send_email()

    print(availability)
    update_html(availability, tenants_dict)


def scrape_schedulicity():
    from datetime import date

    tenants_dict = {
        "Arrowleaf Hair Studio": "https://www.schedulicity.com/scheduling/AHSHAE/services",
        "Embellish Hair Studio": "https://www.schedulicity.com/scheduling/EHS4EQ/services",
        "KW Studio": "https://www.schedulicity.com/scheduling/KSBEET7/services",
        "Meraki Hair Styling": "https://www.schedulicity.com/scheduling/MHSB2B/services",
        "Studio SOUSS": "https://www.schedulicity.com/scheduling/FSSDSZ/services",
        "Thairapy": "https://www.schedulicity.com/scheduling/HMS5CW/services",
        "Align Skin & Massage": "https://www.schedulicity.com/scheduling/ASMDJU/services",
        "Faze Higher Beauty": "https://www.schedulicity.com/scheduling/FSS6RM/services",
        "Jennifer Zowada": "https://www.schedulicity.com/scheduling/JBSXQL/services",  # Jenna Bella Skin Care &
        # Healing Bozeman
        # "Good Karma Nail Studio": "https://www.schedulicity.com/scheduling/NASSMP/services",
        # "Wildflower Nail and Foot Care": "https://www.schedulicity.com/scheduling/WNACSP/services", # only accepting bookings with existing clients
        # "American Treasure Barbershop": "https://www.schedulicity.com/scheduling/TBA9TC/services" # please call to schedule
    }

    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    # get today's date
    date = str(date.today())
    cur_month_num = str(datetime.now().month)

    datetime_object = datetime.strptime(cur_month_num, "%m")

    month_name = datetime_object.strftime("%b")
    print("Short name: ", month_name)

    # get just the day
    today = date[-2:]

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    availability = []

    for tenant, link in tenants_dict.items():
        driver.get(link)

        time.sleep(3)
        try:
            driver.find_element(By.XPATH,
                                "/html/body/app-root/div/div/div/div/section/scheduling-services/div/sc-content-wrapper"
                                "/section[1]/div[1]/div[1]/sc-panel/sc-panel-body/sc-list/sc-list-row[1]/sc-list-item["
                                "4]/sc-btn/div").click()
        except (Exception,) as e:
            print(e)
            send_email()
            continue

        time.sleep(3)
        try:
            driver.find_element(By.XPATH, "/html/body/app-root/sc-modal-container/div/provider-select-modal/sc-list/sc"
                                          "-list-row/sc-list-item[3]/sc-btn/div").click()
        except (Exception,) as e:
            print(e)
            send_email()
            continue

        time.sleep(3)
        try:
            driver.find_element(By.XPATH,
                                "/html/body/app-root/div/div/div/div/section/scheduling-services/div/sc-content-wrapper"
                                "/section[1]/div[3]/sc-panel/sc-panel-body/div/div/div[2]/sc-btn/div").click()
        except (Exception,) as e:
            print(e)
            send_email()
            continue

        time.sleep(3)

        calendar_object = driver.find_element(By.XPATH,
                                              "/html/body/app-root/div/div/div/div/section/service-calendar/sc-content-wrapper/section["
                                              "1]/sc-panel/sc-panel-body")

        if month_name not in calendar_object.text:
            print(tenant + " has no availability :(")
            continue

        try:
            calendar_element = driver.find_elements(By.CLASS_NAME, "calendar-day")
        except (Exception,) as e:
            print(e)
            send_email()
            continue

        try:
            for item in calendar_element:
                if today == item.text:
                    if "unavailable" in item.get_attribute('class'):
                        print(tenant + " has no availability :(")
                    else:
                        print(tenant + " has availability!")
                        availability.append(tenant)
        except (Exception,) as e:
            print(e)
            send_email()

    print(availability)
    update_html(availability, tenants_dict)


def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


def update_html(a_list, tenants_dict):
    # copy last used gildhouse.html into temp file
    shutil.copyfile("../availability.html", "availability_temp.html")

    fin = open("availability_temp.html", "rt")
    fout = open("../availability.html", "wt")

    od1 = OrderedDict([("Schedule now", "No availability"), ("sched-link", "sched-grey-link"),
                       ('class="active"', 'class=""')])

    od2 = OrderedDict([("No availability", "Schedule now"), ("sched-grey-link", "sched-link"),
                       ('class=""', 'class="active"')])

    for line in fin:
        changed = False
        for tenant, link in tenants_dict.items():
            if tenant in line:
                if tenant not in a_list:
                    if "Schedule now" in line:
                        newline = replace_all(line, od1)
                        fout.write(newline)
                        changed = True
                else:
                    if "No availability" in line:
                        newline = replace_all(line, od2)
                        fout.write(newline)
                        changed = True

        if changed:
            continue
        else:
            fout.write(line)

    fin.close()
    fout.close()


def push_to_github():
    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)

    repo_dir = ''
    repo = Repo(repo_dir)
    file_list = ['availability.html']
    commit_message = 'updated availability.html after script ran'
    repo.index.add(file_list)
    repo.index.commit(commit_message)
    origin = repo.remote('origin')
    origin.push()
    print("pushed")

# def send_email():
#     # Import smtplib for the actual sending function
#     import smtplib
#
#     # Import the email modules we'll need
#     from email.mime.text import MIMEText
#
#     # Open a plain text file for reading.  For this example, assume that
#     # the text file contains only ASCII characters.
#     with open(textfile, 'rb') as fp:
#         # Create a text/plain message
#         msg = MIMEText(fp.read())
#
#     # me == the sender's email address
#     # you == the recipient's email address
#     msg['Subject'] = 'The contents of %s' % textfile
#     msg['From'] = me
#     msg['To'] = you
#
#     # Send the message via our own SMTP server, but don't include the
#     # envelope header.
#     s = smtplib.SMTP('localhost')
#     s.sendmail(me, [you], msg.as_string())
#     s.quit()


if __name__ == '__main__':
    scrape_schedulicity()
    scrape_vagaro()
    scrape_r2()
    scrape_leighann_schreiber()
    scrape_haley_walsh()
    scrape_tara_ashley()
    scrape_slicks()
    scrape_libby_hendrix()
    scrape_jenn_sarchet()
    scrape_jodi_griffith()
    scrape_cheree_ryan()
    scrape_jamie_burleigh()
    scrape_waxed_and_tamed()
    scrape_sapphire()
    scrape_inq()
    push_to_github()
