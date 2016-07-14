# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import glob, os
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


def SyncretismPatternSetup(list_of_entries):
    # set up syncs_of_lang, patts_of_lang dictionaries
    # create lanug_dict for later lookup of syncretisms and patterns

    global lang_dict
    global syncs_of_lang
    global patts_of_lang

    for element in list_of_entries:

        element_split = element.split(";")
        if element_split[4] not in syncs_of_lang:
            syncs_of_lang[element_split[4]] = []
            patts_of_lang[element_split[4]] = []

        if element_split[4] in lang_dict:
            lang_dict[element_split[4]][element_split[2]] = element_split[0]
        else:
            lang_dict[element_split[4]] = {}
            lang_dict[element_split[4]][element_split[2]] = element_split[0]
    print str(lang_dict)

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

    dataset = common.Dataset(id=parabank.__name__, domain='parabank.clld.org')
    DBSession.add(dataset)

    """
    # for data inport from local computer
    rawformat = []

    os.chdir("C:/Users/Wolfgang/Documents/Australien/Parabank/Parabank Data/data_open_office")
    for file in glob.glob("*.txt"):
        f = open(file, 'r')
        for line in f:
            rawformat.append(str(line).decode('utf-8'))

    """
    # test data German, English, Matukar
    rawformat = [
        "bruder;bʀuːdɐ;feB;female speaker's older brother;stan1295;Standard German;48.65;12.47",
        "bruder;bʀuːdɐ;fyB;female speaker's younger brother;stan1295;Standard German;48.65;12.47",
        "bruder;bʀuːdɐ;meB;male speaker's older brother;stan1295;Standard German;48.65;12.47",
        "bruder;bʀuːdɐ;myB;male speaker's younger brother;stan1295;Standard German;48.65;12.47",
        "cousin;kuˈzɛ̃ː;fFBS;female speaker's father's brother's son ;stan1295;Standard German;48.65;12.47",
        "cousin;kuˈzɛ̃ː;fFZS;female speaker's father's sister's son ;stan1295;Standard German;48.65;12.47",
        "cousin;kuˈzɛ̃ː;fMBS;female speaker's mother's brother's son ;stan1295;Standard German;48.65;12.47",
        "cousin;kuˈzɛ̃ː;fMZS;female speaker's mother's sister's son ;stan1295;Standard German;48.65;12.47",
        "cousin;kuˈzɛ̃ː;mFBS;male speaker's father's brother's son ;stan1295;Standard German;48.65;12.47",
        "cousin;kuˈzɛ̃ː;mFZS;male speaker's father's sister's son ;stan1295;Standard German;48.65;12.47",
        "cousin;kuˈzɛ̃ː;mMBS;male speaker's mother's brother's son ;stan1295;Standard German;48.65;12.47",
        "cousine;kuˈziːnə;fFBD;female speaker's father's brother's daughter ;stan1295;Standard German;48.65;12.47",
        "cousine;kuˈziːnə;fFZD;female speaker's father's sister's daughter ;stan1295;Standard German;48.65;12.47",
        "cousine;kuˈziːnə;fMBD;female speaker's mother's brother's daughter ;stan1295;Standard German;48.65;12.47",
        "cousine;kuˈziːnə;fMZD;female speaker's mother's sister's daughter ;stan1295;Standard German;48.65;12.47",
        "cousine;kuˈziːnə;mFBD;male speaker's father's brother's daughter ;stan1295;Standard German;48.65;12.47",
        "cousine;kuˈziːnə;mFZD;male speaker's father's sister's daughter ;stan1295;Standard German;48.65;12.47",
        "cousine;kuˈziːnə;mMBD;male speaker's mother's brother's daughter ;stan1295;Standard German;48.65;12.47",
        "ehefrau;ˈeːəˌfʀaʊ̯;mW;speaker's wife;stan1295;Standard German;48.65;12.47",
        "ehemann;ˈeːəˌman;fH;speaker's husband;stan1295;Standard German;48.65;12.47",
        "enkel;ˈɛŋkl̩;fDS;female speaker's daughter's son ;stan1295;Standard German;48.65;12.47",
        "enkel;ˈɛŋkl̩;fSS;female speaker's son's son ;stan1295;Standard German;48.65;12.47",
        "enkel;ˈɛŋkl̩;mDS;male speaker's daughter's son;stan1295;Standard German;48.65;12.47",
        "enkel;ˈɛŋkl̩;mSS;male speaker's son's son;stan1295;Standard German;48.65;12.47",
        "enkelin;ˈɛŋkəlɪn;fDD;female speaker's daugher's daughter ;stan1295;Standard German;48.65;12.47",
        "enkelin;ˈɛŋkəlɪn;fSD;female speaker's son's daughter ;stan1295;Standard German;48.65;12.47",
        "enkelin;ˈɛŋkəlɪn;mDD;male speaker's daughter's daughter;stan1295;Standard German;48.65;12.47",
        "enkelin;ˈɛŋkəlɪn;mSD;male speaker's son's daughter;stan1295;Standard German;48.65;12.47",
        "großmutter;ˈɡʀoːsˌmʊtɐ;fFM;female speaker's father's mother ;stan1295;Standard German;48.65;12.47",
        "großmutter;ˈɡʀoːsˌmʊtɐ;fMM;female speaker's mother's mother ;stan1295;Standard German;48.65;12.47",
        "großmutter;ˈɡʀoːsˌmʊtɐ;mFM;male speaker's father's mother;stan1295;Standard German;48.65;12.47",
        "großvater;ˈɡʀoːsˌfaːtɐ;mMF;male speaker's mother's father;stan1295;Standard German;48.65;12.47",
        "großvater;ˈɡʀoːsˌfaːtɐ;fFF;female speaker's father's father ;stan1295;Standard German;48.65;12.47",
        "großvater;ˈɡʀoːsˌfaːtɐ;fMF;female speaker's mother's father ;stan1295;Standard German;48.65;12.47",
        "großvater;ˈɡʀoːsˌfaːtɐ;mFF;male speaker's fathers father;stan1295;Standard German;48.65;12.47",
        "großmutter;ˈɡʀoːsˌmʊtɐ;mMM;male speaker's mother's mother;stan1295;Standard German;48.65;12.47",
        "mutter;ˈmʊtɐ;fM;female speaker's mother;stan1295;Standard German;48.65;12.47",
        "mutter;ˈmʊtɐ;mM;male speaker's mother;stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;feBS;female speaker's older brother's son ;stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;feZS;female speaker's older sister's son ;stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;fyBS;female spekaer's younger brother's son ;stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;fyZS;female speaker's younger sister's son ;stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;meBS;male speaker's older brother's son ;stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;meZS;male speaker's older sister's son ;stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;mMZS;male speaker's mother's sister's son ;stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;myBS;male speaker's younger brother's son ;stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;myZS;male speaker's younger sister's son ;stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;feBD;female speaker's older brother's daughter ;stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;feZD;female speaker's older sister's daughter ;stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;fyBD;female speaker's younger brother's daughter ;stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;fyZD;female speaker's younger sister's daughter ;stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;meBD;male speaker's older brother's daughter ;stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;meZD;male speaker's older sister's daughter ;stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;mMZD;male speaker's mother's sister's daughter ;stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;myBD;male speaker's younger brother's daughter ;stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;myZD;male speaker's younger sister's daughter ;stan1295;Standard German;48.65;12.47",
        "onkel;ˈɔŋkl̩;fFeB;female speaker's father's older brother ;stan1295;Standard German;48.65;12.47",
        "onkel;ˈɔŋkl̩;fFyB;female speaker's father's younger brother ;stan1295;Standard German;48.65;12.47",
        "onkel;ˈɔŋkl̩;fMeB;female speaker's mother's older brother ;stan1295;Standard German;48.65;12.47",
        "onkel;ˈɔŋkl̩;fMyB;female speaker's mother's younger brother ;stan1295;Standard German;48.65;12.47",
        "onkel;ˈɔŋkl̩;mFeB;male speaker's father's older brother ;stan1295;Standard German;48.65;12.47",
        "onkel;ˈɔŋkl̩;mFyB;male speaker's father's younger brother ;stan1295;Standard German;48.65;12.47",
        "onkel;ˈɔŋkl̩;mMeB;male speaker's mother's older brother ;stan1295;Standard German;48.65;12.47",
        "onkel;ˈɔŋkl̩;mMyB;male speaker's mother's younger brother ;stan1295;Standard German;48.65;12.47",
        "schwester;ˈʃvɛstɐ;feZ;female speaker's older sister;stan1295;Standard German;48.65;12.47",
        "schwester;ˈʃvɛstɐ;fyZ;female speaker's younger sister;stan1295;Standard German;48.65;12.47",
        "schwester;ˈʃvɛstɐ;meZ;male speaker's older sister;stan1295;Standard German;48.65;12.47",
        "schwester;ˈʃvɛstɐ;myZ;male speaker's younger sister;stan1295;Standard German;48.65;12.47",
        "schwiegermutter;ˈʃviːɡɐˌmʊtɐ;fHM;speaker's husband's mother;stan1295;Standard German;48.65;12.47",
        "schwiegermutter;ˈʃviːɡɐˌmʊtɐ;mWM;speaker's wife's mother;stan1295;Standard German;48.65;12.47",
        "schwiegersohn;ˈʃviːɡɐˌzoːn;fDH;female speaker's daughter's husband;stan1295;Standard German;48.65;12.47",
        "schwiegersohn;ˈʃviːɡɐˌzoːn;mDH;male speaker's daughter's husband;stan1295;Standard German;48.65;12.47",
        "schwiegertochter;ˈʃviːɡɐˌtɔχtɐ;fSW;female speaker's son's wife;stan1295;Standard German;48.65;12.47",
        "schwiegertochter;ˈʃviːɡɐˌtɔχtɐ;mSW;male speaker's son's wife;stan1295;Standard German;48.65;12.47",
        "schwiegervater;ˈʃviːɡɐˌfaːtɐ;fHF;speaker's husband's father;stan1295;Standard German;48.65;12.47",
        "schwiegervater;ˈʃviːɡɐˌfaːtɐ;mWF;speaker's wife's father;stan1295;Standard German;48.65;12.47",
        "sohn;zoːn;fS;female speaker's son;stan1295;Standard German;48.65;12.47",
        "sohn;zoːn;mS;male speaker's son;stan1295;Standard German;48.65;12.47",
        "tante;ˈtantə;fFeZ;female speaker's father's older sister ;stan1295;Standard German;48.65;12.47",
        "tante;ˈtantə;fFyZ;female speaker's father's younger sister ;stan1295;Standard German;48.65;12.47",
        "tante;ˈtantə;fMeZ;female speaker's mother's older sister ;stan1295;Standard German;48.65;12.47",
        "tante;ˈtantə;fMyZ;female speaker's mother's younger sister ;stan1295;Standard German;48.65;12.47",
        "tante;ˈtantə;mFeZ;male speaker's father's older sister ;stan1295;Standard German;48.65;12.47",
        "tante;ˈtantə;mFyZ;male speaker's father's younger sister ;stan1295;Standard German;48.65;12.47",
        "tante;ˈtantə;mMeZ;male speaker's mother's older sister ;stan1295;Standard German;48.65;12.47",
        "tante;ˈtantə;mMyZ;male speaker's mother's younger sister ;stan1295;Standard German;48.65;12.47",
        "tochter;ˈtɔχtɐ;fD;female speaker's daughter;stan1295;Standard German;48.65;12.47",
        "tochter;ˈtɔχtɐ;mD;male speaker's daughter;stan1295;Standard German;48.65;12.47",
        "vater;ˈfaːtɐ;fF;female speaker's father;stan1295;Standard German;48.65;12.47",
        "vater;ˈfaːtɐ;mF;male speaker's father;stan1295;Standard German;48.65;12.47",
        "brother;ˈbɹʌðə(ɹ);feB;female speaker's older brother;stan1293;Standard English;52.00;0.00",
        "brother;ˈbɹʌðə(ɹ);fyB;female speaker's younger brother;stan1293;Standard English;52.00;0.00",
        "brother;ˈbɹʌðə(ɹ);meB;male speaker's older brother;stan1293;Standard English;52.00;0.00",
        "brother;ˈbɹʌðə(ɹ);myB;male speaker's younger brother;stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;fFBS;female speaker's father's brother's son ;stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;fFZS;female speaker's father's sister's son ;stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;fMBS;female speaker's mother's brother's son ;stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;fMZS;female speaker's mother's sister's son ;stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;mFBS;male speaker's father's brother's son ;stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;mFZS;male speaker's father's sister's son ;stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;mMBS;male speaker's mother's brother's son ;stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;fFBD;female speaker's father's brother's daughter ;stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;fFZD;female speaker's father's sister's daughter ;stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;fMBD;female speaker's mother's brother's daughter ;stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;fMZD;female speaker's mother's sister's daughter ;stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;mFBD;male speaker's father's brother's daughter ;stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;mFZD;male speaker's father's sister's daughter ;stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;mMBD;male speaker's mother's brother's daughter ;stan1293;Standard English;52.00;0.00",
        "wife;waɪf;mW;speaker's wife;stan1293;Standard English;52.00;0.00",
        "husband;ˈhʌzbənd;fH;speaker's husband;stan1293;Standard English;52.00;0.00",
        "grandson;ˈɡɹæn(d)sʌn;fDS;female speaker's daughter's son ;stan1293;Standard English;52.00;0.00",
        "grandson;ˈɡɹæn(d)sʌn;fSS;female speaker's son's son ;stan1293;Standard English;52.00;0.00",
        "grandson;ˈɡɹæn(d)sʌn;mDS;male speaker's daughter's son;stan1293;Standard English;52.00;0.00",
        "grandson;ˈɡɹæn(d)sʌn;mSS;male speaker's son's son;stan1293;Standard English;52.00;0.00",
        "granddaughter;ˈɡɹæn(d)dɔːtə®;fDD;female speaker's daugher's daughter ;stan1293;Standard English;52.00;0.00",
        "granddaughter;ˈɡɹæn(d)dɔːtə®;fSD;female speaker's son's daughter ;stan1293;Standard English;52.00;0.00",
        "granddaughter;ˈɡɹæn(d)dɔːtə®;mDD;male speaker's daughter's daughter;stan1293;Standard English;52.00;0.00",
        "granddaughter;ˈɡɹæn(d)dɔːtə®;mSD;male speaker's son's daughter;stan1293;Standard English;52.00;0.00",
        "grandmother;ˈɡɹæn(d)mʌðə(ɹ);fFM;female speaker's father's mother ;stan1293;Standard English;52.00;0.00",
        "grandmother;ˈɡɹæn(d)mʌðə(ɹ);fMM;female speaker's mother's mother ;stan1293;Standard English;52.00;0.00",
        "grandmother;ˈɡɹæn(d)mʌðə(ɹ);mFM;male speaker's father's mother;stan1293;Standard English;52.00;0.00",
        "grandfather;ˈɡɹæn(d)fɑː.ðə(ɹ);mMF;male speaker's mother's father;stan1293;Standard English;52.00;0.00",
        "grandfather;ˈɡɹæn(d)fɑː.ðə(ɹ);fFF;female speaker's father's father ;stan1293;Standard English;52.00;0.00",
        "grandfather;ˈɡɹæn(d)fɑː.ðə(ɹ);fMF;female speaker's mother's father ;stan1293;Standard English;52.00;0.00",
        "grandfather;ˈɡɹæn(d)fɑː.ðə(ɹ);mFF;male speaker's fathers father;stan1293;Standard English;52.00;0.00",
        "grandmother;ˈɡɹæn(d)mʌðə(ɹ);mMM;male speaker's mother's mother;stan1293;Standard English;52.00;0.00",
        "mother;ˈmʌðə(ɹ);fM;female speaker's mother;stan1293;Standard English;52.00;0.00",
        "mother;ˈmʌðə(ɹ);mM;male speaker's mother;stan1293;Standard English;52.00;0.00",
        "nephew;ˈnɛv.ju;feBS;female speaker's older brother's son ;stan1293;Standard English;52.00;0.00",
        "nephew;ˈnɛv.ju;feZS;female speaker's older sister's son ;stan1293;Standard English;52.00;0.00",
        "nephew;ˈnɛv.ju;fyBS;female spekaer's younger brother's son ;stan1293;Standard English;52.00;0.00",
        "nephew;ˈnɛv.ju;fyZS;female speaker's younger sister's son ;stan1293;Standard English;52.00;0.00",
        "nephew;ˈnɛv.ju;meBS;male speaker's older brother's son ;stan1293;Standard English;52.00;0.00",
        "nephew;ˈnɛv.ju;meZS;male speaker's older sister's son ;stan1293;Standard English;52.00;0.00",
        "nephew;ˈnɛv.ju;mMZS;male speaker's mother's sister's son ;stan1293;Standard English;52.00;0.00",
        "nephew;ˈnɛv.ju;myBS;male speaker's younger brother's son ;stan1293;Standard English;52.00;0.00",
        "niece;niːs;myZS;male speaker's younger sister's son ;stan1293;Standard English;52.00;0.00",
        "niece;niːs;feBD;female speaker's older brother's daughter ;stan1293;Standard English;52.00;0.00",
        "niece;niːs;feZD;female speaker's older sister's daughter ;stan1293;Standard English;52.00;0.00",
        "niece;niːs;fyBD;female speaker's younger brother's daughter ;stan1293;Standard English;52.00;0.00",
        "niece;niːs;fyZD;female speaker's younger sister's daughter ;stan1293;Standard English;52.00;0.00",
        "niece;niːs;meBD;male speaker's older brother's daughter ;stan1293;Standard English;52.00;0.00",
        "niece;niːs;meZD;male speaker's older sister's daughter ;stan1293;Standard English;52.00;0.00",
        "niece;niːs;mMZD;male speaker's mother's sister's daughter ;stan1293;Standard English;52.00;0.00",
        "niece;niːs;myBD;male speaker's younger brother's daughter ;stan1293;Standard English;52.00;0.00",
        "niece;niːs;myZD;male speaker's younger sister's daughter ;stan1293;Standard English;52.00;0.00",
        "uncle;ŭngʹkəl;fFeB;female speaker's father's older brother ;stan1293;Standard English;52.00;0.00",
        "uncle;ŭngʹkəl;fFyB;female speaker's father's younger brother ;stan1293;Standard English;52.00;0.00",
        "uncle;ŭngʹkəl;fMeB;female speaker's mother's older brother ;stan1293;Standard English;52.00;0.00",
        "uncle;ŭngʹkəl;fMyB;female speaker's mother's younger brother ;stan1293;Standard English;52.00;0.00",
        "uncle;ŭngʹkəl;mFeB;male speaker's father's older brother ;stan1293;Standard English;52.00;0.00",
        "uncle;ŭngʹkəl;mFyB;male speaker's father's younger brother ;stan1293;Standard English;52.00;0.00",
        "uncle;ŭngʹkəl;mMeB;male speaker's mother's older brother ;stan1293;Standard English;52.00;0.00",
        "uncle;ŭngʹkəl;mMyB;male speaker's mother's younger brother ;stan1293;Standard English;52.00;0.00",
        "sister;sĭs'tər;feZ;female speaker's older sister;stan1293;Standard English;52.00;0.00",
        "sister;sĭs'tər;fyZ;female speaker's younger sister;stan1293;Standard English;52.00;0.00",
        "sister;sĭs'tər;meZ;male speaker's older sister;stan1293;Standard English;52.00;0.00",
        "sister;sĭs'tər;myZ;male speaker's younger sister;stan1293;Standard English;52.00;0.00",
        "mother-in-law;ˈmʌðə(ɹ) ɪn ˌlɔ;fHM;speaker's husband's mother;stan1293;Standard English;52.00;0.00",
        "mother-in-law;ˈmʌðə(ɹ) ɪn ˌlɔ;mWM;speaker's wife's mother;stan1293;Standard English;52.00;0.00",
        "son-in-law;sʌn ɪn ˌlɔ;fDH;female speaker's daughter's husband;stan1293;Standard English;52.00;0.00",
        "son-in-law;sʌn ɪn ˌlɔ;mDH;male speaker's daughter's husband;stan1293;Standard English;52.00;0.00",
        "daughter-in-law;ˈdɔːtə(r) ɪn ˌlɔ;fSW;female speaker's son's wife;stan1293;Standard English;52.00;0.00",
        "daughter-in-law;ˈdɔːtə(r) ɪn ˌlɔ;mSW;male speaker's son's wife;stan1293;Standard English;52.00;0.00",
        "father-in-law;ˈfɑː.ðə(ɹ) ɪn ˌlɔ;fHF;speaker's husband's father;stan1293;Standard English;52.00;0.00",
        "father-in-law;ˈfɑː.ðə(ɹ) ɪn ˌlɔ;mWF;speaker's wife's father;stan1293;Standard English;52.00;0.00",
        "son;sʌn;fS;female speaker's son;stan1293;Standard English;52.00;0.00",
        "son;sʌn;mS;male speaker's son;stan1293;Standard English;52.00;0.00",
        "aunt;ɑːnt;fFeZ;female speaker's father's older sister ;stan1293;Standard English;52.00;0.00",
        "aunt;ɑːnt;fFyZ;female speaker's father's younger sister ;stan1293;Standard English;52.00;0.00",
        "aunt;ɑːnt;fMeZ;female speaker's mother's older sister ;stan1293;Standard English;52.00;0.00",
        "aunt;ɑːnt;fMyZ;female speaker's mother's younger sister ;stan1293;Standard English;52.00;0.00",
        "aunt;ɑːnt;mFeZ;male speaker's father's older sister ;stan1293;Standard English;52.00;0.00",
        "aunt;ɑːnt;mFyZ;male speaker's father's younger sister ;stan1293;Standard English;52.00;0.00",
        "aunt;ɑːnt;mMeZ;male speaker's mother's older sister ;stan1293;Standard English;52.00;0.00",
        "aunt;ɑːnt;mMyZ;male speaker's mother's younger sister ;stan1293;Standard English;52.00;0.00",
        "daughter;ˈdɔːtə(r);fD;female speaker's daughter;stan1293;Standard English;52.00;0.00",
        "daughter;ˈdɔːtə(r);mD;male speaker's daughter;stan1293;Standard English;52.00;0.00",
        "father;ˈfɑː.ðə(ɹ);fF;female speaker's father;stan1293;Standard English;52.00;0.00",
        "father;ˈfɑː.ðə(ɹ);mF;male speaker's father;stan1293;Standard English;52.00;0.00",
        "lu dabok;;feB;female speaker's older brother;matu1261;Matukar;-4.91;145.78",
        "lu natun;;fyB;female speaker's younger brother;matu1261;Matukar;-4.91;145.78",
        "ka dabok;;meB;male speaker's older brother;matu1261;Matukar;-4.91;145.78",
        "te natun;;myB;male speaker's younger brother;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;fFBS;female speaker's father's brother's son ;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;fFZS;female speaker's father's sister's son ;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;fMBS;female speaker's mother's brother's son ;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;fMZS;female speaker's mother's sister's son ;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;mFBS;male speaker's father's brother's son ;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;mFZS;male speaker's father's sister's son ;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;mMBS;male speaker's mother's brother's son ;matu1261;Matukar;-4.91;145.78",
        "kol pain;;fFBD;female speaker's father's brother's daughter ;matu1261;Matukar;-4.91;145.78",
        "kol pain;;fFZD;female speaker's father's sister's daughter ;matu1261;Matukar;-4.91;145.78",
        "kol pain;;fMBD;female speaker's mother's brother's daughter ;matu1261;Matukar;-4.91;145.78",
        "kol pain;;fMZD;female speaker's mother's sister's daughter ;matu1261;Matukar;-4.91;145.78",
        "kol pain;;mFBD;male speaker's father's brother's daughter ;matu1261;Matukar;-4.91;145.78",
        "kol pain;;mFZD;male speaker's father's sister's daughter ;matu1261;Matukar;-4.91;145.78",
        "kol pain;;mMBD;male speaker's mother's brother's daughter ;matu1261;Matukar;-4.91;145.78",
        "yawau;;mW;speaker's wife;matu1261;Matukar;-4.91;145.78",
        "yawau;;fH;speaker‘s husband;matu1261;Matukar;-4.91;145.78",
        "sise;;fDS;female speaker's daughter's son ;matu1261;Matukar;-4.91;145.78",
        "sise;;fSS;female speaker's son's son ;matu1261;Matukar;-4.91;145.78",
        "sise;;mDS;male speaker's daughter's son;matu1261;Matukar;-4.91;145.78",
        "sise;;mSS;male speaker's son's son;matu1261;Matukar;-4.91;145.78",
        "sise;;fDD;female speaker's daugher's daughter ;matu1261;Matukar;-4.91;145.78",
        "sise;;fSD;female speaker's son's daughter ;matu1261;Matukar;-4.91;145.78",
        "sise;;mDD;male speaker's daughter's daughter;matu1261;Matukar;-4.91;145.78",
        "sise;;mSD;male speaker's son's daughter;matu1261;Matukar;-4.91;145.78",
        "sise;;fFM;female speaker's father's mother ;matu1261;Matukar;-4.91;145.78",
        "sise;;fMM;female speaker's mother's mother ;matu1261;Matukar;-4.91;145.78",
        "sise;;mFM;male speaker's father's mother;matu1261;Matukar;-4.91;145.78",
        "sise;;mMF;male speaker's mother's father;matu1261;Matukar;-4.91;145.78",
        "sise;;fFF;female speaker's father's father ;matu1261;Matukar;-4.91;145.78",
        "sise;;fMF;female speaker's mother's father ;matu1261;Matukar;-4.91;145.78",
        "sise;;mFF;male speaker's father‘s father;matu1261;Matukar;-4.91;145.78",
        "sise;;mMM;male speaker's mother's mother;matu1261;Matukar;-4.91;145.78",
        "tinau;;fM;female speaker's mother;matu1261;Matukar;-4.91;145.78",
        "tinau;;mM;male speaker's mother;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;feBS;female speaker's older brother's son ;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;feZS;female speaker's older sister's son ;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;fyBS;female speaker's younger brother's son ;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;fyZS;female speaker's younger sister's son ;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;meBS;male speaker's older brother's son ;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;meZS;male speaker's older sister's son ;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;mMZS;male speaker's mother's sister's son ;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;myBS;male speaker's younger brother's son ;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;myZS;male speaker's younger sister's son ;matu1261;Matukar;-4.91;145.78",
        "kol pain;;feBD;female speaker's older brother's daughter ;matu1261;Matukar;-4.91;145.78",
        "kol pain;;feZD;female speaker's older sister's daughter ;matu1261;Matukar;-4.91;145.78",
        "kol pain;;fyBD;female speaker's younger brother's daughter ;matu1261;Matukar;-4.91;145.78",
        "kol pain;;fyZD;female speaker's younger sister's daughter ;matu1261;Matukar;-4.91;145.78",
        "kol pain;;meBD;male speaker's older brother's daughter ;matu1261;Matukar;-4.91;145.78",
        "kol pain;;meZD;male speaker's older sister's daughter ;matu1261;Matukar;-4.91;145.78",
        "kol pain;;mMZD;male speaker's mother's sister's daughter ;matu1261;Matukar;-4.91;145.78",
        "kol pain;;myBD;male speaker's younger brother's daughter ;matu1261;Matukar;-4.91;145.78",
        "kol pain;;myZD;male speaker's younger sister's daughter ;matu1261;Matukar;-4.91;145.78",
        "tamau han ka;;fFeB;female speaker's father's older brother ;matu1261;Matukar;-4.91;145.78",
        "tamau han te;;fFyB;female speaker's father's younger brother ;matu1261;Matukar;-4.91;145.78",
        "tinau han lun;;fMeB;female speaker's mother's older brother ;matu1261;Matukar;-4.91;145.78",
        "tinau han lun;;fMyB;female speaker's mother's younger brother ;matu1261;Matukar;-4.91;145.78",
        "tamau han ka;;mFeB;male speaker's father's older brother ;matu1261;Matukar;-4.91;145.78",
        "tamau han te;;mFyB;male speaker's father's younger brother ;matu1261;Matukar;-4.91;145.78",
        "tinau han lun;;mMeB;male speaker's mother's older brother ;matu1261;Matukar;-4.91;145.78",
        "tinau han lun;;mMyB;male speaker's mother's younger brother ;matu1261;Matukar;-4.91;145.78",
        "ka dabok;;feZ;female speaker's older sister;matu1261;Matukar;-4.91;145.78",
        "te natun;;fyZ;female speaker's younger sister;matu1261;Matukar;-4.91;145.78",
        "lu dabok;;meZ;male speaker's older sister;matu1261;Matukar;-4.91;145.78",
        "lu natun;;myZ;male speaker's younger sister;matu1261;Matukar;-4.91;145.78",
        "rawau;;fHM;speaker's husband's mother;matu1261;Matukar;-4.91;145.78",
        "wau;;mWM;speaker's wife's mother;matu1261;Matukar;-4.91;145.78",
        "wau;;fDH;female speaker's daughter's husband;matu1261;Matukar;-4.91;145.78",
        "wau;;mDH;male speaker's daughter's husband;matu1261;Matukar;-4.91;145.78",
        "wau;;fSW;female speaker's son's wife;matu1261;Matukar;-4.91;145.78",
        "wau;;mSW;male speaker's son's wife;matu1261;Matukar;-4.91;145.78",
        "wau;;fHF;speaker's husband's father;matu1261;Matukar;-4.91;145.78",
        "rawau;;mWF;speaker's wife's father;matu1261;Matukar;-4.91;145.78",
        "aim;;fS;female speaker's son;matu1261;Matukar;-4.91;145.78",
        "aim;;mS;male speaker's son;matu1261;Matukar;-4.91;145.78",
        "tamau han lun;;fFeZ;female speaker's father's older sister ;matu1261;Matukar;-4.91;145.78",
        "tamau han lun;;fFyZ;female speaker's father's younger sister ;matu1261;Matukar;-4.91;145.78",
        "tinau han ka;;fMeZ;female speaker's mother's older sister ;matu1261;Matukar;-4.91;145.78",
        "tinau han te;;fMyZ;female speaker's mother's younger sister ;matu1261;Matukar;-4.91;145.78",
        "tamau han lun;;mFeZ;male speaker's father's older sister ;matu1261;Matukar;-4.91;145.78",
        "tamau han lun;;mFyZ;male speaker's father's younger sister ;matu1261;Matukar;-4.91;145.78",
        "tinau han ka;;mMeZ;male speaker's mother's older sister ;matu1261;Matukar;-4.91;145.78",
        "tinau han ka;;mMyZ;male speaker's mother's younger sister ;matu1261;Matukar;-4.91;145.78",
        "aipain;;fD;female speaker's daughter;matu1261;Matukar;-4.91;145.78",
        "aipain;;mD;male speaker's daughter;matu1261;Matukar;-4.91;145.78",
        "tamau;;fF;female speaker's father;matu1261;Matukar;-4.91;145.78",
        "tamau;;mF;male speaker's father;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;mFeBS;male speaker's father‘s older brother‘s son;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;mFyBS;male speaker‘s father‘s younger brother‘s son;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;mFeZS;male speaker's father‘s older sister‘s son;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;mFyZS;male speaker‘s father‘s younger sister‘s son;matu1261;Matukar;-4.91;145.78",
        "kol pain;;mFeBD;male speaker's father‘s older brother‘s daughter;matu1261;Matukar;-4.91;145.78",
        "kol pain;;mFyBD;male speaker‘s father‘s younger brother‘s daughter;matu1261;Matukar;-4.91;145.78",
        "kol pain;;mFeZD;male speaker's father‘s older sister‘s daughter;matu1261;Matukar;-4.91;145.78",
        "kol pain;;mFyZD;male speaker‘s father‘s younger sister‘s daughter;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;mMeBS;male speaker's mother‘s older brother‘s son;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;mMyBS;male speaker‘s mother‘s younger brother‘s son;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;mMeZS;male speaker's mother‘s older sister‘s son;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;mMyZS;male speaker‘s mother‘s younger sister‘s son;matu1261;Matukar;-4.91;145.78",
        "kol pain;;mMeBD;male speaker's mother‘s older brother‘s daughter;matu1261;Matukar;-4.91;145.78",
        "kol pain;;mMyBD;male speaker‘s mother‘s younger brother‘s daughter;matu1261;Matukar;-4.91;145.78",
        "kol pain;;mMeZD;male speaker's mother‘s older sister‘s daughter;matu1261;Matukar;-4.91;145.78",
        "kol pain;;mMyZD;male speaker‘s mother‘s younger sister‘s daughter;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;fFeBS;female speaker's father‘s older brother‘s son;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;fFyBS;female speaker‘s father‘s younger brother‘s son;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;fFeZS;female speaker's father‘s older sister‘s son;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;fFyZS;female speaker‘s father‘s younger sister‘s son;matu1261;Matukar;-4.91;145.78",
        "kol pain;;fFeBD;female speaker's father‘s older brother‘s daughter;matu1261;Matukar;-4.91;145.78",
        "kol pain;;fFyBD;female speaker‘s father‘s younger brother‘s daughter;matu1261;Matukar;-4.91;145.78",
        "kol pain;;fFeZD;female speaker's father‘s older sister‘s daughter;matu1261;Matukar;-4.91;145.78",
        "kol pain;;fFyZD;female speaker‘s father‘s younger sister‘s daughter;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;fMeBS;female speaker's mother‘s older brother‘s son;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;fMyBS;female speaker‘s mother‘s younger brother‘s son;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;fMeZS;female speaker's mother‘s older sister‘s son;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;fMyZS;female speaker‘s mother‘s younger sister‘s son;matu1261;Matukar;-4.91;145.78",
        "kol pain;;fMeBD;female speaker's mother‘s older brother‘s daughter;matu1261;Matukar;-4.91;145.78",
        "kol pain;;fMyBD;female speaker‘s mother‘s younger brother‘s daughter;matu1261;Matukar;-4.91;145.78",
        "kol pain;;fMeZD;female speaker's mother‘s older sister‘s daughter;matu1261;Matukar;-4.91;145.78",
        "kol pain;;fMyZD;female speaker‘s mother‘s younger sister‘s daughter;matu1261;Matukar;-4.91;145.78"
        ]


    # each datatype is stored in a dictionary to filter out duplicates
    language_dict = {}
    parameter_dict = {}
    valueset_dict = {}
    word_dict = {}

    for datapoint in rawformat:
        list_of_entries = datapoint.split(";")

        # make the variables more readable and compile some of them to unique keys
        word = list_of_entries[0]
        word_ipa = list_of_entries[1]
        word_key = list_of_entries[2] + "-" + list_of_entries[4]
        valueset_key = "vs-" + list_of_entries[2] + "-" + list_of_entries[4]
        parameter_abbr = list_of_entries[2]
        #print parameter_abbr
        parameter_desc = list_of_entries[3]
        glotto = list_of_entries[4]
        language_name = list_of_entries[5]
        language_lat = float(list_of_entries[6])
        language_long = float(list_of_entries[7])

        # collect all languages
        if glotto not in language_dict:
            language_dict[glotto] = [glotto, language_name, language_lat, language_long]

        # collect all parameters
        if parameter_abbr not in parameter_dict:
            parameter_dict[parameter_abbr] = [parameter_abbr, parameter_desc]

        # collect all valuesets
        valueset_dict[valueset_key] = [valueset_key, parameter_abbr, glotto]

        # collect all words
        word_dict[word_key] = [word_key, word, word_ipa, valueset_key]

    for k, v in language_dict.iteritems():  # Languages get stored in data
        data.add(models.ParabankLanguage,
                 k,
                 id=k,
                 name=v[1],
                 latitude=v[2],
                 longitude=v[3],
                 patterns=[])

    for k, v in parameter_dict.iteritems():  # Parameters get stored in data
        data.add(models.ParabankParameter,
                 k,
                 id=k,
                 name=k,
                 description=v[1])

    for k, v in valueset_dict.iteritems():  # ValueSets get stored in data
        data.add(models.ParabankValueSet,
                 k,
                 id=k,
                 language=data['ParabankLanguage'][v[2]],
                 parameter=data['ParabankParameter'][v[1]])

    for k, v in word_dict.iteritems():  # Words get stored in data
        DBSession.add(models.Word(id=k,
                                  name=v[1],
                                  word_name=v[1],
                                  word_ipa=v[2],
                                  valueset=data['ParabankValueSet'][v[3]]))

    # read the rawinput again to look for Syncretisms and Patterns
    SyncretismPatternSetup(rawformat)

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
