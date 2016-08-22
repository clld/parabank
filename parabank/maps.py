from clld.web.maps import Map, Layer, GeoJson


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


def includeme(config):
    config.register_map('syncretism', SyncretismMap)
    config.register_map('pattern', PatternMap)
