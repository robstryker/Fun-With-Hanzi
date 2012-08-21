package dict.util;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;

public class StringUtil {
	public static final String[] TERMINATORS = {
		"......",".....", "....", "...", "!\".", "!\"。",
		".\"", "。\"", "◇\"","?\"", "？\"", "!\"", "…\"",
		".”", "。”", "◇”","?”", "？”", "!”", "…”",
		".", "。", "◇", "…","”", ".", "。"
	}; 
	public static final String[] PUNCTUATION = {
			"，","、", ",", ".", "·", "。", "◇", "…", "：", "；", "？", "?", 
			"！", "!", "“", "”", "/", "%", "(", ")", "《", "》", "【", "】", "[", 
			"]", "∣", "—", "（", "）", "|", "—", "-", ".", "。", "\""," ","』","『","〕",",","–","―","*","─","~","¬",
			// garbage... fuck me
			":",";","‘","’","_","•","　","`","〈","〉","\\","．","％","～","′","－","^","／","{","}","｛","｝",
			"﹑","‵","ˊ","ˋ","〖","〗","°","㎡","ー","+","$","﹒","×","￠","℃","∶","ｌ","α","Ｕ","→","‰","β","=","ɜ","@","Ｎ","︱","½","$","+","‖","㎡","‧","°",
			"Ａ","Ｃ","Ｄ","ｅ","ｃ","ｈ","ｕ","ｏ","ｊ","ｔ","ｉ","ɑ","ｎ","ɡ","ｋ","ｚ"};

	public static final String[] ALPHANUMERICS = {
		"〇","Ｏ","０","１","２","３","４","５","６","７","８","９",
		"0","1","2","3","4","5","6","7","8","9",
		"a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
		"A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"
	};
	public static String[] getTerminators() {
		return TERMINATORS;
	}
	public static String[] getPunctuation() {
		return PUNCTUATION;
	}
	
	public static String[] getAlphaNumerics() {
		return ALPHANUMERICS;
	}
	
	public static String[] getDefaultZeroDifficultyChineseChars() {
		return new String[] {"呀","呢","吧"};
	}
	
	public static ArrayList<String> getAllDefaultIgnoreChars() {
		ArrayList<String> arr = new ArrayList<String>();
		arr.addAll(Arrays.asList(getPunctuation()));
		arr.addAll(Arrays.asList(getAlphaNumerics()));
		arr.addAll(Arrays.asList(getDefaultZeroDifficultyChineseChars()));
		
		return arr;
	}
	
	public static String getAllDefaultIgnoreCharsAsString() {
		ArrayList<String> all = getAllDefaultIgnoreChars();
		StringBuilder sb = new StringBuilder();
		for( Iterator<String> i = all.iterator(); i.hasNext(); ) {
			sb.append(i.next());
		}
		return sb.toString();
	}

    public static String replacePunc(String str, String rep) {
    	String ret = "" + str;
    	String[] punctuation = StringUtil.getPunctuation();
    	for(int i = 0; i < punctuation.length; i++) {
    		ret = ret.replace(punctuation[i], rep);
    	}
    	return ret;
    }

	
	public static int lengthMinusPunc(String s) {
		String[] punctuation = StringUtil.getPunctuation();
		for( int i = 0; i < punctuation.length; i++ ) {
			while(s.contains(punctuation[i])) 
				s = s.replace(punctuation[i], "");
		}
		return s.length();
	}
	
	public static boolean endsWithPunc(String s) {
		String[] punctuation = StringUtil.getPunctuation();
		for( int i = 0; i < punctuation.length; i++ ) {
			if( s.endsWith(punctuation[i])) {
				return true;
			}
		}
		return false;
	}
	
	public static boolean terminatesSentence(String s) {
		String[] terminator = StringUtil.getTerminators();
		for( int i = 0; i < terminator.length; i++ ) {
			if( s.endsWith(terminator[i])) {
				return true;
			}
		}
		return false;
	}
	
	public static int getTerminatedIndex(String s) {
		String[] terminator = StringUtil.getTerminators();
		int ind;
		for( int i = 0; i < terminator.length; i++ ) {
			ind = s.indexOf(terminator[i]);
			if( ind != -1 ) 
				return ind + terminator[i].length();
		}
		return -1;
	}

	/**
	 * Returns a list of sentences, with the last element being a potentially
	 * UNTERMINATED sentence
	 * @param s
	 * @return
	 */
	public static String[] explodeIntoTerminatedSentences(String s) {
		ArrayList<String> list = new ArrayList<String>();
		int termination = getTerminatedIndex(s);
		while(termination != -1) {
			list.add(s.substring(0, termination));
			s = s.substring(termination);
			termination = getTerminatedIndex(s);
		}
		if( !s.equals(""))
			list.add(s);
		return (String[]) list.toArray(new String[list.size()]);
	}
	
	public static String[] findUnknownChars(String s, String allChars) {
		ArrayList<String> list = new ArrayList<String>();
		for( int i = 0; i < s.length(); i++ ) {
			if( !allChars.contains(Character.toString(s.charAt(i)))) {
				list.add(Character.toString(s.charAt(i)));
			}
		}
		return (String[]) list.toArray(new String[list.size()]);
	}
	
	public static void printStringLineByLine(String s) {
		for( int i = 0; i < s.length(); i++ ) {
			System.out.println(Character.toString(s.charAt(i)));
		}
	}
	
	public static String getUpdatedKnownCharacters(String original, ArrayList<String> toCheck) {
		Iterator<String> i = toCheck.iterator();
		String next;
		while(i.hasNext()) {
			next = i.next();
			original = getUpdatedKnownCharacters(original, next);
		}
		return original;
	}
	
	public static String getUpdatedKnownCharacters(String original, String next) {
		for( int j = 0; j < next.length(); j++ ) {
			if( !original.contains(Character.toString(next.charAt(j)))) {
				original += Character.toString(next.charAt(j));
			}
		}
		return original;
	}
	
}
