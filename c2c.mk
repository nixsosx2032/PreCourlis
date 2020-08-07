LOCAL_PLUGINS_PATH = dist
PLUGIN_REPO_PATH = s3://qgis.camptocamp.net/plugins/edf
PLUGIN_REPO_URL = https://qgis.camptocamp.net/plugins/edf
S3_CP_OPTIONS = --cache-control no-cache

include Makefile

.PHONY: upload
upload: ## Deploy plugin on qgis.camptocamp.net
upload: package
	mkdir -p $(LOCAL_PLUGINS_PATH)
	aws --profile qgis.camptocamp.net s3 sync --exact-timestamps --exclude "*" --include "*.txt" $(PLUGIN_REPO_PATH) $(LOCAL_PLUGINS_PATH)/
	unzip -p $(LOCAL_PLUGINS_PATH)/$(PLUGINNAME).zip $(PLUGINNAME)/metadata.txt > $(LOCAL_PLUGINS_PATH)/$(PLUGINNAME).txt
	qgis-plugins.xml $(LOCAL_PLUGINS_PATH)/ $(PLUGIN_REPO_URL)
	aws --profile qgis.camptocamp.net s3 cp $(S3_CP_OPTIONS) $(LOCAL_PLUGINS_PATH)/$(PLUGINNAME).zip $(PLUGIN_REPO_PATH)/
	aws --profile qgis.camptocamp.net s3 cp $(S3_CP_OPTIONS) $(LOCAL_PLUGINS_PATH)/$(PLUGINNAME).txt $(PLUGIN_REPO_PATH)/
	aws --profile qgis.camptocamp.net s3 cp $(S3_CP_OPTIONS) $(LOCAL_PLUGINS_PATH)/plugins.xml $(PLUGIN_REPO_PATH)/
