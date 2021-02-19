#!/usr/bin/env python3
from selenium import webdriver
import asyncio
import time, threading
import re
import os
import make_gif
import multiprocessing
import glob


e_count = 0
count = 0
earthquake_now = False
save_dir = ''
driver = ""
ring_index = 0

def monitoring():
    global earthquake_now
    global count
    global driver
    global save_dir
    global e_count
    global ring_index

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

            # clear ring buffer
            for p in glob.glob("ring/*.png"):
                os.remove(p)
            ring_index = 0

            p = multiprocessing.Process(target=make_gif.make_gif, args=(save_dir,))
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
        else:
            # Save Ring Buffer
            driver.save_screenshot(f"ring/ring{ring_index}.png")
            ring_index = (ring_index + 1) % 20



def main_func():
    global driver

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--window-size=365,720')
    driver = webdriver.Chrome(options=options)  # 今は chrome_options= ではなく options=

    driver.get('http://www.kmoni.bosai.go.jp/')
    print(driver.title)

    time.sleep(3)

    wave_checkbox = driver.find_element_by_id('wave-checkbox')
    label = driver.find_element_by_xpath("//div[@id='wave-checkbox']/label")
    print(label.text)
    label.click()
    print(label.text)
    # ck_wav = driver.find_element_by_id('ck-wave')
    # ck_wav.checked = False

    print("start caturing")

    base_time = time.time()
    next_time = 0
    while True:
        t = threading.Thread(target=monitoring)
        t.start()

        next_time = ((base_time - time.time()) % 1) or 1
        time.sleep(next_time)

    driver.quit()

if __name__ == '__main__':
    main_func()
