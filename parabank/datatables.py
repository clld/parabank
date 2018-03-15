# coding: utf8
from __future__ import unicode_literals, print_function, division

from clld.web import datatables
from clld.web.datatables.base import Col, LinkCol, DataTable
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.language import Languages
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import link
from clld.db.models.common import Parameter, Language, ValueSet
from clld_glottologfamily_plugin.datatables import FamilyLinkCol
from clld_glottologfamily_plugin.models import Family

from parabank.models import Word, ParabankLanguage


class Words(DataTable):
    # list of the words with languages, parameters and paradigms they show up in.
    def col_defs(self):
        return [
            Col(self, 'pk', model_col=Word.pk),
            Col(self, 'id', model_col=Word.id),
            Col(self, 'word', model_col=Word.name),
            Col(self, 'IPA', model_col=Word.ipa),
            Col(self, 'valueset', model_col=Word.valueset_pk),
            Col(self, 'parameter', model_col=ValueSet.parameter_pk),
            Col(self, 'Language'),
            Col(self, 'Syncretism')
        ]


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
            LinkCol(self, 'name'),
            Col(self, 'description')
        ]


class ParabankLanguages(Languages):
    def base_query(self, query):
        return query.join(ParabankLanguage.family)

    def col_defs(self):
        return [
            Col(self, 'id'),
            LinkCol(self, 'name'),
            FamilyLinkCol(self, 'family', ParabankLanguage),
            Col(self, 'contribution'),
        ]


class Values(datatables.Values):
    def col_defs(self):
        if self.language:
            return [
                LinkCol(self, 'name'),
                Col(self, 'ipa', model_col=Word.ipa),
                Col(self, 'alternative', model_col=Word.alternative),
                LinkCol(
                    self,
                    'parameter',
                    sTitle=self.req.translate('Parameter'),
                    model_col=Parameter.name,
                    get_object=lambda i: i.valueset.parameter),
                Col(self, 'comment', model_col=Word.comment),
            ]
        if self.parameter:
            return [
                Col(self, 'id'),
                LinkCol(self, 'name'),
                Col(self, 'ipa', model_col=Word.ipa),
                LinkCol(
                    self,
                    'language',
                    model_col=Language.name,
                    get_object=lambda i: i.valueset.language),
            ]


def includeme(config):
    config.register_datatable('words', Words)
    config.register_datatable('parameters', ParameterTable)
    config.register_datatable('languages', ParabankLanguages)
    config.register_datatable('values', Values)
