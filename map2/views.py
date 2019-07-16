from django.shortcuts import render
from django.views.generic import TemplateView

import csv
from operator import itemgetter
import numpy as np
from mapstatistics.settings import BASE_DIR
import logging


class WorkerListView2(TemplateView):
    template_name = BASE_DIR + "/map2/templates/body.html"

    def get(self, request, *args, **kwargs):
        logger = logging.getLogger(__name__)
        context = super(WorkerListView2, self).get_context_data(**kwargs)

        with open(BASE_DIR + "/map2/csv/map2015.csv", 'r') as f:
            reader = csv.reader(f)

            list = []
            for row in reader:
                if row[0] == "11" or row[0] == "12" or row[0] == "13" or row[0] == "14":
                    list.append(row)
            for row in list:
                row[13] = float(row[13].replace(',', ''))

            list.sort(key=itemgetter(13))
            list.reverse()
            interval = (list[len(list) - 1][13] - list[0][13])

            yolp_str = '''
<img src="http://map.olp.yahooapis.jp/OpenLocalPlatform/V1/static?
width=1200&height=900&lat=35.6&lon=139.8&z=11&appid=dj00aiZpPTd6VmFBandZU2dhOCZzPWNvbnN1bWVyc2VjcmV0Jng9YjI-
&mode=blankmap&style=
'''

            for row in list:
                rgb = self.colorBarRGB((row[13] - list[0][13]) / interval)
                red = format(int(rgb[0] * 255), '02x')
                green = format(int(rgb[1] * 255), '02x')
                blue = format(int(rgb[2] * 255), '02x')
                yolp_str += "bm.p." + row[1] + ":" + red + green + blue + "|"

            yolp_str += '''
">
'''
        logger.error(yolp_str)

        context['yolp_str'] = yolp_str  # 入れ物に入れる
        context['list'] = list  # 入れ物に入れる

        return render(self.request, self.template_name, context)

    def colorBarRGB(self, x):
        gain = 10
        offset_x = 0.2
        offset_green = 0.6

        x = (x * 2) - 1
        red = self.sigmoid(x, gain, -1 * offset_x)
        blue = 1 - self.sigmoid(x, gain, offset_x)
        green = self.sigmoid(x, gain, offset_green) + (1 - self.sigmoid(x, gain, -1 * offset_green))
        green = green - 1.0
        return (blue, green, red)


    def sigmoid(self, x, gain=1, offset_x=0):
        return ((np.tanh(((x + offset_x) * gain) / 2) + 1) / 2)




