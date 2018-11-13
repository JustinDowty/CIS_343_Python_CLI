class CLI_Audio_Exception(Exception):
    """Parent Class for CLI Audio Exceptions"""
    pass

class CLI_Small_Screen_Exception(CLI_Audio_Exception):
    """Exception for when the user's screen size is too small to view application"""
    pass

class CLI_File_Not_Found_Exception(CLI_Audio_Exception):
    """Exception for when the user chooses a file path that does not exist"""
    pass
