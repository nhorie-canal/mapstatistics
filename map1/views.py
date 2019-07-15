from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from map1.models import *
import map1.csv as csv_data
import csv
from operator import itemgetter
import numpy as np
import logging



class WorkerListView(TemplateView):
    template_name = "body.html"

    def get(self, request, *args, **kwargs):
        logger = logging.getLogger(__name__)
        context = super(WorkerListView, self).get_context_data(**kwargs)

        workers = Worker.objects.all()  # データベースからオブジェクトを取得して
        context['workers'] = workers  # 入れ物に入れる

        with open("./map1/csv/map_001_22.csv", 'r') as f:
            reader = csv.reader(f)

            list = []
            for row in reader:
                list.append(row)
            for row in list:
                row[9] = float(row[9])

            list.sort(key=itemgetter(9))
            list.reverse()
            interval = (list[len(list) - 1][9] - list[0][9])

            yolp_str = '''
<img src="http://map.olp.yahooapis.jp/OpenLocalPlatform/V1/static?
width=800&height=600&lat=35.0&lon=138.4&z=10&appid=dj00aiZpPTd6VmFBandZU2dhOCZzPWNvbnN1bWVyc2VjcmV0Jng9YjI-
&mode=blankmap&style=
'''

            for row in list:
                rgb = self.colorBarRGB((row[9] - list[0][9]) / interval)

                red = format(int(rgb[0] * 255), '02x')
                green = format(int(rgb[1] * 255), '02x')
                blue = format(int(rgb[2] * 255), '02x')
                yolp_str += "bm.p." + row[0] + ":" + red + green + blue + "|"

            yolp_str += '''
">
'''
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




