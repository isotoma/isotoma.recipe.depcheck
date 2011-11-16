# Copyright 2010 Isotoma Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os
import stat
import logging

from zc.buildout import UserError

class Depcheck(object):

    def __init__(self, buildout, name, options):
        self.name = name
        self.options = options
        self.buildout = buildout
        self.options.setdefault("locale-file", "/var/lib/locales/supported.d/local")
        # Default action upon missing dep is to fail
        self.options.setdefault("action", "fail")

        self.log = logging.getLogger(__name__)

        self._fail = False
        self.check()

    def dep_fail(self, message):
        self.log.warn(message)
        self._fail = True

    def values(self, values_str):
        if values_str:
            for option in values_str.strip().split():
                yield option.strip()

    def check_executables(self):
        # Check for executables
        for e in self.values(self.options.get("executable", "")):
            if not os.path.exists(e):
                self.dep_fail("Dependency %s does not exist" % e)
            mode = os.stat(e)[stat.ST_MODE]
            if not stat.S_IXOTH & mode:
                self.dep_fail("Dependency %s is not executable" % e)

    def check_dirs(self):
        # Check for directories
        for d in self.values(self.options.get("directory", "")):
            if not os.path.isdir(d):
                self.dep_fail("Dependency %s is not a directory" % d)

    def check_files(self):
        # Check for files
        for f in self.values(self.options.get("file", "")):
            if not os.path.isfile(f):
                self.dep_fail("Dependency %s is not a file" % f)
    
    def check_locales(self):
        # Check for locales
        if not self.options.get("locale", None):
            return

        try:
            locales = [x.split(" ",1)[0] for x in open(
                self.options["locale-file"]
            ).read().split("\n")]

            for l in self.values(self.options.get("locale", "")):
                if l not in locales:
                    self.dep_fail("Missing locale %s from system" % l)
        except IOError:
            self.dep_fail("Could not locate locales file on this system")

    def check_current_user(self):
        # Check current user
        current_user = self.options.get("current-user", None)
        if current_user:
            import getpass
            if not current_user == getpass.getuser():
                self.dep_fail("Buildout must be run as user %s" % current_user)


    # FIXME: Make this work with LDAP users as well
    def check_users(self):
        def fetch_user_list():
            PASSWD_FILE = "/etc/passwd"
            f = open(PASSWD_FILE)
            users = f.read()
            f.close()
            return [u.split(":")[0] for u in users.splitlines()]

        users = fetch_user_list()

        for user in self.values(self.options.get("users", "")):
            if user not in users:
                self.dep_fail("Missing user %s from system" % user)

    def check_python_version(self):
        def this_pyversion():
            return sys.version[:3]

        if self.options.get("python", None):
            if not this_pyversion() in self.values(self.options.get("python")):
                self.dep_fail("Require python version %r, using %s" % (
                    list(self.values(self.options.get("python"))),
                    this_pyversion()
                ))


    def check(self):
        self.check_executables()
        self.check_dirs()
        self.check_files()
        self.check_locales()
        self.check_current_user()
        self.check_users()
        self.check_python_version()

        if self._fail:
            if not self.options["action"] == "warn":
                raise UserError("Requirements not met.")

    def install(self):
        return []

    def update(self):
        pass
