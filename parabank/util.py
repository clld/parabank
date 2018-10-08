# coding: utf8
from __future__ import unicode_literals, print_function, division

from sqlalchemy.orm import joinedload_all

from clld.web.util.htmllib import HTML
from clld.db.meta import DBSession
from clld.db.models.common import Parameter, ValueSet, Value


def language_detail_html(context=None, request=None, **kw):
    # makes sure all display elements have a value
    param_word = {p.id: '#' for p in DBSession.query(Parameter)}

    # override the param_word dict with values from the DB
    for word in DBSession.query(Value)\
            .join(ValueSet)\
            .filter(ValueSet.language_pk == context.pk)\
            .options(joinedload_all(Value.valueset, ValueSet.parameter)):
        param_word[word.valueset.parameter.id] = word.name

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
                tr('3rd Person Singular Gender 1', '3sg_gen1_a', '3sg_gen1_s', '3sg_gen1_o', '3sg_gen1_p'),
                tr('3rd Person Singular Gender 2', '3sg_gen2_a', '3sg_gen2_s', '3sg_gen2_o', '3sg_gen2_p'),
                tr('3rd Person Dual', '3du_gen1_a', '3du_gen1_s', '3du_gen1_o', '3du_gen1_p'),
                tr('3rd Person Plural', '3pl_gen1_a', '3pl_gen1_s', '3pl_gen1_o', '3pl_gen1_p'),
            )
        ),
    }
    return paradigm_tables
