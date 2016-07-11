from pyramid.renderers import render_to_response
from clld.web.util.htmllib import HTML, literal
from models import Word, ParabankValueSet, ParabankLanguage, ParabankParameter
from clld.db.models.common import Value, ValueSet, Parameter, IdNameDescriptionMixin, Language
from clld.db.meta import DBSession

def syncretism_detail_html(context=None, request=None, **kw):
    return {'project': 'my project'}


def language_detail_html(context=None, request=None, **kw):

    language_glott = unicode(request.path_url[-8:])
    #print language_glott
    param_word = {}
    for each in DBSession.query(ParabankLanguage).filter(ParabankLanguage.id == language_glott):
        langu_key = each.pk

    for x in DBSession.query(ParabankValueSet, Word, ParabankParameter, ParabankLanguage)\
                             .join(Word)\
                             .join(ParabankParameter)\
                             .join(ParabankLanguage)\
                             .filter(ParabankValueSet.language_pk == langu_key):

        param_word[x[2].name] = x[1].word_name

    return {'project': HTML.table(
        HTML.thead(
            HTML.th("", style="height:32px; font-weight:"),
            HTML.th("elder brother", style="height:32px; font-weight: bold; padding: 5px"),
            HTML.th("younger brother", style="height:32px; font-weight: bold; padding: 5px"),
            HTML.th("older sister", style="height:32px; font-weight: bold; padding: 5px"),
            HTML.th("younger sister", style="height:32px; font-weight: bold; padding: 5px"),
            style="background: #F2F2F2",
        ),

        HTML.tr(
            HTML.td('male', style="height:32px; font-weight: bold; background: #F2F2F2; padding: 5px"),
            HTML.td(param_word['meB'], style="height:32px; border: 1px solid gray; padding: 5px"),
            HTML.td(param_word['myB'], style="height:32px; border: 1px solid gray; padding: 5px"),
            HTML.td(param_word['meZ'], style="height:32px; border: 1px solid gray; padding: 5px"),
            HTML.td(param_word['myZ'], style="height:32px; border: 1px solid gray; padding: 5px"),
        ),

        HTML.tr(
            HTML.td('female', style="height:32px; font-weight: bold; background: #F2F2F2; padding: 5px"),
            HTML.td(param_word['feB'], style="height:32px; border: 1px solid gray; padding: 5px"),
            HTML.td(param_word['fyB'], style="height:32px; border: 1px solid gray; padding: 5px"),
            HTML.td(param_word['feZ'], style="height:32px; border: 1px solid gray; padding: 5px"),
            HTML.td(param_word['fyZ'], style="height:32px; border: 1px solid gray; padding: 5px"),
        )
    )}

#style="height:32px; border: 1px solid black; font-weight: bold;"