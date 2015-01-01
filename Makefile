.PHONY: all
all: results results.html correlations-ordered correlations-sorted

.PHONY: results
results: data/results

.PHONY: results.html
results.html: data/results.html

.PHONY: correlations-ordered
correlations-ordered: data/correlations-ordered.html

.PHONY: correlations-sorted
correlations-sorted: data/correlations-sorted.html

data/results: systemd-survey.csv tools/build
	@mkdir -p data
	tools/build $@

data/results.html: data/results tools/build-html
	tools/build-html $< $@

data/correlations-ordered.html: correlations.csv tools/build-correlations
	tools/build-correlations --html --ordered > $@

data/correlations-sorted.html: correlations.csv tools/build-correlations
	tools/build-correlations --html > $@


.PHONY: clean
clean:
	-rm -r data

