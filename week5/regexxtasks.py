import re


# 1. Match a string that has 'a' followed by 0 or more 'b'
def task1():
    print("1️ 'a' followed by 0 or more 'b'")
    pattern = r"^ab*$"
    tests = ["a", "ab", "abb", "abbb", "ac"]

    for s in tests:
        if re.match(pattern, s):
            print(s, "-> match")
    print()


# 2. Match 'a' followed by 2 to 3 'b'
def task2():
    print("2️ 'a' followed by 2-3 'b'")
    pattern = r"^ab{2,3}$"
    tests = ["ab", "abb", "abbb", "abbbb"]

    for s in tests:
        if re.match(pattern, s):
            print(s, "-> match")
    print()


# 3. Find sequences of lowercase letters joined with underscore
def task3():
    print("3️ lowercase_words_with_underscore")
    text = "hello_world test_string Hello_World"
    pattern = r"\b[a-z]+_[a-z]+\b"

    print(re.findall(pattern, text))
    print()


# 4. Find sequences of one uppercase letter followed by lowercase letters
def task4():
    print("4️ One uppercase followed by lowercase letters")
    text = "London PARIS Astana Almaty"
    pattern = r"\b[A-Z][a-z]+\b"

    print(re.findall(pattern, text))
    print()


# 5. Match a string that starts with 'a' and ends with 'b'
def task5():
    print("5️ Starts with 'a' and ends with 'b'")
    pattern = r"^a.*b$"
    tests = ["ab", "acb", "a123b", "abc"]

    for s in tests:
        if re.match(pattern, s):
            print(s, "-> match")
    print()


# 6. Replace space, comma, or dot with colon
def task6():
    print("6️ Replace space, comma, or dot with ':'")
    text = "Hello, world. Python is cool"
    result = re.sub(r"[ ,\.]", ":", text)

    print(result)
    print()


# 7. Convert snake_case to camelCase
def snake_to_camel(text):
    parts = text.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


def task7():
    print("7️ snake_case → camelCase")
    print(snake_to_camel("hello_world_test"))
    print()


# 8. Split a string at uppercase letters
def task8():
    print("8️ Split at uppercase letters")
    text = "HelloWorldPython"
    result = re.findall(r"[A-Z][^A-Z]*", text)

    print(result)
    print()


# 9. Insert spaces between words starting with capital letters
def task9():
    print("9️ Insert spaces before capital letters")
    text = "HelloWorldPython"
    result = re.sub(r"(?<!^)(?=[A-Z])", " ", text)

    print(result)
    print()


# 10. Convert camelCase to snake_case
def camel_to_snake(text):
    result = re.sub(r"(?<!^)(?=[A-Z])", "_", text)
    return result.lower()


def task10():
    print("10 camelCase → snake_case")
    print(camel_to_snake("helloWorldTest"))
    print()


# Run all tasks
if __name__ == "__main__":
    task1()
    task2()
    task3()
    task4()
    task5()
    task6()
    task7()
    task8()
    task9()
    task10()