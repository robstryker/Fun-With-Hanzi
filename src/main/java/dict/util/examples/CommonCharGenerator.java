package dict.util.examples;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;

import dict.model.MaxDifficultyModel;
import dict.util.IOUtil;
import dict.util.StringUtil;

public class CommonCharGenerator {
	public String generateCommonCharsFromSources() {
		long start = System.currentTimeMillis();
		File[] all = SourceMaterialFileLoader.listExampleFiles();
		final HashMap<String, Long> map = new HashMap<>();
		for( int i = 0; i < all.length; i++ ) {
			String path = all[i].getAbsolutePath();
			String contents = IOUtil.readFile(all[i].getAbsolutePath(), "UTF-8");
			char[] charArr = contents.toCharArray();
			char c;
			for( int j = 0; j < charArr.length; j++ ) {
				c = charArr[j];
				Long bi = map.get(Character.toString(c));
				if( bi == null ) {
					map.put(Character.toString(c), Long.valueOf(1));
				} else {
					map.put(Character.toString(c), Long.valueOf(bi.longValue() + 1));
				}
			}
		}
		
		ArrayList<String> keys = new ArrayList<>(map.keySet());
		Collections.sort(keys, new Comparator<String>() {

			@Override
			public int compare(String arg0, String arg1) {
				Long l1 = map.get(arg0);
				Long l2 = map.get(arg1);
				if( l1 == null || l2 == null ) {
					return 0;
				}
				return l1.intValue() - l2.intValue();
			}
		});
		Collections.reverse(keys);
		ArrayList<String> ignored = StringUtil.getAllDefaultIgnoreChars();
		
		String k;
		for( Iterator<String> i = keys.iterator(); i.hasNext(); ) {
			k = i.next();
			if( ignored.contains(k))
				i.remove();
		}
		
		
		long end = System.currentTimeMillis();
		System.out.println("\n\n Most Common chars Took " + (end - start) + " ms");
		
		return String.join("", keys);
	}

	private ArrayList<String> findAllSentencesWithMaxDifficulty(int min, int max, String chars, ArrayList<String> examples) {
		ArrayList<String> ret = new ArrayList<>();
		String usable = chars.substring(0, max);
		for( String s : examples ) {
			int found = MaxDifficultyModel.staticGetMaxDifficulty(s, usable);
			if( found != MaxDifficultyModel.NOT_FOUND_CHAR && found != 0 && found >= min && found <= max )
				ret.add(s);
		}
		return ret;
	}
	
	public static void main(String[] args) throws IOException {
		CommonCharGenerator gen = new CommonCharGenerator();
		final String mostCommonChars = gen.generateCommonCharsFromSources();
		String test = mostCommonChars.substring(0,5);
		System.out.println(mostCommonChars);
		long s1 = System.currentTimeMillis();
		ArrayList<String> examples = SourceMaterialFileLoader.loadExampleFiles(mostCommonChars);
		ArrayList<String> zeroToFifty = gen.findAllSentencesWithMaxDifficulty(0, 50, mostCommonChars, examples);
		
		zeroToFifty.sort(new Comparator<String>() {

			@Override
			public int compare(String arg0, String arg1) {
				int dif1 = MaxDifficultyModel.staticGetMaxDifficulty(arg0, mostCommonChars);
				int dif2 = MaxDifficultyModel.staticGetMaxDifficulty(arg1, mostCommonChars);
				return dif1 - dif2;
			}});
		
		//gen.stripNearlyIdentical(zeroToFifty, mostCommonChars);
		long e1 = System.currentTimeMillis();
		System.out.println((e1 - s1));
	}

//	private void stripNearlyIdentical(ArrayList<String> zeroToFifty, String mostCommonChars) {
//		HashSet<String> set = new HashSet<>();
//		Iterator<String> i = zeroToFifty.iterator();
//		String o = null;
//		for( ; i.hasNext(); ) {
//			o = i.next();
//			String stripped = stripIgnored(o);
//			if( set.contains(stripped)) {
//				i.remove();
//			} else {
//				set.add(stripped);
//				System.out.println(o);
//			}
//		}
//	}
	
}
