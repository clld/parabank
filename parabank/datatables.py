# coding: utf8
from __future__ import unicode_literals, print_function, division

from clld.web import datatables
from clld.web.datatables.base import Col, LinkCol, DataTable
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.language import Languages
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import link
from clld.db.models.common import Parameter, Language

from parabank.models import Syncretism, Pattern, Word, Paradigm, ParabankValueSet


class Words(DataTable):
    # list of the words with languages, parameters and paradigms they show up in.
    def col_defs(self):
        return [
            Col(self, 'pk', model_col=Word.pk),
            Col(self, 'id', model_col=Word.id),
            Col(self, 'word', model_col=Word.name),
            Col(self, 'IPA', model_col=Word.ipa),
            Col(self, 'valueset', model_col=Word.valueset_pk),
            Col(self, 'parameter', model_col=ParabankValueSet.parameter_pk),
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


class Syncretisms(DataTable):
    def col_defs(self):
        return [
            LinkCol(self, 'name', model_col=Syncretism.name),
            Col(self, 'description', model_col=Syncretism.description),
            Col(self, 'notation', model_col=Syncretism.notation),
            LanguageUnorderedInCol(self, 'language', bSearchable=False, bSortable=False),
        ]


class Patterns(DataTable):
    def col_defs(self):
        return [
            LinkCol(self, 'name', model_col=Pattern.name),
            Col(self, 'description', model_col=Pattern.description),
            Col(self, 'notation', model_col=Syncretism.notation),
            LanguageUnorderedInCol(self, 'language', bSearchable=False, bSortable=False),
        ]


class Paradigms(DataTable):
    def col_defs(self):
        return [
            Col(self, 'name', model_col=Paradigm.name),
            Col(self, 'description', model_col=Paradigm.description),
            ParameterInCol(self, 'parameters', bSearchable=False, bSortable=False)
        ]


class ParameterTable(Parameters):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            Col(self, 'description')
        ]


class SyncretismInCol(Col):
    def format(self, item):
        return list_of_links(self.dt.req, item.syncretisms)


class PatternInCol(Col):
    def format(self, item):
        return list_of_links(self.dt.req, item.patterns)


class ParabankLanguages(Languages):
    def col_defs(self):
        return [
            Col(self, 'id'),
            LinkCol(self, 'name'),
            Col(self, 'contribution'),
            SyncretismInCol(self, 'syncretism', bSearchable=False, bSortable=False),
            PatternInCol(self, 'pattern', bSearchable=False, bSortable=False),
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
    config.register_datatable('syncretisms', Syncretisms)
    config.register_datatable('patterns', Patterns)
    config.register_datatable('paradigms', Paradigms)
    config.register_datatable('parameters', ParameterTable)
    config.register_datatable('languages', ParabankLanguages)
    config.register_datatable('values', Values)
