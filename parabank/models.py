from zope.interface import implementer
from sqlalchemy import (
    Column,
    Unicode,
    String,
    Integer,
    ForeignKey,
    UniqueConstraint,
    PrimaryKeyConstraint,
    Table
    )
from sqlalchemy.orm import relationship, backref

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import Value, ValueSet, Parameter, IdNameDescriptionMixin

import parabank.interfaces as parabank_interfaces


class ParadigmLanguage(Base):
    """association table for many-to-many lookup between Paradigm and Language"""
    __table_args__ = (UniqueConstraint('paradigm_pk', 'language_pk'),)
    pk = Column(Integer, default=False)
    paradigm_pk = Column(Integer, ForeignKey('paradigm.id'), primary_key=True)
    language_pk = Column(Integer, ForeignKey('language.id'), primary_key=True)


class PatternSyncretism(Base):
    """association table for many-to-many lookup between Pattern and Syncretism"""
    __table_args__ = (PrimaryKeyConstraint('pattern_pk', 'syncretism_pk'),)
    pk = Column(Integer, default=False)
    pattern_pk = Column(Integer, ForeignKey('pattern.pk'), primary_key=True)
    syncretism_pk = Column(Integer, ForeignKey('syncretism.pk'), primary_key=True)


class ParameterParadigm(Base):
    """association table for many-to-many lookup between Parameter and Paradigm"""
    __table_args__ = (UniqueConstraint('parabankparameter_pk', 'paradigm_pk'),)
    pk = Column(Integer, default=False)
    parabankparameter_pk = Column(Integer, ForeignKey('parabankparameter.pk'), primary_key=True)
    paradigm_pk = Column(Integer, ForeignKey('paradigm.pk'), primary_key=True)

# -----------------------------------------------------------------------------
# specialized common mapper classes
# -----------------------------------------------------------------------------


#@implementer(interfaces.ILanguage)
#class ParabankLanguage(CustomModelMixin, Language):
#    """language used as given by CLLD +
#       many-to-many with Paradigm adds backref column: paradigms"""
#    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)

#@implementer(interfaces.IContribution)
#class ParabankContribution(CustomModelMixin, Contribution):
#    """conrtibution used as given by CLLD"""
#    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)


@implementer(interfaces.IValue)
class Word(CustomModelMixin, Value):
    """label on each valueSet
       one-to-many relation to parabankValueSet adds backref column = valuesets"""
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    word_name = Column(Unicode, default=True)
    word_ipa = Column(Unicode)
    word_description = Column(Unicode)
    sound = Column(Unicode)


@implementer(interfaces.IParameter)
class ParabankParameter(CustomModelMixin, Parameter):
    """one-to-many relation to parabankValueSet adds backref column = valuesets
       many-to-many relation to Paradigm adds backref column = paradigms"""
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    # parameter_name = Column(Unicode, default=True) # Inherited from Base class
    # parameter_abbreviation = Column(Unicode) # we don't need it!
    # parameter_description = Column(Unicode) # Inherited from Base class


@implementer(parabank_interfaces.ISyncretism)
class Syncretism(IdNameDescriptionMixin, Base):
    """one-to-many relation to parabankValueSet adds backref column = valuesets
       many-to-many relation to Pattern adds backref column = patterns"""
    pk = Column(Integer, primary_key=True)  # Inherited from Base class
    #name = Column(Unicode, default=True) # Inherited from Base class
    #description = Column(Unicode) # Inherited from Base class


@implementer(parabank_interfaces.IPattern)
class Pattern(IdNameDescriptionMixin, Base):
    """one-to-many relation to parabankValueSet adds backref column = valuesets
       many-to-many relation to Syncretism"""
    pk = Column(Integer, primary_key=True) # Inherited from Base class
    #name = Column(Unicode, default=True) # Inherited from Base class
    #description = Column(Unicode)  # change to pattern_description # Inherited from Base class
    syncretisms = relationship('Syncretism', secondary=PatternSyncretism.__table__, backref='patterns')


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

    # many-to-one with Syncretism
    syncretism_pk = Column(Integer, ForeignKey('syncretism.pk'))
    syncretism = relationship("Syncretism", backref="all_valuesets")

    # many-to-one with Pattern
    pattern_pk = Column(Integer, ForeignKey('pattern.pk'))
    pattern = relationship("Pattern", backref="all_valuesets")

    # many-to-one with Word covered by clld.models.value
    # word_pk = Column(Integer, ForeignKey('word.pk'))
    # word = relationship("Word", backref="all_valuesets")

    # many-to-one with Language covered by clld.models.valueset
    # language_pk = Column(Integer, ForeignKey('parabanklanguage.pk'), default=True)
    # language = relationship("parabankLanguage", backref="all_valuesets")

    # many-to-one with Parameter covered by clld.models.valueset
    # parameter_pk = Column(Integer, ForeignKey('parabankparameter.pk'), default=True)
    # parameter = relationship("parabankParameter", backref="all_valuesets")

    # many-to-one with parabankContribution covered by clld.models.valueset
    # contribution_pk = Column(Integer, ForeignKey('parabankcontribution.pk'))
    # contribution = relationship("parabankContribution", backref="all_valuesets")

    # source = Column(Unicode)


@implementer(parabank_interfaces.IParadigm)
class Paradigm(IdNameDescriptionMixin, Base):
    """many-to-many relation to parabankLanguages
       many-to-many relation to parabankParameter"""
    pk = Column(Integer, primary_key=True)
    id = Column(Unicode)
    name = Column(Unicode, default=True)
    description = Column(Unicode)
    languages = relationship('Language', secondary=ParadigmLanguage.__table__, backref='paradigms')
    parameters = relationship('ParabankParameter', secondary=ParameterParadigm.__table__, backref='paradigms')

    # __mapper_args__ = {'polymorphic_identity': 'paradigm',}
