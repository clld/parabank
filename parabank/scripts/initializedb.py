# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import os
import getpass

from clldutils.path import Path
from clldutils.dsv import reader
from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common

import parabank
from parabank import models

lang_dict = {} # Dictionary: {language: {parameter: word,},}

syncs_of_lang = {} # Dictionary: {language: [syncretism,]}
langs_of_sync = {} # Dictionary: {syncretism: [language,]}

langs_of_patt = {} # Dictionary: {pattern: [language,]}
patts_of_lang = {} # Dictionary: {language: [pattern,]}


if getpass.getuser().endswith('forkel'):
    DATA_DIR = Path(os.path.expanduser('~')).joinpath('venvs', 'parabank', 'data')
else:
    DATA_DIR = Path("C:/Users/Wolfgang/Documents/Australien/Parabank/Parabank Data")


def SyncretismPatternSetup(list_of_entries):
    # set up syncs_of_lang, patts_of_lang dictionaries
    # create lanug_dict for later lookup of syncretisms and patterns

    global lang_dict
    global syncs_of_lang
    global patts_of_lang

    for element_split in list_of_entries:
        if element_split[5] not in syncs_of_lang:
            syncs_of_lang[element_split[7]] = []
            patts_of_lang[element_split[7]] = []

        if element_split[7] in lang_dict:
            lang_dict[element_split[7]][element_split[2]] = element_split[0]
        else:
            lang_dict[element_split[7]] = {}
            lang_dict[element_split[7]][element_split[2]] = element_split[0]
    #print str(lang_dict)


def SyncretismFinder(syncretism_name, *args):
    # syncretism_name = name of the syncretism
    # *args = all parameters to look up for being identical
    global langs_of_sync
    global syncs_of_lang

    langs_of_sync[syncretism_name] = []
    parameter_group = list(args)
    for k, v in lang_dict.iteritems():

        switch = True
        if all(i in v for i in parameter_group):
            for parameter in parameter_group:
                if v[parameter] != v[parameter_group[0]]:
                    switch = False

            if switch:
                syncs_of_lang[k].append(syncretism_name)
                langs_of_sync[syncretism_name].append(k)


def PatternFinder(pattern_name, *args):
    # pattern_name = name of the pattern
    # *args = all parameters to look up in groups. The groups have to be different from each other [A, B],[C,D]
    global langs_of_patt
    global patts_of_lang
    langs_of_patt[pattern_name] = []
    syncretism_group = list(args)

    for k, v in lang_dict.iteritems():
        switch = True  # turns False if parameters inside one syncretism
        # are different or one syncretism is equal to another one

        param_set = set([])
        for syncretism in syncretism_group:
            for param in syncretism:
                if param not in param_set:
                    param_set.add(param)

                # if all(i in v for i in syncretism for syncretism in syncretism_group):
        if not all(params in v for params in param_set):
            switch = False
        else:

            # compare always the first parameter of a syncretism with the first of the other syncretisms
            # they have to be different in order to be a pattern
            for syncretism in syncretism_group[1:]:
                if v[syncretism[0]] == v[syncretism_group[0][0]]:
                    switch = False

                # compare all parameters within a syncretism
                # they have to be the same in order to be a syncretism
                for parameter in syncretism[1:]:
                    if v[parameter] != v[syncretism[0]]:
                        switch = False

        if switch:
            patts_of_lang[k].append(pattern_name)
            langs_of_patt[pattern_name].append(k)


