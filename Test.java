import java.util.*;

public class LetterInventory {
    public static final int DEFAULT_CAPACITY = 26;

    private int[] count;
    private int size;

    public LetterInventory(){
        count = new int[DEFAULT_CAPACITY];
    }

    public LetterInventory(String data){
        count = new int[DEFAULT_CAPACITY];
        data = data.toLowerCase();

        for (int i = 0; i < data.length(); i++){
            char letter = data.charAt(i);
            if (letter - 'a' >= 0 && letter - 'a' < DEFAULT_CAPACITY){
                count[letter - 'a']++;
                size++;
            }  
        }
    }

    public int get(char letter){
        checkAlphabetic(letter);
        return count[letter - 'a'];
    }

    public void set(char letter, int value){
        checkAlphabetic(letter);
        if (value < 0) {
            throw new IllegalArgumentException();
        }

        count[letter - 'a'] = value;
        size += value;
    }

    public int size(){
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public String toString(){
        if(size == 0){
            return "[]";
        } else {
            String result = "[";

            for(int i = 0; i < DEFAULT_CAPACITY; i++){
                if (count[i] > 0){
                    for(int j = 0; j < count[i]; j++){
                        result += (char) ('a' + i);
                    }
                }
            }
            return result + "]";
        }
    }

    public LetterInventory add(LetterInventory other){
        LetterInventory add = new LetterInventory();
        for (int i = 0; i < DEFAULT_CAPACITY; i++){
            add.count[i] = count[i] + other.count[i];
        }
        add.size = size + other.size;
        return add;
    }

    public LetterInventory subtract(LetterInventory other){
        LetterInventory subtract = new LetterInventory();
        for (int i = 0; i < DEFAULT_CAPACITY; i++){
            subtract.count[i] = count[i] - other.count[i];
            if (subtract.count[i] < 0){
                return null;
            }
        }
        subtract.size = size - other.size;
        return subtract;
    }

    private void checkAlphabetic(char letter) {
        if (letter - 'a' < 0 || letter - 'a' >= DEFAULT_CAPACITY){
            throw new IllegalArgumentException();
        }
    }
}