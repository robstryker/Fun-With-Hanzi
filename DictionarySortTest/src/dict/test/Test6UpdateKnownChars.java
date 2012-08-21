package dict.test;

import dict.util.IOUtil;
import dict.util.StringUtil;
import junit.framework.TestCase;

public class Test6UpdateKnownChars extends TestCase {
	public void testUpdateKnownChars() {
		String customFile = "/home/rob/Documents/dict/project/DictionarySort/data/examples/CUSTOM_EXAMPLES";
		String hpFile = "/home/rob/Documents/dict/project/DictionarySort/data/examples/hpexamples.txt";
		String ncikuFile = "/home/rob/Documents/dict/project/DictionarySort/data/examples/ALL_OUT_CN";
		String commonChar = "/home/rob/Documents/dict/project/DictionarySort/data/commonchar_ALL";
		String dusbook3 = "/home/rob/Documents/dict/project/DictionarySort/data/examples/GBK/3.txt";

		String chars = "";

		String customContents = IOUtil.readFile(customFile, "UTF8");
		chars = StringUtil.getUpdatedKnownCharacters(chars, customContents);
		System.out.println(chars.length());

		String hpContents = IOUtil.readFile(hpFile, "UTF8");
		chars = StringUtil.getUpdatedKnownCharacters(chars, hpContents);
		System.out.println(chars.length());
		
		String ncikuContents = IOUtil.readFile(ncikuFile, "UTF8");
		chars = StringUtil.getUpdatedKnownCharacters(chars, ncikuContents);
		System.out.println(chars.length());

		String commonCharContents = IOUtil.readFile(commonChar, "UTF8");
		chars = StringUtil.getUpdatedKnownCharacters(chars, commonCharContents);
		System.out.println(chars.length());
		
		int prevL = chars.length();

		String dusBook3Contents = IOUtil.readFile(dusbook3, "GBK");
		chars = StringUtil.getUpdatedKnownCharacters(chars, dusBook3Contents);
		System.out.println(chars.length() + " - " + chars);
		System.out.println(chars.substring(prevL));
		System.out.println(dusBook3Contents);

	}
}
