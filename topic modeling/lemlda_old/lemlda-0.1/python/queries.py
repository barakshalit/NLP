from res_reader import *



class TopicsFromWord:
   def __init__(self, ldamodel):
      self.m = ldamodel

   def query(self, w):
      return probed_topics_for_word(self.m, w)

class TopicsFromWordMarginalizeLemma:
   def __init__(self, ldamodel):
      self.m = ldamodel
   
   def query(self, w):
      return probed_topics_for_word_l(self.m, w)

def probed_topics_for_word_l(model, word):
   """
   return a list of (topic,prob) pairs, sorted by prob.
   prob = sum_l p(w|l)p(l|t)
   """
   m=model
   topics = defaultdict(float)
   for l in m.lemmas_for_word(word):
      for t in m.topics_for_lemma(l):
         topics[t]+=m.p_wGl(word,l)*m.p_lGt(l,t)
   return sorted(list(topics.items()), key=lambda t_p:-t_p[1])

def probed_topics_for_word(model, word):
   """
   return a list of (topic,prob) pairs, sorted by prob.
   prob = sum_l p(w|t)
   """
   m=model
   topics = defaultdict(float)
   for t in m.topics_for_word(word):
      topics[t]=m.p_wGt(word,t)
   return sorted(list(topics.items()), key=lambda t_p1:-t_p1[1])

class MultiwordToDocs:
   def __init__(self, wordToTopics):
      self.wtquery = wordToTopics

   def query(self, words):
      topics = [self.wtquery.query(w) for w in words]
      m = self.wtquery.m

      doc_scores = defaultdict(float)

      # docs with at least one topic from each word
      relevant_docs=[]
      for tp in topics:
         docs = set()
         for topic,prob in tp[:4]:
            docs.update([d for d in m.docs_for_topic(topic) if m.p_dGt(d,topic) > 0.005]) # @@@
         relevant_docs.append(docs)
      docs = relevant_docs[0]
      print("before intersection:",len(docs))
      for d in relevant_docs[1:]: docs = docs.intersection(d)
      relevant_docs = docs
      print("relevant_docs_len:",len(relevant_docs))

      # first word topics
      for topic, tprob in topics[0]:
         docs = m.docs_for_topic(topic)
         for doc in docs:
            if doc not in relevant_docs: continue
            dprob = m.p_dGt(doc, topic)
            doc_scores[doc]= dprob*tprob

      # other words topics
      for tp in topics[1:]:
         for topic,tprob in tp:
            docs = m.docs_for_topic(topic)
            for doc in docs:
               if doc not in relevant_docs: continue
               dprob = m.p_dGt(doc, topic)
               doc_scores[doc]+= dprob*tprob

      doc_scores = [(doc,prob) for doc,prob in list(doc_scores.items()) if prob>0]
      return sorted(doc_scores, key=lambda d_p:-d_p[1])


if __name__ == '__main__':
   m=LemmaModel.load("rambam-tdl")
   t=TopicsFromWordMarginalizeLemma(m)
   t.query('whatever...')
