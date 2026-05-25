.PHONY: all schema elaborate format validate clean

all: schema elaborate format validate

schema:
	python3 ../../../scripts/generate_schema_permissive.py .

elaborate:
	python3 ../../../scripts/generate_elaborated_profiles.py examples/
	
format:
	python3 ../../../scripts/format_examples.py examples/

validate:
	cd validation && python3 validate_v06.py ../examples
	python3 ../../../scripts/validate_links.py

clean:
	rm -f examples/*_Elaborated.json
