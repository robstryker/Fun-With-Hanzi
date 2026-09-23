package dict.util;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.Iterator;

import dict.model.MaxDifficultyModel;

/**
 * Discover the optimal common character order
 *  for an initial hanzi list and example list. 
 * @author rob
 *
 */
public class CommonCharUtil {
	private int firstHanzi;
	private String hanziList;
	private ArrayList<HanziSentences> hanziSentenceList;
	private String[][] initialSortedExamplesByCharacter;
	public String runFindOptimalString(String hanziList, int firstHanzi, Collection<String> exampleList) {
		this.firstHanzi = firstHanzi;
		this.initialSortedExamplesByCharacter = getExamplesByHanziToIntroduce(hanziList, firstHanzi, exampleList);
		this.hanziSentenceList = new ArrayList<HanziSentences>();
		// Initialize
		for( int i = 0; i < initialSortedExamplesByCharacter.length; i++ ) {
			hanziSentenceList.add(new HanziSentences(hanziList.charAt(i), initialSortedExamplesByCharacter[i]));
		}
	
		System.out.println(findValue(hanziSentenceList) + "    :   " + hanziList);
		ArrayList<HanziSentences> workingArray = cloneHanziSentenceList(hanziSentenceList);
		int max = workingArray.size();
		boolean done = false;
		boolean goLeft = true;
		String originalTrimmedHanziList = getCharString(workingArray);
		while( !done ) {
			String pre = getCharString(workingArray);
			char c;
			String newVal = originalTrimmedHanziList;
			if( goLeft ) {
				for( int i = this.firstHanzi+1; i < max; i++) {
					c = hanziList.charAt(i);
					int prevIndex = newVal.indexOf(c);
					workingArray = findBestLocationLeft(workingArray, i, null);
					newVal = getCharString(workingArray);
					int newIndex = newVal.indexOf(c);
					if( prevIndex != newIndex ) 
						System.out.println(findValue(workingArray) + " - moved  " + c + " from " + prevIndex + " to " + newIndex);
					if( i % 100 == 0 )
						System.out.println(newVal);
				}
				System.out.println(newVal);
			} else {
				for( int i = max-1; i > this.firstHanzi; i--) {
					c = hanziList.charAt(i);
					int prevIndex = newVal.indexOf(c);
					workingArray = findBestLocationRight(workingArray, i, max, null);
					newVal = getCharString(workingArray);
					int newIndex = newVal.indexOf(c);
					if( prevIndex != newIndex ) 
						System.out.println(findValue(workingArray) + " - moved  " + c + " from " + prevIndex + " to " + newIndex);
					if( i % 100 == 0 )
						System.out.println(newVal);
				}
				System.out.println(newVal);
			}
			goLeft = !goLeft;
			done = pre.equals(getCharString(workingArray));
		}

		for( int i = firstHanzi; i < max; i++ ) {
			System.out.println(workingArray.get(i));
		}
		String fVal = getCharString(workingArray);
		System.out.println(fVal);
		return fVal;
	}

	private class ChangeVerifier {
		protected boolean canAbort = false;
	}
	
	private ArrayList<HanziSentences> findBestLocationRight(ArrayList<HanziSentences> original, int originalLoc, int maxRight, ChangeVerifier aborter ) {
		ArrayList<HanziSentences> working = cloneHanziSentenceList(original);
		long originalValue = findValue(working);
		long bestValue = originalValue;
		int bestIndex = originalLoc;
		int displaced = 0;
		int toMoveLength = 0;
		long workingVal = bestValue;
		for( int i = originalLoc; i+1 < original.size() && i+1 < maxRight; i++ ) {
			HanziSentences hs = working.remove(i);
			working.add(i+1, hs);
			char justSkipped = working.get(i).hanzi;
			int moveUpCount = working.get(i).getSentenceCount(); // num moving up
			String[] toMove = working.get(i).removeSentencesUsing(hs.hanzi); // num left behind
			working.get(i+1).addSentences(toMove);
			int dif = moveUpCount - hs.getSentenceCount();
			//long newVal = findValue(working);
			workingVal = workingVal + dif;
			if( workingVal > bestValue ) {
				bestValue = workingVal;
				bestIndex = i+1;
				toMoveLength = toMove.length;
			}
		}
		
		if( originalLoc == bestIndex )
			return original;
		// Do it again, but this time actually clone the model
		working = cloneHanziSentenceList(original);
		for( int i = originalLoc; i < original.size() && i < maxRight; i++ ) {
			HanziSentences hs = working.remove(i);
			working.add(i+1, hs);
			char justSkipped = working.get(i).hanzi;
			String[] toMove = working.get(i).removeSentencesUsing(hs.hanzi);
			working.get(i+1).addSentences(toMove);
			if( i == (bestIndex - 1)) {
				return working;
			}
		}
		return original;
	}
	
