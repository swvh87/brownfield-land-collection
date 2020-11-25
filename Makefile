PIPELINE_NAME=brownfield-land

include makerules/makerules.mk
include makerules/development.mk
include makerules/collection.mk
include makerules/pipeline.mk

.PHONY: commit-update commit-resources commit-data

BRANCH := $(shell git rev-parse --abbrev-ref HEAD)

commit-update:
	git add makerules
	git diff --quiet && git diff --staged --quiet || (git commit -m "Commit Make rule updates on $(shell date +%F)"; git push origin $(BRANCH))

commit-resources:
	git add collection
	git diff --quiet && git diff --staged --quiet || (git commit -m "Commit files collected on $(shell date +%F)"; git push origin $(BRANCH))

commit-data:
	git add var/transformed index
	git diff --quiet && git diff --staged --quiet || (git commit -m "Commit Make task outputs on $(shell date +%F)"; git push origin $(BRANCH))
