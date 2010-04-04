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

class DependencyError(Exception): pass

class Depcheck(object):

    def __init__(self, buildout, name, options):
        self.name = name
        self.options = options
        self.buildout = buildout
        self.options.setdefault("locale-file", "/var/lib/locales/supported.d/local")

    def install(self):
        for e in self.options.get('executable', '').strip().split():
            e = e.strip()
            if not os.path.exists(e):
                raise DependencyError("Dependency %s does not exist" % e)
            mode = os.stat(e)[stat.ST_MODE]
            if not stat.S_IXOTH & mode:
                raise DependencyError("Dependency %s is not executable" % e)
        locales = [x.split(" ",1)[0] for x in open(self.options["locale-file"]).read().split("\n")]
        for l in self.options.get("locale", '').strip().split():
            l = l.strip()
            if l not in locales:
                raise DependencyError("Missing locale %s from system" % l)
        return []

    def update(self):
        pass
