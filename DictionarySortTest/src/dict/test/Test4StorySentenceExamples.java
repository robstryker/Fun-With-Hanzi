package dict.test;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.TreeSet;

import dict.model.MaxDifficultyModel;
import dict.util.ExampleUtil;
import dict.util.ExampleUtil.IExampleAdditionVerifier;
import dict.util.StringUtil;

public class Test4StorySentenceExamples extends AbstractDictTest implements IExampleAdditionVerifier {
	protected void setUp() throws Exception {
		super.setUp();
	}
	protected String getCommonCharFile() {
		return super.getCommonCharFile();
		//return "/home/rob/Documents/dict/project/DictionarySort/data/commonchar_hp";
	}

	
	public void testStoryExamples() {
		harryPotterInOrder();
	}
	
	protected void severalStuff() {
		String hpFile = "/home/rob/Documents/dict/project/DictionarySort/data/examples/hpexamples.txt";
		String ncikuFile = "/home/rob/Documents/dict/project/DictionarySort/data/examples/ALL_OUT_CN";
		String customFile = "/home/rob/Documents/dict/project/DictionarySort/data/examples/ALL_OUT_CN";
		
		// As a set
		Collection<String> hpExamples = ExampleUtil.loadMultiLineExamples(hpFile, this.allChars, "UTF8", true, this);
		Collection<String> ncikuExamples = ExampleUtil.loadSingleLineExamplesFromFile(allChars, ncikuFile, "UTF8", true, this);
		Collection<String> customExamples = ExampleUtil.loadSingleLineExamplesFromFile(allChars, customFile, "UTF8", true, this);
		System.out.println(hpExamples.size());
		System.out.println(ncikuExamples.size());
		TreeSet<String> set = new TreeSet<String>();
		set.addAll(hpExamples);
		set.addAll(ncikuExamples);
		set.addAll(customExamples);
//		System.out.println(set.size());
//		sortAndPrint(set);
		sortAndPrintIgnoredChars();
	}
	
	protected void sortAndPrint(Collection<String> c) {
		ArrayList<String> list = new ArrayList<String>();
		list.addAll(c);
		Collections.sort(list, ExampleUtil.getExampleComparator(allChars));

//		for( int i = 0; i < 1000; i++ ) {
//			System.out.println("(" + MaxDifficultyModel.getMaxDifficulty(list.get(i), allChars)+ ")   - " + list.get(i));
//		}

	}
	
	protected void harryPotterInOrder() {
		String hpFile = "/home/rob/Documents/dict/project/DictionarySort/data/examples/hpexamples.txt";
		ArrayList<String> hpExamples = new ArrayList<String>();
		ExampleUtil.loadMultiLineExamples(hpFile, this.allChars, "UTF8", true, this, hpExamples);
		TreeSet<String> ts = new TreeSet<String>();
		ts.addAll(hpExamples);
		sortAndPrint(ts);
	}

	
	private TreeSet<String> alreadySeen = new TreeSet<String>();
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
	
	private ArrayList<String> ignoredSentences = new ArrayList<String>();
	private HashMap<String, MissingEntry> missingMap =  new HashMap<String, MissingEntry>();
	private class MissingEntry {
		protected String charact;
		protected int count;
		public MissingEntry(String c) {
			this.count = 0;
			this.charact = c;
		}
	}
	
	private void handleMissingCharSentence(String string) {
		ignoredSentences.add(string);
		String[] missing = StringUtil.findUnknownChars(string, allChars);
		for( int i = 0; i < missing.length; i++ ) {
			MissingEntry entry = missingMap.get(missing[i]);
			if( entry == null ) {
				missingMap.put(missing[i], new MissingEntry(missing[i]));
				entry = missingMap.get(missing[i]);
			}
			entry.count++;
		}
	}
	
	protected void sortAndPrintIgnoredChars() {
		
	}
}
