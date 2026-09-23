package dict.util.examples;

import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.TreeSet;

import dict.util.ExampleUtil;

public class SourceMaterialFileLoader {
	
	public static File[] listExampleFiles() {
		File project = new File(".");
		File data = new File(project, "data");
		File examples = new File(data, "examples");
		File storyChina = new File(examples, "storychina");
		ArrayList<File> ret = new ArrayList<>();
		ret.add(new File(examples, "ALL_OUT_CN"));
		ret.add(new File(examples, "CUSTOM_EXAMPLES"));
		ret.add(new File(examples, "hpexamples.txt"));
		
		File[] storyChinas = storyChina.listFiles();
		ret.addAll(Arrays.asList(storyChinas));
		return (File[]) ret.toArray(new File[ret.size()]);
	}

	
	public static ArrayList<String> loadExampleFiles(String usableChars) {
		File[] sources = listExampleFiles();
		TreeSet<String> set = new TreeSet<String>();
		for( int i = 0; i < sources.length; i++ ) {
			Collection<String> e1 = ExampleUtil.loadMultiLineExamples(sources[i].getAbsolutePath(), 
					usableChars, "UTF8", true, null);
			set.addAll(e1);
		}
		ArrayList<String> list = new ArrayList<String>();
		list.addAll(set);
		return list;
	}

}
