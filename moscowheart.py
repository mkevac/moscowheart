import m3u8
import urllib.request
import os
import time

URL = 'https://stream.exdesign.ru/serdcestolicy-1/index.m3u8?token=20aafb38f4a7c951318d9c6d1c0252d14831e983' \
      '-bfcb8475f524ad703f30f7900c531eed-1586113943-1586103143'
BASEURL = URL[0:URL.rindex('/')]


def main():
    while True:
        m3u8_obj = m3u8.load(URL)  # this could also be an absolute filename
        playlist = m3u8_obj.playlists[0]
        m3u8_obj = m3u8.load(playlist.absolute_uri)
        lastfileURL = BASEURL+'/tracks-v1/'+m3u8_obj.files[-1]
        localFile, _ = urllib.request.urlretrieve(lastfileURL)
        os.system("ffmpeg -i {} -r 1 -f singlejpeg {}".format(localFile, 'data/'+time.strftime("%F-%T")+'.jpg'))
        time.sleep(60)


if __name__ == "__main__":
    main()
