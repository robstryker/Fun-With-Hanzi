package dict.test;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;

import dict.main.FullRunAllBooksWithFragments;
import dict.util.ExampleUtil;
import dict.util.ExampleUtil.IExampleAdditionVerifier;
import dict.util.StringUtil;

public class Test5CommonCharsGeneration extends AbstractDictTest implements IExampleAdditionVerifier {

	protected String getCommonCharFile() {
		return "/home/rob/Documents/dict/project/DictionarySort/data/commonchar_hp";
	}

	private HashMap<String, CharEntry> charMap =  new HashMap<String, CharEntry>();
	private class CharEntry {
		protected String charact;
		protected int count;
		protected boolean missing;
		public CharEntry(String c, boolean missing) {
			this.count = 0;
			this.charact = c;
			this.missing = missing;
		}
	}

	protected String hpFile = "/home/rob/Documents/dict/project/DictionarySort/data/examples/hpexamples.txt";
	protected String ncikuFile = "/home/rob/Documents/dict/project/DictionarySort/data/examples/ALL_OUT_CN";
	protected String customFile = "/home/rob/Documents/dict/project/DictionarySort/data/examples/CUSTOM_EXAMPLES";
	
	public void testGenerateCommonChars() {
		int commonCountReserve = 300;
		String seen = StringUtil.getAllDefaultIgnoreCharsAsString();
		
		generateStats();
		ArrayList<CharEntry> entries = getSortedCharMap();
		
		String asString;
		boolean includeCount = true;
		Iterator<CharEntry> i = entries.iterator();
		CharEntry e = null;
		int count2 = 0;
		int min = 100;
		
		StringBuffer buf = new StringBuffer();
		while(i.hasNext() && (e == null || e.count > min)) {
			e = i.next();
			if( !seen.contains(e.charact) ) {
				buf.append(e.charact);
				count2++;
				asString = e.charact + (includeCount ? " : " + e.count : "");
				System.out.println(asString);
			}
		}
		System.out.println(entries.size() + " total characters, " + count2 + " greater than " + min);
		
		// Run the full test with this new common chars
		String newCommon = buf.toString();
		FullRunAllBooksWithFragments main = new FullRunAllBooksWithFragments();
		main.setCommonChars(newCommon);
		main.run();
	}

	protected void generateStats() {
		// As a set
		ExampleUtil.loadMultiLineExamples(hpFile, allChars, "UTF8", false, this);
		ExampleUtil.loadSingleLineExamplesFromFile(allChars, ncikuFile, "UTF8", false, this);
		ExampleUtil.loadSingleLineExamplesFromFile(allChars, customFile, "UTF8", false, this);
	}
	protected ArrayList<CharEntry> getSortedCharMap() {
		// Sort 
		ArrayList<CharEntry> entries = new ArrayList<CharEntry>();
		entries.addAll(charMap.values());
		Collections.sort(entries, new Comparator<CharEntry>() {
			public int compare(CharEntry o1, CharEntry o2) {
				return o2.count - o1.count;
			}
		});
		return entries;
	}
	
	public boolean shouldAddExample(String string, boolean fragment) {
		for( int i = 0; i < string.length(); i++ ) {
			getEntry(string.charAt(i)).count++;
		}
		return false;
	}
	protected CharEntry getEntry(char c) {
		String s = Character.toString(c);
		if( charMap.get(s) != null )
			return charMap.get(s);
		boolean missing = allChars.indexOf(c) == -1;
		CharEntry entry = new CharEntry(s, missing);
		charMap.put(s, entry);
		return entry;
	}
}
