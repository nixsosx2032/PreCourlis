#/***************************************************************************
# PreCourlisPlugin
#
# Creation de profils pour Courlis

#        begin              : 2020-03-13
#        git sha            : $Format:%H$
#        copyright          : (C) 2020 by EDF Hydro, DeltaCAD, Camptocamp
#        email              : matthieu.secher@edf.fr
# ***************************************************************************/

#/***************************************************************************
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# ***************************************************************************/


###########################################################
# This variables may be overriden to match you environment
###########################################################

# If locales are enabled, set the name of the lrelease binary on your system. If
# you have trouble compiling the translations, you may have to specify the full path to
# lrelease
#LRELEASE = lrelease
#LRELEASE = lrelease-qt4

# QGISDIR points to the location where your plugin should be installed.
# This varies by platform, relative to your HOME directory:
# * Linux:
#   .local/share/QGIS/QGIS3/profiles/default/python/plugins/
# * Mac OS X:
#   Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins
# * Windows:
#   AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins'
QGISDIR ?= .local/share/QGIS/QGIS3/profiles/default

###############################################################
# Normally you would not need to override variables below here
###############################################################

PLUGINNAME = PreCourlis
LOCALES = fr

PACKAGES_NO_UI = widgets
PACKAGES = $(PACKAGES_NO_UI) ui

PACKAGES_SOURCES := $(shell find $(PACKAGES) -name "*.py")
SOURCES := PreCourlis.py $(PACKAGES_SOURCES)

PEP8EXCLUDE=pydev,resources.py,conf.py,third_party,ui

default: help

.PHONY: help
help: ## Display this help message
	@echo "Usage: make <target>"
	@echo
	@echo "Possible targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "    %-20s%s\n", $$1, $$2}'

compile:
	make -C resources
	make -C help html

test: compile transcompile
	@echo
	@echo "----------------------"
	@echo "Regression Test Suite"
	@echo "----------------------"

	@# Preceding dash means that make will continue in case of errors
	@-export PYTHONPATH=`pwd`:$(PYTHONPATH); \
		export QGIS_DEBUG=0; \
		export QGIS_LOG_FILE=/dev/null; \
		nosetests -v --with-id --with-coverage --cover-package=. \
		3>&1 1>&2 2>&3 3>&- || true
	@echo "----------------------"
	@echo "If you get a 'no module named qgis.core error, try sourcing"
	@echo "the helper script we have provided first then run make test."
	@echo "e.g. source run-env-linux.sh <path to qgis install>; make test"
	@echo "----------------------"

deploy: ## Deploy plugin to your QGIS plugin directory
deploy: package derase
	unzip PreCourlis.zip -d $(HOME)/$(QGISDIR)/python/plugins/

derase: ## Remove deployed plugin from your QGIS plugin directory
	rm -Rf $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)

package: ## Create a zip package of the plugin named $(PLUGINNAME).zip.
package: compile
	rm -f $(PLUGINNAME).zip
	git archive --prefix=$(PLUGINNAME)/ -o $(PLUGINNAME).zip HEAD

	# remove not needed source files
	zip -d $(PLUGINNAME).zip $(PLUGINNAME)/\*Makefile
	zip -d $(PLUGINNAME).zip $(PLUGINNAME)/\*.gitignore
	zip -d $(PLUGINNAME).zip $(PLUGINNAME)/help/\*
	zip -d $(PLUGINNAME).zip $(PLUGINNAME)/test/\*
	zip -d $(PLUGINNAME).zip $(PLUGINNAME)/pylintrc
	zip -d $(PLUGINNAME).zip $(PLUGINNAME)/README.rst
	#zip -d $(PLUGINNAME).zip $(PLUGINNAME)/dev-requirements.txt

	# create folder for non source files
	rm -rf $(PLUGINNAME)/
	# add user doc
	mkdir -p $(PLUGINNAME)/help/build
	cp -r help/build/html/ $(PLUGINNAME)/help/build/
	# add resource_rc.py
	mkdir -p $(PLUGINNAME)/ui/
	cp ui/*.py $(PLUGINNAME)/ui/
	# add non source files to zip archive
	zip -g $(PLUGINNAME).zip $(PLUGINNAME)/*/*
	zip -g $(PLUGINNAME).zip `find $(PLUGINNAME)/help/build/html`
	# delete non source files temporary folder
	rm -rf $(PLUGINNAME)/

	echo "Created package: $(PLUGINNAME).zip"

.PHONY: upload
upload: ## Upload plugin to QGIS Plugin repo
upload: package
	$(PLUGIN_UPLOAD) $(PLUGINNAME).zip

.PHONY: transup
transup: ## Update translation files with any new strings.
	chmod +x scripts/update-strings.sh
	scripts/update-strings.sh $(LOCALES)

.PHONY: transcompile
transcompile: ## Compile translation files to .qm files
	chmod +x scripts/compile-strings.sh
	scripts/compile-strings.sh $(LRELEASE) $(LOCALES)

.PHONY: clean
clean: ## Delete generated files
	rm -f i18n/*.qm
	rm ui/resources.py

.PHONY: doc
doc: ## Build documentation using sphinx
	make -C help html

.PHONY: pylint
pylint: ## Check the code with pylint
	pylint --reports=n --rcfile=pylintrc . || true
	@echo
	@echo "----------------------"
	@echo "If you get a 'no module named qgis.core' error, try sourcing"
	@echo "the helper script we have provided first then run make pylint."
	@echo "e.g. source run-env-linux.sh <path to qgis install>; make pylint"
	@echo "----------------------"

.PHONY: pylint
pep8: ## Check the code with pep8
	pep8 --repeat --ignore=E203,E121,E122,E123,E124,E125,E126,E127,E128 --exclude $(PEP8EXCLUDE) . || true

.PHONY: link
link: ## Create symbolic link to this folder in your QGIS plugins folder
link: derase
	ln -s $(shell pwd) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)

.PHONY: unlink
unlink: ## Unlink $(PLUGINNAME) in your QGIS plugins folder
ifneq ("$(wildcard $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME))","")
	rm -RI $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
endif
