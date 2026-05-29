# Makefile for India Energy Stack schemas and validations

# Verify python dependencies are available at Makefile parse time
ifeq ($(shell python3 -c "import yaml, jsonschema" >/dev/null 2>&1 && echo ok || echo error),error)
  $(error Error: Required Python packages (PyYAML, jsonschema) are missing. Please activate your virtual environment or install them: pip install pyyaml jsonschema)
endif

.PHONY: all clean build validate index test

test:
	@echo "Running MeterData v0.6 validator tests..."
	@$(MAKE) -C schemas/MeterData/v0.6/validation test
	@echo "Running MeterDataRequest v0.6 validator tests..."
	@$(MAKE) -C schemas/MeterDataRequest/v0.6/validation test

# Find all directories under schemas/ that contain attributes.yaml, excluding ElectricityCredential
ALL_SCHEMA_DIRS := $(dir $(shell find schemas -name attributes.yaml))
SCHEMA_DIRS := $(filter-out schemas/ElectricityCredential/%,$(ALL_SCHEMA_DIRS))

# Compiled outputs for each schema directory
COMPILED_SCHEMAS := $(foreach dir,$(SCHEMA_DIRS),$(dir)schema.json $(dir)context.jsonld $(dir)vocab.jsonld)

# Validation stamps (we write a hidden stamp file to track validation status)
VALIDATION_STAMPS := $(foreach dir,$(SCHEMA_DIRS),$(dir).validate_stamp)

# Default target builds and validates everything
all: build validate index

# Build target compiles all schemas whose attributes.yaml has changed
build: $(COMPILED_SCHEMAS)

# Validate target runs validation only if schema.json or examples changed
validate: $(VALIDATION_STAMPS)

# Generic rule to compile schema files from attributes.yaml
%/schema.json %/context.jsonld %/vocab.jsonld: %/attributes.yaml
	@echo "Compiling schema in $*..."
	@python3 scripts/generate_schema_permissive.py $*

# Enable secondary expansion to match wildcard files under examples/ dynamically
.SECONDEXPANSION:
%/.validate_stamp: %/schema.json $$(wildcard %/examples/*.json)
	@if [ -d $*/examples ]; then \
		echo "Validating examples in $*..."; \
		python3 scripts/validate_schema.py $*/schema.json $*/examples || exit 1; \
	fi
	@touch $@

index:
	@echo "Generating collapsible index.md..."
	@python3 scripts/generate_index.py

# Clean up compiled assets and validation stamps
clean:
	rm -f $(COMPILED_SCHEMAS) $(VALIDATION_STAMPS)

