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
from clld_phylogeny_plugin import models

import parabank.interfaces as parabank_interfaces


# -----------------------------------------------------------------------------
# specialized common mapper classes
# -----------------------------------------------------------------------------
@implementer(interfaces.ILanguage)
class ParabankLanguage(CustomModelMixin, Language, HasFamilyMixin):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    representation = Column(Integer)


@implementer(interfaces.IParameter)
class ParabankParameter(CustomModelMixin, Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    type = Column(Unicode)


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
