.PHONY: all schema validate clean

all: schema validate

schema:
	python3 ../../../scripts/generate_schema_permissive.py $(CURDIR)

validate:
	python3 ../../../scripts/validate_schema.py $(CURDIR)/schema.json $(CURDIR)/examples

clean:
	rm -f schema.json context.jsonld vocab.jsonld
