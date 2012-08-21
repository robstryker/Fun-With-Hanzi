package dict.test;

import dict.model.MaxDifficultyModel;
import dict.util.ExampleUtil;

public class Test2SplittingSentences extends AbstractDictTest {
	protected void setUp() throws Exception {
		super.setUp();
	}

	public void testStorySentences() {
		String example;
		String[] fragments;
		int maxDif, frag1, frag2, frag3, frag4, frag5;
		example = "他的成功是靠他的努力和一定的机遇。";
		fragments = ExampleUtil.getSentenceFragments(example, 1, allChars);
		assertEquals(0, fragments.length);
		
		example = "这篇小说里的人物都是活生生的，有血有肉的。";
		fragments = ExampleUtil.getSentenceFragments(example, 1, allChars);
		assertEquals(2, fragments.length);
		maxDif = MaxDifficultyModel.getMaxDifficulty(example, allChars);
		frag1 = MaxDifficultyModel.getMaxDifficulty(fragments[0], allChars);
		frag2 = MaxDifficultyModel.getMaxDifficulty(fragments[1], allChars);
		assertEquals(maxDif, frag1);
		assertTrue(maxDif > frag2);
		
		example = "“我不知道......不是的,他看起来是真实的......”";
		fragments = ExampleUtil.getSentenceFragments(example, 1, allChars);
		assertEquals(3, fragments.length);
		maxDif = MaxDifficultyModel.getMaxDifficulty(example, allChars);
		frag1 = MaxDifficultyModel.getMaxDifficulty(fragments[0], allChars);
		frag2 = MaxDifficultyModel.getMaxDifficulty(fragments[1], allChars);
		frag3 = MaxDifficultyModel.getMaxDifficulty(fragments[2], allChars);
		assertTrue(frag3 > frag2);
		assertTrue(frag3 > frag1);
		assertTrue(frag3 == maxDif);
	}
}
