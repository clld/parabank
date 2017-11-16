# coding: utf8
from __future__ import unicode_literals, print_function, division

from clld.web.maps import Map, Layer, GeoJson, IMapMarker
from clld.interfaces import ILanguage
from clld.web.util.helpers import map_marker_img
from clld.web.icon import MapMarker

ICONS = {'kin': 'c4d6cee',  # blue
         'pron': 'cffff00', # yellow
         'both': 'c00ff00', # green
         }


def icon_url(req, type_):
    return req.static_url('clld:web/static/icons/%s.png' % ICONS[type_])

class SyncretismMap(Map):
    def get_layers(self):
        for de in self.ctx.languages:
            yield Layer(
                de.id,
                de.name,
                GeoJson(self.ctx).render(de, self.req, dump=False))


class PatternMap(Map):
    def get_layers(self):
        for de in self.ctx.languages:
            yield Layer(
                de.id,
                de.name,
                GeoJson(self.ctx).render(de, self.req, dump=False))



"""
class ParabankMapMarker(IMapMarker):
    def __call__(self, ctx, req):

        asset_spec = 'clld:web/static/icons/ffffff.png'
        return req.static_url(asset_spec)
"""
class ParabankMapMarker(MapMarker):
    def __call__(self, ctx, req):
        if ILanguage.providedBy(ctx):
            if ctx:
                icon = 'c4d6cee'
            else:
                icon = 'cffff00'
            asset_spec = 'clld:web/static/icons/%s.png' % icon
        return req.static_url(asset_spec)

class LanguagesMap(Map):
    def __init__(self, ctx, req, eid='map'):

        Map.__init__(self, ctx, req, eid=eid)
        print (self.req.params)
        print (self.ctx)
        print (ctx.__provides__)
        print(req.registry)

    def get_options(self):
        return {'icon_size': 10}

"""
class ParabankMapMarker(IMapMarker):
    def __call__(self, ctx, req):
        if ILanguage.providedBy(ctx):
            if ctx.has_kinship:
                icon = 'c4d6cee'
            elif ctx.has_pronoun:
                icon = 'cffff00'
            asset_spec = 'clld:web/static/icons/%s.png' % icon
        return req.static_url(asset_spec)
"""

def includeme(config):
    config.register_map('syncretism', SyncretismMap)
    config.register_map('pattern', PatternMap)
    config.register_map('languages', LanguagesMap)