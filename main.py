import threading
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import StaleElementReferenceException
import os
import subprocess


def scrolldown(driver):
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except Exception as e:
        pass


def scrollhalf(driver):
    try:
        driver.execute_script("document.body.style.zoom='100%'; window.scrollBy(0, window.innerHeight / 1.25);")
    except Exception as e:
        pass


def scrollup(driver):
    try:
        driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);")
    except Exception as e:
        pass


def clickifclickable(xpath, driver):
    try:
        wait = WebDriverWait(driver, 20)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        time.sleep(1)
        # Click the element
        element.click()
    except Exception as e:
        clickifclickable(xpath, driver)


def retopt(city):
    if (city.lower() == "islamabad"):
        opt = 1
    elif (city.lower() == "karachi"):
        opt = 2
    elif (city.lower() == "lahore"):
        opt = 3
    elif (city.lower() == "mirpur"):
        opt = 4
    return opt


def wait_for_page(xpath, driver, timeout=10, ):
    try:
        element_present = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        pass


def refresh(driver):
    scrollhalf(driver)
    xpath = '/html/body/app-root/div/app-book-appointment/section/mat-card[1]/div[2]/div/div/full-calendar/div[1]/div[3]/div/button[2]/span'
    clickifclickable(xpath, driver)
    time.sleep(1)
    xpath2 = '/html/body/app-root/div/app-book-appointment/section/mat-card[1]/div[2]/div/div/full-calendar/div[1]/div[3]/div/button[1]/span'
    clickifclickable(xpath2, driver)
    time.sleep(1)


def login(driver, wait, data):
    xpath = '//*[@id="passwordKey"][1]'
    driver.get("https://visa.vfsglobal.com/pak/en/gbr/login")
    wait_for_page(xpath, driver)
    time.sleep(1)
    cook = '//*[@id="onetrust-accept-btn-handler"]'

    driver.find_element(By.XPATH, xpath).send_keys(data["ref"])
    time.sleep(1)
    check23 = driver.find_element(By.XPATH, cook)
    if check23:
        check23.click()
    else:
        pass
    xpath2 = '//*[@id="mat-input-1"]'
    wait_for_page(xpath2, driver)
    driver.find_element(By.XPATH, xpath2).send_keys(data["gmail"])
    time.sleep(1)
    xpath3 = '/html/body/app-root/div/app-login/section/div/div/mat-card/form/button'
    clickifclickable(xpath3, driver)
    time.sleep(1)


def check_specific_page(driver, data):
    time.sleep(1)

    while True:
        try:
            # Use WebDriverWait to wait for an element on the specific page

            xpath = '//*[@id="passwordKey"][1]'
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

            driver.close()

            break
        except TimeoutException:
            # If TimeoutException occurs, the element is not present yet
            pass
        # Add a delay to avoid continuous checking and reduce resource usage
        time.sleep(1)


def test(driver, wait, data):
    driver.execute_script("document.body.style.zoom='100%'; window.scrollBy(0, window.innerHeight / 3);")
    load(driver, wait)
    div_class_name = "fc-daygrid-day-top"
    anchor_class_name = "fc-daygrid-day-number"
    div_selector = f".{div_class_name}:not([style*='color:'])"
    div_elements = driver.find_elements(By.CSS_SELECTOR, div_selector)
    newlist = []
    dates = []
    for div_element in div_elements:
        # Find the corresponding anchor element within the div
        anchor_selector = f".{div_class_name} a.{anchor_class_name}"
        anchor_element = div_element.find_element(By.CSS_SELECTOR, anchor_selector)
        if (len(anchor_element.text) > 2):
            newlist.append(anchor_element)
            text = anchor_element.text.split(" ")

            text = text[0]
            text = text.replace('\n', ' ')

            dates.append(text)
        else:
            pass
    reqdate = data["date"]
    reqdate = [date.upper() for date in reqdate]
    checkdate = False

    for i in reqdate:
        try:
            ind = dates.index(i)

            checkdate = True
            break
        except ValueError:
            pass
    try:
        ele = newlist[ind]
    except IndexError:
        pass
    except Exception as e:
        pass

    if checkdate == True:
        time.sleep(1)
        ele.click()
        pass

    else:
        scrollup(driver)
        refresh(driver)
        time.sleep(1)
        test(driver, wait, data)


def load(driver, wait):
    try:
        LONG_TIMEOUT = 40
        xpath = '/html/body/app-root/ngx-ui-loader/div[1]/div[1]/div'
        progress = wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        load(driver, wait)


def task1(data):
    try:
        driver = webdriver.Chrome()
        driver.delete_all_cookies()
        wait = WebDriverWait(driver, 30)

        login(driver, wait, data)
        time.sleep(1)
        page_check_thread = threading.Thread(target=check_specific_page, args=(driver, data))
        page_check_thread.start()
        scrolldown(driver)
        xpath4 = '//*[@id="mat-select-value-1"]'

        clickifclickable(xpath4, driver)
        opt = retopt(data["city"])

        xpath5 = f'//*[@id="mat-option-{opt}"]/span'
        clickifclickable(xpath5, driver)
        time.sleep(1)
        xpath6 = '/html/body/app-root/div/app-eligibility-criteria/section/form/mat-card[2]/div/div[2]/button'
        clickifclickable(xpath6, driver)
        load(driver, wait)

        scrollhalf(driver)
        test(driver, wait, data)
        time.sleep(1)
        scrolldown(driver)
        xpath40 = '/html/body/app-root/div/app-book-appointment/section/mat-card[1]/button'
        check = True
        count = 0

        while check:
            check = driver.find_elements(By.XPATH, xpath40)

            if not check:
                break
            else:
                check[0].click()
                scrolldown(driver)
                count += 1

        if count == 0:
            count = 10
        else:
            count = count * 10
        time.sleep(1)
        driver.execute_script("document.body.style.zoom='25%'")
        time.sleep(1)
        o = 0
        check2 = True

        while check2:
            if o < count:
                apptime = count - o
                xpath56 = f'//*[@id="STRadio{apptime}"]'
                w = driver.execute_script(
                    f"return document.evaluate('{xpath56}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;")

                try:
                    if not w:
                        o += 1
                    else:

                        driver.execute_script("arguments[0].click();", w)
                        break
                except Exception as e:
                    pass
            else:
                break

        driver.execute_script("document.body.style.zoom='100%'")

        # cont
        xpath30 = '/html/body/app-root/div/app-book-appointment/section/mat-card[2]/div/div[2]/button'
        clickifclickable(xpath30, driver)
        time.sleep(1)
        scrolldown(driver)

        # last contniue
        lastcont = '/html/body/app-root/div/app-manage-service/section/mat-card[2]/div/div[2]/button'
        clickifclickable(lastcont, driver)
        time.sleep(5)

    except Exception as E:

        try:
            driver.close()
        except Exception as E:
            pass

        time.sleep(1)

        task1(data)


# enter a new dictionary for a new user in the list
data = [{"ref": "GWF074037850", "gmail": "abdulkhaliq1122uk@gmail.com", "city": "Islamabad", "date": ["13 November"]}, ]

threads = [threading.Thread(target=task1, args=(i,)) for i in data]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()