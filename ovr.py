#!/usr/bin/env python

import IPython
import numpy as np
from PIL import Image
from moviepy.editor import VideoFileClip
from fitparse import FitFile
import datetime, math
import doom

class OVR:

    def __init__(self, vid=None, fit=None, fit_offset=0, strain=150):
        self.fit = fit
        self.lfit = len(fit)
        self.vid = vid
        self.fit_offset = fit_offset
        self.strain = strain
        self.framedur = 1.0/self.vid.fps
        self.frameno = 0

    def __call__(self, frame):
        self.frameno += 1
        currentts = self.frameno*self.framedur
        currenttsfloor = int(math.floor(currentts))
        fit_index = currenttsfloor - self.fit_offset
        if fit_index < 0:
            fit_index = 0
        elif fit_index >= self.lfit:
            fit_index = self.lfit - 1
        img = Image.fromarray(frame)
        img.paste(doom.generate(self._interpolate(self.fit, self.lfit, fit_index, currentts - currenttsfloor), self.strain), (0, 888))
        return np.asarray(img, dtype=np.uint8)

    def _cubic(self, y, mu=0.5):
       mu2 = mu*mu
       a0 = y[3] - y[2] - y[0] + y[1]
       a1 = y[0] - y[1] - a0
       a2 = y[2] - y[0]
       a3 = y[1]

       return a0*mu*mu2+a1*mu2+a2*mu+a3;

    def _lastvalid(self, data, i, key, default=0):
        cnt = 0
        while True:
            cnt+=1
            if i-cnt < 1:
                return default
            value = data[i-cnt].get(key, None)
            if value is not None:
                return value

    def _interpolate(self, data, datalen, i, mu):
        offsets = [-1, 0, 1, 2]
        if i < 1:
            offsets[0] = 0
        if i >= datalen - 3:
            offsets[2] = 0
            offsets[3] = 0
        timestamps = []
        distances = []
        altitudes = []
        temperatures = []
        speeds = []
        heartrates = []
        cadences = []
        altgains = []
        for o in offsets:
            timestamps.append(data[i+o]['timestamp'].timestamp())
        for o in offsets:
            distances.append(float(data[i+o].get('distance', self._lastvalid(data, i+o, 'distance', 0))))
        for o in offsets:
            altitudes.append(float(data[i+o].get('altitude', self._lastvalid(data, i+o, 'altitude', 0))))
        for o in offsets:
            temperatures.append(float(data[i+o].get('temperature', 0)))
        for o in offsets:
            speeds.append(float(data[i+o].get('speed', 0))*3.6)
        for o in offsets:
            heartrates.append(float(data[i+o].get('heart_rate', 0)))
        for o in offsets:
            cadences.append(float(data[i+o].get('cadence', 0)))
        for o in offsets:
            altgains.append(float(data[i+o].get('altgain', 0)))

        return dict(
                timestamp = self._cubic(timestamps, mu),
                distance = self._cubic(distances, mu),
                altitude = self._cubic(altitudes, mu),
                temperature = self._cubic(temperatures, mu),
                speed = self._cubic(speeds, mu),
                heartrate = self._cubic(heartrates, mu),
                cadence = self._cubic(cadences, mu),
                altgain = self._cubic(altgains, mu),
                )

def main(video_filename, fit_filename, output_filename, fit_offset=0, duration=0, strain=150):
    v = VideoFileClip(video_filename)
    f = FitFile(fit_filename)

    fit = list()
    lfit = 0
    altgain = 0
    lastchange = 0
    for msg in f.get_messages('record'):
        d = dict()
        d.update(msg.get_values())
        fit.append(d)
        lfit += 1
        if lfit > 1:
            try:
                gain = fit[-1].get('altitude') - fit[-2].get('altitude')
            except:
                gain = 0
            if gain > 0:
                altgain += gain
            fit[-1]['altgain'] = altgain

    ovr = OVR(v, fit, fit_offset, strain)
    if duration:
        nv = v.subclip(t_end=duration).fl_image(ovr)
    else:
        nv = v.fl_image(ovr)
    nv.write_videofile(output_filename, progress_bar=True, bitrate='34000000')

if __name__ == '__main__':
    import sys, os
    try:
        video = os.path.realpath(sys.argv[1])
        fit = os.path.realpath(sys.argv[2])
        outvideo = os.path.dirname(video) + '/ovr_' + os.path.basename(video)
    except IndexError:
        print('Usage: {} <videofile> <fitfile> [--fit-start seconds_after_video_start] [--duration seconds_to_encode] [--output videofile.mp4]'.format(sys.argv[0]))
        sys.exit(1)

    if '--output' in sys.argv:
        outvideo = sys.argv[sys.argv.index('--output')+1]

    if '--fit-start' in sys.argv:
        offset = int(sys.argv[sys.argv.index('--fit-start')+1])
    else:
        offset = 0

    if '--duration' in sys.argv:
        duration = int(sys.argv[sys.argv.index('--duration')+1])
    else:
        duration = 0

    if '--strain' in sys.argv:
        strain = int(sys.argv[sys.argv.index('--strain')+1])
    else:
        strain = 150

    main(video, fit, outvideo, offset, duration, strain)

