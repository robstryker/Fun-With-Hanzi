package dict.util.output;

import java.util.List;
import java.util.Map;

import dict.model.DictionaryEntry;

/**
 * Writes the same layout as the historical outputs/tmp.xml:
 * every hanzi gets its words, then a (possibly empty) sentences block.
 */
public class XMLOutputMethod implements IOutputMethod {
	private boolean inSentences = false;
	public void start() {
		System.out.println("<?xml-stylesheet type=\"text/xsl\" href=\"tmp.xsl\"?>");
		System.out.println("<dict>");
	}
	public void printKnown(Map<Character, List<DictionaryEntry>> known) {
		System.out.println("  <known>");
		for( Map.Entry<Character, List<DictionaryEntry>> k : known.entrySet()) {
			System.out.println("    <hanzi char=\"" + escape(String.valueOf(k.getKey())) + "\">");
			for( DictionaryEntry entry : k.getValue())
				System.out.println("  " + wordElement(entry));
			System.out.println("    </hanzi>");
		}
		System.out.println("  </known>");
	}
	public void startHanzi(int hanziId, char hanzi) {
		inSentences = false;
		System.out.println("  <hanzi id=\"" + hanziId + "\" char=\"" + escape(String.valueOf(hanzi)) + "\">");
	}
	public void printDefinition(int hanziId, DictionaryEntry entry) {
		System.out.println(wordElement(entry));
	}
	private static String wordElement(DictionaryEntry entry) {
		return "    <word><t>" + escape(entry.traditional) + "</t><m>" + escape(entry.modern)
				+ "</m><p>" + escape(entry.pinyin) + "</p><d>" + escape(entry.desc) + "</d></word>";
	}
	public void printSentence(int hanziId, char hanzi, String sentence) {
		openSentences();
		System.out.println("      <sent>" + escape(sentence) + "</sent>");
	}
	public void endHanzi(int hanziId, char hanzi) {
		openSentences();
		System.out.println("    </sentences>");
		System.out.println("  </hanzi>");
	}
	public void end() {
		System.out.println("</dict>");
	}

	private void openSentences() {
		if( !inSentences ) {
			System.out.println("    <sentences>");
			inSentences = true;
		}
	}

	private static String escape(String s) {
		return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
	}
}
