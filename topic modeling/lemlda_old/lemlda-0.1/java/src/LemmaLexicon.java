interface LemmaLexicon {

   /**
    * Number of tokens in the lexicon (including prefixated items).
    * (may be data-driven -- just tokens seen in text)
    */
   int countTokens(); 

   /**
    * Number of lemmas in the lexicon.
    * (may be data-driven -- only lemmas possible in text)
    */
   int countLemmas();

   /**
    * A list of possible lemmas for the word wi, according to lexicon
    */
   int[] possibleLemmasForWord(int wi);

   /**
    * Number of words (may not be seen in text!) that can be generated from this lemma
    */
   int numWordsForLemma(int li);

}
