timelapse:
	ffmpeg -r 24 -pattern_type glob -i 'data/*.jpg' -s hd1080 -vcodec libx264 -crf 18 -preset slow timelapse.mp4