	private ArrayList<HanziSentences> findBestLocationLeft(ArrayList<HanziSentences> original, int originalLoc, ChangeVerifier aborter ) {
		ArrayList<HanziSentences> working = cloneHanziSentenceList(original);
		long originalValue = findValue(working);
		long bestValue = originalValue;
		int bestIndex = originalLoc;
		long workingVal = originalValue;
		for( int i = originalLoc; i > firstHanzi+1 && working.get(i).sentences.size() > 0; i-- ) {
			if( working.get(i).sentences.size() == 0 )
				break;
			HanziSentences hs = working.remove(i);
			working.add(i-1, hs);
			int oCount = hs.getSentenceCount();
			char justMovedDown = working.get(i).hanzi;
			String[] toMove = hs.removeSentencesUsing(justMovedDown);
			int displaced = working.get(i).getSentenceCount();
			working.get(i).addSentences(toMove);
			int dif = oCount - toMove.length - displaced; 
			workingVal = workingVal + dif;
			// long newVal = findValue(working);
			if( workingVal > bestValue ) {
				bestValue = workingVal;
				bestIndex = i-1;
			}
		}
		
		if( originalLoc == bestIndex )
			return original;
		// Do it again, but this time actually clone the model
		working = cloneHanziSentenceList(original);
		for( int i = originalLoc; i > firstHanzi; i-- ) {
			HanziSentences hs = working.remove(i);
			working.add(i-1, hs);
			char justMovedDown = working.get(i).hanzi;
			String[] toMove = hs.removeSentencesUsing(justMovedDown);
			int displaced = working.get(i).getSentenceCount();
			working.get(i).addSentences(toMove);
			if( i == (bestIndex + 1) ) {
				return working;
			}
		}
		return original;
	}
	
	private void validateBestModel(ArrayList<HanziSentences> potentiallyBroken, int max) {
		StringBuffer allChars = new StringBuffer();
		for( int i = 0; i < max; i++ ) {
			allChars.append(potentiallyBroken.get(i).hanzi);
			String toStr = allChars.toString();
			String[] sents = potentiallyBroken.get(i).getSentences();
			for( int k = 0; k < sents.length; k++ ) {
				for( int m = 0; m < sents[k].length(); m++ ) {
					if( !toStr.contains("" + sents[k].charAt(m))) {
						throw new RuntimeException();
					}
				}
			}
		}
	}
	
	private String getCharString(ArrayList<HanziSentences> sentences) {
		return getCharString(sentences, sentences.size()-1);
	}
	private String getCharString(ArrayList<HanziSentences> sentences, int upTo) {
		StringBuffer sb = new StringBuffer();
		for( int i = firstHanzi; i <= upTo; i++ ) {
			sb.append(sentences.get(i).hanzi);
		}
		return sb.toString();
	}
	
	private long findValue(ArrayList<HanziSentences> list) {
		long l = 0;
		int size = list.size();
		for( int i = 0; i < size; i++ ) {
			l += (list.get(i).getSentenceCount() * (size-i));
		}
		return l;
	}
	private ArrayList<HanziSentences> cloneHanziSentenceList(ArrayList<HanziSentences> original) {
		ArrayList<HanziSentences> ret = new ArrayList<HanziSentences>();
		HanziSentences hs = null;
		for(Iterator<HanziSentences> i = original.iterator(); i.hasNext(); ) {
			hs = i.next();
			ret.add(new HanziSentences(hs.getHanzi(), hs.getSentences()));
		}
		return ret;
	}
	
	public class HanziSentences {
		private char hanzi;
		private ArrayList<String> sentences;
		public HanziSentences(char hanzi) {
			this.hanzi = hanzi;
			this.sentences = new ArrayList<String>();
		}

		public HanziSentences(char hanzi, String[] sentences) {
			this(hanzi);
			this.sentences.addAll(Arrays.asList(sentences));
		}
		public String toString() {
			return "hanzi: " + hanzi + " and " + sentences.size() + " sentences: " + sentences;
		}
		public char getHanzi() {
			return hanzi;
		}
		public void addSentences(String[] toAdd) {
			sentences.addAll(Arrays.asList(toAdd));
		}
		public int getSentenceCount() {
			return sentences.size();
		}

		public String[] getSentences() {
			return (String[]) sentences.toArray(new String[sentences.size()]);
		}
		public String[] removeSentencesUsing(char c) {
			ArrayList<String> ret = new ArrayList<String>();
			String next;
			for( Iterator<String> i = sentences.iterator(); i.hasNext(); ) {
				next = i.next();
				if( next.contains(Character.toString(c))) {
					ret.add(next);
					i.remove();
				}
			}
			return ret.toArray(new String[ret.size()]);
		}
	}
	
	
	protected static String[][] getExamplesByHanziToIntroduce(String hanziList, int firstHanzi, Collection<String> exampleList) {
		ArrayList<String> sorted = getSortedCollection(hanziList, exampleList);
		int examplePointer = 0;
		ArrayList<String[]> stringList = new ArrayList<String[]>();
		for( int i = 0; i < hanziList.length(); i++ ) {
			int hanziMaxDif = MaxDifficultyModel.getMaxDifficulty(Character.toString(hanziList.charAt(i)), hanziList);
			ArrayList<String> tmp = new ArrayList<String>();
			String e;
			int mdtmp;
			while(examplePointer < sorted.size()) {
				e = sorted.get(examplePointer);
				mdtmp = MaxDifficultyModel.getMaxDifficulty(e, hanziList);
				if( mdtmp <= hanziMaxDif ) 
					tmp.add(sorted.get(examplePointer++));
				else
					break;
			}
			stringList.add((String[]) tmp.toArray(new String[tmp.size()]));
			//System.out.println("added " + tmp.size() + " for char " + Character.toString(hanziList.charAt(i)));
		}
		String[][] all = (String[][]) stringList.toArray(new String[stringList.size()][]);
		MaxDifficultyModel.getDefault().clear();
		return all;
	}

	public static ArrayList<String> getSortedCollection(String hanziList, Collection<String> exampleList) {
		ArrayList<String> examples = new ArrayList<String>();
		examples.addAll(exampleList);
		Collections.sort(examples, ExampleUtil.getExampleComparator(hanziList));
		MaxDifficultyModel.getDefault().clear();
		return examples;
	}
}
