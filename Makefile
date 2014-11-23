.PHONY: all
all: results

.PHONY: results
results: data/results

data/results: systemd-survey.csv tools/build
	@mkdir -p data
	tools/build $@


.PHONY: clean
clean:
	-rm -r data

