import re

# This class takes a regex pattern and breaks it down into smaller pieces, or tokens.
class Tokenizer:
    def __init__(self, pattern):
        # Save the pattern and start at the beginning
        self.pattern = pattern
        self.position = 0

    def next_token(self):
        # If we've reached the end of the pattern, there's nothing left to tokenize
        if self.position >= len(self.pattern):
            return None

        # Get the current character and move to the next one
        char = self.pattern[self.position]
        self.position += 1

        # If the character is one of the special regex symbols, return it as is
        if char in '()*+?.':
            return char
        else:
            # Otherwise, return it as a character token
            return ('CHAR', char)

    def peek(self):
        # Look at the next character without moving the position
        if self.position < len(self.pattern):
            return self.pattern[self.position]
        return None

# This class represents a node that matches either a specific character or any character (using '.')
class CharNode:
    def __init__(self, char):
        # Store the character this node is supposed to match
        self.char = char

    def match(self, text, pos):
        # Check if we're within the bounds of the text
        if pos < len(text):
            # If the character in the text matches this node's character,
            # or if this node is a wildcard ('.'), we found a match
            if text[pos] == self.char or self.char == '.':
                return pos + 1  # Return the next position for further matching
        # If there's no match, return -1 to indicate failure
        return -1


# AST Node for '*' operator (zero or more of the preceding element)
class StarNode:
    def __init__(self, child):
        self.child = child

    def match(self, text, pos):
        match_pos = pos
        while True:
            next_pos = self.child.match(text, match_pos)
            if next_pos == -1:
                break
            match_pos = next_pos
        return match_pos

# AST Node for '+' operator (one or more of the preceding element)
class PlusNode:
    def __init__(self, child):
        self.child = child

    def match(self, text, pos):
        match_pos = self.child.match(text, pos)
        if match_pos == -1:
            return -1

        while True:
            next_pos = self.child.match(text, match_pos)
            if next_pos == -1:
                break
            match_pos = next_pos

        return match_pos

# AST Node for '?' operator (zero or one of the preceding element)
class QuestionNode:
    def __init__(self, child):
        self.child = child

    def match(self, text, pos):
        next_pos = self.child.match(text, pos)
        if next_pos != -1:
            return next_pos
        return pos
# AST Node for matching any character '.'
class DotNode:
    def match(self, text, pos):
        if pos < len(text):
            return pos + 1
        return -1

# AST Node for matching start of the string '^'
class StartAnchorNode:
    def match(self, text, pos):
        return pos if pos == 0 else -1

# AST Node for matching end of the string '$'
class EndAnchorNode:
    def match(self, text, pos):
        return pos if pos == len(text) else -1

# AST Node for matching a sequence of nodes
class SequenceNode:
    def __init__(self):
        #Empty list for child nodes
        self.children = []

    def add_child(self, child):
        # add child node to list of children
        self.children.append(child)

    def match(self, text, pos):
        current_pos = pos  # Stores current position of input text
        for child in self.children:
            # Match current child node w/ text
            next_pos = child.match(text, current_pos)
            if next_pos == -1:  # Match fails -1 failure
                return -1
            current_pos = next_pos  # Update position
        return current_pos

# Parser to build the Abstract Syntax Tree (AST) from the tokens
class Parser:
    def __init__(self, tokenizer):
        # Initialize the parser with a tokenizer to process regex tokens
        self.tokenizer = tokenizer

    def parse(self):
        # Start the parsing process by calling parse_sequence
        return self.parse_sequence()

    def parse_sequence(self):
        # Create a new SequenceNode to hold the sequence of matched nodes (regex characters)
        sequence_node = SequenceNode()

        while True:
            token = self.tokenizer.next_token()
            # If there are no more tokens, exit the loop
            if not token:
                break

            if isinstance(token, tuple):
                token_value = token[1]
            else:
                token_value = token

            if token_value in '|)':
                break

            # Handle the opening parenthesis for grouped expressions
            if token_value == '(':
                child = self.parse_sequence()
                # If the next token is a closing parenthesis, consume it
                if self.tokenizer.peek() == ')':
                    self.tokenizer.position += 1  # Consume ')'
                sequence_node.add_child(child)
            # Wild Card
            elif token_value == '.':
                sequence_node.add_child(DotNode())
            # Start Anchor
            elif token_value == '^':
                sequence_node.add_child(StartAnchorNode())
            # End Anchor
            elif token_value == '$':
                sequence_node.add_child(EndAnchorNode())

            else:
                # Create a CharNode for regular characters
                char_node = CharNode(token[1]) if isinstance(token, tuple) else CharNode(token)
                # Check the next token for a modifier (like *, +, or ?)
                modifier = self.tokenizer.peek()

                # If the modifier is '*', create a StarNode for zero or more occurrences
                if modifier == '*':
                    self.tokenizer.position += 1  # Consume '*'
                    sequence_node.add_child(StarNode(char_node))
                # If the modifier is '+', create a PlusNode for one or more occurrences
                elif modifier == '+':
                    self.tokenizer.position += 1  # Consume '+'
                    sequence_node.add_child(PlusNode(char_node))
                # If the modifier is '?', create a QuestionNode for zero or one occurrence
                elif modifier == '?':
                    self.tokenizer.position += 1  # Consume '?'
                    sequence_node.add_child(QuestionNode(char_node))
                else:
                    # No modifier; just add the character node to the sequence
                    sequence_node.add_child(char_node)

        return sequence_node


