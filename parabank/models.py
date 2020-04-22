from zope.interface import implementer
from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    ForeignKey,
)

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import Value, Language
from clld_glottologfamily_plugin.models import HasFamilyMixin


# -----------------------------------------------------------------------------
# specialized common mapper classes
# -----------------------------------------------------------------------------
@implementer(interfaces.ILanguage)
class ParabankLanguage(CustomModelMixin, Language, HasFamilyMixin):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    representation = Column(Integer)
    source = Column(Unicode)
    classification = Column(Unicode)


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
    original = Column(Unicode)
