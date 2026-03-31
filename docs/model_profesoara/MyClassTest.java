/*
Graful asociat programului poate fi vizualizat prin intermediul site-ului:
https://app.code2flow.com
In folderul Materiale exista 2. CFG_Proiect_v2.png

Despre plugin-ul de generare a mutantilor in Java, dar si despre
libraria SystemOutRule mai multe detalii in fisierul pluginuri_utile_Java.
*/

package pachet2;

//import org.junit.Test;
//import static org.junit.Assert.assertEquals;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

//import org.junit.Rule;
//import org.junit.contrib.java.lang.system.SystemOutRule;

import static com.github.stefanbirkner.systemlambda.SystemLambda.tapSystemOut;

import pachet1.MyClass;

public class MyClassTest {
    MyClass tester = new MyClass();

    /*
     * @Rule
     * public final SystemOutRule systemOutRule = new SystemOutRule().enableLog();
     */
    @Test
    public void testMain() {
        tester.find(3, "abc", 'd', 'n');
    }

    @Test
    public void equivalencePartitioning() {
        tester.find(0, "", 'a', 'y');
        tester.find(25, "", 'a', 'y');
        tester.find(3, "abc", 'a', 'y');
        tester.find(3, "abc", 'a', 'n');
        tester.find(3, "abc", 'd', 'y');
        tester.find(3, "abc", 'd', 'n');
    }

    @Test
    public void boundaryValueAnalysis() {
        tester.find(0, "", 'a', 'y');
        tester.find(21, "", 'a', 'y');
        tester.find(1, "a", 'a', 'y');
        tester.find(1, "a", 'a', 'n');
        tester.find(1, "a", 'b', 'y');
        tester.find(1, "a", 'b', 'n');
        tester.find(20, "abcdefghijklmnoprstu", 'a', 'y');
        tester.find(20, "abcdefghijklmnoprstu", 'a', 'n');
        tester.find(20, "abcdefghijklmnoprstu", 'u', 'y');
        tester.find(20, "abcdefghijklmnoprstu", 'u', 'n');
        tester.find(20, "abcdefghijklmnoprstu", 'z', 'y');
        tester.find(20, "abcdefghijklmnoprstu", 'z', 'n');
    }

    @Test
    public void categoryPartitioning() {
        tester.find(-5, "", 'a', 'y');
        tester.find(0, "", 'a', 'y');
        tester.find(21, "", 'a', 'y');
        tester.find(25, "", 'a', 'y');
        tester.find(1, "a", 'a', 'y');
        tester.find(1, "a", 'a', 'n');
        tester.find(1, "a", 'b', 'y');
        tester.find(1, "a", 'b', 'n');
        tester.find(3, "abc", 'a', 'y');
        tester.find(3, "abc", 'a', 'n');
        tester.find(3, "abc", 'b', 'y');
        tester.find(3, "abc", 'b', 'n');
        tester.find(3, "abc", 'c', 'y');
        tester.find(3, "abc", 'c', 'n');
        tester.find(3, "abc", 'd', 'y');
        tester.find(3, "abc", 'd', 'n');
        tester.find(20, "abcdefghijklmnoprstu", 'a', 'y');
        tester.find(20, "abcdefghijklmnoprstu", 'a', 'n');
        tester.find(20, "abcdefghijklmnoprstu", 'c', 'y');
        tester.find(20, "abcdefghijklmnoprstu", 'c', 'n');
        tester.find(20, "abcdefghijklmnoprstu", 'u', 'y');
        tester.find(20, "abcdefghijklmnoprstu", 'u', 'n');
        tester.find(20, "abcdefghijklmnoprstu", 'z', 'y');
        tester.find(20, "abcdefghijklmnoprstu", 'z', 'n');
    }

    @Test
    public void statementCoverage() {
        tester.find(0, "", 'd', 'y');
        tester.find(1, "a", 'a', 'y');
        tester.find(1, "a", 'b', 'n');
    }

    @Test
    public void branchCoverage() {
        tester.find(0, "", 'd', 'y');
        tester.find(1, "a", 'a', 'y');
        tester.find(1, "a", 'b', 'n');
    }

    @Test
    public void conditionCoverage() {
        tester.find(0, "", 'd', 'y');
        tester.find(25, "", 'd', 'y');
        tester.find(1, "a", 'a', 'y');
        tester.find(1, "a", 'b', 'n');
    }

    @Test
    public void circuitsCoverage() {
        tester.find(0, "", 'd', 'y');
        tester.find(1, "a", 'a', 'y');
        tester.find(1, "a", 'b', 'n');
    }

    /*
     * Mutation coverage before running tests from killMutants 19% sau 3/16
     * Mutation coverage after running only test MyClass.find(20,"a",'a','y') from
     * killMutants 25% sau 4/16
     * este distins mutantul negated conditional la linia 12: if(x.charAt(i) == c)
     * Mutation coverage after running tests including killMutants 100% sau 16/16
     */

    /*
     * @Test
     * public void killMutants() {
     * 
     * tester.find(1,"a",'a', 'y');
     * tester.find(0,"a",'a', 'y');
     * tester.find(1, "a", 'b', 'n');
     * tester.find(20,"a",'a', 'y');
     * 
     * assertEquals("Character a appears at position 1.\nInput character to search for.\n\n"
     * +
     * "Input integer between 1 and 20.\n\n"+
     * "Character b does not appear in the string.\n\n"+
     * "Character a appears at position 1.\nInput character to search for.\n\n",
     * systemOutRule.getLogWithNormalizedLineSeparator());
     * }
     */

    @Test
    void killMutants_junit5() throws Exception {
        String text = tapSystemOut(() -> {
            tester.find(1, "a", 'a', 'y');
            tester.find(0, "a", 'a', 'y');
            tester.find(1, "a", 'b', 'n');
            tester.find(20, "a", 'a', 'y');
        });

        assertEquals("Character a appears at position 1.\nInput character to search for.\n\n" +
                "Input integer between 1 and 20.\n\n" +
                "Character b does not appear in the string.\n\n" +
                "Character a appears at position 1.\nInput character to search for.\n\n", text);
    }

}
