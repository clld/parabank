# coding: utf8
from __future__ import unicode_literals, print_function, division

from clldutils.path import Path
from clld.tests.util import TestWithApp

import parabank


class Tests(TestWithApp):
    __cfg__ = Path(parabank.__file__).parent.joinpath('..', 'development.ini').resolve()

    def test_home(self):
        self.app.get('/')

    def test_language(self):
        self.app.get('/languages/wang1287')
