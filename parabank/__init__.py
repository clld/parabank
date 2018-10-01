# coding: utf8
from __future__ import unicode_literals, print_function, division

from pyramid.config import Configurator
from clld_glottologfamily_plugin.util import LanguageByFamilyMapMarker, ISOLATES_ICON
from clld.interfaces import IValue, IValueSet, IMapMarker, IDomainElement, ILanguage
from clld.lib.svg import icon, data_url

# we must make sure custom models are known at database initialization!
from parabank import models

from parabank.models import Word

_ = lambda s: s
_('Familys')
_('Parameter')
_('Parameters')


class ParabankMapMarker(LanguageByFamilyMapMarker):
    def svg_icon(self, de):
        return data_url(icon(('t' if de.description.endswith('other') else 'c') + de.jsondata['color'][1:]))

    def __call__(self, ctx, req):
        if IDomainElement.providedBy(ctx):
            return self.svg_icon(ctx)
        if IValue.providedBy(ctx):
            if ctx.domainelement_pk:
                return self.svg_icon(ctx.domainelement)
            return LanguageByFamilyMapMarker.__call__(self, ctx.valueset.language, req)
        if IValueSet.providedBy(ctx):
            if ctx.values[0].domainelement_pk:
                return self.svg_icon(ctx.values[0].domainelement)
            return LanguageByFamilyMapMarker.__call__(self, ctx.language, req)
        if ILanguage.providedBy(ctx):
            if ctx.family:
                return data_url(icon(ctx.family.jsondata['icon']))
            return data_url(icon(req.registry.settings.get('clld.isolates_icon', ISOLATES_ICON)))
        return LanguageByFamilyMapMarker.__call__(self, ctx, req)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clld.web.app')
    config.include('clld_glottologfamily_plugin')
    config.registry.registerUtility(ParabankMapMarker(), IMapMarker)
    return config.make_wsgi_app()
