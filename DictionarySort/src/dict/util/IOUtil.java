package dict.util;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.text.StringCharacterIterator;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;

import dict.model.DictionaryEntry;
import dict.model.MaxDifficultyModel;
import dict.util.output.IOutputMethod;
import dict.util.output.SQLOutputMethod;
import dict.util.output.XMLOutputMethod;

public class IOUtil {
	private static IOutputMethod out;

	public static String loadCommonCharsFromFile(String filename) {
		return readFile(filename, "UTF8");
	}
	
	public static String readFile(String filename, String encoding) {
		String fromFile = "";
		try { 
			BufferedReader in = new BufferedReader( 
					new InputStreamReader(new FileInputStream(filename), encoding)); 
			String str = in.readLine();
			while(str != null ) {
				if( str.length() > 0 )
					fromFile += str.charAt(0);
				str = in.readLine();
			}
		} catch (UnsupportedEncodingException e) { 
			e.printStackTrace();
		} catch (IOException e) { 
			e.printStackTrace();
		} 
		return fromFile;
	}

	public static ArrayList<DictionaryEntry> loadDictionary(String filename) {
		return loadDictionary(filename, "UTF8");
	}
	
	public static ArrayList<DictionaryEntry> loadDictionary(String filename, String encoding) {	
		ArrayList<DictionaryEntry> dict = new ArrayList<DictionaryEntry>();
		try { 
			BufferedReader in = new BufferedReader( 
					new InputStreamReader(new FileInputStream(filename), encoding)); 
			String str = in.readLine();
			while(str != null ) {
				handleDictionaryLine(str, dict);
				str = in.readLine();
			}
		} catch (UnsupportedEncodingException e) { 
		} catch (IOException e) { 
		} 
		return dict;
	}

	private static void handleDictionaryLine(String str, ArrayList<DictionaryEntry> dict) {
		if(str.charAt(0) != '#') {
			DictionaryEntry e = new DictionaryEntry(str);
			if( e.isWellFormed()) 
				dict.add(e);
		}
	}

	public static ArrayList<DictionaryEntry> loadSortedDictionary(String filename, String encoding, final String commonChars) {
		ArrayList<DictionaryEntry> dict = loadDictionary(filename, encoding);
		final HashMap<String, Integer> tmp = new HashMap<String, Integer>();
		Comparator<DictionaryEntry> dictComparator = new Comparator<DictionaryEntry>() {
			public int compare(DictionaryEntry o1, DictionaryEntry o2) {
				if( tmp.get(o1) == null )
					tmp.put(o1.modern, new Integer(MaxDifficultyModel.getMaxDifficulty(o1.modern, commonChars)));
				if( tmp.get(o2) == null )
					tmp.put(o2.modern, new Integer(MaxDifficultyModel.getMaxDifficulty(o2.modern, commonChars)));
				int o1v = tmp.get(o1.modern).intValue();
				int o2v = tmp.get(o2.modern).intValue();
				if( o1v == MaxDifficultyModel.NOT_FOUND_CHAR && o2v != MaxDifficultyModel.NOT_FOUND_CHAR)
					return 1;
				if( o2v == MaxDifficultyModel.NOT_FOUND_CHAR && o1v != MaxDifficultyModel.NOT_FOUND_CHAR)
					return -1;
				if( o1v == o2v )
					return o1.modern.compareTo(o2.modern);
				return o1v-o2v;
			}
		};
		Collections.sort(dict, dictComparator);
		return dict;
	}
	
	
    public static String addSlashes( String text ){    	
        final StringBuffer sb                   = new StringBuffer( text.length() * 2 );
        final StringCharacterIterator iterator  = new StringCharacterIterator( text );
        
  	  	char character = iterator.current();
        
        while( character != StringCharacterIterator.DONE ){
            if( character == '"' ) sb.append( "\\\"" );
            else if( character == '\'' ) sb.append( "\\\'" );
            else if( character == '\\' ) sb.append( "\\\\" );
            else if( character == '\n' ) sb.append( "\\n" );
            else if( character == '{'  ) sb.append( "\\{" );
            else if( character == '}'  ) sb.append( "\\}" );
            else sb.append( character );
            
            character = iterator.next();
        }
        
        return sb.toString();
    }
	
	public static IOutputMethod getOut() {
		if( out == null )
			out = getSQLOut();
		return out;
	}
	
	public static IOutputMethod getSQLOut() {
		return new SQLOutputMethod();
	}
	public static IOutputMethod getPrintOut() {
		return new XMLOutputMethod();
	}
	
	
}
