package dict.test;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;

import dict.model.MaxDifficultyModel;
import dict.util.ExampleUtil;
import dict.util.ExampleUtil.IExampleAdditionVerifier;

public class Test3SortExamples extends AbstractDictTest implements IExampleAdditionVerifier {
	protected void setUp() throws Exception {
		super.setUp();
	}
	public void testSortExamples() {
		String exampleFile = "/home/rob/Documents/dict/project/DictionarySort/data/examples/ALL_OUT_CN";
		Collection<String> standardExamples = ExampleUtil.loadSingleLineExamplesFromFile(allChars, exampleFile);
		ArrayList<String> standardExamples2 = new ArrayList<String>();
		standardExamples2.addAll(standardExamples);
		long sort1Time = System.currentTimeMillis();
		Collections.sort(standardExamples2, ExampleUtil.getExampleComparator(allChars));
		sort1Time = System.currentTimeMillis() - sort1Time;
		
		Collection<String> standardExamplesWithFrag = 
				ExampleUtil.loadExamplesAndFragments(allChars, exampleFile, new Test3SortExamples());
		ArrayList<String> standardExamplesWithFrag2 = new ArrayList<String>();
		standardExamplesWithFrag2.addAll(standardExamplesWithFrag);
		
		long sort2Time = System.currentTimeMillis();
		Collections.sort(standardExamplesWithFrag2, ExampleUtil.getExampleComparator(allChars));
		sort2Time = System.currentTimeMillis() - sort2Time;
		
		System.out.println(sort1Time + ":" + sort2Time);
		int noFragSize = standardExamples2.size();
		int max1, max2, prevMax1 = 0, prevMax2 = 0;
		for( int i = 0; i < noFragSize; i++) {
			max1 = MaxDifficultyModel.getMaxDifficulty(standardExamples2.get(i), allChars);
			max2 = MaxDifficultyModel.getMaxDifficulty(standardExamplesWithFrag2.get(i), allChars);
			assertTrue(max1 >= max2);
			assertTrue(prevMax1 <= max1);
			assertTrue(prevMax2 <= max2);
			prevMax1 = max1;
			prevMax2 = max2;
		}
	}

	@Override
	public boolean shouldAddExample(String string, boolean fragment) {
		return string.length() > 4;
	}
}
