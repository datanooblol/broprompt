from typing import List, Dict, Any, Optional


class Example:
    """Single example for few-shot learning"""
    
    def __init__(self, input_text: str, output_text: str, metadata: Optional[Dict] = None):
        self.input = input_text
        self.output = output_text
        self.metadata = metadata or {}
    
    def format(self, input_label: str = "Input", output_label: str = "Output") -> str:
        """Format example as text"""
        return f"{input_label}: {self.input}\n{output_label}: {self.output}"


class FewShot:
    """Few-shot learning prompt builder"""
    
    def __init__(self):
        self.examples: List[Example] = []
        self.instruction = ""
        self.input_label = "Input"
        self.output_label = "Output"
    
    def add_example(self, input_text: str, output_text: str, metadata: Optional[Dict] = None) -> 'FewShot':
        """Add an example"""
        self.examples.append(Example(input_text, output_text, metadata))
        return self
    
    def add_examples(self, examples: List[Dict[str, str]]) -> 'FewShot':
        """Add multiple examples from list of dicts"""
        for ex in examples:
            self.add_example(ex["input"], ex["output"], ex.get("metadata"))
        return self
    
    def set_instruction(self, instruction: str) -> 'FewShot':
        """Set the instruction/task description"""
        self.instruction = instruction
        return self
    
    def set_labels(self, input_label: str, output_label: str) -> 'FewShot':
        """Set custom labels for input/output"""
        self.input_label = input_label
        self.output_label = output_label
        return self
    
    def build(self, query: str = None) -> str:
        """Build the few-shot prompt"""
        parts = []
        
        if self.instruction:
            parts.append(self.instruction)
        
        # Add examples
        for example in self.examples:
            parts.append(example.format(self.input_label, self.output_label))
        
        # Add query if provided
        if query:
            parts.append(f"{self.input_label}: {query}")
            parts.append(f"{self.output_label}:")
        
        return "\n\n".join(parts)
    
    def build_with_query(self, query: str) -> str:
        """Build prompt with query"""
        return self.build(query)


class ZeroShot:
    """Zero-shot prompt builder"""
    
    def __init__(self, instruction: str):
        self.instruction = instruction
    
    def build(self, query: str) -> str:
        """Build zero-shot prompt"""
        return f"{self.instruction}\n\nQuery: {query}\nResponse:"


class OneShot:
    """One-shot prompt builder"""
    
    def __init__(self, instruction: str, example_input: str, example_output: str):
        self.instruction = instruction
        self.example = Example(example_input, example_output)
    
    def build(self, query: str) -> str:
        """Build one-shot prompt"""
        parts = [
            self.instruction,
            self.example.format(),
            f"Input: {query}",
            "Output:"
        ]
        return "\n\n".join(parts)