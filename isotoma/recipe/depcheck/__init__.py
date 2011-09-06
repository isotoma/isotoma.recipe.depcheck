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

    def values(self, values_str):
        for option in values_str.strip().split():
            yield option.strip()

    def install(self):
        try:
            # Check for executables
            for e in self.values(self.options.get("executable", "")):
                if not os.path.exists(e):
                    raise UserError("Dependency %s does not exist" % e)
                mode = os.stat(e)[stat.ST_MODE]
                if not stat.S_IXOTH & mode:
                    raise UserError("Dependency %s is not executable" % e)

            # Check for directories
            for d in self.values(self.options.get("directory", "")):
                if not os.path.isdir(d):
                    raise UserError("Dependency %s is not a directory" % d)

            # Check for files
            for f in self.values(self.options.get("file", "")):
                if not os.path.isfile(f):
                    raise UserError("Dependency %s is not a file" % f)

            # Check for locales
            locales = [x.split(" ",1)[0] for x in open(
                self.options["locale-file"]
            ).read().split("\n")]

            for l in self.values(self.options.get("locale", "")):
                if l not in locales:
                    raise UserError("Missing locale %s from system" % l)

            # Check current user
            current_user = self.options.get("current-user", None)
            if current_user:
                import getpass
                if not current_user == getpass.getuser():
                    raise UserError("Buildout must be run as user %s" % current_user)


            # Check system-installed users
            # FIXME: Make this work with LDAP users as well
            PASSWD_FILE = "/etc/passwd"
            f = open(PASSWD_FILE)
            users = f.read()
            f.close()

            users = [u.split(":")[0] for u in users.splitlines()]
            for user in self.values(self.options.get("users", "")):
                if user not in users:
                    raise UserError("Missing user %s from system" % user)

        except UserError, e:
            if self.options["action"] == "warn":
                self.log.warn(str(e))
            else:
                raise   # re-raise

        return []

    def update(self):
        pass
