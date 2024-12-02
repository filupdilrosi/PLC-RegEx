import re


# Regex Engine to tie everything together
class RegexEngine:
    def __init__(self, pattern):
        # Compile the provided regex pattern for matching
        self.pattern = re.compile(pattern)

    def match(self, text):
        # Use the fullmatch method to check if the entire string matches the pattern
        return bool(self.pattern.fullmatch(text))


def generate_regex_for_string(input_string):
    """
    Generate a regex to match common formats like emails, URLs, phone numbers, and ZIP codes.
    """
    # Check for URL patterns
    if input_string.startswith("http://") or input_string.startswith("https://") or "www." in input_string:
        return r'(http|https):\/\/(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}([\/a-zA-Z0-9#-]*)?'

    # Check for email address patterns
    elif "@" in input_string and "." in input_string:
        return r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    # Check for phone number patterns
    elif re.match(r'[\d\s\(\)-]{10,}', input_string):  # Basic phone number structure
        return r'(\+?1[-.\s]?)?(\(?\d{3}\)?)[-.\s]?\d{3}[-.\s]?\d{4}'

    # Check for ZIP code patterns
    elif re.match(r'\d{5}(-\d{4})?', input_string):
        return r'\d{5}(-\d{4})?'

    # Default fallback: simple alphanumeric regex
    else:
        regex_parts = []
        for char in input_string:
            if char.isdigit():
                regex_parts.append(r'\d')
            elif char.isalpha():
                regex_parts.append(r'[a-zA-Z]')
            elif char.isspace():
                regex_parts.append(r'\s')
            else:
                regex_parts.append(re.escape(char))
        return ''.join(regex_parts)


# User input function
def user_input_regex_engine():
    while True:
        print("\nOptions:\n1. Match a string with a regex\n2. Generate regex for a string\n3. Exit")
        choice = input("Select an option (1/2/3): ")

        if choice == '3':  # Exit option
            print("Goodbye!")
            break

        elif choice == '1':  # Matching functionality
            pattern = input("Enter a regex pattern: ")
            string_to_match = input("Enter a string to match: ")
            engine = RegexEngine(pattern)
            result = engine.match(string_to_match)

            if result:
                print(f'The string "{string_to_match}" matches the regex "{pattern}".')
            else:
                print(f'The string "{string_to_match}" does not match the regex "{pattern}".')

        elif choice == '2':  # Regex generation functionality
            print("\nEnter a string in one of the following formats:")
            print(" - URL (e.g., https://example.com)")
            print(" - Email (e.g., user@example.com)")
            print(" - Phone number (e.g., (123) 456-7890)")
            print(" - ZIP code (e.g., 12345 or 12345-6789)")
            user_string = input("\nEnter your string: ")

            generated_regex = generate_regex_for_string(user_string)
            print(f"\nGenerated regex for the input string: {generated_regex}")

        else:  # Invalid option
            print("Invalid choice. Please enter 1, 2, or 3.")


# Testing the regex engine
def test_regex_engine():
    test_cases = [
        # URLs
        (r'(http|https):\/\/(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}([\/a-zA-Z0-9#-]*)?', "https://example.com", True),
        (r'(http|https):\/\/(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}([\/a-zA-Z0-9#-]*)?', "http://example.org/test", True),

        # Emails
        (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', "test@example.com", True),
        (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', "user.name+alias@domain.co", True),

        # Phone numbers
        (r'(\+?1[-.\s]?)?(\(?\d{3}\)?)[-.\s]?\d{3}[-.\s]?\d{4}', "(123) 456-7890", True),
        (r'(\+?1[-.\s]?)?(\(?\d{3}\)?)[-.\s]?\d{3}[-.\s]?\d{4}', "123-456-7890", True),

        # ZIP codes
        (r'\d{5}(-\d{4})?', "12345", True),
        (r'\d{5}(-\d{4})?', "12345-6789", True),
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
