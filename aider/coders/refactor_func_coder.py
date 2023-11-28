from aider.coders.base_coder import Coder

class RefactorFunctionCoder(Coder):
    def generate_prompt(self, source_file, start_line, end_line):
        # This method will generate the prompt for the model
        prompt = f"Refactor the function in the following Python code starting from line {start_line} to line {end_line}:\n\n"
        prompt += source_file
        return prompt

    def process_response(self, response):
        # This method will process the response from the model
        # and return the refactored code or necessary edits
        # For now, we will just return the response as is
        return response
