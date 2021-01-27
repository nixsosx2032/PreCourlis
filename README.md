# PreCourlis QGIS plugin

QGIS 3 plugin that is meant to model the bed of rivers and export data for the
Courlis module of Telemac-Mascaret.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE.md)
![Continuous integration](https://github.com/msecher/PreCourlis/workflows/Continuous%20integration/badge.svg)

## Development / testing

Plugin source code is in folder `PreCourlis`.

Recommended development environment is Linux.
You can also use Windows but you'll not have the help of `make` targets.

Automated tests suite can be runned with Docker on any Linux operating system.

### Build development docker image

``````````
make build
``````````

This will build the docker image named `camptocamp/edf-precourlis-builder` and
build or retrieve some runtime files:
- PreCourlis/ui/resources_rc.py  (generated from PreCourlis/resources/resources.qrc)
- PreCourlis/lib/TatooineMesher  (cloned from https://github.com/arnaud-morvan/TatooineMesher/tree/PreCourlis)

This image will be later used to run a QGIS desktop application in a adapted
environment or to run automated tests suite.

### Run automated tests suite

``````````
make tests
``````````

This will run the automated tests suite in a docker container.

Note that this plugin contains tools that take some datasets as input
and produce other datasets as outputs.
Some tests compare those outputs to expected ones.
There is an option to overwrite the expected result datasets:

```````````````````````````
make test-overwrite-outputs
```````````````````````````

This will run the tests and overwrite the expected resultsets.
After that you can check the expected results sets feet your needs and commit them.

### Test the plugin with QGIS desktop in a docker environment

`````````
make qgis
`````````

This will run a docker container with QGIS desktop application.

Source code in mounted though a volume in folder `/app`.

This `/app` folder is also declared in `QGIS_PLUGINPATH` so the plugin can be
directly activated in "QGIS Extensions manager".

You can also access the tests input and expected results datasets in folder
`/app/tests/data`.

Note that QGIS setting are also stored in a named volume, so they will persist
when QGIS container is deleted and recreated.

### Test the plugin with QGIS desktop

#### Linux

`````````
make link
`````````

This will create a symbolic link to the plugin source code folder in your home
QGIS Python plugins folder.

#### Windows

In QGIS settings, in tab *System* add an environment variable named
`QGIS_PLUGINPATH` with as value the path to this folder (git repository root folder).

#### All operating systems

In QGIS desktop extensions manager:

- load plugin `PreCourlis`;
- install QGIS Plugin `Plugin Reloader`.

Now you can easily make changes in source code, reload plugin `PreCourlis` and
see changes in QGIS desktop.

### Packaging

````````````
make package
````````````

This will create an archive of the plugin in `dist/reperesDeCrues.zip`

### Test the package archive

```````````
make deploy
```````````

This will update the Zip archive (package) and extract files in your home QGIS
Python plugins folder.
With this you can test the packaged Zip archive contains all required files.

### List all available make targets

`````````
make help
`````````
