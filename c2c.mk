PLUGIN_REPO_PATH = s3://qgis.camptocamp.net/plugins/edf
PLUGIN_REPO_URL = https://qgis.camptocamp.net/plugins/edf

.PHONY: deploy
deploy: ## Deploy plugin on qgis.camptocamp.net
deploy: .build/dev-requirements.timestamp
deploy: package
	aws --profile qgis.camptocamp.net s3 sync --exclude "*" --include "*.txt" $(PLUGIN_REPO_PATH) .build/plugins/
	cp DPFE.zip .build/plugins/
	cp metadata.txt .build/plugins/DPFE.txt
	.build/venv/bin/qgis-plugins.xml .build/plugins/ $(PLUGIN_REPO_URL)
	aws --profile qgis.camptocamp.net s3 cp .build/plugins/DPFE.zip $(PLUGIN_REPO_PATH)
	aws --profile qgis.camptocamp.net s3 cp .build/plugins/DPFE.txt $(PLUGIN_REPO_PATH)
	aws --profile qgis.camptocamp.net s3 cp .build/plugins/plugins.xml $(PLUGIN_REPO_PATH)
