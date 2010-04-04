import unittest
from isotoma.recipe.depcheck import Depcheck, DependencyError
import tempfile
import os

class TestDepcheck(unittest.TestCase):

    def setUp(self):
        self.locale_file = tempfile.NamedTemporaryFile(delete=False)
        print >>self.locale_file, "en_GB.UTF-8 UTF-8"
        print >>self.locale_file, "en_US.UTF-8 UTF-8"
        print >>self.locale_file, "es_ES.UTF-8 UTF-8"
        print >>self.locale_file, "nl_NL.UTF-8 UTF-8"
        self.locale_file.close()

    def tearDown(self):
        os.unlink(self.locale_file.name)

    def test_empty(self):
        dc = Depcheck(None, None, {})
        dc.install()

    def test_locales_exists_one(self):
        dc = Depcheck(None, None, {
            "locale-file": self.locale_file.name,
            "locale": "en_GB.UTF-8",
        })
        dc.install()

    def test_locales_exists_many(self):
        dc = Depcheck(None, None, {
            "locale-file": self.locale_file.name,
            "locale": "\n    en_GB.UTF-8\n    nl_NL.UTF-8",
        })
        dc.install()

    def test_locales_not_exist(self):
        dc = Depcheck(None, None, {
            "locale-file": self.locale_file.name,
            "locale": "\n    ar_AR.UTF-8\n    de_DE.UTF-8",
        })
        self.assertRaises(DependencyError, dc.install)

    def test_executable(self):
        dc = Depcheck(None, None, {
            "executable": "/usr/bin/env"
        })
        dc.install()

    def test_nonexecutable(self):
        dc = Depcheck(None, None, {
            "executable": "/etc/hosts"
        })
        self.assertRaises(DependencyError, dc.install)



