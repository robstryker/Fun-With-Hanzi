package dict.test;

import java.util.Iterator;

import dict.model.DictionaryEntry;
import dict.model.MaxDifficultyModel;

public class Test1DictSort extends AbstractDictTest {
	protected void setUp() throws Exception {
		super.setUp();
	}
	
	public void testOne() {
		DictionaryEntry e;
		int previousDif = 0;
		for( Iterator<DictionaryEntry> i = dict.iterator(); i.hasNext(); ) {
			e = i.next();
			int dif = MaxDifficultyModel.getMaxDifficulty(e.modern, allChars);
			if( dif == -1 )
				return;
			assertTrue("dif: " + dif + " and previous " + previousDif + ":  " + e.modern, previousDif <= dif);
			previousDif = dif;
		}
	}

}
