def multiply(x, y):
    """Multiply two numbers"""
    return x * y

def greet(name):
    """Greet a person"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    result = multiply(5, 3)
    message = greet("World")
    print(f"{message} Result: {result}")