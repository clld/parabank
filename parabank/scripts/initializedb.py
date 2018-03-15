# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import sys
import os
from collections import defaultdict, Counter
from itertools import chain, groupby

from sqlalchemy.orm import joinedload, joinedload_all
from clldutils.path import Path, as_unicode
from clldutils.dsv import reader
from clldutils.misc import slug
from clld.scripts.util import initializedb, Data, add_language_codes
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.color import qualitative_colors
from pyglottolog.api import Glottolog
from pyglottolog.languoids import Glottocode
from clld_glottologfamily_plugin.util import load_families
from clld_phylogeny_plugin.models import Phylogeny, TreeLabel, LanguageTreeLabel

from parabank import models
from parabank.scripts.global_tree import tree


DATA_DIR = Path(os.path.expanduser('~')).joinpath('venvs', 'parabank', 'parabank-pronoun-data')
PARADIGMS = {
    "singular": "1sg_a 1sg_s 3sg_m_a 3sg_m_s 3sg_f_a 3sg_f_s 1sg_o 1sg_p 3sg_m_o 3sg_m_p 3sg_f_o 3sg_f_p 2sg_a 2sg_s 2sg_o 2sg_p",
    "dual": "1du_a 2du_a 1du_s 1du_o 1du_p 3du_m_s 3du_m_o 3du_m_p 3du_m_a 2du_s 2du_o 2du_p 12du_a 12du_s 12du_o 12du_p",
    "plural": "1pl_a 1pl_s 12pl_o 12pl_p 1pl_o 3pl_m_a 3pl_m_o 3pl_m_p 3pl_m_s 2pl_p 2pl_a 2pl_s 2pl_o 1pl_p 12pl_a 12pl_s",
    "first person": "12pl_a 12pl_s 1du_o 1pl_o 1sg_o 1du_a 1du_s 1pl_a 1pl_s 12pl_o 1sg_a 1sg_s 12pl_p 12du_p 12du_a 12du_s 1du_p 1pl_p 12du_o 1sg_p",
    "second person": "2sg_a 2sg_o 2du_s 2sg_s 2pl_s 2pl_p 2pl_a 2pl_o 2du_p 2sg_p 2du_a 2du_o",
    "third person": "3pl_m_s 3du_m_a 3sg_m_s 3sg_f_s 3sg_m_p 3sg_f_p 3pl_m_o 3sg_m_a 3sg_f_a 3pl_m_p 3pl_m_a 3du_m_o 3du_m_s 3du_m_p 3sg_m_o 3sg_f_o",
    "actor": "1sg_a 3sg_m_a 1du_a 1pl_a 12du_a 12pl_a 3sg_f_a 3du_m_a 3pl_m_a 2sg_a 2du_a 2pl_a",
    "subject": "1sg_s 3du_m_s 3pl_m_s 1du_s 1pl_s 12du_s 12pl_s 2sg_s 2du_s 2pl_s 3sg_m_s 3sg_f_s",
    "object": "1sg_o 3sg_m_o 3sg_f_o 3du_m_o 3pl_m_o 1du_o 1pl_o 12du_o 12pl_o 2sg_o 2du_o 2pl_o",
    "possessive": "1sg_p 2pl_p 1du_p 1pl_p 12du_p 12pl_p 3du_m_p 3pl_m_p 3sg_m_p 3sg_f_p 2sg_p 2du_p",
}
PARADIGMS = {k: v.split() for k, v in PARADIGMS.items()}


