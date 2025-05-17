from StudiiFezabilitate.Avize.functii import check_required_fields
import sys
import os
from StudiiFezabilitate.result import DocumentGenerationResult
sys.path.append('e:/NEW_python/RGT')

# Create an output file
with open(os.path.join(os.path.dirname(__file__), 'test_output.txt'), 'w') as f:
    # Test with None value
    result1 = check_required_fields([(None, "Test error message for None")])
    f.write(
        f"Test with None value: {'Error returned' if result1 else 'No error returned'}\n")
    f.write(f"Result1 type: {type(result1)}, value: {result1}\n")

    # Test with empty string
    result2 = check_required_fields(
        [("", "Test error message for empty string")])
    f.write(
        f"Test with empty string: {'Error returned' if result2 else 'No error returned'}\n")
    f.write(f"Result2 type: {type(result2)}, value: {result2}\n")

    # Test with zero
    result3 = check_required_fields([(0, "Test error message for zero")])
    f.write(
        f"Test with zero value: {'Error returned' if result3 else 'No error returned'}\n")
    f.write(f"Result3 type: {type(result3)}, value: {result3}\n")

    # Test with float zero
    result4 = check_required_fields(
        [(0.0, "Test error message for float zero")])
    f.write(
        f"Test with float zero value: {'Error returned' if result4 else 'No error returned'}\n")
    f.write(f"Result4 type: {type(result4)}, value: {result4}\n")

    # Check the actual implementation of check_required_fields
    f.write("\nSource code of check_required_fields:\n")
    import inspect
    f.write(inspect.getsource(check_required_fields))
