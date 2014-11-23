.PHONY: all
all: results results.html

.PHONY: results
results: data/results

.PHONY: results.html
results.html: data/results.html

data/results: systemd-survey.csv tools/build
	@mkdir -p data
	tools/build $@

data/results.html: data/results tools/build-html
	tools/build-html $< $@


.PHONY: clean
clean:
	-rm -r data

