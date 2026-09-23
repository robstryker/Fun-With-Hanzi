package dict.util.output;

import dict.model.DictionaryEntry;

public class XMLOutputMethod implements IOutputMethod {
	private boolean inSentences = false;
	public void start() {
		System.out.println("<?xml-stylesheet type=\"text/xsl\" href=\"tmp.xsl\"?>");
		System.out.println("<dict>");
	}
	public void startHanzi(int hanziId, char hanzi) {
		System.out.println("   <hanzi id=\"" + hanziId + "\" char=\"" + hanzi + "\">");
	}
	public void printDefinition(int hanziId, DictionaryEntry entry) {
		System.out.println("   " + entry);
	}
	public void printSentence(int hanziId, char hanzi, String sentence) {
		if( !inSentences ) {
			System.out.println("      <sentences>");
			inSentences = true;
		}
		System.out.println("         <sent>" + sentence + "</sent>");
	}
	public void endHanzi(int hanziId, char hanzi) {
		System.out.println("      </sentences>");
		System.out.println("   </hanzi>");
	}
	public void end() {
		System.out.println("</dict>");
	}
}
