Dependency checker buildout recipe
==================================

If you are relying on the OS to provide some facilities for your software, this
recipe can help verify that the dependencies exist.

The recipe can check for any of the following:

    * If certain files exist in the filesystem and that they are executable
    * If certain locales are available on the system
    * If buildout is being run as a particular user
    * If certain users are present on the system
    * If buildout is being run by any of a list of python versions

Note that locales are checked in an Ubuntu-specific way, so may not work for
you.

If any dependencies fail, and the "action" option isn't set to "warn", the
recipe will raise an exception.

An example::

    [foo]
    program = /usr/sbin/foo

    [bar]
    binary = /usr/sbin/bar
    locale = nl_NL.UTF-8

    [dependencies]
    recipe = isotoma.recipe.depcheck
    executable = 
        ${foo:program}
        ${bar:binary}
    locale = ${bar:locale}
    current-user = webappuser
    users =
        taskqueue
        www-data
    python =
        2.5
        2.6
        2.7
    action = warn

Parameters
----------

executable
    A list of one or more paths to files that must be executable
directory
    A list of one or more paths to inodes that must exist and be directories
file
    A list of one or more paths to inodes that must exist and be files
locale-file
    The name of a file on disk to look for locales in (defaults to the Ubuntu location)
locale
    A list of one or more locales to check are in locale-file
current-user
    Ensures that buildout is being run by the user specified.
users
    A list of users that must have accounts on the local system. (Users must 
    be present in /etc/passwd)
python
    A list of python versions that buildout be executed under (useful if your
    application is py2.4-only, etc.)
action
    Either "warn" or "fail". The default is to "fail" if a dependency isn't met.

License
-------

Copyright 2010 Isotoma Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