def main(args):
    data = Data()
    data.add(
        common.Contributor, 'barthwolfgang',
        id='barthwolfgang',
        name="Wolfgang Barth",
        url="http://www.dynamicsoflanguage.edu.au/")

    dataset = common.Dataset(
        id='parabank',
        name='Parabank',
        description='Database of kinship terminology',
        domain='parabank.clld.org',
        publisher_name="CoEDL Centre of Excellence for the Dynamics of Language",
        publisher_place="Canberra, Australia",
        publisher_url="http://www.dynamicsoflanguage.edu.au/",
        license='http://creativecommons.org/licenses/by/4.0/',
        contact='wolfgang.barth@anu.edu.au',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0'})
    DBSession.add(dataset)

    for i, editor in enumerate(['barthwolfgang']):
        common.Editor(dataset=dataset, contributor=data['Contributor'][editor], ord=i + 1)

    contrib = common.Contribution(id='contrib', name='the contribution')

    for fname in DATA_DIR.glob('*.txt'):
        lid = as_unicode(fname.stem)
        comps = lid.split()
        gc = comps.pop()
        if Glottocode.pattern.match(gc) and gc not in ['glot0001', 'glot0002', 'pama1238', 'glot0048', 'glot0049']:
            lang = data.add(
                models.ParabankLanguage,
                lid,
                id=slug(lid),
                name=' '.join(comps))
            add_language_codes(data, lang, None, glottocode=gc)
        else:
            continue

        rows = sorted(
            reader(fname, delimiter=';', dicts=True, encoding='utf-8-sig'),
            key=lambda i: i['parameter'])
        form_counts = Counter([r['word'] for r in rows])

        for p, items in groupby(rows, lambda i: i['parameter']):
            item, word, wc = None, None, 0
            # choose the form with the highest frequency in the language's wordlist
            for item_ in items:
                if form_counts[item_['word']] > wc:
                    word, wc, item = item_['word'], form_counts[item_['word']], item_

            param = data['ParabankParameter'].get(p)
            if not param:
                param = data.add(
                    models.ParabankParameter,
                    p,
                    id=p,
                    name=p,
                    type='concept',
                    description=item['description'])

            id_ = p + "-" + lang.id
            vs = common.ValueSet(
                id=id_,
                language=lang,
                parameter=param,
                contribution=contrib)

            DBSession.add(models.Word(
                id=id_,
                name=word,
                ipa=item['ipa'],
                alternative=item.get('alternative'),
                comment=item.get('comment'),
                valueset=vs))

    load_families(
        data,
        [(l.glottocode, l) for l in data['ParabankLanguage'].values()],
        glottolog_repos=DATA_DIR.joinpath('..', '..', 'glottolog3', 'glottolog'),
        isolates_icon='tcccccc')

    langs_by_gc = defaultdict(list)
    for l in data['ParabankLanguage'].values():
        langs_by_gc[l.glottocode].append(l)

    newick, glottocodes = tree(
        list(langs_by_gc.keys()),
        DATA_DIR.joinpath('..', '..', 'glottolog3', 'glottolog'))
    phylo = Phylogeny(id='p', name='glottolog global tree', newick=newick)
    for gc in glottocodes:
        label = TreeLabel(id=gc, name=gc, phylogeny=phylo)
        for lang in langs_by_gc[gc]:
            LanguageTreeLabel(language=lang, treelabel=label)
    DBSession.add(phylo)


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """
    languages = DBSession.query(common.Language).options(
        joinedload_all(common.Language.valuesets, common.ValueSet.parameter),
        joinedload(common.Language.valuesets, common.ValueSet.values)
    ).all()
    contrib = DBSession.query(common.Contribution).first()

    for name, params in PARADIGMS.items():
        patterns = defaultdict(lambda: defaultdict(list))
        for lang in languages:
            for vs in sorted(lang.valuesets, key=lambda i: i.parameter_pk):
                if vs.parameter.id in params:
                    patterns[lang.pk][vs.values[0].name].append((vs.parameter_pk, vs.parameter.id))

        tmp = defaultdict(list)
        for l, pattern in patterns.items():
            ps = []
            for v in sorted(pattern.values(), key=lambda p: p[0][0]):
                ps.append(', '.join([vv[1] for vv in v]))
            tmp[' '.join(['({0})'.format(vv) for vv in ps])].append(l)

        patterns = {'other': []}
        for pattern, langs_ in tmp.items():
            if len(langs_) == 1:
                patterns['other'].append(langs_[0])
            else:
                patterns[pattern] = langs_[:]

        colors = qualitative_colors(len(patterns))
        param = models.ParabankParameter(id=slug(name), name=name, type='paradigm')
        for i, (pattern, langs_) in enumerate(patterns.items()):
            deid = '{0}-{1}'.format(param.id, i + 1)
            de = common.DomainElement(
                id=deid,
                name=deid,
                description=pattern,
                parameter=param,
                jsondata={'color': colors[i]})
            for lang_ in langs_:
                vsid = '{0}-{1}'.format(param.id, lang_)
                vs = common.ValueSet(id=vsid, language_pk=lang_, parameter=param, contribution=contrib)
                models.Word(id=vsid, valueset=vs, name=pattern, domainelement=de)
        DBSession.add(param)


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
