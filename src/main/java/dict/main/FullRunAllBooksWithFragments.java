package dict.main;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeSet;

import dict.model.DictionaryEntry;
import dict.model.MaxDifficultyModel;
import dict.util.ExampleUtil;
import dict.util.ExampleUtil.IExampleAdditionVerifier;
import dict.util.IOUtil;
import dict.util.StringUtil;

public class FullRunAllBooksWithFragments implements IExampleAdditionVerifier {
	/**
	 * Usage: FullRunAllBooksWithFragments [--sql] [orderFile]
	 * Writes XML (default) or SQL to stdout. orderFile defaults to data/commonchar.
	 */
	public static void main(String[] args) {
		String orderFile = "data/commonchar";
		for( String arg : args ) {
			if( arg.equals("--sql"))
				IOUtil.setOut(IOUtil.getSQLOut());
			else
				orderFile = arg;
		}
		FullRunAllBooksWithFragments runner = new FullRunAllBooksWithFragments();
		runner.setCommonChars(IOUtil.loadCommonCharsFromFile(orderFile));
		runner.run();
	}
	
	protected String allChars;
	protected String commonChars;
	protected ArrayList<DictionaryEntry> dict;
	private TreeSet<String> alreadySeen = new TreeSet<String>();
	private ArrayList<String> examples;
	public FullRunAllBooksWithFragments() {
	}
	public void setCommonChars(String c) {
		this.commonChars = c;
	}
	
	public void run() {
		if( commonChars == null ) {
			String commonCharFile = "data/commonchar_ALL";
			commonChars = IOUtil.loadCommonCharsFromFile(commonCharFile);
		}
		String allDefaultChars = StringUtil.getAllDefaultIgnoreCharsAsString();
		
		allChars = allDefaultChars + commonChars;
		
		String dictFile = "data/cedict_ts.u8";
		dict = IOUtil.loadSortedDictionary(dictFile, "UTF8", allChars);
		
		examples = loadSortedExamples();
		
		IOUtil.getOut().start();
		IOUtil.getOut().printKnown(knownEntries());
		for( int i = 0; i < commonChars.length(); i++ ) {
			runHanziOutput(i);
		}
		IOUtil.getOut().end();
	}
	
	/** Dictionary entries for the free mood particles (StringUtil's zero-difficulty chars). */
	protected Map<Character, List<DictionaryEntry>> knownEntries() {
		Map<Character, List<DictionaryEntry>> known = new LinkedHashMap<Character, List<DictionaryEntry>>();
		for( String s : StringUtil.getDefaultZeroDifficultyChineseChars()) {
			List<DictionaryEntry> entries = new ArrayList<DictionaryEntry>();
			for( DictionaryEntry e : dict ) {
				if( e.modern.equals(s))
					entries.add(e);
			}
			known.put(s.charAt(0), entries);
		}
		return known;
	}

	int lastDictEntry = 0;
	int lastExample = 0;
	
	protected void runHanziOutput(int index) {
		char hanzi = commonChars.charAt(index);
		IOUtil.getOut().startHanzi(index, hanzi);
		if( shouldPrintWords())
			printWords(index);
		if( shouldPrintSentences()) 
			printSentences(index);
		IOUtil.getOut().endHanzi(index, hanzi);
	}
	
	protected boolean shouldPrintWords() {
		return true;
	}
	
	protected boolean shouldPrintSentences() {
		return true;
	}
	
	protected void printWords(int index) {
		char hanzi = commonChars.charAt(index);
		int hanziDif = getDifficulty(hanzi);
		boolean done = false;
		DictionaryEntry e;
		
		// Print dict entries
		while( !done ) {
			if( dict.size() <= lastDictEntry) {
				done = true;
				continue;
			}
			e = dict.get(lastDictEntry);
			int dif = getDifficulty(e.modern);
			// unknown-character entries sort last; never print them
			if( dif != MaxDifficultyModel.NOT_FOUND_CHAR && dif <= hanziDif ) {
				lastDictEntry++;
				IOUtil.getOut().printDefinition(index, e);
			} else {
				done = true;
			}
		}
	}
	
	protected void printSentences(int index) {
		char hanzi = commonChars.charAt(index);
		int hanziDif = getDifficulty(hanzi);
		// print the examples
		boolean done = false;
		String example;
		while( !done ) {
			if( examples.size() <= lastExample) {
				done = true;
				continue;
			}
			example = examples.get(lastExample);
			if( getDifficulty(example) <= hanziDif ) {
				IOUtil.getOut().printSentence(index, hanzi, example);
				lastExample++;
			} else {
				done = true;
			}
		}
	}
	
	protected int getDifficulty(char hanzi) {
		return getDifficulty(Character.toString(hanzi));
	}
	protected int getDifficulty(String string) {
		return MaxDifficultyModel.getMaxDifficulty(string, allChars);
	}
	
	protected ArrayList<String> loadSortedExamples() {
		// As a set
		String hpFile = "data/examples/hpexamples.txt";
		String ncikuFile = "data/examples/ALL_OUT_CN";
		String customFile = "data/examples/CUSTOM_EXAMPLES";

		Collection<String> hpExamples = ExampleUtil.loadMultiLineExamples(hpFile, this.allChars, "UTF8", true, this);
		Collection<String> ncikuExamples = ExampleUtil.loadSingleLineExamplesFromFile(allChars, ncikuFile, "UTF8", true, this);
		Collection<String> customExamples = ExampleUtil.loadSingleLineExamplesFromFile(allChars, customFile, "UTF8", true, this);
		TreeSet<String> set = new TreeSet<String>();
		set.addAll(hpExamples);
		set.addAll(ncikuExamples);
		set.addAll(customExamples);
		ArrayList<String> list = new ArrayList<String>();
		list.addAll(set);
		Collections.sort(list, ExampleUtil.getExampleComparator(allChars));
		return list;
	}

	public boolean shouldAddExample(String string, boolean fragment) {
		String noPunc = StringUtil.replacePunc(string, "");
		if( alreadySeen.contains(noPunc))
			return false;
		
		int fragDif = MaxDifficultyModel.getMaxDifficulty(string, allChars);
		if( fragDif == MaxDifficultyModel.NOT_FOUND_CHAR) {
			handleMissingCharSentence(string);
			return false;
		}

		int shiDif = MaxDifficultyModel.getMaxDifficulty("" + commonChars.charAt(0), allChars);
		boolean shouldAdd = string.length() > 4 && ( fragDif > shiDif ); 
		if( shouldAdd )
			alreadySeen.add(noPunc);
		return shouldAdd;
	}
	
	private void handleMissingCharSentence(String s) {
		System.err.println("ERROR: " + s);
	}
}
