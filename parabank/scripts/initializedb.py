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
        #print(langu)
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
                    #print(lang_dict[item['glottocode']][item['parameter']], item['word'])
                    continue
                continue
            lang_dict[item['glottocode']][item['parameter']] = item['word']
            #print(fname)
            #print(fname, item['glottocode'], item['parameter'])
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
        ("patrichild", "male speaker's children and children of brothers", "mS mD meBS meBD myBS myBD "
                                                                               "feBS feBD fyBS fyBD"),
        ("matrichild", "female speaker's children and children of sisters", "fS fD feZS feZD fyZS fyZD "
                                                                                "meZS meZD myZS myZD"),
        ("grandfathers", "all grandparents have the same address term", "mFF mMF fFF fMF"),
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
            "sons vs. daughters",
            "Children are in two groups depending on their gender",
            "(mS, fS) (mD, fD)"],
        [
            "parents by gender and one term for all siblings of parents",
            "simple",
            "(mF, fF) "
            "(mM, fM) "
            "(mFeB, mFyB, mFeZ, mFyZ, mMeB, mMyB, mMeZ, mMyZ, mFeB, fFyB, fFeZ, fFyZ, fMeB, fMyB, fMeZ, fMyZ)"],
        [
            "Hawaiian Kinship System",
            "Differences are distinguished by generation and by gender",
            "(meB, myB, mFBS, mFZS, mMBS, mMZS, feZ, fyZ, fFBD, fFZD, fMBD, fMZD) "
            "(meZ, myZ, mFBD, mFZD, mMBD, mMZD) (feB, fyB, fFBS, fFZS, fMBS, fMZS) "
            "(mF, fF, mFeB, mFyB, mMeB, mMyB, fFeB, fFyB, fMeB, fMyB) "
            "(mM, fM, mFeZ, mFyZ, mMeZ, mMyZ, fFeZ, fFyZ, fMeZ, fMyZ)"],
        [
            "#3 siblings: gender division",
            "Siblings are in two groups depending on the gender",
            "(meZ, myZ, feZ, fyZ) (meB, myB, feB, fyB)"],
        [
            "#5 siblings: age division",
            "Siblings are in two groups depending on the relative age to the speaker",
            "(meB, meZ, feB, feZ) (myB, myZ, fyB, fyZ)"],
        [
            "#4 siblings: male speaker / female speaker",
            "Siblings are in two groups depending on the gender of speaker",
            "(meB, myB, meZ, myZ) (feB, fyB, feZ, fyZ)"],
        [
            "#2 siblings: gender division plus meB and fyZ",
            "Siblings are in two groups: male/female, where male elder brother and female younger sister have own term",
            "(meB) (myB, feB, fyB) (meZ, myZ, feZ) (fyZ)"],
        [
            "#1 siblings: elder brother / younger brother / elder sister / younger sister",
            "Siblings are in four groups distinguished by age and gender",
            "(meB, feB) (myB, fyB) (meZ, feZ) (myZ, fyZ)"],
        [
            "#6 siblings: four groups: gender of speaker, gender of sibling",
            "Siblings are in four groups distinguished by gender of speaker and gender of sibling",
            "(meB, myB) (feB, fyB) (meZ, myZ) (feZ, fyZ)"],
        [
            "#7 siblings: eight terms",
            "Each sibling is addressed differently",
            "(meB) (myB) (feB) (fyB) (meZ) (myZ) (feZ) (fyZ)"],
        [
            "#8 siblings: gender of sibling plus distinction of male/female speaker for brothers",
            "distinction by gender and brother distinction by gender of speaker",
            "(meB, myB) (feB, fyB) (meZ, myZ, feZ, fyZ)"],
        [
            "#9 siblings: gender of sibling plus distinction of male/female speaker for sisters",
            "distinction by gender and sister distinction by gender of speaker",
            "(meB, myB, feB, fyB) (meZ, myZ) (feZ, fyZ)"],
        [
            "#10 siblings: gender distinction plus same gender by age",
            "distinction by gender and same gender siblings are distinguished by age",
            "(meB) (myB, fyZ) (feB, fyB) (meZ, myZ) (feZ)"],
        [
            "#11 siblings: age distinction plus older siblings by gender",
            "distinction by gender and same gender siblings are distinguished by age",
            "(meB, feB) (myB, fyB, myZ, fyZ) (meZ, feZ)"],
        [
            "#12 siblings: gender division plus age division for brothers",
            "gender division plus age division for brothers",
            "(meB, feB) (myB, fyB) (myZ, fyZ, meZ, feZ)"],
        [
            "#13 siblings: age division plus sex of speaker division for older siblings",
            "gender division plus age division for brothers",
            "(meB, meB) (feB, feZ) (myB, myZ, fyB, fyZ)"],
        [
            "#14 siblings: cross gender distinction plus age distinction in same gender",
            "cross gender plus age in same gender",
            "(meB, feZ) (myB, fyZ) (feB, fyB, meZ, myZ)"],
        [
            "#15 siblings: one term for same gender sibling, cross gender divided in male and female",
            "one term for same gender sibling cross gender divided in male and female",
            "(meB, myB, feZ, fyZ) (feB, fyB) (meZ, myZ)"],
        [
            "#16 siblings: one term for cross gender sibling same gender divided in male and female",
            "one term for cross gender sibling same gender divided in male and female",
            "(meB, myB) (feZ, fyZ) (feB, fyB, meZ, myZ)"],
        [
            "#17 siblings", "complex", "(meB) (myB, fyB) (feZ) (fyZ) (feB) (meZ) (myZ)"],
        [
            "#18 siblings", "complex", "(meB) (myB, fyB, fyZ) (feZ) (feB) (meZ) (myZ)"],
        [
            "#19 siblings", "complex", "(meB) (myB, fyB, feB) (feZ, fyZ) (meZ, myZ)"],
        [
            "#20 siblings", "complex", "(meB, feB) (myB, fyB, myZ, fyZ) (meZ) (feZ)"],
        [
            "#21 siblings: age and gender distinction plus younger sister by sex of speaker",
            "age and gender distinction plus younger sister by sex of speaker",
            "(meB, feB) (myB, fyB) (meZ, feZ) (myZ) (fyZ)"],
        [
            "#22 siblings", "complex", "(meB, feB) (myB) (fyB) (meZ, feZ) (myZ) (fyZ)"],
        [
            "#23 siblings", "complex", "(meB) (feB) (myB) (fyB) (meZ) (feZ) (myZ, fyZ)"],
        [
            "#24 siblings: brothers and age distinction in sisters",
            "brothers and age distinction in sisters",
            "(meB, feB, myB, fyB) (meZ, feZ) (myZ, fyZ)"],
        [
            "#25 siblings: one term for all",
            "one term for all siblings",
            "(meB, feB, myB, fyB, meZ, feZ, myZ, fyZ)"],
        [
            "#26 siblings: cross vs. same sex sibling",
            "two terms: one for cross one for same sex sibling",
            "(meB, myB, feZ, fyZ) (meZ, myZ, feB, fyB)"],
        [
            "#27 siblings: age distinction plus gender in older siblings plus speaker distinction for older brother",
            "age and gender plus speaker distinction for older brother",
            "(meB) (myB, fyB, myZ, fyZ) (feB) (meZ, feZ)"],
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
            "parents, aunts & uncles",
            "all kinship terms for father, mother and their siblings",
            ["mF", "mM", "fF", "fM",
             "mFeB", "mFyB", "mFeZ", "mFyZ", "mMeB", "mMyB", "mMeZ", "mMyZ",
             "fFeB", "fFyB", "fFeZ", "fFyZ", "fMeB", "fMyB", "fMeZ", "fMyZ"]],
        [
            "siblings",
            "all brothers and sisters",
            ["meB", "myB", "meZ", "myZ", "feB", "fyB", "feZ", "fyZ"]],
        [
            "cousins - no age distinction",
            "all children of parent's siblings",
            ["mFBS", "mFBD", "mFZS", "mFZD", "mMBS", "mMBD", "mMZS", "mMZD",
             "fFBS", "fFBD", "fFZS", "fFZD", "fMBS", "fMBD", "fMZS", "fMZD"]],
        [
            "cousins - age distinction depends on relative age between ego and cousin",
            "all children of parent's siblings by relative age between ego and cousin",
            ["mFBeS", "mFBeD", "mFZeS", "mFZeD", "mMBeS", "mMBeD", "mMZeS", "mMZeD",
             "mFByS", "mFByD", "mFZyS", "mFZyD", "mMByS", "mMByD", "mMZyS", "mMZyD",
             "fFBeS", "fFBeD", "fFZeS", "fFZeD", "fMBeS", "fMBeD", "fMZeS", "fMZeD",
             "fFByS", "fFByD", "fFZyS", "fFZyD", "fMByS", "fMByD", "fMZyS", "fMZyD"]],
        [
            "cousins - age distinction depends on relative age between parent of ego and parent of cousin",
            "all children of parent's siblings by relative age of parents",
            ["mFeBS", "mFeBD", "mFeZS", "mFeZD", "mMeBS", "mMeBD", "mMeZS", "mMeZD",
             "mFyBS", "mFyBD", "mFyZS", "mFyZD", "mMyBS", "mMyBD", "mMyZS", "mMyZD",
             "fFeBS", "fFeBD", "fFeZS", "fFeZD", "fMeBS", "fMeBD", "fMeZS", "fMeZD",
             "fFyBS", "fFyBD", "fFyZS", "fFyZD", "fMyBS", "fMyBD", "fMyZS", "fMyZD"]],
        [
            "grandparents & grandchildren",
            "all direct ancestors of the grandparent generation & all direct "
            "descendants of the grandchildren generation",
            ["mFF", "mFM", "mMF", "mMM", "fFF", "fFM", "fMF", "fMM",
             "mSS", "mSD", "mDS", "mDD", "fSS", "fSD", "fDS", "fDD"]],
        [
            "sons & daughters, nieces & nephews",
            "all children of ego and ego's siblings",
            ["mS", "mD", "fS", "fD",
             "meBS", "meBD", "myBS", "myBD", "meZS", "meZD", "myZS", "myZD",
             "feBS", "feBD", "fyBS", "fyBD", "feZS", "feZD", "fyZS", "fyZD"]],
        [
            "In-laws & affines",
            "relatives through marriage",
            ["mW", "fH", "fHF", "fHM", "mWF", "mWM",
             "mSW", "mDH", "fSW", "fDH"]],
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
