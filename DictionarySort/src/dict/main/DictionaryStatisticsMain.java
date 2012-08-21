package dict.main;

import java.util.ArrayList;

import dict.model.DictionaryEntry;
import dict.model.MaxDifficultyModel;
import dict.util.IOUtil;
import dict.util.StringUtil;

public class DictionaryStatisticsMain {

	public static void main(String[] args) {
		new DictionaryStatisticsMain().run();
	}
	protected String allChars;
	protected String commonChars;
	protected ArrayList<DictionaryEntry> dict;
	public void run() {
		if( commonChars == null ) {
			String commonCharFile = "/home/rob/code/dict/project/DictionarySort/data/commonchar_ALL";
			commonChars = IOUtil.loadCommonCharsFromFile(commonCharFile);
		}
		String allDefaultChars = StringUtil.getAllDefaultIgnoreCharsAsString();
		
		allChars = allDefaultChars + commonChars;
		
		String dictFile = "/home/rob/code/dict/project/DictionarySort/data/cedict_ts.u8";
		dict = IOUtil.loadSortedDictionary(dictFile, "UTF8", allChars);
		
		int runningCount = 0;
		int maxDif = -1;
		int count = 0;
		for( int i = 0; i < dict.size(); i++ ) {
			int dif = MaxDifficultyModel.getMaxDifficulty(dict.get(i).modern, commonChars);
			if( dif != maxDif ) {
				System.out.println("You can make " + count + " new words (" + runningCount + " total) from the first " + maxDif + " characters");
				maxDif = dif;
				count = 0;
			}
			count++;
			runningCount++;
		}
	}
}
