from clld.web import datatables
from clld.web.datatables.base import Col, LinkCol, DetailsRowLinkCol, IdCol, LinkToMapCol, DataTable
from clld.web.datatables.value import Values
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.language import Languages
from parabank.models import Syncretism, Pattern, Word, ParabankParameter, Paradigm, ParabankValueSet, ParabankLanguage
from clld.db.models.common import Language
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import link

#class SyncretismInCol(Col):
#    def format(self, item):
#        return HTML.ul(
#            *[HTML.li(link(self.dt.req, syncretism)) for pair in item.syncretisms],
#            class_="unstyled")


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
            #Col(self, 'parameter'),
            Col(self, 'Language'),
            #Col(self, 'Paradigm')
            Col(self, 'Syncretism')

            ]

class ReferencedInCol(Col):
    def format(self, item):
        return HTML.ul(
            *[HTML.li(link(self.dt.req, language)) for language in item.languages],
            class_="unstyled")


class Syncretisms(DataTable):
    # Lists of syncretisms
    def col_defs(self):
        return [
            LinkCol(self, 'pk', model_col=Syncretism.pk),
            LinkCol(self, 'id', model_col=Syncretism.id),
            LinkCol(self, 'name', model_col=Syncretism.name),
            Col(self, 'description', model_col=Syncretism.description),
            ReferencedInCol(self, 'language', bSearchable=False, bSortable=False),
            ]


class Patterns(DataTable):
    # Lists of patterns
    def col_defs(self):
        return [
            # DetailsRowLinkCol(self, 'd'),
            Col(self, 'pk', model_col=Pattern.pk),
            Col(self, 'id', model_col=Pattern.id),
            Col(self, 'name', model_col=Pattern.name),
            Col(self, 'description', model_col=Pattern.description),
            ReferencedInCol(self, 'language', bSearchable=False, bSortable=False),
            ]


class Paradigms(DataTable):
    # list of paradigms
    def col_defs(self):
        return [
            Col(self, 'pk', model_col=Paradigm.pk),
            Col(self, 'name', model_col=Paradigm.name),
            Col(self, 'description', model_col=Paradigm.description),
            #Col(self, 'languages', model_col=Paradigm.languages),
            #Col(self, 'name', model_col=Paradigm.parameters)
            ]


class ParabankLanguage(Languages):
    def col_defs(self):
        return [
            Col(self, 'Language'),
            Col(self, 'Glottocode'),
            Col(self, 'Family'),
            Col(self, 'Paradigm'),
            Col(self, 'Syncretism'),
            Col(self, 'Source'),
            ]


class ParameterTable(Parameters):
    def col_defs(self):
        return [
            #Col(self, 'id', model_col=ParabankParameter.id),
            #Col(self, 'pk', model_col=ParabankParameter.pk),
            LinkCol(self, 'Name', model_col=ParabankParameter.name),
            Col(self, 'Description', model_col=ParabankParameter.description)
            ]


def includeme(config):
    config.register_datatable('words', Words)
    config.register_datatable('syncretisms', Syncretisms)
    config.register_datatable('patterns', Patterns)
    config.register_datatable('paradigms', Paradigms)
    config.register_datatable('newlanguages', ParabankLanguage) # route /sentences or /languages
    config.register_datatable('parameters', ParameterTable)

