PIPELINE_NAME=brownfield-land

include makerules/makerules.mk
include makerules/development.mk
include makerules/collection.mk
include makerules/pipeline.mk

init::
	pip install -e .
