class RefactorFunctionPrompts:
    @staticmethod
    def refactor_function(source_code, start_line, end_line):
        return (
            f"Please refactor the function in the following Python code. "
            f"Make sure the refactored function starts from line {start_line} "
            f"and ends at line {end_line}. Apply best coding practices and "
            f"improve the code structure without changing the functionality.\n\n"
            f"{source_code}"
        )
