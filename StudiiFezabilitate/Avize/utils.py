import os
from django.db.models.fields.files import FieldFile
from StudiiFezabilitate.result import DocumentGenerationResult


def safe_access_file_path(file_field, error_msg=None, raise_error=False):
    """
    Safely access the path attribute of a file field.
    Returns the path if the file exists, or None if it doesn't.
    This avoids the 'The X attribute has no file associated with it' error.
    
    Args:
        file_field: The file field to check.
        error_msg: Optional error message to return as a DocumentGenerationResult if file doesn't exist.
        raise_error: If True, raise a ValueError with the error message instead of returning None.
    
    Returns:
        - The file path if the file exists
        - DocumentGenerationResult with error if error_msg is provided and file doesn't exist
        - None if the file doesn't exist and no error options are provided
    """
    if file_field and hasattr(file_field, 'path'):
        try:
            return file_field.path
        except Exception as e:
            if error_msg:
                if raise_error:
                    raise ValueError(error_msg)
                return DocumentGenerationResult.error_result(error_msg)
            return None
    else:
        if error_msg:
            if raise_error:
                raise ValueError(error_msg)
            return DocumentGenerationResult.error_result(error_msg)
        return None

# Example usage:
# Instead of: cu.cale_CU.path
# Use: safe_access_file_path(cu.cale_CU)
# 
# With error handling:
# path = safe_access_file_path(cu.cale_CU, "Certificatul de Urbanism lipsește!")
# if isinstance(path, DocumentGenerationResult):
#     return path  # Return the error result
