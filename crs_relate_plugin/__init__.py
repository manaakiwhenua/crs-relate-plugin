# =================================================================
#
# Authors: Richard Law <lawr@landcareresearch.co.nz>
#
# Copyright (c) 2020 Landcare Research
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import logging

from pyproj import CRS
from shapely import wkt
from shapely.geometry import box

from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError

LOGGER = logging.getLogger(__name__)

#: Process metadata and description
PROCESS_METADATA = {
    'version': '0.0.1',
    'id': 'crs-extent',
    'title': 'CRS Extent',
    'description': 'A process that validates geometric relationships between an arbitrary geometry and its declared CRS\' extent. For example, this process allows you to take a geometry that is stated to be recorded in a particular coordinate reference system, and then validate whether it is actually contained by the CRS\' area of use',
    'keywords': ['CRS', 'extent', 'topology', 'DE-9IM'],
    'links': [{
        'type': 'text/html',
        'rel': 'help',
        'title': 'DE-9IM information',
        'href': 'https://en.wikipedia.org/wiki/DE-9IM',
        'hreflang': 'en-US'
    }, {
        'type': 'text/html',
        'rel': 'help',
        'title': 'Shapely\'s documentation on DE-9IM relationships',
        'href': 'https://shapely.readthedocs.io/en/latest/manual.html#de-9im-relationships',
        'hreflang': 'en-US'
    }],
    'inputs': [{
        'id': 'wkt', # TODO a URI?
        'title': 'WKT geometry',
        'abstract': 'Candidate geometry.',
        'input': {
            'literalDataDomain': {
                'dataType': 'string',
                'valueDefinition': {
                    'anyValue': False,
                    'defaultValue': 'MULTIPOINT ((10 40), (40 30), (20 20), (30 10))'
                }
            }
        },
        'minOccurs': 1,
        'maxOccurs': None,
        'metadata': None, # TODO how to use?
        'keywords': ['WKT', 'geometry']
    }, {
        'id': 'crs',
        'title': 'CRS',
        'abstract': 'CRS of the input geometry. If multiple geometries are given, all are assumed to have the same declared CRS.',
        'input': {
            'literalDataDomain': {
                'dataType': 'string',
                'valueDefinition': {
                    'anyValue': False,
                    'defaultValue': 'EPSG:4326'
                }
            }
        },
        'minOccurs': 1,
        'maxOccurs': 1,
        'metadata': None,
        'keywords': ['CRS', 'PROJ']
    }],
    'outputs': [{
        'id': 'de-9im',
        'title': 'DE-9IM relationship',
        'description': 'A string representing the DE-9IM relationship between the bounds of the input CRS, and the candidate geometry.',
        'output': {
            'formats': [{
                'mimeType': 'application/json'
            }]
        }
    }],
    'example': {
        'inputs': [{
            'id': 'wkt',
            'value': 'MULTIPOINT ((10 40), (40 30), (20 20), (30 10))',
            'type': 'text/plain'
        },{
            'id': 'crs',
            'value': 'WPSG:4326',
            'type': 'text/plain'
        }]
    }
}


class CRSExtentProcessor(BaseProcessor):
    """CRS Extent Processor"""

    def __init__(self, processor_def):
        """
        Initialize object
        :param processor_def: provider definition
        :returns: pygeoapi.process.crs_extent.CRSExtentProcessor
        """

        BaseProcessor.__init__(self, processor_def, PROCESS_METADATA)

    def execute(self, data):
        wkt_input = data.get('wkt', self.get_default('wkt'))
        if not isinstance(wkt_input, list):
            wkt_input = [wkt_input]
        geoms = map(lambda geom: wkt.loads(geom), wkt_input)
        crs = CRS.from_user_input(data.get('crs').strip())
        area_of_use = box(*crs.area_of_use.bounds) # minx, miny, maxx, maxy
        return [{
            'id': 'de-9im', 'value': area_of_use.relate(geom)
        } for geom in geoms] # https://shapely.readthedocs.io/en/latest/manual.html#object.relate

    def __repr__(self):
        return '<CRSExtentProcessor> {}'.format(self.name)
