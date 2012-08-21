package dict.model;


public class DictionaryEntry implements Comparable {
	public final String traditional;
	public final String modern;
	public final String pinyin;
	public final String desc;
	public DictionaryEntry(String string) {
		int space = string.indexOf(' ');
		traditional = string.substring(0, space);
		int oldspace = space+1;
		space = string.indexOf(' ', oldspace);
		modern = string.substring(oldspace, space);
		oldspace = space+2;
		space = string.indexOf("] ", oldspace);
		pinyin = string.substring(oldspace, space).toLowerCase();
		desc = string.substring(space+2);
	}
	
	public boolean isWellFormed() {
		return true;
	}

	public int compareTo(Object o) {
		if( !(o instanceof DictionaryEntry))
			return -1;
		DictionaryEntry o2 = (DictionaryEntry)o;
		String[] myPinyinArray = pinyin.split(" ");
		String[] newPinyinArray = o2.pinyin.split(" ");
		for( int i = 0; i < myPinyinArray.length; i++ ) {
			if( newPinyinArray.length <= i)
				return 1; 
			int comparePinyin = myPinyinArray[i].compareTo(newPinyinArray[i]);
			if( comparePinyin != 0 ) {
				return comparePinyin;
			}
			if( modern.charAt(i) != o2.modern.charAt(i)) {
				return modern.charAt(i) - o2.modern.charAt(i);
			}
		}
		return 0;
	}
	
	public String toString() {
		return traditional + " " + modern + " [" + pinyin + "] " + desc;
	}
	
	public boolean allCharsInString(String usableChars) {
		String hanzi = modern;
		for( int j = 0; j < hanzi.length(); j++ ) {
			if( !usableChars.contains(""+hanzi.charAt(j))) {
				return false;
			}
		}
		// entry acceptable
		return true;
	}
	
}
