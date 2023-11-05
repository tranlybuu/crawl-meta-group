from dotenv import load_dotenv
import undetected_chromedriver as uc
import pyautogui
import datetime
from selenium.webdriver.common.by import By
from time import sleep
import os

if __name__ == "__main__":
    os.system('cls')
    load_dotenv()
    fb_email = os.environ.get('LOGIN_EMAIL')
    fb_password = os.environ.get('LOGIN_PASSWORD')
    proxy = os.environ.get('PROXY')
    PROXY_HOST = os.environ.get('PROXY_HOST')
    PROXY_PORT = os.environ.get('PROXY_PORT')
    PROXY_USER = os.environ.get('PROXY_USER')
    PROXY_PASSWORD = os.environ.get('PROXY_PASSWORD')
    PROXY_PASSWORD = os.environ.get('PROXY_PASSWORD')
    TIMEOUT = float(os.environ.get('TIMEOUT'))

    print("\nPROXY_HOST = ", PROXY_HOST)
    print("\nPROXY_PORT = ", PROXY_PORT)
    print("\nPROXY_USER = ", PROXY_USER)
    print("\nPROXY_PASSWORD = ", PROXY_PASSWORD)

    search_list = str(input("\n\nNhập tên nhóm tìm kiếm: ")).strip().replace(" ", "%20")
    search_list = search_list.split("|")
    time_scroll = int(input("\n\nNhập số lần cuộn trang: ").strip())
    
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("start-maximized")
    options.add_argument('--proxy-server=' + str(PROXY_HOST) + ":" + str(PROXY_PORT))
    driver = uc.Chrome(options=options)
    sleep(TIMEOUT + 0.5)
    with driver:
        driver.get("https://www.facebook.com")
        pyautogui.typewrite(PROXY_USER)
        pyautogui.press('tab')
        pyautogui.typewrite(PROXY_PASSWORD)
        pyautogui.press('enter')
        sleep(TIMEOUT + 6)
        driver.maximize_window()
        username = driver.find_element(By.ID, 'email')
        password = driver.find_element(By.ID, 'pass')
        username.send_keys(fb_email)
        password.send_keys(fb_password)
        submit_button = driver.find_element(By.CLASS_NAME, '_6ltg')
        submit_button.find_element(By.XPATH, '//button[contains(@class, "_42ft _4jy0 _6lth _4jy6 _4jy1 selected _51sy")]').click()
        sleep(TIMEOUT + 2)
        for search in search_list:
            driver.get("https://www.facebook.com/search/groups?q=" + str(search).strip() + "&filters=eyJwdWJsaWNfZ3JvdXBzOjAiOiJ7XCJuYW1lXCI6XCJwdWJsaWNfZ3JvdXBzXCIsXCJhcmdzXCI6XCJcIn0ifQ%3D%3D")
            sleep(TIMEOUT + 2)
            pyautogui.click(x=670, y=720)
            for i in range(time_scroll):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(TIMEOUT + 3)
            entries = []
            count = driver.find_elements(By.CSS_SELECTOR, '.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xzsf02u.x1s688f')
            for index in range(len(count)):
                try:
                    url = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[' + str(index+1) + ']/div/div/div/div/div/div/div/div/div/div/div[1]/div/a').get_attribute('href')
                    name = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[' + str(index+1) + ']/div/div/div/div/div/div/div/div/div/div/div[2]/div[1]/div/div/div[1]/span/div/a').text
                    description = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[' + str(index+1) + ']/div/div/div/div/div/div/div/div/div/div/div[2]/div[1]/div/div/div[2]/span/span').text
                    data = description.split("·")
                    status = data[0].strip()
                    member_data = data[1].lower().strip().split(" ")
                    if "k" in member_data[0]:
                        total_member = member_data[0].replace("k", "").split(",")
                        decimal = str(total_member[1])
                        if len(decimal) < 3:
                            decimal = decimal + '0' * (3 - len(decimal))
                        total_member = int(total_member[0])*1000 + int(decimal)
                    elif "triệu" in data[1]:
                        total_member = member_data[0].replace("k", "").split(",")
                        decimal = str(total_member[1])
                        if len(decimal) < 3:
                            decimal = decimal + '0' * (3 - len(decimal))
                        total_member = int(total_member[0])*1000000 + int(decimal)*1000
                    else:
                        total_member = member_data[0]
                    entries.append({
                        "url": url,
                        "name": name,
                        "status": status,
                        "total_member": total_member
                    })
                except:
                    continue
            filename = str(search).replace("%20", "_").strip("_").strip("") + "_" + str(datetime.datetime.now()).replace(" ", "_").replace(":", "-") + ".csv"
            with open(filename, 'w', encoding='utf-8') as file:
                file.write("name,status,member,url\n")
                for entry in entries:
                    file.write(str(entry["name"]).replace(",", " ") + ',' + str(entry["status"]) + ',' + str(entry["total_member"]) + ',' + str(entry["url"]) + '\n')