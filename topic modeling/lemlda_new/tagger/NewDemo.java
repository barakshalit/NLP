import java.util.List;
import java.util.Set;
import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;

import hebrewNER.NERTagger;
import vohmm.application.SimpleTagger3;
import vohmm.corpus.AnalProb;
import vohmm.corpus.Anal;
import vohmm.corpus.Corpus;
import vohmm.corpus.Sentence;
import vohmm.corpus.Sentence.OutputData;
import vohmm.corpus.Token;
import vohmm.corpus.TokenExt;
import vohmm.corpus.Tag;
import vohmm.corpus.AffixInterface;
import vohmm.corpus.UnknownResolver;
import vohmm.corpus.AnalysisInterface;
import vohmm.corpus.BitmaskResolver;
import yg.chunker.TaggerBasedHebrewChunker;
import yg.sentence.MeniTaggeedSentenceFactory;
import yg.sentence.MeniTokenExpander;


public class NewDemo {
	
	public static void main(String[] args) {
		
		if (args.length != 3) {
			System.out.println("Usage: java -Xmx1G -XX:MaxPermSize=256m -cp trove-2.0.2.jar:morphAnalyzer.jar:opennlp.jar:gnu.jar:chunker.jar:splitsvm.jar:duck1.jar:tagger.jar NewDemo <tagger data directory> <in text file> <out>");
			System.exit(0);
		}
		try {
			// The follwoing object constructions are heavy - SHOULD BE APPLIED ONLY ONCE!
			// create the morphological analyzer and disambiguator 
			SimpleTagger3 tagger = new SimpleTagger3(args[0]);
			// create the named-entity recognizer
			NERTagger nerTagger = new NERTagger(args[0],tagger);
			// create the noun-phrase chunker
			MeniTaggeedSentenceFactory sentenceFactory = new MeniTaggeedSentenceFactory(null, MeniTokenExpander.expander);
	        String chunkModelPrefix = args[0] + vohmm.util.Dir.CHUNK_MODEL_PREF;
			TaggerBasedHebrewChunker chunker = new TaggerBasedHebrewChunker(sentenceFactory, chunkModelPrefix);


			// The tagger gets an InputStream, i.e. both given string and text file of UTF-8 encoding is supported.
			// create input and output streams
			// Output stream
			PrintStream out = new PrintStream(new FileOutputStream(args[2]),false,"UTF-8");
			
			// Input stream
			
			// For string
			InputStream in = new ByteArrayInputStream(new String("הרכבת הממשלה").getBytes("UTF-8"));
			List<Sentence> taggedSentences = tagger.getTaggedSentences(in);
			// print tagged sentence
			// by applying toString method of Senetence class with OutputData.TAGGED mode
			for (Sentence sentence : taggedSentences) 
				out.println(sentence.toString(OutputData.TAGGED));

			// For text file (UTF-8)
			in = new FileInputStream(args[1]);			
			taggedSentences = tagger.getTaggedSentences(in);
			for (Sentence sentence : taggedSentences) {
			
				// Named-entiry recognition for the given tagged sentence
				nerTagger.addNerLabels(sentence);

				//Noun-phrase chunking for the given tagged sentence (will be available soon in Java)
				chunker.addBIOLabels(sentence);
			
				// print tagged sentence by using AnalysisInterface, as follows:
				for (TokenExt tokenExt : sentence.getTokens()) {
					Token token = tokenExt._token;
					out.println(token.getOrigStr());
					Anal anal =  token.getSelectedAnal();
					out.println("\tLemma: " + anal.getLemma());

					// NOTE: In our tagger we consider participle of a 'verb' type as a present verb.
					// In order to adapt it to MILA's schema the last parameter of BitmaskResolver constructor should be 'false' (no present verb)
					AnalysisInterface bitmaskResolver = new BitmaskResolver(anal.getTag().getBitmask(),token.getOrigStr(),false);
					out.println("\tPOS: " + bitmaskResolver.getPOS());
					out.println("\tPOS type: " + bitmaskResolver.getPOSType()); // the type of participle is "noun/adjective" or "verb"
					out.println("\tGender: " + bitmaskResolver.getGender());
					out.println("\tNumber: " + bitmaskResolver.getNumber());
					out.println("\tPerson: " + bitmaskResolver.getPerson());
					out.println("\tStatus: " + bitmaskResolver.getStatus());
					out.println("\tTense: " + bitmaskResolver.getTense());
					out.println("\tPolarity: " + bitmaskResolver.getPolarity());
					out.println("\tDefiniteness: " + bitmaskResolver.isDefinite());
					if (bitmaskResolver.hasPrefix()) {
						out.print("\tPrefixes: ");
						List<AffixInterface> prefixes = bitmaskResolver.getPrefixes();
						for (AffixInterface prefix : prefixes)
							out.print(prefix.getStr() + " " + Tag.toString(prefix.getBitmask(),true) + " ");
						out.print("\n");
					} else
						out.println("\tPrefixes: None");
					if (bitmaskResolver.hasSuffix()) {
						out.println("\tSuffix Function: " + bitmaskResolver.getSuffixFunction());
						out.println("\tSuffix Gender: " + bitmaskResolver.getSuffixGender());
						out.println("\tSuffix Number: " + bitmaskResolver.getSuffixNumber());
						out.println("\tSuffix Person: " + bitmaskResolver.getSuffixPerson());
					} else 
						out.println("\tSuffix: None");		
				
				    // print token NER and Chunk properties	
					out.println("\tNER: " + tokenExt.getNER());			
					out.println("\tChunk: " + tokenExt.getChunk());			
				}
				
				out.println("\n\n----------------------------------------------------------------------\n");
			} 
		} catch (Exception e) {
			e.printStackTrace(); 
			System.exit(0);
		}
	}    
}
