class TestClass:
    def __init__(self):
        self.value = 42

    def get_value(self):
        return self.value

def main():
    obj = TestClass()
    print(f"Value: {obj.get_value()}")

if __name__ == "__main__":
    main()
