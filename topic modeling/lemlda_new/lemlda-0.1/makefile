DOCS_DIR=test/docs
DOCS_PAT=*.txt
OUT=model

TOPICS=100
ITERATIONS=2500
# alpha near 0 -> sparser documents (less topics per document)
# beta near 0 -> sparser topics (less lemmas per topic) [require more topics]
# gamma near 0 -> sparser lemmas (less words per lemma)
ALPHA=0.5
BETA=0.1
GAMMA=0.1

all:
	echo your template files need work

train:
	python/files_to_lemmlda.py ${DOCS_DIR} ${DOCS_PAT} ${OUT}
	java -cp java/trove-2.0.4.jar:java/bin LemmLdaGibbsSampler ${OUT}.dat ${OUT}.lemlex ${OUT} ${TOPICS} ${ITERATIONS} ${ALPHA} ${BETA} ${GAMA}

topics:
	python/show_topics.py ${OUT} > ${OUT}.topics.html

browse:
	python/result_browser.py 8080 ${OUT}
	# now open your browser at http://host:8080/topics/


clean:
	rm -rf ${OUT}.*
