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
        return HTML.td(param_word[p] if p else '')

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
                tr('my father (F)', 'mS', 'mS', 'mS', 'mD', 'mD', 'mD', 'mW'),
                tr('eB', 'mF', '', 'myB', 'myB', 'myZ', 'myZ', '', 'mM'),
                tr('yB', 'mF', 'meB', '', 'meB', 'meZ', '', 'meZ', 'mM'),
                tr('me (male)', 'mF', 'meB', 'myB', '', '', 'myZ', 'meZ', 'mM'),
                tr('me (female)', 'mF', 'meB', 'myB', '', '', 'myZ', 'meZ', 'mM'),
                tr('yZ', 'fF', 'feB', '', 'fyB', 'fyZ', '', 'feZ', 'fM'),
                tr('eZ', 'fF', '', 'fyB', 'fyB', 'fyZ', 'fyZ', '', 'fM'),
                tr('my mother (M)', 'fH', 'fS', 'fS', 'fS', 'fD', 'fD', 'fD', ''),
            )
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
