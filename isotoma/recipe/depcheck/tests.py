import unittest
from isotoma.recipe.depcheck import Depcheck
from zc.buildout import UserError
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
        self.assertRaises(UserError, Depcheck, None, None, {
            "locale-file": self.locale_file.name,
            "locale": "\n    ar_AR.UTF-8\n    de_DE.UTF-8",
        })

    def test_executable(self):
        dc = Depcheck(None, None, {
            "executable": "/usr/bin/env"
        })
        dc.install()

    def test_nonexecutable(self):
        self.assertRaises(UserError, Depcheck, None, None, {
            "executable": "/etc/hosts"
        })

    def test_warn(self):
        dc = Depcheck(None, None, {
            "executable": "/etc/hosts",
            "action": "warn",
        })
        dc.install()

    def test_current_user(self):
        import subprocess
        p = subprocess.Popen(["whoami"], stdout=subprocess.PIPE)
        user = p.stdout.read().strip()

        dc = Depcheck(None, None, {
            "current-user": user,
        })
        dc.install()

    def test_incorrect_current_user(self):
        self.assertRaises(UserError, Depcheck, None, None, {
            "current-user": "4284vp984r984jpf8q4f98wefkdefj043"
        })

    def test_users(self):
        dc = Depcheck(None, None, {
            "users": "root\ndaemon\nbin",
        })
        dc.install()

    def test_nonexistent_user(self):
        self.assertRaises(UserError, Depcheck, None, None, {
            "users": "4284vp984r984jpf8q4f98wefkdefj043"
        })

    def test_pyversion(self):
        dc = Depcheck(None, None, {
            "python": "\t2.3\n\t2.4\n\t2.5\n\t2.6\n\t2.7\n\t3.0"
        })
        dc.install()

    def test_incorrect_pyversion(self):
        self.assertRaises(UserError, Depcheck, None, None, {
            "python": "\tfoo"
        })
