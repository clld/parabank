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
            thead("A", "S", "O", "P"),
            HTML.tbody(
                tr('1st (excl) Person Singular', '1sg_a', '1sg_s', '1sg_o', '1sg_p'),
                tr('1st (excl) Person Dual', '1du_a', '1du_s', '1du_o', '1du_p'),
                tr('1st (excl) Person Plural', '1pl_a', '1pl_s', '1pl_o', '1pl_p'),
                tr('1st (incl) Person Dual', '12du_a', '12du_s', '12du_o', '12du_p'),
                tr('1st (incl) Person Plural', '12pl_a', '12pl_s', '12pl_o', '12pl_p'),
                tr('2nd Person Singular', '2sg_a', '2sg_s', '2sg_o', '2sg_p'),
                tr('2nd Person Dual', '2du_a', '2du_s', '2du_o', '2du_p'),
                tr('2nd Person Plural', '2pl_a', '2pl_s', '2pl_o', '2pl_p'),
                tr('3rd Person Singular Gender 1', '3sg_m_a', '3sg_m_s', '3sg_m_o', '3sg_m_p'),
                tr('3rd Person Singular Gender 2', '3sg_f_a', '3sg_f_s', '3sg_f_o', '3sg_f_p'),
                tr('3rd Person Dual', '3du_m_a', '3du_m_s', '3du_m_o', '3du_m_p'),
                tr('3rd Person Plural', '3pl_m_a', '3pl_m_s', '3pl_m_o', '3pl_m_p'),
            )
        ),
        'verb_agreement': HTML.table(
            thead("Present", "Past"),
            HTML.tbody(
                tr('1st (excl) Person Singular', '1exSiActVA', '1exSiSubVA'),
                tr('1st (excl) Person Dual', '1exDuActVA', '1exDuSubVA'),
                tr('1st (excl) Person Plural', '1exPlActVA', '1exPlSubVA'),
                tr('1st (incl) Person Dual', '1inDuActVA', '1inDuSubVA'),
                tr('1st (incl) Person Plural', '1inPlActVA', '1inPlSubVA'),
                tr('2nd Person Singular', '2SiActVA', '2SiSubVA'),
                tr('2nd Person Dual', '2DuActVA', '2DuSubVA'),
                tr('2nd Person Plural', '2PlActVA', '2PlSubVA'),
                tr('3rd Person Singular Gender 1', '3SiG1ActVA', '3SiG1SubVA'),
                tr('3rd Person Singular Gender 2', '3SiG2ActVA', '3SiG2SubVA'),
                tr('3rd Person Dual', '3DuActVA', '3DuSubVA'),
                tr('3rd Person Plural', '3PlActVA', '3PlSubVA'),
            ),

        ),
        'verb_agreement2': HTML.table(
            thead("Present", "Past"),
            HTML.tbody(
                tr('1st (excl) Person Singular', '1exSiActVA2', '1exSiSubVA2'),
                tr('1st (excl) Person Dual', '1exDuActVA2', '1exDuSubVA2'),
                tr('1st (excl) Person Plural', '1exPlActVA2', '1exPlSubVA2'),
                tr('1st (incl) Person Dual', '1inDuActVA2', '1inDuSubVA2'),
                tr('1st (incl) Person Plural', '1inPlActVA2', '1inPlSubVA2'),
                tr('2nd Person Singular', '2SiActVA2', '2SiSubVA2'),
                tr('2nd Person Dual', '2DuActVA2', '2DuSubVA2'),
                tr('2nd Person Plural', '2PlActVA2', '2PlSubVA2'),
                tr('3rd Person Singular Gender 1', '3SiG1ActVA2', '3SiG1SubVA2'),
                tr('3rd Person Singular Gender 2', '3SiG2ActVA2', '3SiG2SubVA2'),
                tr('3rd Person Dual', '3DuActVA2', '3DuSubVA2'),
                tr('3rd Person Plural', '3PlActVA2', '3PlSubVA2'),
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
