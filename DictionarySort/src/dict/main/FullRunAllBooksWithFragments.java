package dict.main;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.TreeSet;

import dict.model.DictionaryEntry;
import dict.model.MaxDifficultyModel;
import dict.util.ExampleUtil;
import dict.util.ExampleUtil.IExampleAdditionVerifier;
import dict.util.IOUtil;
import dict.util.StringUtil;

public class FullRunAllBooksWithFragments implements IExampleAdditionVerifier {
	public static void main(String[] args) {
		new FullRunAllBooksWithFragments().run();
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
			String commonCharFile = "/home/rob/Documents/dict/project/DictionarySort/data/commonchar_ALL";
			commonChars = IOUtil.loadCommonCharsFromFile(commonCharFile);
		}
		String allDefaultChars = StringUtil.getAllDefaultIgnoreCharsAsString();
		
		allChars = allDefaultChars + commonChars;
		
		String dictFile = "/home/rob/Documents/dict/project/DictionarySort/data/cedict_ts.u8";
		dict = IOUtil.loadSortedDictionary(dictFile, "UTF8", allChars);
		
		examples = loadSortedExamples();
		
		IOUtil.getOut().start();
		for( int i = 0; i < commonChars.length()-1; i++ ) {
			runHanziOutput(i);
		}
		IOUtil.getOut().end();
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
			e = dict.get(lastDictEntry);
			if( getDifficulty(e.modern) <= hanziDif ) {
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
		String hpFile = "/home/rob/Documents/dict/project/DictionarySort/data/examples/hpexamples.txt";
		String ncikuFile = "/home/rob/Documents/dict/project/DictionarySort/data/examples/ALL_OUT_CN";
		String customFile = "/home/rob/Documents/dict/project/DictionarySort/data/examples/CUSTOM_EXAMPLES";

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
		System.out.println("ERROR: " + s);
	}
}
