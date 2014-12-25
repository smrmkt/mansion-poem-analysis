#!/usr/bin/env python
#-*-coding:utf-8-*-

import os.path

cd = os.path.dirname(__file__)


class KmlGenerator(object):
    def __init__(self):
        pass

    def generate(self, title, coordinates):
        kml = self._generate_header(title)
        for lon, lat in coordinates:
            kml += '\t{0}\n\t{1}\n\t{2}\n\t{3}{4},{5},0{6}\n\t{7}\n\t{8}\n'.format(
                '<Placemark>',
                '<styleUrl>#icon-22</styleUrl>',
                '<Point>',
                '<coordinates>',
                lon,
                lat,
                '</coordinates>',
                '</Point>',
                '</Placemark>'
            )
        return kml +self._generate_footer()

    @staticmethod
    def _generate_header(title):
        return '{0}\n{1}\n\t{2}\n\t{3}{4}{5}\n'.format(
            '<?xml version=\'1.0\' encoding=\'UTF-8\'?>',
            '<kml xmlns=\'http://www.opengis.net/kml/2.2\'>',
            '<Document>',
            '<name>',
            title,
            '</name>'
        )

    @staticmethod
    def _generate_footer():
        return '\t{0}\n\t{1}\n\t{2}\n\t{3}\n\t{4}\n\t{5}\n\t{6}\n\t{7}\n\t{8}\n{9}'.format(
            '<Style id=\'icon-22\'>',
            '<IconStyle>',
            '<scale>1.1</scale>',
            '<Icon>',
            '<href>http://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>',
            '</Icon>',
            '</IconStyle>',
            '</Style>',
            '</Document>',
            '</kml>'
        )