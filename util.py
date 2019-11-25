import time


def get_abp_numblocked(driver, ext_id):
    driver.get("chrome-extension://{}/popup.html".format(ext_id))
    total = driver.find_element_by_id("stats-total").text
    return int(total.split(" ")[0])


def get_ghostery_numblocked(driver, ext_id):
    driver.get("chrome-extension://{}/app/templates/panel.html".format(ext_id))
    driver.find_element_by_xpath(
        "//*[@class='PlusPromoModal__button basic']").click()
    # /html/body/div/div/div/div[2]/div[1]/div/div[3]/div
    total = driver.find_element_by_xpath(
        "/html/body/div/div/div/div[2]/div[1]/div/div[3]/div").text
    return int(total)


def get_adguard_numblocked(driver, ext_id):
    driver.get("chrome-extension://{}/pages/popup.html".format(ext_id))
    time.sleep(2)
    blocked = driver.find_element_by_css_selector(
        "body > div.widget-popup.status-checkmark > div.tabstack.status-inner > div.tab-main.tab-main--base.active.tab-switch-tab > div.head > div.total.blocked-all").text
    result = int(blocked.split(": ")[1].strip())
    return result


def get_ubp_numblocked(driver, ext_id):
    driver.get("chrome-extension://{}/popup.html".format(ext_id))
    time.sleep(2)
    blocked = driver.find_element_by_id("total-blocked").text
    result = int(blocked.split(" ")[0])
    return result


def get_privacybadger_numblocked(driver, ext_id):
    driver.get("chrome-extension://{}/skin/popup.html".format(ext_id))
    splitted = [""]
    while len(splitted) < 3:
        driver.refresh()
        time.sleep(2)
        if driver.find_element_by_id("instructions_one_tracker").text:
            return 1
        if driver.find_element_by_id("instructions_no_trackers").text:
            return 0
        total = driver.find_element_by_id("instructions-many-trackers").text
        splitted = total.split(" ")
    return int(splitted[3])


f = open("urls/test.txt")
URLS = f.readlines()
f.close()
URLS = [i.strip() for i in URLS]
EXTENSIONS = {
    # "Adguard": get_adguard_numblocked,
    "AdBlockPlus": get_abp_numblocked,
    # "Ghostery": get_ghostery_numblocked,
    # "PrivacyBadger": get_privacybadger_numblocked,
    # "uBlockOrigin": get_ubp_numblocked
}
