import java.util.List;
import java.util.ArrayList;

public class TestClass {
    private List<String> items;
    private String name;
    private volatile boolean running = true;

    public TestClass() {
        this.items = new ArrayList<>();
        this.name = "test";
    }

    public void addItem(String item) {
        this.items.add(item);
    }

    public void deprecatedMethod() {
        // Properly terminate the thread using cooperative termination
        running = false;
        System.out.println("Thread termination requested");
    }

    public boolean isRunning() {
        return running;
    }

    public static void main(String[] args) {
        TestClass obj = new TestClass();
        obj.addItem("hello");
        obj.deprecatedMethod();
    }
}
