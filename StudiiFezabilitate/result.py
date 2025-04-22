class DocumentGenerationResult:
    """
    A class to represent the result of a document generation operation.

    This class allows for consistent handling of both successful operations and errors,
    making it easier to propagate error information through the application.
    """

    def __init__(self, success=True, files=None, error_message=None):
        """
        Initialize a document generation result.

        Args:
            success (bool): Whether the generation was successful
            files (list): List of generated file paths (for successful operations)
            error_message (str): Error message (for failed operations)
        """
        self.success = success
        self.files = files or []
        self.error_message = error_message

    @classmethod
    def success_result(cls, files):
        """
        Create a success result with generated files.

        Args:
            files: A list of file paths or a single file path

        Returns:
            DocumentGenerationResult: A successful result
        """
        if isinstance(files, str):
            files = [files]  # Convert single path to list
        return cls(success=True, files=files)

    @classmethod
    def error_result(cls, error_message):
        """
        Create an error result with the specified error message.

        Args:
            error_message: The error message

        Returns:
            DocumentGenerationResult: An error result
        """
        return cls(success=False, error_message=error_message)

    def is_success(self):
        """Check if the operation was successful."""
        return self.success

    def get_files(self):
        """Get list of generated files (empty list if error)."""
        return self.files

    def get_error(self):
        """Get error message (None if success)."""
        return self.error_message

    def add_file(self, file_path):
        """Add a file path to the result."""
        if file_path:
            self.files.append(file_path)

    def __bool__(self):
        """Allow using the result object in boolean contexts."""
        return self.success
