# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import sys

from clld.scripts.util import initializedb, Data, add_language_codes
from clld.db.meta import DBSession
from clld.db.models import common
from clld_glottologfamily_plugin.util import load_families
from pycldf import Wordlist

from parabank import models


def main(args):  # pragma: no cover
    wl = Wordlist.from_metadata(args.data_file('cldf', 'cldf-metadata.json'))

    data = Data()
    data.add(
        common.Contributor, 'barthwolfgang',
        id='barthwolfgang',
        name="Wolfgang Barth",
        url="http://www.dynamicsoflanguage.edu.au/")
    #
    # FIXME: get dataset attributes from CLDF metadata!
    #
    dataset = common.Dataset(
        id='parabank',
        name='Parabank Pronouns',
        description='Database of pronouns',
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

    for l in wl['LanguageTable']:
        lang = data.add(
            models.ParabankLanguage,
            l['ID'],
            id=l['ID'],
            name=l['Name'],
            description=l['Notes'],
            source=l['Source_Citation'],
            classification=l['Classification'],
        )
        add_language_codes(data, lang, None, glottocode=l['Glottocode'])

    for p in wl['ParameterTable']:
        data.add(
            common.Parameter,
            p['ID'],
            id=p['ID'],
            name='{0} ({1})'.format(p['Name'], p['ID']),
            #description=p['Description'],
        )

    for f in wl['FormTable']:
        vsid = '{0}-{1}'.format(f['Parameter_ID'], f['Language_ID'])
        vs = data['ValueSet'].get(vsid)
        if not vs:
            vs = data.add(
                common.ValueSet,
                vsid,
                id=vsid,
                language=data['ParabankLanguage'][f['Language_ID']],
                parameter=data['Parameter'][f['Parameter_ID']],
                contribution=contrib)

        DBSession.add(models.Word(
            id=f['ID'],
            name=f['Form'],
            comment=f.get('Comment'),
            valueset=vs))

    load_families(
        data,
        [(l.glottocode, l) for l in data['ParabankLanguage'].values()],
        glottolog_repos=args.data_file('glottolog'),
        isolates_icon='tcccccc')


def prime_cache(args):  # pragma: no cover
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """


if __name__ == '__main__':  # pragma: no cover
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
