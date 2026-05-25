.PHONY: all schema elaborate format validate clean

all: schema elaborate format validate

schema:
	~/learn/ies/venv/bin/python3 ../../../scripts/generate_schema_permissive.py .

elaborate:
	~/learn/ies/venv/bin/python3 ../../../scripts/generate_elaborated_profiles.py examples/
	
format:
	~/learn/ies/venv/bin/python3 ../../../scripts/format_examples.py examples/

validate:
	cd validation && ~/learn/ies/venv/bin/python3 validate_v06.py ../examples

clean:
	rm -f examples/*_Elaborated.json
