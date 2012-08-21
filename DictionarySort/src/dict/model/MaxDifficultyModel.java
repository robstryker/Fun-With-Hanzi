package dict.model;

import java.util.HashMap;

public class MaxDifficultyModel {
	public static final int NOT_FOUND_CHAR = -1;
	public static MaxDifficultyModel model;
	public static MaxDifficultyModel getDefault() {
		if( model == null )
			model = new MaxDifficultyModel();
		return model;
	}
	
	public static int getMaxDifficulty(String string, String hanziList) {
		return getDefault().getModel(hanziList).getMaxDifficulty(string);
	}
	
	protected HashMap<String, MaxDifficultyModel2> modelMap;
	public MaxDifficultyModel() {
		modelMap = new HashMap<String, MaxDifficultyModel2>();
	}
	public void clear() {
		modelMap.clear();
	}
	public MaxDifficultyModel2 getModel(String chars) {
		if( modelMap.get(chars) == null ) {
			modelMap.put(chars, new MaxDifficultyModel2(chars));
		}
		return modelMap.get(chars);
	}
	
	public static class MaxDifficultyModel2 {
		private String chars;
		private HashMap<String, Integer> maxDif;
		public MaxDifficultyModel2(String chars) {
			this.chars = chars;
			maxDif = new HashMap<String, Integer>();
		}
		
		public int getMaxDifficulty(String s) {
			if( maxDif.get(s) == null ) {
				maxDif.put(s, staticGetMaxDifficulty(s, chars));
			}
			return maxDif.get(s);
		}
	}
	
	public static int staticGetMaxDifficulty(String s, String usable) {
		int max = 0;
		for( int i = 0; i < s.length(); i++ ) {
			int intval = staticGetDifficulty(s.charAt(i), usable);
			if( intval == NOT_FOUND_CHAR ) {
				return NOT_FOUND_CHAR;
			}
			max = max > intval ? max : intval;
		}
		return max;
	}

	public static int staticGetDifficulty(char c, String usable) {
		return usable.indexOf(c);
	}

}
