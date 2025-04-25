import sys
import traceback

class CustomException(Exception):
    """
    A custom exception that provides detailed error information,
    including the file name and line number where the error occurred.
    """

    def __init__(self, error_message: str, error_detail: sys):
        """
        Initializes the CustomException with a detailed error message.

        Parameters:
        - error_message: A short description of the error.
        - error_detail: Should be the 'sys' module to extract traceback info.
        """
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_detail)

    @staticmethod
    def get_detailed_error_message(error_message: str, error_detail: sys) -> str:
        """
        Builds a detailed error message using traceback information.

        Returns:
        - A string with file name, line number, and the original message.
        """
        exc_type, exc_value, exc_tb = error_detail.exc_info()
        if exc_tb is not None:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
            return f"Error in {file_name}, line {line_number}: {error_message}"
        else:
            return f"Error (no traceback available): {error_message}"

    def __str__(self) -> str:
        """
        Returns the detailed error message when the exception is printed.
        """
        return self.error_message