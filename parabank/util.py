from pyramid.renderers import render_to_response
from clld.web.util.htmllib import HTML, literal
from models import Word, ParabankValueSet, ParabankLanguage, ParabankParameter
from clld.db.models.common import Value, ValueSet, Parameter, IdNameDescriptionMixin, Language
from clld.db.meta import DBSession
from clld.web.util.multiselect import MultiSelect, CombinationMultiSelect

def language_detail_html(context=None, request=None, **kw):

    language_glott = unicode(request.path_url[-8:])
    #print language_glott
    parameter_list = [
        "mF", "mM", "fF", "fM",
        "mEB", "mYB", "mEZ", "mYZ", "fEB", "fYB", "fEZ", "fYZ",
        "mFBS", "mFBD", "mFZS", "mFZD", "mMBS", "mMBD", "mMZS", "mMZD",
        "fFBS", "fFBD", "fFZS", "fFZD", "fMBS", "fMBD", "fMZS", "fMZD",
        "mFeB", "mFyB", "mFeZ", "mFyZ", "mMeB", "mMyB", "mMeZ", "mMyZ",
        "fFeB", "fFyB", "fFeZ", "fFyZ", "fMeB", "fMyB", "fMeZ", "fMyZ",
        "mFBeS", "mFByS", "mFBeD", "mFByD", "mFZeS", "mFZyS", "mFZeD", "mFZyD",
        "fFBeS", "fByS", "fFBeD", "fFByD", "fFZeS", "fFZyS", "fFZeD", "fFZyD",
        "mFF", "mFM", "mMF", "mMM", "mSS", "mSD", "mDS", "mDD",
        "fFF", "fFM", "fMF", "fMM", "fSS", "fSD", "fDS", "fDD",
        "meBS", "meBD", "myBS", "myBD", "meZS", "meZD", "myZS", "myZD",
        "feBS", "feBD", "fyBS", "fyBD", "feZS", "feZD", "fyZS", "fyZD",
        "mS", "mD", "fS", "fD",
        "mW", "fH", "mWF", "mWM", "fHF", "fHM",
        "mSW", "mDH", "fSW", "fDH",
        ]

    param_word = {}
    for pa in parameter_list:
        param_word[pa] = "-"

    for each in DBSession.query(ParabankLanguage).filter(ParabankLanguage.id == language_glott):
        langu_key = each.pk

    for x in DBSession.query(ParabankValueSet, Word, ParabankParameter, ParabankLanguage)\
                             .join(Word)\
                             .join(ParabankParameter)\
                             .join(ParabankLanguage)\
                             .filter(ParabankValueSet.language_pk == langu_key):

        param_word[x[2].name] = x[1].word_name

    paradigm_tables = \
        {
        'siblings':
            HTML.table(
                HTML.thead(
                    HTML.th("", style="height:26px; font-weight:"),
                    HTML.th("eB",),
                    HTML.th("yB",),
                    HTML.th("eZ",),
                    HTML.th("yZ",),
                    style="background: #F2F2F2",
                ),

                HTML.tr(
                    HTML.td('male', style="height:26px; font-weight: bold; background: #F2F2F2; padding: 5px"),
                    HTML.td(param_word['meB'],),
                    HTML.td(param_word['myB'],),
                    HTML.td(param_word['meZ'],),
                    HTML.td(param_word['myZ'],),
                ),

                HTML.tr(
                    HTML.td('female', style="height:26px; font-weight: bold; background: #F2F2F2; padding: 5px"),
                    HTML.td(param_word['feB'],),
                    HTML.td(param_word['fyB'],),
                    HTML.td(param_word['feZ'],),
                    HTML.td(param_word['fyZ'],),
                )
            ),
        'cousins':
            HTML.table(
                HTML.thead(
                    HTML.th("", style="height:26px; font-weight:"),
                    HTML.th("FBS",),
                    HTML.th("FBD",),
                    HTML.th("FZS",),
                    HTML.th("FZD",),
                    HTML.th("MBS",),
                    HTML.th("MBD",),
                    HTML.th("MZS",),
                    HTML.th("MZD",),
                    style="background: #F2F2F2",
                ),

                HTML.tr(
                    HTML.td('male', style="height:26px; font-weight: bold; background: #F2F2F2; padding: 5px"),
                    HTML.td(param_word['mFBS'],),
                    HTML.td(param_word['mFBD'],),
                    HTML.td(param_word['mFZS'],),
                    HTML.td(param_word['mFZD'],),
                    HTML.td(param_word['mMBS'],),
                    HTML.td(param_word['fMBD'],),
                    HTML.td(param_word['fMZS'],),
                    HTML.td(param_word['fMZD'],),
                ),

                HTML.tr(
                    HTML.td('female', style="height:26px; font-weight: bold; background: #F2F2F2; padding: 5px"),
                    HTML.td(param_word['fFBS'],),
                    HTML.td(param_word['fFBD'],),
                    HTML.td(param_word['fFZS'],),
                    HTML.td(param_word['fFZD'],),
                    HTML.td(param_word['fMBS'],),
                    HTML.td(param_word['fMBD'],),
                    HTML.td(param_word['fMZS'],),
                    HTML.td(param_word['fMZD'],),
                )
            ),
        'parents':
            HTML.table(
                HTML.thead(
                    HTML.th("",),
                    HTML.th("FEB",),
                    HTML.th("FYB",),
                    HTML.th("FEZ",),
                    HTML.th("FYZ",),
                    HTML.th("F",),
                    HTML.th("M",),
                    HTML.th("MEB",),
                    HTML.th("MYB",),
                    HTML.th("MEZ",),
                    HTML.th("MYZ",),
                ),

                HTML.tr(
                    HTML.td('male', style="height:26px; font-weight: bold; background: #F2F2F2; padding: 5px"),
                    HTML.td(param_word['mFeB'],),
                    HTML.td(param_word['mFyB'],),
                    HTML.td(param_word['mFeZ'],),
                    HTML.td(param_word['mFyZ'],),
                    HTML.td(param_word['mF'],),
                    HTML.td(param_word['mM'],),
                    HTML.td(param_word['mMeB'],),
                    HTML.td(param_word['mMyB'],),
                    HTML.td(param_word['mMeZ'],),
                    HTML.td(param_word['mMyZ'],),
                ),

                HTML.tr(
                    HTML.td('female', style="height:26px; font-weight: bold; background: #F2F2F2; padding: 5px"),
                    HTML.td(param_word['fFeB'],),
                    HTML.td(param_word['fFyB'],),
                    HTML.td(param_word['fFeZ'],),
                    HTML.td(param_word['fFyZ'],),
                    HTML.td(param_word['mF'],),
                    HTML.td(param_word['mM'],),
                    HTML.td(param_word['fMeB'],),
                    HTML.td(param_word['fMyB'],),
                    HTML.td(param_word['fMeZ'],),
                    HTML.td(param_word['fMyZ'],),
                )
            ),
        'grand':
            HTML.table(
                HTML.thead(
                    HTML.th("", ),
                    HTML.th("FF", ),
                    HTML.th("FM", ),
                    HTML.th("MF", ),
                    HTML.th("MM", ),
                    HTML.th("SS", ),
                    HTML.th("SD", ),
                    HTML.th("DS", ),
                    HTML.th("DD", ),
                ),

                HTML.tr(
                    HTML.td('male', style="height:26px; font-weight: bold; background: #F2F2F2; padding: 5px"),
                    HTML.td(param_word['mFF'], ),
                    HTML.td(param_word['mFM'], ),
                    HTML.td(param_word['mMF'], ),
                    HTML.td(param_word['mMM'], ),
                    HTML.td(param_word['mSS'], ),
                    HTML.td(param_word['mSD'], ),
                    HTML.td(param_word['mDS'], ),
                    HTML.td(param_word['mDD'], ),
                ),

                HTML.tr(
                    HTML.td('female', style="height:26px; font-weight: bold; background: #F2F2F2; padding: 5px"),
                    HTML.td(param_word['fFF'], ),
                    HTML.td(param_word['fFM'], ),
                    HTML.td(param_word['fMF'], ),
                    HTML.td(param_word['fMM'], ),
                    HTML.td(param_word['fSS'], ),
                    HTML.td(param_word['fSD'], ),
                    HTML.td(param_word['fDS'], ),
                    HTML.td(param_word['fDD'], ),
                )
            ),

        'sons':
            HTML.table(
                HTML.thead(
                    HTML.th("", ),
                    HTML.th("EBS", ),
                    HTML.th("EBD", ),
                    HTML.th("YBS", ),
                    HTML.th("YBD", ),
                    HTML.th("S", ),
                    HTML.th("D", ),
                    HTML.th("EZS", ),
                    HTML.th("EZD", ),
                    HTML.th("YZS", ),
                    HTML.th("YZD", ),
                ),

                HTML.tr(
                    HTML.td('male', style="height:26px; font-weight: bold; background: #F2F2F2; padding: 5px"),
                    HTML.td(param_word['meBS'], ),
                    HTML.td(param_word['meBD'], ),
                    HTML.td(param_word['myBS'], ),
                    HTML.td(param_word['myBD'], ),
                    HTML.td(param_word['mS'], ),
                    HTML.td(param_word['mD'], ),
                    HTML.td(param_word['meZS'], ),
                    HTML.td(param_word['meZD'], ),
                    HTML.td(param_word['myZS'], ),
                    HTML.td(param_word['myZD'], ),
                ),

                HTML.tr(
                    HTML.td('female', style="height:26px; font-weight: bold; background: #F2F2F2; padding: 5px"),
                    HTML.td(param_word['feBS'], ),
                    HTML.td(param_word['feBD'], ),
                    HTML.td(param_word['fyBS'], ),
                    HTML.td(param_word['fyBD'], ),
                    HTML.td(param_word['fS'], ),
                    HTML.td(param_word['fD'], ),
                    HTML.td(param_word['feZS'], ),
                    HTML.td(param_word['feZD'], ),
                    HTML.td(param_word['fyZS'], ),
                    HTML.td(param_word['fyZD'], ),
                )
            ),

        'inlaws':
            HTML.table(
                HTML.thead(
                    HTML.th("", ),
                    HTML.th("H / W", ),
                    HTML.th("HF / WF", ),
                    HTML.th("HM / WM", ),
                    HTML.th("SW", ),
                    HTML.th("DH", ),
                ),

                HTML.tr(
                    HTML.td('male', style="height:26px; font-weight: bold; background: #F2F2F2; padding: 5px"),
                    HTML.td(param_word['mW'], ),
                    HTML.td(param_word['mWF'], ),
                    HTML.td(param_word['mWM'], ),
                    HTML.td(param_word['mSW'], ),
                    HTML.td(param_word['mDH'], ),
                ),

                HTML.tr(
                    HTML.td('female', style="height:26px; font-weight: bold; background: #F2F2F2; padding: 5px"),
                    HTML.td(param_word['fH'], ),
                    HTML.td(param_word['fHF'], ),
                    HTML.td(param_word['fHM'], ),
                    HTML.td(param_word['fSW'], ),
                    HTML.td(param_word['fDH'], ),
                )
            ),
        }

    if param_word['mFeBS'] != param_word['mFyBS']:
        paradigm_tables['cousins'] = HTML.table(
                HTML.thead(
                    HTML.th("", style="height:26px; font-weight:"),
                    HTML.th("FBS",),
                    HTML.th("FBD",),
                    HTML.th("FZS",),
                    HTML.th("FZD",),
                    HTML.th("MBS",),
                    HTML.th("MBD",),
                    HTML.th("MZS",),
                    HTML.th("MZD",),
                    style="background: #F2F2F2",
                ),

                HTML.tr(
                    HTML.td("male speaker (parent is younger sibling)",
                            style="height:26px; font-weight: bold; background: #F2F2F2; padding: 5px"),
                    HTML.td(param_word['mFeBS'],),
                    HTML.td(param_word['mFeBD'],),
                    HTML.td(param_word['mFeZS'],),
                    HTML.td(param_word['mFeZD'],),
                    HTML.td(param_word['mMeBS'],),
                    HTML.td(param_word['mMeBD'],),
                    HTML.td(param_word['mMeZS'],),
                    HTML.td(param_word['mMeZD'],),
                ),

                HTML.tr(
                    HTML.td("male speaker (parent is older sibling)",
                            style="height:26px; font-weight: bold; background: #F2F2F2; padding: 5px"),
                    HTML.td(param_word['mFyBS'], ),
                    HTML.td(param_word['mFyBD'], ),
                    HTML.td(param_word['mFyZS'], ),
                    HTML.td(param_word['mFyZD'], ),
                    HTML.td(param_word['mMyBS'], ),
                    HTML.td(param_word['mMyBD'], ),
                    HTML.td(param_word['mMyZS'], ),
                    HTML.td(param_word['mMyZD'], ),
                ),

                HTML.tr(
                    HTML.td("female speaker (parent is younger sibling)",
                            style="height:26px; font-weight: bold; background: #F2F2F2; padding: 5px"),
                    HTML.td(param_word['fFeBS'],),
                    HTML.td(param_word['fFeBD'],),
                    HTML.td(param_word['fFeZS'],),
                    HTML.td(param_word['fFeZD'],),
                    HTML.td(param_word['fMeBS'],),
                    HTML.td(param_word['fMeBD'],),
                    HTML.td(param_word['fMeZS'],),
                    HTML.td(param_word['fMeZD'],),
                ),

                HTML.tr(
                    HTML.td("female speaker (parent is older sibling)",
                            style="height:26px; font-weight: bold; background: #F2F2F2; padding: 5px"),
                    HTML.td(param_word['fFyBS'], ),
                    HTML.td(param_word['fFyBD'], ),
                    HTML.td(param_word['fFyZS'], ),
                    HTML.td(param_word['fFyZD'], ),
                    HTML.td(param_word['fMyBS'], ),
                    HTML.td(param_word['fMyBD'], ),
                    HTML.td(param_word['fMyZS'], ),
                    HTML.td(param_word['fMyZD'], ),
                ),
            )

    if param_word['mFBeS'] and param_word['mFBeS'] != param_word['mFByS']:
        paradigm_tables['cousins'] = HTML.table(
            HTML.thead(
                HTML.th("", style="height:26px; font-weight:"),
                HTML.th("FBS", ),
                HTML.th("FBD", ),
                HTML.th("FZS", ),
                HTML.th("FZD", ),
                HTML.th("MBS", ),
                HTML.th("MBD", ),
                HTML.th("MZS", ),
                HTML.th("MZD", ),
                style="background: #F2F2F2",
            ),

            HTML.tr(
                HTML.td("male speaker (younger than cousin)",
                        style="height:26px; font-weight: bold; background: #F2F2F2; padding: 5px"),
                HTML.td(param_word['mFBeS'], ),
                HTML.td(param_word['mFBeD'], ),
                HTML.td(param_word['mFZeS'], ),
                HTML.td(param_word['mFZeD'], ),
                HTML.td(param_word['mMBeS'], ),
                HTML.td(param_word['mMBeD'], ),
                HTML.td(param_word['mMZeS'], ),
                HTML.td(param_word['mMZeD'], ),
            ),

            HTML.tr(
                HTML.td("male speaker (older than cousin)",
                        style="height:26px; font-weight: bold; background: #F2F2F2; padding: 5px"),
                HTML.td(param_word['mFByS'], ),
                HTML.td(param_word['mFByD'], ),
                HTML.td(param_word['mFZyS'], ),
                HTML.td(param_word['mFZyD'], ),
                HTML.td(param_word['mMByS'], ),
                HTML.td(param_word['mMByD'], ),
                HTML.td(param_word['mMZyS'], ),
                HTML.td(param_word['mMZyD'], ),
            ),

            HTML.tr(
                HTML.td("female speaker (younger than cousin)",
                        style="height:26px; font-weight: bold; background: #F2F2F2; padding: 5px"),
                HTML.td(param_word['fFBeS'], ),
                HTML.td(param_word['fFBeD'], ),
                HTML.td(param_word['fFZeS'], ),
                HTML.td(param_word['fFZeD'], ),
                HTML.td(param_word['fMBeS'], ),
                HTML.td(param_word['fMBeD'], ),
                HTML.td(param_word['fMZeS'], ),
                HTML.td(param_word['fMZeD'], ),
            ),

            HTML.tr(
                HTML.td("female speaker (older than cousin)",
                        style="height:26px; font-weight: bold; background: #F2F2F2; padding: 5px"),
                HTML.td(param_word['fFByS'], ),
                HTML.td(param_word['fFByD'], ),
                HTML.td(param_word['fFZyS'], ),
                HTML.td(param_word['fFZyD'], ),
                HTML.td(param_word['fMByS'], ),
                HTML.td(param_word['fMByD'], ),
                HTML.td(param_word['fMZyS'], ),
                HTML.td(param_word['fMZyD'], ),
            ),
        )
    return paradigm_tables
