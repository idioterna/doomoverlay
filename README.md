# Doom overlay

Currently uses fitparse and moviepy to extract garmin device data and
render an overlay, currently statically set up to fit a 1920x1080 frame
size, that displays heart rate, speed, cadence, the space marine face
icon that becomes visibly strained above a preset heart rate, distance
travelled and elevation gained.

Usage is fairly straightforward:

`$ ./ovr.py video.mp4 yyyy-mm-dd-hh-mm-ss.fit
--output out.mp4 --fit-start 3 --duration 60 --strain 150`

The `--fit-start 3` parameter allows you to synchronize start of ride
with start of video, `--duration 60` renders only the first 60 seconds
and `--strain 150` tells the program to display a strained facial
expression when heart rate is above 150 beats per minute.
`--output out.mp4` allows you to set output file, which by default is
constructed by prepending `ovr_` to the original filename.

It looks [like this](https://www.youtube.com/watch?v=f3gKqMLJU7c).

