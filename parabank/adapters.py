# coding: utf8
from __future__ import unicode_literals, print_function, division
from clld.db.meta import DBSession

from clld_phylogeny_plugin.interfaces import ITree
from clld_phylogeny_plugin.tree import Tree
from clld_phylogeny_plugin.models import Phylogeny


class ParadigmTree(Tree):
    def __init__(self, req, param):
        self._param = param
        phylo = DBSession.query(Phylogeny).first()
        Tree.__init__(self, phylo, req, eid='tree' + phylo.id)

    @property
    def parameters(self):
        return [self._param]

    def get_marker(self, valueset):
        color = '#fff'
        if valueset.values and valueset.values[0].domainelement_pk:
            color = valueset.values[0].domainelement.jsondata['color']
        return 'c', color


def includeme(config):
    config.registry.registerUtility(ParadigmTree, ITree)
