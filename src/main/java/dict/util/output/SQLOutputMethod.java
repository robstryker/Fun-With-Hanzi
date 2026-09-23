package dict.util.output;

import dict.model.DictionaryEntry;
import dict.util.IOUtil;

public class SQLOutputMethod implements IOutputMethod {
	private int dictIndex = 0;
	private int sentenceIndex = 0;
	public void start() {
		// Print the createTables
		System.out.println(
				"CREATE TABLE hanzi (\n" + 
				"    hid int NOT NULL default '0',\n" +  
				"    hanzi varchar(255) NOT NULL,\n"+
				"    PRIMARY KEY (hid));");
				
		System.out.println(
				"CREATE TABLE list (\n" + 
				"    eid int NOT NULL AUTO_INCREMENT,\n" +  
				"    listid int NOT NULL,\n" +  
				"    position int NOT NULL,\n"+
				"    hanziId int NOT NULL,\n"+
				"    PRIMARY KEY (eid));");

		System.out.println(
				"CREATE TABLE dict (\n" + 
				"    id int NOT NULL AUTO_INCREMENT,\n" +  
				"    traditional varchar(255) NOT NULL,\n" +  
				"    modern varchar(255) NOT NULL,\n" +  
				"    pinyin varchar(255) NOT NULL,\n" +  
				"    descr varchar(255) NOT NULL,\n"+
				"    PRIMARY KEY (id));");

		System.out.println(
				"CREATE TABLE dictHanziMap (\n" + 
				"    id int NOT NULL AUTO_INCREMENT,\n" +  
				"    list int NOT NULL,\n" +  
				"    hid int NOT NULL,\n" +  
				"    did int NOT NULL,\n" +  
				"    PRIMARY KEY (id));");

		System.out.println(
				"CREATE TABLE sentences (\n" + 
				"    sid int NOT NULL AUTO_INCREMENT,\n" +  
				"    sentence text NOT NULL,\n" +  
				"    PRIMARY KEY (sid));");

				
		System.out.println(
				"CREATE TABLE sentenceHanziMap (\n" + 
				"    uid int NOT NULL AUTO_INCREMENT,\n" +  
				"    list int NOT NULL,\n" +  
				"    hid int NOT NULL,\n" +  
				"    sid int NOT NULL,\n" +  
				"    PRIMARY KEY (uid)   );");
	}
	public void startHanzi(int hanziId, char hanzi) {
		System.out.println("insert into hanzi values(" + hanziId + ", '" + IOUtil.addSlashes("" + hanzi) + "');");
		System.out.println("insert into list values(null, 1, " + hanziId + ", " + hanziId + ");");
	}
	public void printDefinition(int hanziId, DictionaryEntry entry) {
		System.out.println("insert into dict values(" + dictIndex + ", " +
				"'" + entry.traditional + "', '" + entry.modern + "', '" + entry.pinyin + "', '" 
				+ IOUtil.addSlashes(entry.desc) + "');");
		System.out.println("insert into dictHanziMap values(null, 1, " + hanziId + ", " + dictIndex + ");");
		dictIndex++;
	}
	public void printSentence(int hanziId, char hanzi, String sentence) {
		System.out.println("insert into sentences values(" + sentenceIndex + ", '" 
				+ IOUtil.addSlashes(sentence) + "');");
		System.out.println("insert into sentenceHanziMap values(null, 1, " + hanziId + ", " + sentenceIndex + ");");
		sentenceIndex++;
	}
	public void endHanzi(int hanziId, char hanzi) {
	}
	public void end() {
	}
}
