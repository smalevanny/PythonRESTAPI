class TestPhrase:
    def test_phrase(self):
        max_length = 15
        phrase = input(f"Set a phrase with a lenth less than {max_length} symbols: ")
        assert len(phrase) < max_length, f"Length of your phrase has to be less than {max_length}"