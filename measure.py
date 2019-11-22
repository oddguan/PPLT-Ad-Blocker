import os
import time
import argparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from util import URLS, EXTENSIONS  # For testing purpose

# the number of loads to perform for a single website
LOADS = 10


def read_file(path):
    result = None
    with open(path, "r") as f:
        result = f.readlines()
    return result


def get_driver(extension):
    '''
    Get a Chrome driver with a specific extension installed
    '''
    options = Options()
    path = "extensions/{}.crx".format(extension)
    options.add_extension(path)
    options.add_argument("--enable-precise-memory-info")
    return webdriver.Chrome(options=options)


def expand_shadow_element(driver, element):
    shadow_root = driver.execute_script(
        'return arguments[0].shadowRoot', element)
    return shadow_root


def toggle_developer_mode(driver):
    root1 = driver.find_element_by_tag_name("extensions-manager")
    shadow1 = expand_shadow_element(driver, root1)
    root2 = shadow1.find_element_by_css_selector("extensions-toolbar")
    shadow2 = expand_shadow_element(driver, root2)
    root3 = shadow2.find_element_by_css_selector("cr-toolbar")
    root3.find_element_by_css_selector("cr-toggle").click()


def get_extension_id(driver):
    root1 = driver.find_element_by_tag_name("extensions-manager")
    shadow1 = expand_shadow_element(driver, root1)
    shadow2 = shadow1.find_element_by_css_selector("cr-view-manager")
    root3 = shadow2.find_element_by_id("items-list")
    shadow3 = expand_shadow_element(driver, root3)
    items = shadow3.find_elements_by_css_selector("extensions-item")
    for item in items:
        shadow4 = expand_shadow_element(driver, item)
        if shadow4.find_element_by_id("name").text != "Chrome Automation Extension":
            return item.get_attribute("id")


def get_memory_usage(driver):
    value = float(driver.execute_script(
        "return window.performance.memory.usedJSHeapSize"))
    return value / (1024 * 1024)


def close_popup(driver):
    curr = driver.current_window_handle
    for i, handle in enumerate(driver.window_handles):
        if handle == curr:
            continue
        driver.switch_to.window(driver.window_handles[i])
        driver.close()
    driver.switch_to.window(curr)


def with_blockers():
    result = []
    for extension in EXTENSIONS:
        for url in URLS:
            line = [extension, url]
            print(line)
            avg_memory_used = 0
            avg_num_blocked = 0
            avg_load_time = 0
            for _ in range(LOADS):
                driver = get_driver(extension)
                time.sleep(5)
                close_popup(driver)
                driver.get("chrome://extensions")
                toggle_developer_mode(driver)
                ext_id = get_extension_id(driver)
                start = time.time()
                driver.get(url)
                end = time.time()
                time.sleep(5)
                avg_memory_used += get_memory_usage(driver)
                avg_num_blocked += EXTENSIONS[extension](driver, ext_id)
                avg_load_time += end - start
                # print(avg_num_blocked)
                driver.quit()
            avg_memory_used /= LOADS
            avg_num_blocked /= LOADS
            avg_load_time /= LOADS
            line.append(avg_memory_used)
            line.append(avg_num_blocked)
            line.append(avg_load_time)
            result.append(line)
    return result


def without_blockers():
    result = []
    for url in URLS:
        line = [url]
        avg_memory_used = 0
        avg_load_time = 0
        for _ in range(LOADS):
            driver = webdriver.Chrome()
            start = time.time()
            driver.get(url)
            end = time.time()
            time.sleep(5)
            avg_memory_used += get_memory_usage(driver)
            avg_load_time += end - start
            driver.quit()
        avg_memory_used /= LOADS
        avg_load_time /= LOADS
        line.append(avg_memory_used)
        line.append(avg_load_time)
        result.append(line)
    return result


def parse_argument():
    args = argparse.ArgumentParser()
    args.add_argument("--load", "-l", type=int, default=10,
                      help="The number of loads for a website")
    args.add_argument("--urls", "-u", type=str,
                      default="urls.csv", help="The path to the url csv file")
    args.add_argument("--extensions", "-e", type=str,
                      deault="extensions.csv", help="The path to the extension csv file")
    return args.parse_args()


def main():
    with open("blocked.csv", "w") as f:
        blocked = with_blockers()
        f.write("extension,url,avg_memory_used,avg_num_blocked,avg_load_time\n")
        for line in blocked:
            f.write(",".join([str(i) for i in line]) + "\n")
    with open("unblocked.csv", "w") as f:
        unblocked = without_blockers()
        f.write("extension,url,avg_memory_used,avg_load_time\n")
        for line in unblocked:
            f.write(",".join([str(i) for i in line]) + "\n")


if __name__ == "__main__":
    main()
