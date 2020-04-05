import m3u8
import urllib.request
import os
import time

URL = 'https://stream.exdesign.ru/serdcestolicy-1/index.m3u8?token=ee8d8f8029152285366c30abd7874b151dac9d87-3492a6bb71f678f1cd29652b9607214d-1586127742-1586116942'
BASEURL = URL[0:URL.rindex('/')]


def main():
    while True:
        m3u8_obj = m3u8.load(URL)  # this could also be an absolute filename
        playlist = m3u8_obj.playlists[0]
        m3u8_obj = m3u8.load(playlist.absolute_uri)
        lastfileURL = BASEURL+'/tracks-v1/'+m3u8_obj.files[-1]
        localFile, _ = urllib.request.urlretrieve(lastfileURL)
        os.system("ffmpeg -i {} -r 1 -f singlejpeg {}".format(localFile, 'data/'+time.strftime("%F-%H-%M-%S")+'.jpg'))
        time.sleep(60)


if __name__ == "__main__":
    main()
