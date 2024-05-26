from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import sniffer
import json
import sys
import logging
import traceback

options = Options()
options.add_argument("--log-level=3")
options.add_argument('--headless')  
options.add_argument('--disable-gpu')
 
logger = logging.getLogger(__name__)

# 打开网页
prefix = 'https://www.youtube.com/watch?v='

max_catch_seconds = 300

def visit(file_name, turn):
    sniffer_ = sniffer.Sniffer()
    with open(file_name, 'r') as file:
        for line in file.readlines():
            url = prefix + line.strip()
            print('url: ' + url)
            should_loop = True
            # 广告检测
            while should_loop:
                sniffer_.run(tag = f'{line.strip()}')
                driver = webdriver.Chrome(options=options)
                driver.execute_script(f'window.location.replace("{url}");')
                try:
                    ad_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ytp-ad-player-overlay-layout')))
                    sniffer_.stop(if_save=False)
                    print('遇到广告')
                    # time.sleep(100)
                    ad_end = EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.ytp-ad-player-overlay-layout'))
                    ad_skip = EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.ytp-skip-ad-button__text'))
                    WebDriverWait(driver, 60).until(EC.any_of(ad_end, ad_skip))
                    try:
                        ad_skip = driver.find_element(By.CSS_SELECTOR, 'div.ytp-skip-ad-button__text')
                        if ad_skip.is_displayed():
                            ad_skip.click()
                    except:
                        pass
                    time.sleep(2)
                    driver.quit()
                    driver = webdriver.Chrome(options=options)
                except TimeoutException:
                    print('未遇到广告')
                    should_loop = False
            sys.stdout.flush()
            try:
                # 以及读取总时长
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'span.ytp-time-duration')))
                time_duration = driver.find_element(By.CSS_SELECTOR, 'span.ytp-time-duration')
                time_duration = time_duration.text
                print('总时长：' + time_duration)
                # 等待播放按钮加载
                play_button = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.ytp-play-button')))
                # print(play_button)
                play_button.click()
                print('按下播放按钮')
                sys.stdout.flush()
            except:
                print('读取时长和等待播放时异常退出: ', traceback.format_exc())
                sys.stdout.flush()
                driver.quit()
                sniffer_.stop(if_save=False)
                continue
            # 等待现在播放进度等于总时长
            try:
                WebDriverWait(driver, max_catch_seconds).until(
                    EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'span.ytp-time-current'), time_duration)
                )
            except:
                print('播放时异常退出: ', traceback.format_exc())
                sys.stdout.flush()
                driver.quit()
                sniffer_.stop(if_save=False)
                continue
            time.sleep(1)
            print('播放结束')
            sys.stdout.flush()
            sniffer_.stop()
            print('存储完毕')
            sys.stdout.flush()
            driver.quit()
            time.sleep(1)

def load(file_name):
    with open(file_name, 'r') as file:
        raw = file.read()
        d = json.loads(raw)
        pos = d['pos']
        turn = d['turn']
        return pos, turn

args = sys.argv
file_name = args[1]
max_turn = args[2]
max_turn = int(max_turn)
for i in range(max_turn):
    visit(file_name, str(i))