def main(args):
    data = Data()

    # each CLLD APplication has one dataset
    dataset = common.Dataset(id=parabank.__name__, domain='parabank.clld.org')
    DBSession.add(dataset)

    for langu in reader(DATA_DIR.joinpath('data_basics', 'all_languages.txt'), delimiter=';', dicts=True):
        data.add(models.ParabankLanguage,
                 langu['glotto'],
                 id=langu['glotto'],
                 name=langu['language name'],
                 latitude=float(langu['latitude']),
                 longitude=float(langu['longitude']),
                 patterns=[],
                 comment=langu['comment'],)

    # each datatype is stored in a dictionary to filter out duplicates
    parameter_dict = {}
    valueset_dict = {}
    word_dict = {}
    rows = []

    for fname in DATA_DIR.joinpath('data_open_office').glob('*.txt'):
        for i, list_of_entries in enumerate(reader(fname, delimiter=';')):
            if i > 0:
                rows.append(list_of_entries)
                # make the variables more readable and compile some of them to unique keys
                word = list_of_entries[0]
                word_ipa = list_of_entries[1]
                word_key = list_of_entries[2] + "-" + list_of_entries[7]
                valueset_key = "vs-" + list_of_entries[2] + "-" + list_of_entries[7]
                parameter_abbr = list_of_entries[2]
                parameter_desc = list_of_entries[3]
                glotto = list_of_entries[7]

                # collect all parameters
                if parameter_abbr not in parameter_dict:
                    parameter_dict[parameter_abbr] = [parameter_abbr, parameter_desc]

                # collect all valuesets
                valueset_dict[valueset_key] = [valueset_key, parameter_abbr, glotto]

                # collect all words
                word_dict[word_key] = [word_key, word, word_ipa, valueset_key, ]

    for k, v in parameter_dict.items():  # Parameters get stored in data
        data.add(models.ParabankParameter,
                 k,
                 id=k,
                 name=k,
                 description=v[1])

    for k, v in valueset_dict.items():  # ValueSets get stored in data
        data.add(models.ParabankValueSet,
                 k,
                 id=k,
                 language=data['ParabankLanguage'][v[2]],
                 parameter=data['ParabankParameter'][v[1]])

    for k, v in word_dict.items():  # Words get stored in data
        DBSession.add(models.Word(id=k,
                                  name=v[1],
                                  word_name=v[1],
                                  word_ipa=v[2],
                                  valueset=data['ParabankValueSet'][v[3]]))

    # read the rawinput again to look for Syncretisms and Patterns
    SyncretismPatternSetup(rows)

    syncretism_list = [
        ["1", "grandparents", "all grandparents have the same address term"],
        ["2", "sisters", "all sisters have the same address term"],
        ["3", "brothers", "all brothers have the same address term"],
        ["4", "father-in-law", "all fathers-in-law have the same address term"]
        ]

    # all syncretisms you want to look up have to be added here with name and parameters
    SyncretismFinder("grandparents", "mFF", "mMF", "fFF", "fMF")
    SyncretismFinder("brothers", "meB", "myB", "fyB", "feB")
    SyncretismFinder("father-in-law", "fHF", "mWF")
    SyncretismFinder("sisters", "meZ", "myZ", "feZ", "fyZ")

    for sSyncretism in syncretism_list:  # syncretims added to data
        data.add(models.Syncretism,
                 sSyncretism[1],
                 id=sSyncretism[0],
                 name=sSyncretism[1],
                 description=sSyncretism[2],
                 languages=[],
                 )

    for s, l in langs_of_sync.iteritems():  # each language is added to data
        for lang in l:
            data['Syncretism'][s].languages.append(data['ParabankLanguage'][lang])

    pattern_list = [
        ["1", "gender division in siblings", "the siblings are in two groups depending on the gender"],
        ["2", "age division in siblings", "the siblings are in two groups depending on the relative age to the speaker"],
        ["3", "sons vs. daughters", "children are in two groups depending on their gender"]
    ]

    # all patterns you want to look up have to be added here with name and lists of parameters
    PatternFinder("gender division in siblings",
                  ["meZ", "myZ", "feZ", "fyZ"],
                  ["meB", "myB", "feB", "fyB"],
                  )

    PatternFinder("age division in siblings",
                  ["meZ", "feZ", "meB", "feB"],
                  ["myZ", "myB", "fyB", "fyZ"],
                  )

    PatternFinder("sons vs. daughters",
                  ["mS", "fS"],
                  ["mD", "fD"],
                  )

    for sPattern in pattern_list:  # Patterns are added to data
        data.add(models.Pattern,
                 sPattern[1],
                 id=sPattern[0],
                 name=sPattern[1],
                 description=sPattern[2],
                 languages=[],
                 )

    for p, l in langs_of_patt.iteritems():  # each language from dict is added to data
        for lang in l:
            data['Pattern'][p].languages.append(data['ParabankLanguage'][lang])

    paradigm_list = [["1", "all terms", "all kinship terms", ["meB", "myB"]],
                     ["2", "siblings", "all brothers and sisters", ["meB", "myB", "meZ", "myZ", "feB", "fyB", "feZ", "fyZ"]],
                     ]

    for sParadigm in paradigm_list:  # Patterns are added to data
        data.add(models.Paradigm,
                 sParadigm[1],
                 id=sParadigm[0],
                 name=sParadigm[1],
                 description=sParadigm[2],
                 parameters=[],
                 )

        for param in sParadigm[3]:
            data['Paradigm'][sParadigm[1]].parameters.append(data['ParabankParameter'][param])


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
