from clld.web import datatables
from clld.web.datatables.base import Col, LinkCol, DetailsRowLinkCol, IdCol, LinkToMapCol, DataTable
from clld.web.datatables.value import Values
from clld.web.datatables.language import Languages
from parabank08.models import Syncretism, Pattern, Word, ParabankParameter, Paradigm
from clld.db.models.common import Language


class Words(Values):
    # list of the words with languages, parameters and paradigms they show up in.
    def col_defs(self):
        return [
            Col(self, 'word', model_col=Word.word_name, get_object=lambda i: i.Word.word_name),
            Col(self, 'iso', model_col=Word.word_ipa, get_object=lambda i: i.Word.word_ipa),
            Col(self, 'description', model_col=Word.word_description, get_object=lambda i: i.Word.word_description),
            Col(self, 'Parameter', model_col=ParabankParameter.name, get_object=lambda i: i.ParabankParameter.name),
            Col(self, 'Language'),
            Col(self, 'Paradigm')
        ]


class Syncretisms(DataTable):
    # Lists of syncretisms
    def col_defs(self):
        return [
            LinkCol(self, 'name', model_col=Syncretism.name, get_object=lambda i: i.Syncretism.name),
            LinkCol(self, 'description', model_col=Syncretism.description, get_object=lambda i: i.Syncretism.description)
            ]


class Patterns(DataTable):
    # Lists of patterns
    def col_defs(self):
        return [
            LinkCol(self, 'name', model_col=Pattern.name, get_object=lambda i: i.Pattern.name),
            LinkCol(self, 'description', model_col=Pattern.description, get_object=lambda i: i.Pattern.description)
            ]


class Paradigms(DataTable):
    # list of paradigms
    def col_defs(self):
        return [
            Col(self, 'name', model_col=Paradigm.name, get_object=lambda i: i.Paradigm.name),
            Col(self, 'description', model_col=Paradigm.description, get_object=lambda i: i.Paradigm.description),
            Col(self, 'Languages', model_col=Paradigm.languages, get_object=lambda i: i.Paradigm.languages),
            Col(self, 'name', model_col=Paradigm.parameters, get_object=lambda i: i.Paradigm.parameters)
            ]

class ParabankLanguageTable(Languages):
    def col_defs(self):
        return [
            Col(self, 'Language'),
            Col(self, 'Glottocode'),
            Col(self, 'Family'),
            Col(self, 'Paradigm'),
            Col(self, 'Syncretism'),
            Col(self, 'Source')
        ]


def includeme(config):
    config.register_datatable('words', Words)
    config.register_datatable('syncretisms', Syncretisms)
    config.register_datatable('patterns', Patterns)
    config.register_datatable('paradigms', Paradigms)
    config.register_datatable('sentences', ParabankLanguageTable) # route /sentences or /languages
