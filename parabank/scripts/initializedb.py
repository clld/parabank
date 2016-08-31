# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import sys
import os
import getpass
from collections import defaultdict
import re
from itertools import chain

from clldutils.path import Path
from clldutils.dsv import reader
from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common

from parabank import models


if getpass.getuser().endswith('forkel'):
    DATA_DIR = Path(os.path.expanduser('~')).joinpath('venvs', 'parabank', 'data')
else:
    DATA_DIR = Path("C:/Users/Wolfgang/Documents/Australien/Parabank/Parabank Data")


def has_syncretism(words, *params):
    """
    Determine whether a dictionary of words shows a syncretism for a set of parameters.

    A syncretism is shown, when the dictionary contains words for all parameters and all
    of these words are the same.

    :param words: A dict of words keyed by parameter.
    :param params: A set of parameters.
    :return: True if the syncretism is found, otherwise False
    """
    return all(i in words for i in params) and len(set(words[p] for p in params)) == 1


def has_pattern(words, *syncretisms):
    """
    Determine whether a dictionary of words shows a pattern.

    :param words: A dict of words keyed by parameter.
    :param syncretisms: A set of distinct parameter groups.
    :return: True if the pattern is found, else False
    """
    if all(param in words for param in chain(*syncretisms)):
        # compare always the first parameter of a syncretism with the first of the other
        # syncretisms. they have to be different in order to be a pattern.
        if len(set(words[s[0]] for s in syncretisms)) == len(syncretisms):
            if all(has_syncretism(words, *s) for s in syncretisms):
                return True
    return False


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
            'license_icon': 'http://wals.info/static/images/cc_by.png',
            'license_name': 'Creative Commons Attribution 4.0'})
    DBSession.add(dataset)

    for i, editor in enumerate(['barthwolfgang']):
        common.Editor(dataset=dataset, contributor=data['Contributor'][editor], ord=i + 1)

    contrib = common.Contribution(id='contrib', name='the contribution')

    for langu in reader(DATA_DIR.joinpath('data_basics', 'all_languages.txt'), delimiter=';', dicts=True):
        data.add(common.Language,
                 langu['glotto'],
                 id=langu['glotto'],
                 name=langu['language name'],
                 latitude=float(langu['latitude']),
                 longitude=float(langu['longitude']),
                 description=langu['comment'],)

    lang_dict = defaultdict(dict)
    for fname in DATA_DIR.joinpath('data_open_office').glob('*.txt'):
        for item in reader(fname, delimiter=';', dicts=True, encoding='utf-8-sig'):
            if item['parameter'] in lang_dict[item['glottocode']]:
                if lang_dict[item['glottocode']][item['parameter']] != item['word']:
                    print(fname, item['glottocode'], item['parameter'])
                    print(lang_dict[item['glottocode']][item['parameter']], item['word'])
                    continue
                continue
            lang_dict[item['glottocode']][item['parameter']] = item['word']
            lang = data['Language'][item['glottocode']]
            param = data['Parameter'].get(item['parameter'])
            if not param:
                param = data.add(
                    common.Parameter,
                    item['parameter'],
                    id=item['parameter'],
                    name=item['parameter'],
                    description=item['description'])

            id_ = item['parameter'] + "-" + item['glottocode']
            vs = models.ParabankValueSet(
                id=id_,
                language=lang,
                parameter=param,
                contribution=contrib)

            DBSession.add(models.Word(
                id=id_,
                name=item['word'],
                ipa=item['ipa'],
                alternative=item.get('alternative'),
                comment=item.get('comment'),
                valueset=vs))

    for i, (name, desc, params) in enumerate([
        ("grandparents", "all grandparents have the same address term", "mFF mMF fFF fMF"),
        ("sisters", "all sisters have the same address term", "meZ myZ feZ fyZ"),
        ("brothers", "all brothers have the same address term", "meB myB feB fyB"),
        ("father-in-law", "all fathers-in-law have the same address term", "fHF mWF"),
    ]):
        params = params.split()
        syncretism = models.Syncretism(
            id='%s' % (i + 1,),
            name=name,
            description=desc,
            notation='(%s)' % ', '.join(params))

        for lang, words in lang_dict.items():
            if has_syncretism(words, *params):
                syncretism.languages.append(data['Language'][lang])

    for i, (name, desc, partition) in enumerate([
        [
            "gender division in siblings",
            "Siblings are in two groups depending on the gender",
            "(meZ, myZ, feZ, fyZ) (meB, myB, feB, fyB)"],
        [
            "age division in siblings",
            "Siblings are in two groups depending on the relative age to the speaker",
            "(meB, meZ, feB, feZ) (myB, myZ, fyB, fyZ)"],
        [
            "sons vs. daughters",
            "Children are in two groups depending on their gender",
            "(mS, fS) (mD, fD)"],
        [
            "siblings in four groups young/old - male/female",
            "Siblings are in four groups of older/younger, male/female distinction",
            "(meZ, feZ) (meB, feB) (myB, myB) (fyB fyB)"],
        [
            "Hawaiian Kinship System",
            "Differences are distinguished by generation and by gender",
            "(meB, myB, mFBS, mFZS, mMBS, mMZS, feZ, fyZ, fFBD, fFZD, fMBD, fMZD) "
            "(meZ, myZ, mFBD, mFZD, mMBD, mMZD) (feB, fyB, fFBS, fFZS, fMBS, fMZS) "
            "(mF, fF, mFeB, mFyB, mMeB, mMyB, fFeB, fFyB, fMeB, fMyB) "
            "(mM, fM, mFeZ, mFyZ, mMeZ, mMyZ, fFeZ, fFyZ, fMeZ, fMyZ)"]
    ]):
        pattern = models.Pattern(
            id='%s' % (i + 1,), name=name, description=desc, notation=partition)
        param_groups = [
            re.split(',\s*', group)
            for group in re.split('\s*\)\s*\(\s*', partition.strip()[1:-1])]
        for lang, words in lang_dict.items():
            if has_pattern(words, *param_groups):
                pattern.languages.append(data['Language'][lang])

    for i, (name, desc, params) in enumerate([
        [
            "all terms",
            "all kinship terms",
            ["meB", "myB"]],
        [
            "siblings",
            "all brothers and sisters",
            ["meB", "myB", "meZ", "myZ", "feB", "fyB", "feZ", "fyZ"]],
    ]):
        paradigm = models.Paradigm(id='%s' % (i + 1,), name=name, description=desc)
        for param in params:
            paradigm.parameters.append(data['Parameter'][param])


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
