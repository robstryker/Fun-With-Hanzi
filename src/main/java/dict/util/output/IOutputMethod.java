package dict.util.output;

import java.util.List;
import java.util.Map;

import dict.model.DictionaryEntry;

public interface IOutputMethod {
	public void start();
	/** The free mood particles, known before character #1, with their dictionary entries. */
	public void printKnown(Map<Character, List<DictionaryEntry>> known);
	public void startHanzi(int id, char hanzi);
	public void printDefinition(int hanziId, DictionaryEntry entry);
	public void printSentence(int hanziId, char hanzi, String sentence);
	public void endHanzi(int id, char hanzi);
	public void end();
}
