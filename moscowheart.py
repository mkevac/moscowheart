import m3u8
import urllib.request
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getURL():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://moscowheart.ru")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "open_webcam"))
        )
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "open_webcam"))
        )
    except Exception:
        return

    # still need this :-(
    time.sleep(2)

    elem = driver.find_element_by_class_name("open_webcam")
    elem.click()

    # still need this :-(
    time.sleep(2)

    playeriframe = driver.find_element_by_tag_name("iframe")
    driver.switch_to.frame(playeriframe)
    for script in driver.find_elements_by_tag_name("script"):
        innerHTML = str(script.get_attribute('innerHTML'))
        try:
            ind = innerHTML.rindex("m3u8") + 4
            indEnd = ind + innerHTML[ind:].index("'")
            indBegin = innerHTML[:ind].rindex("'")+1
            result = "https:"+innerHTML[indBegin:indEnd]
        except Exception:
            pass

    driver.close()
    return result


def main():
    url = getURL()
    baseurl = url[0:url.rindex('/')]

    while True:
        m3u8_obj = m3u8.load(url)  # this could also be an absolute filename
        playlist = m3u8_obj.playlists[0]
        m3u8_obj = m3u8.load(playlist.absolute_uri)
        lastfile_url = baseurl + '/tracks-v1/' + m3u8_obj.files[-1]
        local_file, _ = urllib.request.urlretrieve(lastfile_url)
        os.system(
            "ffmpeg -i {} -r 1 -f singlejpeg {}".format(local_file, 'data/' + time.strftime("%F-%H-%M-%S") + '.jpg'))
        os.remove(local_file)
        time.sleep(60)


if __name__ == "__main__":
    main()