# Regex Engine to tie everything together
class RegexEngine:
    def __init__(self, pattern):
        # Store the provided regex pattern for later use in matching
        self.pattern = pattern

    def match(self, text):
        # Create a tokenizer that breaks the pattern into manageable tokens
        tokenizer = Tokenizer(self.pattern)

        # Create a parser that will convert the tokens into an Abstract Syntax Tree (AST)
        parser = Parser(tokenizer)

        # Parse the tokenized pattern into an AST structure
        ast = parser.parse()

        # Attempt to match the entire text against the AST starting from position 0
        # If the match is successful and encapsulates the entire text, return True
        return ast.match(text, 0) == len(text)


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
    # Pattern: "a*b" -> zero or more 'a's followed by exactly one 'b'
    engine = RegexEngine("a*b")

    # Test 1: "b" should match "a*b"
    # Explanation: 'a*' allows zero 'a's, so "b" matches as no 'a' is required before the 'b'.
    result = engine.match("b")
    print(f'Test 1 - Pattern: "a*b", Input: "b", Expected: True, Got: {result}')
    assert result == True

    # Test 2: "ab" should match "a*b"
    # Explanation: 'a*' allows one or more 'a's, and the pattern is followed by a single 'b'.
    result = engine.match("ab")
    print(f'Test 2 - Pattern: "a*b", Input: "ab", Expected: True, Got: {result}')
    assert result == True

    # Test 3: "aab" should match "a*b"
    # Explanation: 'a*' allows two 'a's followed by exactly one 'b'.
    result = engine.match("aab")
    print(f'Test 3 - Pattern: "a*b", Input: "aab", Expected: True, Got: {result}')
    assert result == True

    # Test 4: "aac" should NOT match "a*b"
    # Explanation: 'a*' matches two 'a's, but the pattern requires a 'b' at the end, and the input ends with 'c'.
    result = engine.match("aac")
    print(f'Test 4 - Pattern: "a*b", Input: "aac", Expected: False, Got: {result}')
    assert result == False

    # Pattern: "a+b" -> one or more 'a's followed by exactly one 'b'
    engine = RegexEngine("a+b")

    # Test 5: "b" should NOT match "a+b"
    # Explanation: 'a+' requires at least one 'a', but there is no 'a' in the input.
    result = engine.match("b")
    print(f'Test 5 - Pattern: "a+b", Input: "b", Expected: False, Got: {result}')
    assert result == False

    # Test 6: "ab" should match "a+b"
    # Explanation: 'a+' matches one 'a', followed by exactly one 'b'.
    result = engine.match("ab")
    print(f'Test 6 - Pattern: "a+b", Input: "ab", Expected: True, Got: {result}')
    assert result == True

    # Test 7: "aab" should match "a+b"
    # Explanation: 'a+' matches two 'a's (one or more 'a's), followed by exactly one 'b'.
    result = engine.match("aab")
    print(f'Test 7 - Pattern: "a+b", Input: "aab", Expected: True, Got: {result}')
    assert result == True

    # Pattern: "a?b" -> zero or one 'a' followed by exactly one 'b'
    engine = RegexEngine("a?b")

    # Test 8: "b" should match "a?b"
    # Explanation: 'a?' allows zero 'a's, so "b" matches with no 'a' required before the 'b'.
    result = engine.match("b")
    print(f'Test 8 - Pattern: "a?b", Input: "b", Expected: True, Got: {result}')
    assert result == True

    # Test 9: "ab" should match "a?b"
    # Explanation: 'a?' allows one 'a', and the 'b' matches exactly.
    result = engine.match("ab")
    print(f'Test 9 - Pattern: "a?b", Input: "ab", Expected: True, Got: {result}')
    assert result == True

    # Test 10: "aab" should NOT match "a?b"
    # Explanation: 'a?' only allows zero or one 'a', but there are two 'a's in the input.
    result = engine.match("aab")
    print(f'Test 10 - Pattern: "a?b", Input: "aab", Expected: False, Got: {result}')
    assert result == False
    # New test cases for additional features
    engine = RegexEngine("a.b")

    # Test 11: "acb" should match "a.b"
    # Explanation: '.' matches any character between 'a' and 'b'.
    result = engine.match("acb")
    print(f'Test 11 - Pattern: "a.b", Input: "acb", Expected: True, Got: {result}')
    assert result == True

    # Test 12: "ab" should NOT match "a.b"
    # Explanation: '.' expects one character between 'a' and 'b', but there isn't any.
    result = engine.match("ab")
    print(f'Test 12 - Pattern: "a.b", Input: "ab", Expected: False, Got: {result}')
    assert result == False

    engine = RegexEngine("^ab")

    # Test 13: "ab" should match "^ab"
    # Explanation: '^' anchors the pattern to the start of the string.
    result = engine.match("ab")
    print(f'Test 13 - Pattern: "^ab", Input: "ab", Expected: True, Got: {result}')
    assert result == True

    # Test 14: "cab" should NOT match "^ab"
    # Explanation: '^' requires 'ab' to be at the start of the string.
    result = engine.match("cab")
    print(f'Test 14 - Pattern: "^ab", Input: "cab", Expected: False, Got: {result}')
    assert result == False

    engine = RegexEngine("ab$")

    # Test 15: "ab" should match "ab$"
    # Explanation: '$' anchors the pattern to the end of the string.
    result = engine.match("ab")
    print(f'Test 15 - Pattern: "ab$", Input: "ab", Expected: True, Got: {result}')
    assert result == True

    # Test 16: "abc" should NOT match "ab$"
    # Explanation: '$' requires 'ab' to be at the end of the string.
    result = engine.match("abc")
    print(f'Test 16 - Pattern: "ab$", Input: "abc", Expected: False, Got: {result}')
    assert result == False

    print("Now for more complex test cases:")




    # Pattern: "a*b.c+"
    engine = RegexEngine("a*b.c+")

    # Test 1: "aab1c" should match "a*b.c+"
    result = engine.match("aab1c")
    print(f'Test 1 - Pattern: "a*b.c+", Input: "aab1c", Expected: True, Got: {result}')
    assert result == True

    ''' FOR FUTURE META
    # Pattern: "^x?(y|z)*a.*"
    engine = RegexEngine("^x?(y|z)*a.*")

    # Test 2: "xyzabc" should match "^x?(y|z)*a.*"
    result = engine.match("xyzabc")
    print(f'Test 2 - Pattern: "^x?(y|z)*a.*", Input: "xyzabc", Expected: True, Got: {result}')
    assert result == True

    # Test 3: "xyz" should NOT match "^x?(y|z)*a.*"
    result = engine.match("xyz")
    print(f'Test 4 - Pattern: "^x?(y|z)*a.*", Input: "xyz", Expected: False, Got: {result}')
    assert result == False
    '''
    # Pattern: "a+b?c*"
    engine = RegexEngine("a+b?c*")

    # Test 2: "aaabc" should match "a+b?c*"
    result = engine.match("aaabc")
    print(f'Test 2 - Pattern: "a+b?c*", Input: "aaabc", Expected: True, Got: {result}')
    assert result == True

    # Test 3: "aabbc" should NOT match "a+b?c*"
    result = engine.match("aabbc")
    print(f'Test 3 - Pattern: "a+b?c*", Input: "aab", Expected: False, Got: {result}')
    assert result == False

    ''' NOT DONE NEED TO IMPLEMENT [] 0-9 a-z A-Z | into code logic
    # Pattern: ".*[0-9]+[a-zA-Z]$"
    engine = RegexEngine(".*[0-9]+[a-zA-Z]$")

    # Test 4: "The price is 20d" should match ".*[0-9]+[a-zA-Z]$"
    result = engine.match("The price is 20d")
    print(f'Test 4 - Pattern: ".*[0-9]+[a-zA-Z]$", Input: "The price is 20d", Expected: True, Got: {result}')
    assert result == True

    # Test 7: "Your score is 45 " should NOT match ".*[0-9]+[a-zA-Z]$"
    result = engine.match("Your score is 45 ")
    print(f'Test 8 - Pattern: ".*[0-9]+[a-zA-Z]$", Input: "Your score is 45 ", Expected: False, Got: {result}')
    assert result == False
    print("All tests passed!")
    '''
# Run the tests
test_regex_engine()
# Start the user input loop
user_input_regex_engine()