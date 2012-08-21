package dict.util;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.TreeSet;

import dict.model.MaxDifficultyModel;

public class ExampleUtil {
	
	public static Comparator<String> getExampleComparator(String charsInOrder) {
		final String s = charsInOrder;
		final HashMap<String, Integer> tmp = new HashMap<String, Integer>();
		Comparator<String> c = new Comparator<String>(){
			public int compare(String o1, String o2) {
				if( tmp.get(o1) == null )
					tmp.put(o1, new Integer(MaxDifficultyModel.getMaxDifficulty(o1, s)));
				if( tmp.get(o2) == null )
					tmp.put(o2, new Integer(MaxDifficultyModel.getMaxDifficulty(o2, s)));
				int o1v = tmp.get(o1).intValue();
				int o2v = tmp.get(o2).intValue();
				return o1v-o2v;
			}
		};
		return c;
	}

	public static Collection<String> loadSingleLineExamplesFromFile(String acceptedChars, String filename) {
		return loadSingleLineExamplesFromFile(acceptedChars, filename, "UTF8");
	}
	
	public static Collection<String> loadSingleLineExamplesFromFile(String acceptedChars, String filename, String encoding) {
		return loadSingleLineExamplesFromFile(acceptedChars, filename, encoding, false, null);
	}

	public static Collection<String> loadSingleLineExamplesFromFile(String acceptedChars, String filename, String encoding, boolean includeFragments) {
		return loadSingleLineExamplesFromFile(acceptedChars, filename, encoding, includeFragments, null);
	}

	public static Collection<String> loadSingleLineExamplesFromFile(String acceptedChars, String filename, String encoding, 
			boolean includeFragments, IExampleAdditionVerifier verifier) {
		TreeSet<String> examples = new TreeSet<String>();
		try { 
			BufferedReader in = new BufferedReader( 
					new InputStreamReader(new FileInputStream(filename), encoding)); 
			String str = in.readLine();
			while(str != null ) {
				if( verifier.shouldAddExample(str, false)) 
					examples.add(str.trim());
				str = in.readLine();
			}
		} catch (UnsupportedEncodingException e) { 
		} catch (IOException e) { 
		} 
		return examples;
	}

	
    public static String[] getSentenceFragments(String str, int maxDifficulty, String charList) {
    	Collection<String> exampleList = new ArrayList<String>();
    	// If we got numbers, we don't want to split a 20,000 or something
    	for( int k = 0; k < 10; k++ ) {
    		if( str.contains("" + k))
    			return new String[0]; // Skip this one
    	}
    	// Now lets split on punctuation
    	String str2 = "" + StringUtil.replacePunc(str, ",");
    	String noPunc = "" + StringUtil.replacePunc(str, "");
    	if( !str2.equals(str)) { // Punctuation found
    		String[] split = str2.split(",");
    		if( split.length == 1 || (split.length > 1 && split[0].equals(str)))
    				return new String[0];
    		
    		for( int j = 0; j < split.length; j++ ) {
    			int tmpMax = MaxDifficultyModel.getMaxDifficulty(split[j], charList);
    			if( !"".equals(split[j]) && !noPunc.equals(split[j]) && tmpMax != maxDifficulty ) //&& shouldAddExample(split[j]))
    				exampleList.add(split[j].trim());
    		}
    	}
    	return exampleList.toArray(new String[exampleList.size()]);
    }
    
	public static Collection<String> loadMultiLineExamples(String filename, String usable) {
		return loadMultiLineExamples(filename, usable, "UTF8");
	}

	public static Collection<String> loadMultiLineExamples(String filename, String usable, boolean includeFragments) {
		return loadMultiLineExamples(filename, usable, "UTF8", includeFragments);
	}
	public static Collection<String> loadMultiLineExamples(String filename, String usable, boolean includeFragments, IExampleAdditionVerifier verifier) {
		return loadMultiLineExamples(filename, usable, "UTF8", includeFragments, verifier);
	}

	public static Collection<String> loadMultiLineExamples(String filename, String usable, String encoding) {
		return loadMultiLineExamples(filename, usable, encoding, false);
	}
	public static Collection<String> loadMultiLineExamples(String filename, String usable, String encoding, boolean includeFragments) {
		IExampleAdditionVerifier defaultVerifier = new IExampleAdditionVerifier() {
			public boolean shouldAddExample(String string, boolean fragment) {
				return string.length() > 4;
			}
		};
		return loadMultiLineExamples(filename, usable, encoding, includeFragments, defaultVerifier);
	}
	public static Collection<String> loadMultiLineExamples(String filename, String usable, String encoding, boolean includeFragments, IExampleAdditionVerifier verifier) {
		TreeSet<String> exampleList = new TreeSet<String>();
		loadMultiLineExamples(filename, usable, encoding, includeFragments, verifier, exampleList);
		return exampleList;
	}
	
