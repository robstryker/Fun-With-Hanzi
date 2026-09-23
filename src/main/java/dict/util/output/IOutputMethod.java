package dict.util.output;

import dict.model.DictionaryEntry;

public interface IOutputMethod {
	public void start();
	public void startHanzi(int id, char hanzi);
	public void printDefinition(int hanziId, DictionaryEntry entry);
	public void printSentence(int hanziId, char hanzi, String sentence);
	public void endHanzi(int id, char hanzi);
	public void end();
}
