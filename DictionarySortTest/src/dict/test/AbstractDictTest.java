package dict.test;

import java.util.ArrayList;

import dict.model.DictionaryEntry;
import dict.util.IOUtil;
import dict.util.StringUtil;
import junit.framework.TestCase;

public abstract class AbstractDictTest extends TestCase {
	protected String allChars;
	protected String commonChars;
	protected ArrayList<DictionaryEntry> dict;
	protected String getCommonCharFile() {
		return "/home/rob/Documents/dict/project/DictionarySort/data/commonchar";
	}
	protected void setUp() throws Exception {
		String commonCharFile = getCommonCharFile();
		commonChars = IOUtil.loadCommonCharsFromFile(commonCharFile);
		String allDefaultChars = StringUtil.getAllDefaultIgnoreCharsAsString();
		allChars = allDefaultChars + commonChars;
		
		String dictFile = "/home/rob/Documents/dict/project/DictionarySort/data/cedict_ts.u8";
		dict = IOUtil.loadSortedDictionary(dictFile, "UTF8", allChars);
	}

}
