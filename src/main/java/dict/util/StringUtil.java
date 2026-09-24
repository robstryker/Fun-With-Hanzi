package dict.util;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Iterator;

public class StringUtil {
	public static final String[] TERMINATORS = {
		"......",".....", "....", "...", "!\".", "!\"。",
		".\"", "。\"", "◇\"","?\"", "？\"", "!\"", "…\"",
		".”", "。”", "◇”","?”", "？”", "!”", "…”",
		"?", "?", "?","?","?","?","?","?","?","?",
		"?","?","?","?","?","?","?","?","?","﹖",
		".", "。", "◇", "…","”", ".", "。", " ", "\n", "\t", "\r"
	}; 
	public static final String[] PUNCTUATION = {
			"，","、", ",", ".", "·", "。", "◇", "…", "：", "；", "？", "?", 
			"！", "!", "“", "”", "(", ")", "《", "》", "【", "】", "[", 
			"]", "∣", "—", "（", "）", "|", "—", "-", ".", "。", "\""," ","』","『","〕",",","–","―","*","─","~","¬",
			// garbage... fuck me
			":",";","‘","’","_","•","　","`","〈","〉","\\","．","′","－","^","／","{","}","｛","｝",
			"﹑","‵","ˊ","ˋ","〖","〗","﹒","∶","‧","°",
			"'", "」", "「", 
			"＂", "﹕", "｡", "﹗", "", "︰", "巜", "﹍", "＞", "＇",
			"＿","］","［","＜","﹔","〃",">","﹚",
			"﹙","く","■","<","﹐",
			"″","‥"," ","｜","｀","﹞","﹝",
			"˙", "〔", 
			};

	public static final String[] OTHER_IGNORED = {
			"ы","р","о","е","π","ǎ","ō","ｐ","Ｚ","Ｙ","Ｌ","Ｈ","Ｅ","゜","✕","◎","◆","▪","□","③","※",
			"━", "①", "ｘ", "②",  "/", "%","╱","∩","∞","∕","°","㎡","ー","+","$","×","￠","℃",
			"Ｑ", "Ｍ", "Ｂ", "Ｔ", "α","Ｕ","→","‰","β","=","ɜ","@","Ｒ","Ｐ","Ｉ","＆","Ｋ", "卍","ш","Х","С","ˆ","�","￼","ǔ","ǒ",
			"ｙ","ｇ","ｄ","ａ","я","щ","с","н","д","Ｆ","﹨","♀","●","∥","",
			"︿","︸","❹","❸","❷","❶","☆","★","△","▬","╰","╯","⑷","⑶","⑵","⑴","⑩","④","∪","↓","Ⅱ",
			"＼","Ｗ","Ｇ","﹡","ю","э","ь","ъ","δ","γ","Θ",
			"ū","ś","Ņ","ч","ц",
			"ф","у","п","й","ж","Я","Р","П","О","И","Г","В","Б","А","Ｊ","＃",
			"", "Ｖ", "Ｓ", "﹪","⊙","✘","ｂ","т","к","в",
			"ｌ","Ｎ","︱","½","$","+","‖","㎡","％","～"
			
	};
	public static final String[] ALPHANUMERICS = {
		"〇","Ｏ","０","１","２","３","４","５","６","７","８","９",
		"0","1","2","3","4","5","6","7","8","9",
		"a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
		"A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
		"Ａ","Ｃ","Ｄ","ｅ","ｃ","ｈ","ｕ","ｏ","ｊ","ｔ","ｉ","ɑ","ｎ","ɡ","ｋ","ｚ", 
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
		return new String[] {"啊","呀","呢","吧"};
	}
	
	
	private static ArrayList<String> ALL_DEFAULT_IGNORE = null;
	public static ArrayList<String> getAllDefaultIgnoreChars() {
		if( ALL_DEFAULT_IGNORE == null ) {
			HashSet<String> arr = new HashSet<String>();
			arr.addAll(Arrays.asList(getPunctuation()));
			arr.addAll(Arrays.asList(getTerminators()));
			arr.addAll(Arrays.asList(getAlphaNumerics()));
			arr.addAll(Arrays.asList(OTHER_IGNORED));
			arr.addAll(Arrays.asList(getDefaultZeroDifficultyChineseChars()));
			ALL_DEFAULT_IGNORE = new ArrayList<String>(new HashSet<String>(arr));
		}
		return ALL_DEFAULT_IGNORE;
	}
	
	private static String ALL_DEFAULT_IGNORE_AS_STRING = null;
	public static String getAllDefaultIgnoreCharsAsString() {
		if( ALL_DEFAULT_IGNORE_AS_STRING == null ) {
			ArrayList<String> all = getAllDefaultIgnoreChars();
			StringBuilder sb = new StringBuilder();
			for( Iterator<String> i = all.iterator(); i.hasNext(); ) {
				sb.append(i.next());
			}
			ALL_DEFAULT_IGNORE_AS_STRING = sb.toString();
		}
		return ALL_DEFAULT_IGNORE_AS_STRING;
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
