# coding: utf8
from __future__ import unicode_literals, print_function, division

from sqlalchemy.orm import joinedload_all

from clld.web.util.htmllib import HTML
from clld.db.meta import DBSession
from clld.db.models.common import Parameter, ValueSet, Value


def language_detail_html(context=None, request=None, **kw):
    # makes sure all display elements have a value
    param_word = {p.name: '#' for p in DBSession.query(Parameter)}

    # override the param_word dict with values from the DB
    for word in DBSession.query(Value)\
            .join(ValueSet)\
            .filter(ValueSet.language_pk == context.pk)\
            .options(joinedload_all(Value.valueset, ValueSet.parameter)):
        param_word[word.valueset.parameter.name] = word.name

    def thead(*cols):
        return HTML.thead(
            HTML.tr(
                HTML.th("", style="height:26px; font-weight:"),
                *[HTML.th(col) for col in cols],
                **dict(style="background: #F2F2F2")
            )
        )

    def td(p):
        return HTML.td(param_word.get(p, '') if p else '')

    def tr(name, *params):
        return HTML.tr(
            HTML.td(
                name, 
                style="height:26px; font-weight: bold; background: #F2F2F2; padding: 5px"),
            *[td(p) for p in params])

    def table(*cols, **kw):
        male_cols = kw.get('male', ['m' + col for col in cols])
        female_cols = kw.get('female', ['f' + col for col in cols])
        return HTML.table(
            thead(*cols), HTML.tbody(tr('male', *male_cols), tr('female', *female_cols)))

    # create a paradigm_tables dict for the HTML rendering
    paradigm_tables = {
        'siblings': table('eB', 'yB', 'eZ', 'yZ'),
        'cousins': table("FBS", "FBD", "FZS", "FZD", "MBS", "MBD", "MZS", "MZD"),
        'parents': table("F", "FeB", "FyB", "FeZ", "FyZ", "M", "MyZ", "MeZ", "MyB", "MeB"),
        'grand': table('FF', 'FM', 'MF', 'MM', 'SS', 'SD', 'DS', 'DD'),
        'sons': table("eBS", "eBD", "yBS", "yBD", "S", "D", "eZS", "eZD", "yZS", "yZD"),
        'inlaws': table(
            "H / W", "HF / WF", "HM / WM", "SW", "DH",
            male=["mW", "mWF", "mWM", "mSW", "mDH"],
            female=["fH", "fHF", "fHM", "fSW", "fDH"]),
        'levenshtein_siblings': HTML.table(
            thead("F", "eB", "yB", "me (m)", "me (f)", "yZ", "eZ", "M"),
            HTML.tbody(
                tr('father (F)', '', 'mS', 'mS', 'mS', 'mD', 'mD', 'mD', 'mW'),
                tr('eB', 'mF', '', 'myB', 'myB', 'myZ', 'myZ', '', 'mM'),
                tr('yB', 'mF', 'meB', '', 'meB', 'meZ', '', 'meZ', 'mM'),
                tr('ego (male)', 'mF', 'meB', 'myB', '', '', 'myZ', 'meZ', 'mM'),
                tr('ego (female)', 'mF', 'meB', 'myB', '', '', 'myZ', 'meZ', 'mM'),
                tr('yZ', 'fF', 'feB', '', 'fyB', 'fyZ', '', 'feZ', 'fM'),
                tr('eZ', 'fF', '', 'fyB', 'fyB', 'fyZ', 'fyZ', '', 'fM'),
                tr('mother (M)', 'fH', 'fS', 'fS', 'fS', 'fD', 'fD', 'fD', ''),
            )
        ),
        'pronouns': HTML.table(
            thead("Actor", "Subject", "Object", "Possessive"),
            HTML.tbody(
                tr('1st (excl) Person Singular', '1exSiAct', '1exSiSub', '1exSiObj', '1exSiPoss'),
                tr('1st (excl) Person Dual', '1exDuAct', '1exDuSub', '1exDuObj', '1exDuPoss'),
                tr('1st (excl) Person Plural', '1exPlAct', '1exPlSub', '1exPlObj', '1exPlPoss'),
                tr('1st (incl) Person Dual', '1inDuAct', '1inDuSub', '1inDuObj', '1inDuPoss'),
                tr('1st (incl) Person Plural', '1inPlAct', '1inPlSub', '1inPlObj', '1inPlPoss'),
                tr('2nd Person Singular', '2SiAct', '2SiSub', '2SiObj', '2SiPoss'),
                tr('2nd Person Dual', '2DuAct', '2DuSub', '2DuObj', '2DuPoss'),
                tr('2nd Person Plural', '2PlAct', '2PlSub', '2PlObj', '2PlPoss'),
                tr('3rd Person Singular Gender 1', '3SiG1Act', '3SiG1Sub', '3SiG1Obj', '3SiG1Poss'),
                tr('3rd Person Singular Gender 2', '3SiG2Act', '3SiG2Sub', '3SiG2Obj', '3SiG2Poss'),
                tr('3rd Person Dual', '3DuAct', '3DuSub', '3DuObj', '3DuPoss'),
                tr('3rd Person Plural', '3PlAct', '3PlSub', '3PlObj', '3PlPoss'),
            )
        ),
        'verb_agreement': HTML.table(
            thead("Present", "Past", "Future", "#"),
            HTML.tbody(
                tr('1st (excl) Person Singular', '1exSiActVA', '1exSiSubVA', '1exSiObjVA', '1exSiPossVA'),
                tr('1st (excl) Person Dual', '1exDuActVA', '1exDuSubVA', '1exDuObjVA', '1exDuPossVA'),
                tr('1st (excl) Person Plural', '1exPlActVA', '1exPlSubVA', '1exPlObjVA', '1exPlPossVA'),
                tr('1st (incl) Person Dual', '1inDuActVA', '1inDuSubVA', '1inDuObjVA', '1inDuPossVA'),
                tr('1st (incl) Person Plural', '1inPlActVA', '1inPlSubVA', '1inPlObjVA', '1inPlPossVA'),
                tr('2nd Person Singular', '2SiActVA', '2SiSubVA', '2SiObjVA', '2SiPossVA'),
                tr('2nd Person Dual', '2DuActVA', '2DuSubVA', '2DuObjVA', '2DuPossVA'),
                tr('2nd Person Plural', '2PlActVA', '2PlSubVA', '2PlObjVA', '2PlPossVA'),
                tr('3rd Person Singular Gender 1', '3SiG1ActVA', '3SiG1SubVA', '3SiG1ObjVA', '3SiG1PossVA'),
                tr('3rd Person Singular Gender 2', '3SiG2ActVA', '3SiG2SubVA', '3SiG2ObjVA', '3SiG2PossVA'),
                tr('3rd Person Dual', '3DuActVA', '3DuSubVA', '3DuObjVA', '3DuPossVA'),
                tr('3rd Person Plural', '3PlActVA', '3PlSubVA', '3PlObjVA', '3PlPossVA'),
            ),

        ),
        'verb_agreement2': HTML.table(
            thead("Present", "Past", "Future", "#"),
            HTML.tbody(
                tr('1st (excl) Person Singular', '1exSiActVA2', '1exSiSubVA2', '1exSiObjVA2', '1exSiPossVA2'),
                tr('1st (excl) Person Dual', '1exDuActVA2', '1exDuSubVA2', '1exDuObjVA2', '1exDuPossVA2'),
                tr('1st (excl) Person Plural', '1exPlActVA2', '1exPlSubVA2', '1exPlObjVA2', '1exPlPossVA2'),
                tr('1st (incl) Person Dual', '1inDuActVA2', '1inDuSubVA2', '1inDuObjVA2', '1inDuPossVA2'),
                tr('1st (incl) Person Plural', '1inPlActVA2', '1inPlSubVA2', '1inPlObjVA2', '1inPlPossVA2'),
                tr('2nd Person Singular', '2SiActVA2', '2SiSubVA2', '2SiObjVA2', '2SiPossVA2'),
                tr('2nd Person Dual', '2DuActVA2', '2DuSubVA2', '2DuObjVA2', '2DuPossVA2'),
                tr('2nd Person Plural', '2PlActVA2', '2PlSubVA2', '2PlObjVA2', '2PlPossVA2'),
                tr('3rd Person Singular Gender 1', '3SiG1ActVA2', '3SiG1SubVA2', '3SiG1ObjVA2', '3SiG1PossVA2'),
                tr('3rd Person Singular Gender 2', '3SiG2ActVA2', '3SiG2SubVA2', '3SiG2ObjVA2', '3SiG2PossVA2'),
                tr('3rd Person Dual', '3DuActVA2', '3DuSubVA2', '3DuObjVA2', '3DuPossVA2'),
                tr('3rd Person Plural', '3PlActVA2', '3PlSubVA2', '3PlObjVA2', '3PlPossVA2'),
            ),

        ),
    }

    if param_word['mFeBS'] != "#":  # != param_word['mFyBS']:
        paradigm_tables['cousins'] = HTML.table(
            HTML.thead(
                HTML.tr(
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
                )
            ),
            HTML.tbody(
                tr("male speaker (parent is younger sibling)",
                   'mFeBS', 'mFeBD', 'mFeZS', 'mFeZD', 'mMeBS', 'mMeBD', 'mMeZS', 'mMeZD'),
                tr("male speaker (parent is older sibling)",
                   'mFyBS', 'mFyBD', 'mFyZS', 'mFyZD', 'mMyBS', 'mMyBD', 'mMyZS', 'mMyZD'),
                tr("female speaker (parent is younger sibling)",
                    'fFeBS', 'fFeBD', 'fFeZS', 'fFeZD', 'fMeBS', 'fMeBD', 'fMeZS', 'fMeZD'),
                tr("female speaker (parent is older sibling)",
                   'fFyBS', 'fFyBD', 'fFyZS', 'fFyZD', 'fMyBS', 'fMyBD', 'fMyZS', 'fMyZD'),
            )
        )

    if param_word['mFBeS'] != "#":  # and param_word['mFBeS'] != param_word['mFByS']:
        paradigm_tables['cousins'] = HTML.table(
            HTML.thead(
                HTML.tr(
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
                )
            ),
            HTML.tbody(
                tr("male speaker (younger than cousin)",
                   'mFBeS', 'mFBeD', 'mFZeS', 'mFZeD', 'mMBeS', 'mMBeD', 'mMZeS', 'mMZeD'),
                tr("male speaker (older than cousin)",
                   'mFByS', 'mFByD', 'mFZyS', 'mFZyD', 'mMByS', 'mMByD', 'mMZyS', 'mMZyD'),
                tr("female speaker (younger than cousin)",
                   'fFBeS', 'fFBeD', 'fFZeS', 'fFZeD', 'fMBeS', 'fMBeD', 'fMZeS', 'fMZeD'),
                tr("female speaker (older than cousin)",
                   'fFByS', 'fFByD', 'fFZyS', 'fFZyD', 'fMByS', 'fMByD', 'fMZyS', 'fMZyD'),
            ),
        )
    return paradigm_tables
