# coding: utf8
from __future__ import unicode_literals, print_function, division

from zope.interface import implementer
from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import (
    Value, ValueSet, IdNameDescriptionMixin, Language, Parameter,
)
from clld_glottologfamily_plugin.models import HasFamilyMixin

import parabank.interfaces as parabank_interfaces


class ParadigmLanguage(Base):
    """association table for many-to-many lookup between Paradigm and Language"""
    __table_args__ = (UniqueConstraint('paradigm_pk', 'language_pk'),)
    paradigm_pk = Column(Integer, ForeignKey('paradigm.pk'))
    language_pk = Column(Integer, ForeignKey('language.pk'))


class LanguageSyncretism(Base):
    __table_args__ = (UniqueConstraint('language_pk', 'syncretism_pk'),)
    language_pk = Column(Integer, ForeignKey('language.pk'))
    syncretism_pk = Column(Integer, ForeignKey('syncretism.pk'))


class LanguagePattern(Base):
    __table_args__ = (UniqueConstraint('language_pk', 'pattern_pk'),)
    language_pk = Column(Integer, ForeignKey('language.pk'))
    pattern_pk = Column(Integer, ForeignKey('pattern.pk'))


class ParameterParadigm(Base):
    """association table for many-to-many lookup between Parameter and Paradigm"""
    __table_args__ = (UniqueConstraint('parameter_pk', 'paradigm_pk'),)
    parameter_pk = Column(Integer, ForeignKey('parameter.pk'))
    paradigm_pk = Column(Integer, ForeignKey('paradigm.pk'))


# -----------------------------------------------------------------------------
# specialized common mapper classes
# -----------------------------------------------------------------------------
@implementer(interfaces.ILanguage)
class ParabankLanguage(CustomModelMixin, Language, HasFamilyMixin):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    representation = Column(Integer)





@implementer(interfaces.IValue)
class Word(CustomModelMixin, Value):
    """label on each valueSet
       one-to-many relation to parabankValueSet adds backref column = valuesets"""
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    ipa = Column(Unicode)
    reference = Column(Unicode)
    alternative = Column(Unicode)
    comment = Column(Unicode)
    sound = Column(Unicode)


@implementer(parabank_interfaces.ISyncretism)
class Syncretism(IdNameDescriptionMixin, Base):
    """one-to-many relation to parabankValueSet adds backref column = valuesets
       many-to-many relation to Pattern adds backref column = patterns"""
    notation = Column(Unicode)
    languages = relationship(
        Language, secondary=LanguageSyncretism.__table__, backref='syncretisms')


@implementer(parabank_interfaces.IPattern)
class Pattern(IdNameDescriptionMixin, Base):
    """one-to-many relation to parabankValueSet adds backref column = valuesets
       many-to-many relation to Syncretism"""
    notation = Column(Unicode)
    languages = relationship(
        Language, secondary=LanguagePattern.__table__, backref='patterns')


@implementer(interfaces.IValueSet)
class ParabankValueSet(CustomModelMixin, ValueSet):
    """core model for lookup
       many-to-one relation to Word
       many-to-one relation to Language
       many-to-one relation to Parameter
       many-to-one relation to Syncretism
       many-to-one relation to Pattern
       """
    pk = Column(Integer, ForeignKey('valueset.pk'), primary_key=True)

    syncretism_pk = Column(Integer, ForeignKey('syncretism.pk'))
    syncretism = relationship(Syncretism, backref="all_valuesets")

    pattern_pk = Column(Integer, ForeignKey('pattern.pk'))
    pattern = relationship(Pattern, backref="all_valuesets")


@implementer(parabank_interfaces.IParadigm)
class Paradigm(IdNameDescriptionMixin, Base):
    """many-to-many relation to parabankLanguages
       many-to-many relation to parabankParameter"""
    languages = relationship(
        Language, secondary=ParadigmLanguage.__table__, backref='paradigms')
    parameters = relationship(
        Parameter, secondary=ParameterParadigm.__table__, backref='paradigms')
