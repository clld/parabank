# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common

import parabank
from parabank import models


def main(args):
    data = Data()

    dataset = common.Dataset(id=parabank.__name__, domain='parabank14.clld.org')
    DBSession.add(dataset)

    rawformat = [
        "bruder;bʀuːdɐ;meB;male speaker's elder brother;stan1295;Standard German;48.65;12.47",
        "bruder;bʀuːdɐ;myB;male speaker's younger brother;stan1295;Standard German;48.65;12.47",
        "schwester;ˈʃvɛstɐ;meZ;male speaker's elder sister;stan1295;Standard German;48.65;12.47",
        "schwester;ˈʃvɛstɐ;myZ;male speaker's younger sister;stan1295;Standard German;48.65;12.47",
        "bruder;bʀuːdɐ;feB;female speaker's elder brother;stan1295;Standard German;48.65;12.47",
        "bruder;bʀuːdɐ;fyB;female speaker's younger brother;stan1295;Standard German;48.65;12.47",
        "schwester;ˈʃvɛstɐ;feZ;female speaker's elder sister;stan1295;Standard German;48.65;12.47",
        "schwester;ˈʃvɛstɐ;fyZ;female speaker's younger sister;stan1295;Standard German;48.65;12.47",
        "vater;ˈfaːtɐ;F;speaker's father;stan1295;Standard German;48.65;12.47",
        "mutter;ˈmʊtɐ;M;speaker's mother;stan1295;Standard German;48.65;12.47",
        "sohn;zoːn;mS;male speaker's son;stan1295;Standard German;48.65;12.47",
        "tochter;ˈtɔχtɐ;mD;male speaker's daughter;stan1295;Standard German;48.65;12.47",
        "sohn;zoːn;fS;female speaker's son;stan1295;Standard German;48.65;12.47",
        "tochter;ˈtɔχtɐ;fD;female speaker's daughter;stan1295;Standard German;48.65;12.47",
        "tante;ˈtantə;FZ;speaker's father's sister (aunt);stan1295;Standard German;48.65;12.47",
        "onkel;ˈɔŋkl̩;FB;speaker's father's brother (uncle);stan1295;Standard German;48.65;12.47",
        "onkel;ˈɔŋkl̩;MB;speaker's mother's brother (uncle);stan1295;Standard German;48.65;12.47",
        "tante;ˈtantə;MZ;speaker's mother's sister (aunt);stan1295;Standard German;48.65;12.47",
        "tante;ˈtantə;MyZ;speaker's mother's younger sister (aunt);stan1295;Standard German;48.65;12.47",
        "tante;ˈtantə;MeZ;speaker's mother's elder sister (aunt);stan1295;Standard German;48.65;12.47",
        "tante;ˈtantə;FeZ;speaker's father's elder sister (aunt);stan1295;Standard German;48.65;12.47",
        "tante;ˈtantə;FyZ;speaker's father's younger sister (aunt);stan1295;Standard German;48.65;12.47",
        "onkel;ˈɔŋkl̩;FeB;speaker's father's elder brother (uncle);stan1295;Standard German;48.65;12.47",
        "onkel;ˈɔŋkl̩;FyB;speaker's father's younger brother (uncle);stan1295;Standard German;48.65;12.47",
        "onkel;ˈɔŋkl̩;MyB;speaker's mother's younger brother (unlce);stan1295;Standard German;48.65;12.47",
        "onkel;ˈɔŋkl̩;MeB;speaker's mother's elder brother (uncle);stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;mBS;male speaker's brother's son (nephew);stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;mBD;male speaker's brother's daughter (niece);stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;mZS;male speaker's sister's son (nephew);stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;mZD;male speaker's sister's daughter (niece);stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;fBS;female speaker's brother's son (nephew);stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;fBD;female speaker's brother's daughter (niece);stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;fZS;female speaker's sister's son (nephew);stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;fZD;female speaker's sister's daughter (niece);stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;meBS;male speaker's elder brother's son (nephew);stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;meBD;male speaker's elder brother's daughter (niece);stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;myBS;male speaker's younger brother's son (nephew);stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;myBD;male speaker's younger brother's daughter (niece);stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;meZS;male speaker's elder sister's son (nephew);stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;myZS;male speaker's younger sister's son (nephew);stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;meZD;male speaker's elder sister's daughter (niece);stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;myZD;male speaker's younger sister's daughter (niece);stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;feBS;female speaker's elder brother's son (nephew);stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;feBD;female speaker's elder brother's daughter (niece);stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;fyBS;female spekaer's younger brother's son (nephew);stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;fyBD;female speaker's younger brother's daughter (niece);stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;feZS;female speaker's elder sister's son (nephew);stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;fyZS;female speaker's younger sister's son (nephew);stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;feZD;female speaker's elder sister's daughter (niece);stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;fyZD;female speaker's younger sister's daughter (niece);stan1295;Standard German;48.65;12.47",
        "großmutter;ˈɡʀoːsˌmʊtɐ;MM_FM;speaker's grandmother;stan1295;Standard German;48.65;12.47",
        "großvater;ˈɡʀoːsˌfaːtɐ;FF_MF;speaker's grandfather;stan1295;Standard German;48.65;12.47",
        "enkel;ˈɛŋkl̩;SS_DS;speaker's grandson;stan1295;Standard German;48.65;12.47",
        "enkelin;ˈɛŋkəlɪn;DD_SD;speaker's granddaughter;stan1295;Standard German;48.65;12.47",
        "tante;ˈtantə;MF;speaker's mother's father (grandfather);stan1295;Standard German;48.65;12.47",
        "großmutter;ˈɡʀoːsˌmʊtɐ;FM;speaker's father's mother (grandmother);stan1295;Standard German;48.65;12.47",
        "großmutter;ˈɡʀoːsˌmʊtɐ;MM;speaker's mother's mother (grandmother);stan1295;Standard German;48.65;12.47",
        "großvater;ˈɡʀoːsˌfaːtɐ;FF;speaker's father's father (grandfather);stan1295;Standard German;48.65;12.47",
        "enkel;ˈɛŋkl̩;mSS;male speaker's son's son (grandson);stan1295;Standard German;48.65;12.47",
        "enkelin;ˈɛŋkəlɪn;mSD;male speaker's son's daughter (granddaughter);stan1295;Standard German;48.65;12.47",
        "enkel;ˈɛŋkl̩;mDS;male speaker's daughter's son (grandson);stan1295;Standard German;48.65;12.47",
        "enkelin;ˈɛŋkəlɪn;mDD;male speaker's daughter's daughter (granddaughter);stan1295;Standard German;48.65;12.47",
        "enkel;ˈɛŋkl̩;fSS;female speaker's son's son (grandson);stan1295;Standard German;48.65;12.47",
        "enkelin;ˈɛŋkəlɪn;fSD;female speaker's son's daughter (granddaughter);stan1295;Standard German;48.65;12.47",
        "enkel;ˈɛŋkl̩;fDS;female speaker's daughter's son (grandson);stan1295;Standard German;48.65;12.47",
        "enkelin;ˈɛŋkəlɪn;fDD;female speaker's daugher's daughter (granddaughter);stan1295;Standard German;48.65;12.47",
        "cousin;kuˈzɛ̃ː;FZS_MZS_FBS_MBS;speaker's male cousin;stan1295;Standard German;48.65;12.47",
        "cousine;kuˈziːnə;FZD_MZD_FBD_MBD;speakers female cousin;stan1295;Standard German;48.65;12.47",
        "cousin;kuˈzɛ̃ː;mFBS;male speaker's father' brother's son (cousin);stan1295;Standard German;48.65;12.47",
        "cousine;kuˈziːnə;mFBD;male speaker's father's brother's daughter (cousin);stan1295;Standard German;48.65;12.47",
        "cousin;kuˈzɛ̃ː;mFZS;male speaker's father's sister's son (cousin);stan1295;Standard German;48.65;12.47",
        "cousine;kuˈziːnə;mFZD;male speaker's father's sister's daughter (cousin);stan1295;Standard German;48.65;12.47",
        "cousin;kuˈzɛ̃ː;mMBS;male speaker's mother's brother's son (cousin);stan1295;Standard German;48.65;12.47",
        "cousine;kuˈziːnə;mMBD;male speaker's mother's brother's daughter (cousin);stan1295;Standard German;48.65;12.47",
        "nichte;ˈnɪçtə;mMZD;male speaker's mother's sister's daughter (niece);stan1295;Standard German;48.65;12.47",
        "neffe;ˈnɛfə;mMZS;male speaker's mother's sister's son (nephew);stan1295;Standard German;48.65;12.47",
        "cousin;kuˈzɛ̃ː;fFBS;female speaker's father'S brother's son (cousin);stan1295;Standard German;48.65;12.47",
        "cousine;kuˈziːnə;fFBD;female speaker's father's brother's daughter (cousin);stan1295;Standard German;48.65;12.47",
        "cousin;kuˈzɛ̃ː;fFZS;female speaker's father's sister's son (cousin);stan1295;Standard German;48.65;12.47",
        "cousine;kuˈziːnə;fFZD;female speaker's father's sister's daughter (cousin);stan1295;Standard German;48.65;12.47",
        "cousin;kuˈzɛ̃ː;fMBS;female speaker's mother's brother's son (cousin);stan1295;Standard German;48.65;12.47",
        "cousin;kuˈzɛ̃ː;fMZS;female speaker's mother's sister's son (cousin);stan1295;Standard German;48.65;12.47",
        "cousine;kuˈziːnə;fMBD;female speaker's mother's brother's daughter (cousin);stan1295;Standard German;48.65;12.47",
        "cousine;kuˈziːnə;fMZD;female speaker's mother's sister's daughter (cousin);stan1295;Standard German;48.65;12.47",
        "ehemann;ˈeːəˌman;H;speakers husband;stan1295;Standard German;48.65;12.47",
        "schwiegervater;ˈʃviːɡɐˌfaːtɐ;HF;speaker's husband's father;stan1295;Standard German;48.65;12.47",
        "schwiegermutter;ˈʃviːɡɐˌmʊtɐ;HM;speaker's husband's mother;stan1295;Standard German;48.65;12.47",
        "schwiegertochter;ˈʃviːɡɐˌtɔχtɐ;fSW;female speaker's son's wife;stan1295;Standard German;48.65;12.47",
        "schwiegersohn;ˈʃviːɡɐˌzoːn;fDH;female speaker's daughter's husband;stan1295;Standard German;48.65;12.47",
        "ehefrau;ˈeːəˌfʀaʊ̯;W;speaker's wife;stan1295;Standard German;48.65;12.47",
        "schwiegervater;ˈʃviːɡɐˌfaːtɐ;WF;speaker's wife's father;stan1295;Standard German;48.65;12.47",
        "schwiegermutter;ˈʃviːɡɐˌmʊtɐ;WM;speaker's wife's mother;stan1295;Standard German;48.65;12.47",
        "schwiegersohn;ˈʃviːɡɐˌzoːn;mDH;male speaker's daughter's husband;stan1295;Standard German;48.65;12.47",
        "schwiegertochter;ˈʃviːɡɐˌtɔχtɐ;mSW;male speaker's son's wife;stan1295;Standard German;48.65;12.47",
        "brother;ˈbɹʌðə(ɹ);meB;male speaker's elder brother;stan1293;Standard English;52.00;0.00",
        "brother;ˈbɹʌðə(ɹ);myB;male speaker's younger brother;stan1293;Standard English;52.00;0.00",
        "sister;sĭs'tər;meZ;male speaker's elder sister;stan1293;Standard English;52.00;0.00",
        "sister;sĭs'tər;myZ;male speaker's younger sister;stan1293;Standard English;52.00;0.00",
        "brother;ˈbɹʌðə(ɹ);feB;female speaker's elder brother;stan1293;Standard English;52.00;0.00",
        "brother;ˈbɹʌðə(ɹ);fyB;female speaker's younger brother;stan1293;Standard English;52.00;0.00",
        "sister;sĭs'tər;feZ;female speaker's elder sister;stan1293;Standard English;52.00;0.00",
        "sister;sĭs'tər;fyZ;female speaker's younger sister;stan1293;Standard English;52.00;0.00",
        "father;ˈfɑː.ðə(ɹ);F;speaker's father;stan1293;Standard English;52.00;0.00",
        "mother;ˈmʌðə(ɹ);M;speaker's mother;stan1293;Standard English;52.00;0.00",
        "son;sʌn;mS;male speaker's son;stan1293;Standard English;52.00;0.00",
        "daughter;ˈdɔːtə(r);mD;male speaker's daughter;stan1293;Standard English;52.00;0.00",
        "son;sʌn;fS;female speaker's son;stan1293;Standard English;52.00;0.00",
        "daughter;ˈdɔːtə(r);fD;female speaker's daughter;stan1293;Standard English;52.00;0.00",
        "aunt;ɑːnt;FZ;speaker's father's sister (aunt);stan1293;Standard English;52.00;0.00",
        "uncle;ŭngʹkəl;FB;speaker's father's brother (uncle);stan1293;Standard English;52.00;0.00",
        "uncle;ŭngʹkəl;MB;speaker's mother's brother (uncle);stan1293;Standard English;52.00;0.00",
        "aunt;ɑːnt;MZ;speaker's mother's sister (aunt);stan1293;Standard English;52.00;0.00",
        "aunt;ɑːnt;MyZ;speaker's mother's younger sister (aunt);stan1293;Standard English;52.00;0.00",
        "aunt;ɑːnt;MeZ;speaker's mother's elder sister (aunt);stan1293;Standard English;52.00;0.00",
        "aunt;ɑːnt;FeZ;speaker's father's elder sister (aunt);stan1293;Standard English;52.00;0.00",
        "aunt;ɑːnt;FyZ;speaker's father's younger sister (aunt);stan1293;Standard English;52.00;0.00",
        "uncle;ŭngʹkəl;FeB;speaker's father's elder brother (uncle);stan1293;Standard English;52.00;0.00",
        "uncle;ŭngʹkəl;FyB;speaker's father's younger brother (uncle);stan1293;Standard English;52.00;0.00",
        "uncle;ŭngʹkəl;MyB;speaker's mother's younger brother (unlce);stan1293;Standard English;52.00;0.00",
        "uncle;ŭngʹkəl;MeB;speaker's mother's elder brother (uncle);stan1293;Standard English;52.00;0.00",
        "nephew;ˈnɛv.ju;mBS;male speaker's brother's son (nephew);stan1293;Standard English;52.00;0.00",
        "niece;niːs;mBD;male speaker's brother's daughter (niece);stan1293;Standard English;52.00;0.00",
        "nephew;ˈnɛv.ju;mZS;male speaker's sister's son (nephew);stan1293;Standard English;52.00;0.00",
        "niece;niːs;mZD;male speaker's sister's daughter (niece);stan1293;Standard English;52.00;0.00",
        "nephew;ˈnɛv.ju;fBS;female speaker's brother's son (nephew);stan1293;Standard English;52.00;0.00",
        "niece;niːs;fBD;female speaker's brother's daughter (niece);stan1293;Standard English;52.00;0.00",
        "nephew;ˈnɛv.ju;fZS;female speaker's sister's son (nephew);stan1293;Standard English;52.00;0.00",
        "niece;niːs;fZD;female speaker's sister's daughter (niece);stan1293;Standard English;52.00;0.00",
        "nephew;ˈnɛv.ju;meBS;male speaker's elder brother's son (nephew);stan1293;Standard English;52.00;0.00",
        "niece;niːs;meBD;male speaker's elder brother's daughter (niece);stan1293;Standard English;52.00;0.00",
        "nephew;ˈnɛv.ju;myBS;male speaker's younger brother's son (nephew);stan1293;Standard English;52.00;0.00",
        "niece;niːs;myBD;male speaker's younger brother's daughter (niece);stan1293;Standard English;52.00;0.00",
        "nephew;ˈnɛv.ju;meZS;male speaker's elder sister's son (nephew);stan1293;Standard English;52.00;0.00",
        "nephew;ˈnɛv.ju;myZS;male speaker's younger sister's son (nephew);stan1293;Standard English;52.00;0.00",
        "niece;niːs;meZD;male speaker's elder sister's daughter (niece);stan1293;Standard English;52.00;0.00",
        "niece;niːs;myZD;male speaker's younger sister's daughter (niece);stan1293;Standard English;52.00;0.00",
        "nephew;ˈnɛv.ju;feBS;female speaker's elder brother's son (nephew);stan1293;Standard English;52.00;0.00",
        "niece;niːs;feBD;female speaker's elder brother's daughter (niece);stan1293;Standard English;52.00;0.00",
        "nephew;ˈnɛv.ju;fyBS;female spekaer's younger brother's son (nephew);stan1293;Standard English;52.00;0.00",
        "niece;niːs;fyBD;female speaker's younger brother's daughter (niece);stan1293;Standard English;52.00;0.00",
        "nephew;ˈnɛv.ju;feZS;female speaker's elder sister's son (nephew);stan1293;Standard English;52.00;0.00",
        "nephew;ˈnɛv.ju;fyZS;female speaker's younger sister's son (nephew);stan1293;Standard English;52.00;0.00",
        "niece;niːs;feZD;female speaker's elder sister's daughter (niece);stan1293;Standard English;52.00;0.00",
        "niece;niːs;fyZD;female speaker's younger sister's daughter (niece);stan1293;Standard English;52.00;0.00",
        "grandmother;ˈɡɹæn(d)mʌðə(ɹ);MM_FM;speaker's grandmother;stan1293;Standard English;52.00;0.00",
        "grandfather;ˈɡɹæn(d)fɑː.ðə(ɹ);FF_MF;speaker's grandfather;stan1293;Standard English;52.00;0.00",
        "grandson;ˈɡɹæn(d)sʌn;SS_DS;speaker's grandson;stan1293;Standard English;52.00;0.00",
        "granddaughter;ˈɡɹæn(d)dɔːtə®;DD_SD;speaker's granddaughter;stan1293;Standard English;52.00;0.00",
        "grandfather;ˈɡɹæn(d)fɑː.ðə(ɹ);MF;speaker's mother's father (grandfather);stan1293;Standard English;52.00;0.00",
        "grandmother;ˈɡɹæn(d)mʌðə(ɹ);FM;speaker's father's mother (grandmother);stan1293;Standard English;52.00;0.00",
        "grandmother;ˈɡɹæn(d)mʌðə(ɹ);MM;speaker's mother's mother (grandmother);stan1293;Standard English;52.00;0.00",
        "grandfather;ˈɡɹæn(d)fɑː.ðə(ɹ);FF;speaker's father's father (grandfather);stan1293;Standard English;52.00;0.00",
        "grandson;ˈɡɹæn(d)sʌn;mSS;male speaker's son's son (grandson);stan1293;Standard English;52.00;0.00",
        "granddaughter;ˈɡɹæn(d)dɔːtə®;mSD;male speaker's son's daughter (granddaughter);stan1293;Standard English;52.00;0.00",
        "grandson;ˈɡɹæn(d)sʌn;mDS;male speaker's daughter's son (grandson);stan1293;Standard English;52.00;0.00",
        "granddaughter;ˈɡɹæn(d)dɔːtə®;mDD;male speaker's daughter's daughter (granddaughter);stan1293;Standard English;52.00;0.00",
        "grandson;ˈɡɹæn(d)sʌn;fSS;female speaker's son's son (grandson);stan1293;Standard English;52.00;0.00",
        "granddaughter;ˈɡɹæn(d)dɔːtə®;fSD;female speaker's son's daughter (granddaughter);stan1293;Standard English;52.00;0.00",
        "grandson;ˈɡɹæn(d)sʌn;fDS;female speaker's daughter's son (grandson);stan1293;Standard English;52.00;0.00",
        "granddaughter;ˈɡɹæn(d)dɔːtə®;fDD;female speaker's daugher's daughter (granddaughter);stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;FZS_MZS_FBS_MBS;speaker's male cousin;stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;FZD_MZD_FBD_MBD;speakers female cousin;stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;mFBS;male speaker's father' brother's son (cousin);stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;mFBD;male speaker's father's brother's daughter (cousin);stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;mFZS;male speaker's father's sister's son (cousin);stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;mFZD;male speaker's father's sister's daughter (cousin);stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;mMBS;male speaker's mother's brother's son (cousin);stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;mMBD;male speaker's mother's brother's daughter (cousin);stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;mMZD;male speaker's mother's sister's daughter (niece);stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;mMZS;male speaker's mother's sister's son (nephew);stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;fFBS;female speaker's father'S brother's son (cousin);stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;fFBD;female speaker's father's brother's daughter (cousin);stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;fFZS;female speaker's father's sister's son (cousin);stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;fFZD;female speaker's father's sister's daughter (cousin);stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;fMBS;female speaker's mother's brother's son (cousin);stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;fMZS;female speaker's mother's sister's son (cousin);stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;fMBD;female speaker's mother's brother's daughter (cousin);stan1293;Standard English;52.00;0.00",
        "cousin;ˈkʌz(ə)n;fMZD;female speaker's mother's sister's daughter (cousin);stan1293;Standard English;52.00;0.00",
        "husband;ˈhʌzbənd;H;speakers husband;stan1293;Standard English;52.00;0.00",
        "father-in-law;ˈfɑː.ðə(ɹ) ɪn ˌlɔ;HF;speaker's husband's father;stan1293;Standard English;52.00;0.00",
        "mother-in-law;ˈmʌðə(ɹ) ɪn ˌlɔ;HM;speaker's husband's mother;stan1293;Standard English;52.00;0.00",
        "daughter-in-law;ˈdɔːtə(r) ɪn ˌlɔ;fSW;female speaker's son's wife;stan1293;Standard English;52.00;0.00",
        "son-in-law;sʌn ɪn ˌlɔ;fDH;female speaker's daughter's husband;stan1293;Standard English;52.00;0.00",
        "wife;waɪf;W;speaker's wife;stan1293;Standard English;52.00;0.00",
        "father-in-law;ˈfɑː.ðə(ɹ) ɪn ˌlɔ;WF;speaker's wife's father;stan1293;Standard English;52.00;0.00",
        "mother-in-law;ˈmʌðə(ɹ) ɪn ˌlɔ;WM;speaker's wife's mother;stan1293;Standard English;52.00;0.00",
        "son-in-law;sʌn ɪn ˌlɔ;mDH;male speaker's daughter's husband;stan1293;Standard English;52.00;0.00",
        "daughter-in-law;ˈdɔːtə(r) ɪn ˌlɔ;mSW;male speaker's son's wife;stan1293;Standard English;52.00;0.00",
        "ka dabok;;meB;male speaker's elder brother;matu1261;Matukar;-4.91;145.78",
        "te natun;;myB;male speaker's younger brother;matu1261;Matukar;-4.91;145.78",
        "lu dabok;;meZ;male speaker's elder sister;matu1261;Matukar;-4.91;145.78",
        "lu natun;;myZ;male speaker's younger sister;matu1261;Matukar;-4.91;145.78",
        "lu dabok;;feB;female speaker's elder brother;matu1261;Matukar;-4.91;145.78",
        "lu natun;;fyB;female speaker's younger brother;matu1261;Matukar;-4.91;145.78",
        "ka dabok;;feZ;female speaker's elder sister;matu1261;Matukar;-4.91;145.78",
        "te natun;;fyZ;female speaker's younger sister;matu1261;Matukar;-4.91;145.78",
        "tamau;;F;speaker's father;matu1261;Matukar;-4.91;145.78",
        "tinau;;M;speaker's mother;matu1261;Matukar;-4.91;145.78",
        "aim;;mS;male speaker's son;matu1261;Matukar;-4.91;145.78",
        "aipain;;mD;male speaker's daughter;matu1261;Matukar;-4.91;145.78",
        "aim;;fS;female speaker's son;matu1261;Matukar;-4.91;145.78",
        "aipain;;fD;female speaker's daughter;matu1261;Matukar;-4.91;145.78",
        "tamau han lun;;FZ;speaker's father's sister (aunt);matu1261;Matukar;-4.91;145.78",
        "tinau han lun;;MB;speaker's mother's brother (uncle);matu1261;Matukar;-4.91;145.78",
        "tinau han te;;MyZ;speaker's mother's younger sister (aunt);matu1261;Matukar;-4.91;145.78",
        "tinau han ka;;MeZ;speaker's mother's elder sister (aunt);matu1261;Matukar;-4.91;145.78",
        "tamau han lun;;FeZ;speaker's father's elder sister (aunt);matu1261;Matukar;-4.91;145.78",
        "tamau han lun;;FyZ;speaker's father's younger sister (aunt);matu1261;Matukar;-4.91;145.78",
        "tamau han ka;;FeB;speaker's father's elder brother (uncle);matu1261;Matukar;-4.91;145.78",
        "tamau han te;;FyB;speaker's father's younger brother (uncle);matu1261;Matukar;-4.91;145.78",
        "tinau han lun;;MyB;speaker's mother's younger brother (unlce);matu1261;Matukar;-4.91;145.78",
        "tinau han lun;;MeB;speaker's mother's elder brother (uncle);matu1261;Matukar;-4.91;145.78",
        "sise;;MM_FM;speaker's grandmother;matu1261;Matukar;-4.91;145.78",
        "sise;;FF_MF;speaker's grandfather;matu1261;Matukar;-4.91;145.78",
        "sise;;SS_DS;speaker's grandson;matu1261;Matukar;-4.91;145.78",
        "sise;;DD_SD;speaker's granddaughter;matu1261;Matukar;-4.91;145.78",
        "sise;;MF;speaker's mother's father (grandfather);matu1261;Matukar;-4.91;145.78",
        "sise;;FM;speaker's father's mother (grandmother);matu1261;Matukar;-4.91;145.78",
        "sise;;MM;speaker's mother's mother (grandmother);matu1261;Matukar;-4.91;145.78",
        "sise;;FF;speaker's father's father (grandfather);matu1261;Matukar;-4.91;145.78",
        "sise;;mSS;male speaker's son's son (grandson);matu1261;Matukar;-4.91;145.78",
        "sise;;mSD;male speaker's son's daughter (granddaughter);matu1261;Matukar;-4.91;145.78",
        "sise;;mDS;male speaker's daughter's son (grandson);matu1261;Matukar;-4.91;145.78",
        "sise;;mDD;male speaker's daughter's daughter (granddaughter);matu1261;Matukar;-4.91;145.78",
        "sise;;fSS;female speaker's son's son (grandson);matu1261;Matukar;-4.91;145.78",
        "sise;;fSD;female speaker's son's daughter (granddaughter);matu1261;Matukar;-4.91;145.78",
        "sise;;fDS;female speaker's daughter's son (grandson);matu1261;Matukar;-4.91;145.78",
        "sise;;fDD;female speaker's daugher's daughter (granddaughter);matu1261;Matukar;-4.91;145.78",
        "kol tamat;;FZS_MZS_FBS_MBS;speaker's male cousin;matu1261;Matukar;-4.91;145.78",
        "kol pain;;FZD_MZD_FBD_MBD;speakers female cousin;matu1261;Matukar;-4.91;145.78",
        "kol tamat;;mFBS;male speaker's father' brother's son (cousin);matu1261;Matukar;-4.91;145.78",
        "kol pain;;mFBD;male speaker's father's brother's daughter (cousin);matu1261;Matukar;-4.91;145.78",
        "kol tamat;;mFZS;male speaker's father's sister's son (cousin);matu1261;Matukar;-4.91;145.78",
        "kol pain;;mFZD;male speaker's father's sister's daughter (cousin);matu1261;Matukar;-4.91;145.78",
        "kol tamat;;mMBS;male speaker's mother's brother's son (cousin);matu1261;Matukar;-4.91;145.78",
        "kol pain;;mMBD;male speaker's mother's brother's daughter (cousin);matu1261;Matukar;-4.91;145.78",
        "kol pain;;mMZD;male speaker's mother's sister's daughter (niece);matu1261;Matukar;-4.91;145.78",
        "kol tamat;;mMZS;male speaker's mother's sister's son (nephew);matu1261;Matukar;-4.91;145.78",
        "kol tamat;;fFBS;female speaker's father'S brother's son (cousin);matu1261;Matukar;-4.91;145.78",
        "kol pain;;fFBD;female speaker's father's brother's daughter (cousin);matu1261;Matukar;-4.91;145.78",
        "kol tamat;;fFZS;female speaker's father's sister's son (cousin);matu1261;Matukar;-4.91;145.78",
        "kol pain;;fFZD;female speaker's father's sister's daughter (cousin);matu1261;Matukar;-4.91;145.78",
        "kol tamat;;fMBS;female speaker's mother's brother's son (cousin);matu1261;Matukar;-4.91;145.78",
        "kol tamat;;fMZS;female speaker's mother's sister's son (cousin);matu1261;Matukar;-4.91;145.78",
        "kol pain;;fMBD;female speaker's mother's brother's daughter (cousin);matu1261;Matukar;-4.91;145.78",
        "kol pain;;fMZD;female speaker's mother's sister's daughter (cousin);matu1261;Matukar;-4.91;145.78",
        "yawau;;H;speakers husband;matu1261;Matukar;-4.91;145.78",
        "wau;;HF;speaker's husband's father;matu1261;Matukar;-4.91;145.78",
        "rawau;;HM;speaker's husband's mother;matu1261;Matukar;-4.91;145.78",
        "wau;;fSW;female speaker's son's wife;matu1261;Matukar;-4.91;145.78",
        "wau;;fDH;female speaker's daughter's husband;matu1261;Matukar;-4.91;145.78",
        "yawau;;W;speaker's wife;matu1261;Matukar;-4.91;145.78",
        "rawau;;WF;speaker's wife's father;matu1261;Matukar;-4.91;145.78",
        "wau;;WM;speaker's wife's mother;matu1261;Matukar;-4.91;145.78",
        "wau;;mDH;male speaker's daughter's husband;matu1261;Matukar;-4.91;145.78",
        "wau;;mSW;male speaker's son's wife;matu1261;Matukar;-4.91;145.78",
        ]

    # each datatype is stored in a dictionary to filter out duplicates
    language_dict = {}
    parameter_dict = {}
    valueset_dict = {}
    word_dict = {}

    for element in rawformat:


        list_of_entries = element.split(";")

        # make the variables more readable and compile some of them to unique keys
        word = list_of_entries[0]
        word_ipa = list_of_entries[1]
        word_key = list_of_entries[2] + "-" + list_of_entries[4]
        valueset_key = "vs-" + list_of_entries[2] + "-" + list_of_entries[4]
        parameter_abbr = list_of_entries[2]
        parameter_desc = list_of_entries[3]
        glotto = list_of_entries[4]
        language_name= list_of_entries[5]
        language_lat = float(list_of_entries[6])
        language_long = float(list_of_entries[7])

        # collect all languages
        if glotto in language_dict:
            pass
        else:
            language_dict[glotto] = [glotto, language_name, language_lat, language_long]

        # collect all parameters
        if parameter_abbr in parameter_dict:
            pass
        else:
            parameter_dict[parameter_abbr] = [parameter_abbr, parameter_desc]

        # collect all valuesets
        valueset_dict[valueset_key] = [valueset_key, parameter_abbr, glotto]

        # collect all words
        word_dict[word_key] = [word_key, word, word_ipa, valueset_key]

    # Languages get stored in data
    print str(language_dict)
    for k, v in language_dict.iteritems():
        print k, v

        data.add(common.Language,
                 k,
                 id=k,
                 name=v[1],
                 latitude=v[2],
                 longitude=v[3])

    print "-"
    # Parameters get stored in data
    print str(parameter_dict)
    for k, v in parameter_dict.iteritems():
        print k, v

        data.add(models.ParabankParameter,
                 k,
                 id=k,
                 name=k,
                 description=v[1])

    print "-"
    # ValueSets get stored in data
    print str(valueset_dict)
    for k, v in valueset_dict.iteritems():
        print k, v
        data.add(models.ParabankValueSet,
                 k,
                 id=k,
                 language=data['Language'][v[2]],
                 parameter=data['ParabankParameter'][v[1]])

    print "-"
    # Words get added to DBsession
    print str(word_dict)
    for k, v in word_dict.iteritems():
        print k, v

        DBSession.add(models.Word(id=k,
                                  name=v[1],
                                  word_name=v[1],
                                  word_ipa=v[2],
                                  valueset=data['ParabankValueSet'][v[3]]))

        # ++++++++++++++++++++++++


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
