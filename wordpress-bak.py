from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import config


def timename():
    a = time.ctime(time.time())
    tlabel = ''
    c = []
    o = []
    for b in a:
        if b != ' ':
            c.append(b)
        elif b == ' ':
            o.append(''.join(c))
            c.clear()

    o.append(''.join(c))
    tlabel = str('-'.join(o))
    return tlabel


def duplicator():
    browser = webdriver.Chrome()
    browser.get(config.site_name+"wp-login.php")
    username_box = browser.find_element_by_id("user_login")
    username_box.send_keys(config.username)
    password_box = browser.find_element_by_id("user_pass")
    password_box.send_keys(config.password)
    password_box.submit()
    time.sleep(1)
    browser.get(config.site_name+"wp-admin/admin.php?page=duplicator")
    crnew = browser.find_element_by_id("dup-create-new")
    crnew.click()
    browser.implicitly_wait(20)
    pkname = browser.find_element_by_xpath(
        "//input[@name='package-name'][@type='text']")
    pkname.send_keys(timename())
    browser.execute_script("window.scrollTo(0, 100)")
    pkname.submit()
    browser.implicitly_wait(20)
    browser.execute_script("window.scrollTo(0, 100)")
    browser.find_element_by_id("dup-scan-warning-continue-checkbox").click()
    browser.find_element_by_id("dup-build-button").click()
    WebDriverWait(browser, 199).until(
        ec.visibility_of_element_located((By.ID, "dup-btn-installer"))).click()
    browser.implicitly_wait(10)
    browser.find_element_by_id("dup-btn-archive").click()
    browser.get(config.site_name+"wp-admin/update-core.php")
    checkboxes = browser.find_elements_by_css_selector(
        'input[type="checkbox"]')
    for each_checkbox in checkboxes:
        each_checkbox.click()
    browser.implicitly_wait(10)
    browser.find_element_by_xpath('//*[@id="upgrade-plugins-2"]').click()
    time.sleep(10)


try:
    duplicator()
except AssertionError as err:
    print(err)
    webdriver.Chrome.quit()
