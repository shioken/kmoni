#!/usr/bin/env python3
from selenium import webdriver
import time
import re
import os
import make_gif
import multiprocessing

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--window-size=365,720')
driver = webdriver.Chrome(options=options)  # 今は chrome_options= ではなく options=

driver.get('http://www.kmoni.bosai.go.jp/')
print(driver.title)

time.sleep(3)

print("start caturing")

e_count = 0
count = 0
earthquake_now = False
save_dir = ''

while True:
    message_time = driver.find_element_by_id('map-message-time').text
    message_num = driver.find_element_by_id('map-message-num').text
    message_area = driver.find_element_by_id('map-message-area').text
    mag = driver.find_element_by_id('map-message-mag-value').text
    depth = driver.find_element_by_id('map-message-depth-value').text
    sindo = driver.find_element_by_id('map-message-sindo-value').text
    alert = driver.find_element_by_id('map-message-alert-value').text

    if earthquake_now:
        print(f"{message_time},{message_num}, {message_area}, {mag}, {depth}, {sindo}, {alert}")
        if len(message_time) == 0:
            print("地震終了")
            earthquake_now = False
            count = 0

            p = multiprocessing.Process(target=make_gif, args=(save_dir))
            p.start()
        else:
            count += 1
            cz = "{0:05d}".format(count)
            driver.save_screenshot(f"capture/{save_dir}/eq_{e_count}_{cz}.png")

    else:
        if len(message_time) > 0:
            print("地震発生")
            print(f"{message_time},{message_num}, {message_area}, {mag}, {depth}, {sindo}, {alert}")

            save_dir = re.sub(r"\D", "", message_time)
            print(f"save_dir:{save_dir}")
            os.makedirs(f"capture/{save_dir}", exist_ok=True)

            earthquake_now = True

            e_count += 1
            count = 1
            cz = "{0:05d}".format(count)
            driver.save_screenshot(f"capture/{save_dir}/eq_{e_count}_{cz}.png")

    time.sleep(1)

driver.quit()
