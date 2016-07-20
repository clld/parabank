from clld.web import datatables
from clld.web.datatables.base import Col, LinkCol, DetailsRowLinkCol, IdCol, LinkToMapCol, DataTable
from clld.web.datatables.value import Values
from clld.web.datatables.parameter import Parameters
from clld.web import datatables
from parabank.models import Syncretism, Pattern, Word, ParabankParameter, Paradigm, ParabankValueSet, ParabankLanguage
#from clld.db.models.common import Language
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import link


class Words(DataTable):
    # list of the words with languages, parameters and paradigms they show up in.
    def col_defs(self):
        return [
            Col(self, 'pk', model_col=Word.pk),
            Col(self, 'id', model_col=Word.id),
            Col(self, 'word', model_col=Word.word_name),
            Col(self, 'IPA', model_col=Word.word_ipa),
            #Col(self, 'description', model_col=Word.word_description),
            Col(self, 'valueset', model_col=Word.valueset_pk),
            Col(self, 'parameter', model_col=ParabankValueSet.parameter_pk),
            Col(self, 'Language'),
            #Col(self, 'Paradigm')
            Col(self, 'Syncretism')

            ]

class LanguageInCol(Col):
    def format(self, item):
        return HTML.ul(
            *[HTML.li(link(self.dt.req, language)) for language in item.languages],
            class_="unstyled")

class ParameterInCol(Col):
    def format(self, item):
        return HTML.p(
            *[link(self.dt.req, parameter, style_="padding-left:10px") for parameter in item.parameters],
            class_="unstyled")


class Syncretisms(DataTable):
    # Lists of syncretisms
    def col_defs(self):
        return [
            #LinkCol(self, 'pk', model_col=Syncretism.pk),
            #LinkCol(self, 'id', model_col=Syncretism.id),
            LinkCol(self, 'name', model_col=Syncretism.name),
            Col(self, 'description', model_col=Syncretism.description),
            LanguageInCol(self, 'language', bSearchable=False, bSortable=False),
            ]


class Patterns(DataTable):
    # Lists of patterns
    def col_defs(self):
        return [
            # DetailsRowLinkCol(self, 'd'),
            #Col(self, 'pk', model_col=Pattern.pk),
            #Col(self, 'id', model_col=Pattern.id),
            LinkCol(self, 'name', model_col=Pattern.name),
            Col(self, 'description', model_col=Pattern.description),
            LanguageInCol(self, 'language', bSearchable=False, bSortable=False),
            ]


class Paradigms(DataTable):
    # list of paradigms
    def col_defs(self):
        return [
            #Col(self, 'pk', model_col=Paradigm.pk),
            Col(self, 'name', model_col=Paradigm.name),
            Col(self, 'description', model_col=Paradigm.description),
            #Col(self, 'languages', model_col=Paradigm.languages),
            ParameterInCol(self, 'parameters', bSearchable=False, bSortable=False)
            ]


class ParameterTable(Parameters):
    def col_defs(self):
        return [
            #Col(self, 'id', model_col=ParabankParameter.id),
            #Col(self, 'pk', model_col=ParabankParameter.pk),
            LinkCol(self, 'Name', model_col=ParabankParameter.name),
            Col(self, 'Description', model_col=ParabankParameter.description)
            ]

class SyncretismInCol(Col):
    def format(self, item):
        return HTML.ul(
            *[HTML.li(link(self.dt.req, syncretism)) for syncretism in item.syncretisms],
            class_="unstyled")

class PatternInCol(Col):
    def format(self, item):
        return HTML.ul(
            *[HTML.li(link(self.dt.req, pattern)) for pattern in item.patterns],
            class_="unstyled")

class Languages(datatables.Languages):
    def col_defs(self):
        return [
            Col(self, 'id'),
            LinkCol(self, 'name'),
            #Col(self, 'latitude'),
            #Col(self, 'longitude'),
            SyncretismInCol(self, 'syncretism', bSearchable=False, bSortable=False),
            SyncretismInCol(self, 'pattern', bSearchable=False, bSortable=False),
        ]


class Values(datatables.Values):

    def col_defs(self):

        if self.language:
            return [
                #Col(self, 'id'),
                LinkCol(self, 'name'),
                Col(self, 'ipa', model_col=Word.word_ipa),
                Col(self, 'reference', model_col=Word.word_reference),
                LinkCol(self,
                        'parameter',
                        sTitle=self.req.translate('Parameter'),
                        model_col=ParabankParameter.name,
                        get_object=lambda i: i.valueset.parameter),
            ]
        if self.parameter:
            return [
                Col(self, 'id'),
                LinkCol(self, 'name'),
                Col(self, 'ipa', model_col=Word.word_ipa),
                LinkCol(self,
                        'language',
                        model_col=ParabankLanguage.name,
                        get_object=lambda i: i.valueset.language),
            ]

def includeme(config):
    config.register_datatable('words', Words)
    config.register_datatable('syncretisms', Syncretisms)
    config.register_datatable('patterns', Patterns)
    config.register_datatable('paradigms', Paradigms)
    config.register_datatable('parameters', ParameterTable)
    config.register_datatable('languages', Languages)
    config.register_datatable('values', Values)

