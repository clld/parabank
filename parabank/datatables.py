from clld.web import datatables
from clld.web.datatables.base import Col, LinkCol, DataTable
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.language import Languages
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import link
from clld.db.models.common import Parameter, Language, ValueSet
from clld_glottologfamily_plugin.datatables import FamilyCol
from clld.web.util import glottolog

from parabank.models import Word, ParabankLanguage


def list_of_links(req, items, container=HTML.ul, item=HTML.li, link_attrs=None):
    link_attrs = link_attrs or {}
    return container(
        *[item(link(req, i, **link_attrs)) for i in items], class_="unstyled")


class LanguageInCol(Col):
    def format(self, item):
        return list_of_links(self.dt.req, item.languages)


class ParameterInCol(Col):
    def format(self, item):
        return list_of_links(
            self.dt.req,
            item.parameters,
            container=HTML.p,
            item=HTML.span,
            link_attrs=dict(style_="padding-left:10px"))


class LanguageUnorderedInCol(Col):
    def format(self, item):
        return HTML.p(
            *[link(self.dt.req, language, style_="padding-left:10px") + ","
              for language in item.languages],
            class_="unstyled")


class ParameterTable(Parameters):
    def col_defs(self):
        return [
            IdLinkCol(self, 'id', sTitle='Name'),
            Col(self, 'name', sTitle='Description'),
            Col(self, 'description', sTitle='Examples')
        ]


class GlottocodeCol(Col):
    def format(self, item):
        return glottolog.link(self.dt.req, item.id, label=item.id)


class ParabankLanguages(Languages):
    def base_query(self, query):
        return query.join(ParabankLanguage.family)

    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            GlottocodeCol(self, 'id'),
            FamilyCol(self, 'family', ParabankLanguage),
            Col(self, 'classification', model_col=ParabankLanguage.classification),
            Col(self, 'source', model_col=ParabankLanguage.source),
        ]


class IdLinkCol(LinkCol):
    def get_attrs(self, item):
        return {'label': self.get_obj(item).id}


class Values(datatables.Values):
    def col_defs(self):
        if self.language:
            return [
                Col(self, 'name', sTitle='Term'),
                IdLinkCol(
                    self,
                    'parameter',
                    sTitle=self.req.translate('Parameter'),
                    model_col=Parameter.id,
                    get_object=lambda i: i.valueset.parameter),
                LinkCol(
                    self,
                    'description',
                    model_col=Parameter.name,
                    get_object=lambda i: i.valueset.parameter),
                Col(self, 'comment', model_col=Word.comment),
                Col(self, '#', model_col=Word.original),
            ]
        if self.parameter:
            return [
                Col(self, 'name', sTitle='Term'),
                LinkCol(
                    self,
                    'language',
                    model_col=Language.name,
                    get_object=lambda i: i.valueset.language),
                FamilyCol(
                    self,
                    'family',
                    ParabankLanguage,
                    get_object=lambda i: i.valueset.language),
                Col(self,
                    'classification',
                    model_col=ParabankLanguage.classification,
                    get_object=lambda i: i.valueset.language),
                Col(self,
                    'source',
                    model_col=ParabankLanguage.source,
                    get_object=lambda i: i.valueset.language),
                Col(self, '#', model_col=Word.original),
            ]


def includeme(config):
    config.register_datatable('parameters', ParameterTable)
    config.register_datatable('languages', ParabankLanguages)
    config.register_datatable('values', Values)
