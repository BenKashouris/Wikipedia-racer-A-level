import re
_USERNAME_AND_PASSWORD_REGEX = re.compile(r"""([a-z]|[0-9]|[A-Z])+""")
def _valid_username_or_password(test_string: str) -> bool:
    """Test if a string is a valid username/password
         Rules: Must consist only of lowercase or uppercase letter or number and must be less than 33 characters
         Parameter: test_string: the string to test
         Returns: True or False"""
    return re.fullmatch(_USERNAME_AND_PASSWORD_REGEX, test_string) != None and len(test_string) < 33
