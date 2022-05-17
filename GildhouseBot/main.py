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

# Arrowleaf Hair Studio = "https://www.schedulicity.com/scheduling/AHSHAE/services"
# Ashley Cleo Hair Studio = "https://www.vagaro.com/ashleycleohairstudio/book-now"
# Chroma = "https://www.vagaro.com/chromabzn/book-now"
# Embellish Hair Studio = "https://www.schedulicity.com/scheduling/EHS4EQ/services"
# Fringe = "https://www.vagaro.com/fringehairstudio406/book-now"
# Hyalite_Studio = "https://hyalitestudio.com/stylists/"
# KW_Studio = "https://www.schedulicity.com/scheduling/KSBEET7/services"
# Meraki_Hair_Styling = "https://www.schedulicity.com/scheduling/MHSB2B/services"
# R2 = "https://randirammell.glossgenius.com/"
# Salon_South = "https://www.vagaro.com/salonsouth2/book-now"
# Studio_Souss = "https://www.schedulicity.com/scheduling/FSSDSZ/services"
# Thairapy = "https://www.schedulicity.com/scheduling/HMS5CW/services"
# Velvet = "http://thevelvetstudio.com/"
# Slicks_Wax_Skin = "https://square.site/book/06680NG66P1E5/slicks-wax-skin-bozeman-mt"
# Align_Skin_Massage = "https://www.schedulicity.com/scheduling/ASMDJU/services"
# Faze_Higher_Beauty = "https://www.schedulicity.com/scheduling/FSS6RM/services"
# Jamie_Burleigh_Permanent_Makeup = "https://jamie-burleigh-pmu.square.site/"
# Jenna_Bella = "https://www.schedulicity.com/scheduling/JBSXQL/services"
# Waxed_and_Tamed = "https://bookings.gettimely.com/waxedandtamed/book?uri=https%3A%2F%2Fbook.gettimely.com%2FBooking" \
#                   "%2FLocation%2F128669%3Fmobile%3DTrue%26params%3D%25253fclient-login%25253dtrue"
# Good Karma Nail Studio = "https://www.schedulicity.com/scheduling/NASSMP/services"
# Wildflower = "https://www.schedulicity.com/scheduling/WNACSP/services"
# Jenna Bella Skin Care = "https://www.schedulicity.com/scheduling/JBSXQL/services"
# Vibrant_Life_Therapy = "https://vibrantlifetherapy.com/"
# American_Treasure_Barbershop = "https://www.schedulicity.com/scheduling/TBA9TC/services"
# INQ = "https://square.site/book/KX0RR40A42H7X/inq-bozeman-mt"
# Sapphire_Medical_Aesthetics = "https://sapphiremedicalaesthetics.myaestheticrecord.com/book/appointments" \
#                               "/MV8xMjU5Ml9jbGluaWNz"
# Shiloh_Medical_Clinic = "https://shilohmedicalclinic.com/"


def scrape_vagaro():
    from datetime import date

    vagaro_dict = {
        "Ashley Cleo Hair Studio": "https://www.vagaro.com/ashleycleohairstudio/book-now",
        "Chroma": "https://www.vagaro.com/chromabzn/book-now",
        #  "Fringe": "https://www.vagaro.com/fringehairstudio406/book-now", defaults to tomorrow's date, probably
        # does not want same-day appointments
        "Salon South": "https://www.vagaro.com/salonsouth2/book-now"
    }

    chrome_options = Options()
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


def scrape_schedulicity():
    from datetime import date

    tenants_dict = {
        "Arrowleaf Hair Studio": "https://www.schedulicity.com/scheduling/AHSHAE/services",
        "Embellish Hair Studio": "https://www.schedulicity.com/scheduling/EHS4EQ/services",
        "KW Studio": "https://www.schedulicity.com/scheduling/KSBEET7/services",
        "Meraki Hair Styling": "https://www.schedulicity.com/scheduling/MHSB2B/services",
        "Studio Souss": "https://www.schedulicity.com/scheduling/FSSDSZ/services",
        "Thairapy": "https://www.schedulicity.com/scheduling/HMS5CW/services",
        "Align Skin & Massage": "https://www.schedulicity.com/scheduling/ASMDJU/services",
        "Faze Higher Beauty": "https://www.schedulicity.com/scheduling/FSS6RM/services",
        "Jenna Bella Skin Care": "https://www.schedulicity.com/scheduling/JBSXQL/services",
        "Good Karma Nail Studio": "https://www.schedulicity.com/scheduling/NASSMP/services",
        "Wildflower Nail and Foot Care": "https://www.schedulicity.com/scheduling/WNACSP/services",
        "American Treasure Barbershop": "https://www.schedulicity.com/scheduling/TBA9TC/services"
    }

    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    # get today's date
    date = str(date.today())

    # get just the day
    today = date[-2:]

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    availability = []

    for tenant, link in tenants_dict.items():
        driver.get(link)

        time.sleep(3)
        driver.find_element(By.XPATH,
                            "/html/body/app-root/div/div/div/div/section/scheduling-services/div/sc-content-wrapper"
                            "/section[1]/div[1]/div[1]/sc-panel/sc-panel-body/sc-list/sc-list-row[1]/sc-list-item["
                            "4]/sc-btn/div").click()
        time.sleep(3)
        driver.find_element(By.XPATH, "/html/body/app-root/sc-modal-container/div/provider-select-modal/sc-list/sc"
                                      "-list-row/sc-list-item[3]/sc-btn/div").click()

        time.sleep(3)
        driver.find_element(By.XPATH,
                            "/html/body/app-root/div/div/div/div/section/scheduling-services/div/sc-content-wrapper"
                            "/section[1]/div[3]/sc-panel/sc-panel-body/div/div/div[2]/sc-btn/div").click()

        time.sleep(3)
        calendar_element = driver.find_elements(By.CLASS_NAME, "calendar-day")

        for item in calendar_element:
            if today == item.text:
                if "unavailable" in item.get_attribute('class'):
                    print(tenant + " has no availability :(")
                else:
                    print(tenant + " has availability!")
                    availability.append(tenant)

    print(availability)
    update_html(availability, tenants_dict)


def update_html(a_list, tenants_dict):
    # copy last used gildhouse.html into temp file
    shutil.copyfile("../gildhouse.html", "gildhouse_temp.html")

    fin = open("gildhouse_temp.html", "rt")
    fout = open("../gildhouse.html", "wt")

    for line in fin:
        changed = False
        for tenant, link in tenants_dict.items():
            if tenant in line:
                if tenant not in a_list:
                    if "green" in line:
                        fout.write(line.replace("green", "red"))
                        changed = True
                else:
                    if "red" in line:
                        fout.write(line.replace("red", "green"))
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
    file_list = [
        'gildhouse.html'
    ]
    commit_message = 'updated gildhouse.html after script ran'
    repo.index.add(file_list)
    repo.index.commit(commit_message)
    origin = repo.remote('origin')
    origin.push()
    print("pushed")


if __name__ == '__main__':
    scrape_schedulicity()
    # scrape_vagaro()
    # push_to_github()
