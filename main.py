import re

# Regex Engine to tie everything together
class RegexEngine:
    def __init__(self, pattern):
        # Compile the provided regex pattern for matching
        self.pattern = re.compile(pattern)

    def match(self, text):
        # Use the fullmatch method to check if the entire string matches the pattern
        return bool(self.pattern.fullmatch(text))

# User input function
def user_input_regex_engine():
    while True:
        # Prompt user for regex and string
        pattern = input("Enter a regex pattern (or 'exit' to quit): ")
        if pattern.lower() == 'exit':
            break

        string_to_match = input("Enter a string to match: ")

        # Create the regex engine and check for a match
        engine = RegexEngine(pattern)
        result = engine.match(string_to_match)

        # Print the result
        if result:
            print(f'The string "{string_to_match}" matches the regex "{pattern}".')
        else:
            print(f'The string "{string_to_match}" does not match the regex "{pattern}".')

# Testing the regex engine
def test_regex_engine():
    test_cases = [
        # Phone Number Test Cases
        (r'(\+?1[-.\s]?)?(\(?\d{3}\)?)[-.\s]?\d{3}[-.\s]?\d{4}', "(123) 456-7890", True),
        (r'(\+?1[-.\s]?)?(\(?\d{3}\)?)[-.\s]?\d{3}[-.\s]?\d{4}', "123-456-7890", True),
        (r'(\+?1[-.\s]?)?(\(?\d{3}\)?)[-.\s]?\d{3}[-.\s]?\d{4}', "123-45-67890", False),
        (r'(\+?1[-.\s]?)?(\(?\d{3}\)?)[-.\s]?\d{3}[-.\s]?\d{4}', "12a-456-7890", False),

        # Email Address Test Cases
        (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', "test@example.com", True),
        (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', "user.name+alias@domain.co", True),
        (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', "test@.com", False),
        (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', "test.com", False),

        # URL Test Cases
        (r'((http|https):\/\/)?(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}([\/a-zA-Z0-9#-]*)', "http://example.com", True),
        (r'((http|https):\/\/)?(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}([\/a-zA-Z0-9#-]*)', "www.example.org", True),
        (r'((http|https):\/\/)?(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}([\/a-zA-Z0-9#-]*)', "htp://domain.com", False),
        (r'((http|https):\/\/)?(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}([\/a-zA-Z0-9#-]*)', "examplecom", False),

        # ZIP Code Test Cases
        (r'\d{5}(-\d{4})?', "12345", True),
        (r'\d{5}(-\d{4})?', "12345-6789", True),
        (r'\d{5}(-\d{4})?', "1234", False),
        (r'\d{5}(-\d{4})?', "123456", False),
    ]

    for pattern, input_str, expected in test_cases:
        engine = RegexEngine(pattern)
        result = engine.match(input_str)
        assert result == expected, f'Failed for pattern: {pattern}, input: {input_str}'

    print("All tests passed!")

# Run the tests
test_regex_engine()

# Start the user input loop
user_input_regex_engine()