	public static void loadMultiLineExamples(String filename, String usable, 
			String encoding, boolean includeFragments, IExampleAdditionVerifier verifier, 
			Collection<String> collection) {
		try { 
			BufferedReader in = new BufferedReader( 
					new InputStreamReader(new FileInputStream(filename), encoding)); 
			String str = in.readLine();
			while(str != null ) {
				int terminationIndex = StringUtil.getTerminatedIndex(str);
				if( terminationIndex == -1 /*!terminates*/ ) {
					String tmp2 = in.readLine();
					while(tmp2 != null && terminationIndex == -1) {
						str += tmp2;
						tmp2 = in.readLine();
						terminationIndex = StringUtil.getTerminatedIndex(str+tmp2);
					}
					str += tmp2;
				}
				
				// str now ends with a termination, but MAY have several sentences in it. Such as:
				// I love myself. Julie is cool, but I love myself more. Life is cool when
				String[] sentences = StringUtil.explodeIntoTerminatedSentences(str);
				for( int k = 0; k < sentences.length -1; k++ ) {
					if( (k != sentences.length -1) || StringUtil.terminatesSentence(sentences[k])) { 
						// Handle terminated sentences
						int maxDif = MaxDifficultyModel.getMaxDifficulty(sentences[k], usable);
						if( verifier.shouldAddExample(sentences[k], false)) {
							collection.add(sentences[k]);
							if( includeFragments ) {
								String[] fragments = getSentenceFragments(sentences[k], maxDif, usable);
								for( int j = 0; j < fragments.length; j++ ) {
									if(verifier.shouldAddExample(fragments[j], true)){
										collection.add(fragments[j]);
									}
								}
							}
						}
					}
				}
				
				str = in.readLine();
				if( str == null ) 
					continue;
				if( !StringUtil.terminatesSentence(sentences[sentences.length -1])) 
					str = sentences[sentences.length-1] + str;
			}
		} catch (UnsupportedEncodingException e) { 
		} catch (IOException e) { 
		} 
	}

//	protected static boolean approveFragment(String fragment, String usable) {
//		int fragmentDif = MaxDifficultyModel.getMaxDifficulty(fragment, usable);
//		if( fragmentDif <= StringUtil.getAllDefaultIgnoreChars().get(index))
//		return fragment.length() > 4;
//	}
	
    public static interface IExampleAdditionVerifier {
    	public boolean shouldAddExample(String string, boolean fragment);
    }
    
	public static Collection<String> loadExamplesAndFragments(String allChars, String filename, 
			IExampleAdditionVerifier verifier ) {
		return loadExamplesAndFragments(allChars, filename, "UTF8", verifier);
	}

	public static Collection<String> loadExamplesAndFragments(String allChars, String filename, 
			String encoding, IExampleAdditionVerifier verifier ) {
		TreeSet<String> ts = new TreeSet<String>();
		loadExamplesAndFragments(allChars, filename, encoding, verifier, ts);
		return ts;
	}
	
	public static Collection<String> loadExamplesAndFragments(String allChars, String[] filename, 
			IExampleAdditionVerifier verifier ) {
		TreeSet<String> ts = new TreeSet<String>();
		for( int i = 0; i < filename.length; i++ ) {
			loadExamplesAndFragments(allChars, filename[i], "UTF8", verifier, ts);
		}
		return ts;
	}

	public static Collection<String> loadExamplesAndFragments(String allChars, 
			String[] filename, String[] encodings, 
			IExampleAdditionVerifier verifier ) {
		TreeSet<String> ts = new TreeSet<String>();
		for( int i = 0; i < filename.length; i++ ) {
			loadExamplesAndFragments(allChars, filename[i], encodings[i], verifier, ts);
		}
		return ts;
	}

	public static void loadExamplesAndFragments(
			String allChars, String filename, 
			IExampleAdditionVerifier verifier, Collection<String> exampleList) {
		loadExamplesAndFragments(allChars, filename, "UTF8", verifier, exampleList);
	}
	public static void loadExamplesAndFragments(
			String allChars, String filename, String encoding, 
			IExampleAdditionVerifier verifier, Collection<String> exampleList) {
		Collection<String> examples = ExampleUtil.loadSingleLineExamplesFromFile(allChars, filename, encoding);
		exampleList.addAll(examples);
		Iterator<String> i = examples.iterator();
		String next;
		while(i.hasNext()) {
			// Iterate through new examples found
			next = i.next();
			String[] fragments = ExampleUtil.getSentenceFragments(next, MaxDifficultyModel.getMaxDifficulty(next, allChars), allChars);
			for( int j = 0; j < fragments.length; j++ ) {
				if( verifier == null || verifier.shouldAddExample(fragments[j], true))
					exampleList.add(fragments[j]);
			}
		}
	}
}
