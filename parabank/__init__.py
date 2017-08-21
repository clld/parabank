# coding: utf8
from __future__ import unicode_literals, print_function, division

from pyramid.config import Configurator
from clld_glottologfamily_plugin.util import LanguageByFamilyMapMarker
from clld.interfaces import IMapMarker

# we must make sure custom models are known at database initialization!
from parabank import models

from parabank.models import Syncretism, Pattern, Paradigm, Word
from parabank.interfaces import ISyncretism, IPattern, IParadigm
from clld import interfaces as clldInt


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clld.web.app')
    config.include('clld_glottologfamily_plugin')
    config.registry.registerUtility(LanguageByFamilyMapMarker(), IMapMarker)

    config.register_resource('syncretism', Syncretism, ISyncretism, with_index=True)
    config.register_resource('pattern', Pattern, IPattern, with_index=True)
    config.register_resource('paradigm', Paradigm, IParadigm, with_index=True)
    #config.register_resource('word', Word, clldInt.IValue, with_index=True)

    return config.make_wsgi_app()
