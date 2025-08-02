from typing import Optional, List


class ReflectionStep:
    """Single reflection step"""
    
    def __init__(self, response: str = "", critique: str = "", refinement: str = ""):
        self.response = response
        self.critique = critique
        self.refinement = refinement
    
    def format(self) -> str:
        """Format reflection step"""
        parts = []
        if self.response:
            parts.append(f"Response: {self.response}")
        if self.critique:
            parts.append(f"Critique: {self.critique}")
        if self.refinement:
            parts.append(f"Refinement: {self.refinement}")
        return "\n\n".join(parts)


class Reflection:
    """Reflection pattern for self-improvement"""
    
    def __init__(self):
        self.steps: List[ReflectionStep] = []
        self.instruction = ""
        self.critique_instruction = "Please critique the above response and identify areas for improvement."
        self.refinement_instruction = "Based on the critique, provide a refined response."
    
    def set_instruction(self, instruction: str) -> 'Reflection':
        """Set main instruction"""
        self.instruction = instruction
        return self
    
    def set_critique_instruction(self, instruction: str) -> 'Reflection':
        """Set critique instruction"""
        self.critique_instruction = instruction
        return self
    
    def set_refinement_instruction(self, instruction: str) -> 'Reflection':
        """Set refinement instruction"""
        self.refinement_instruction = instruction
        return self
    
    def add_step(self, response: str = "", critique: str = "", refinement: str = "") -> 'Reflection':
        """Add complete reflection step"""
        self.steps.append(ReflectionStep(response, critique, refinement))
        return self
    
    def initial_response(self, response: str) -> 'Reflection':
        """Add initial response"""
        if not self.steps:
            self.steps.append(ReflectionStep())
        self.steps[-1].response = response
        return self
    
    def critique(self, critique: str) -> 'Reflection':
        """Add critique to current step"""
        if not self.steps:
            self.steps.append(ReflectionStep())
        self.steps[-1].critique = critique
        return self
    
    def refinement(self, refinement: str) -> 'Reflection':
        """Add refinement to current step"""
        if not self.steps:
            self.steps.append(ReflectionStep())
        self.steps[-1].refinement = refinement
        return self
    
    def build_initial_prompt(self, query: str) -> str:
        """Build prompt for initial response"""
        parts = []
        if self.instruction:
            parts.append(self.instruction)
        parts.append(f"Query: {query}")
        return "\n\n".join(parts)
    
    def build_critique_prompt(self, query: str, response: str) -> str:
        """Build prompt for critique"""
        parts = [
            f"Query: {query}",
            f"Response: {response}",
            self.critique_instruction
        ]
        return "\n\n".join(parts)
    
    def build_refinement_prompt(self, query: str, response: str, critique: str) -> str:
        """Build prompt for refinement"""
        parts = [
            f"Query: {query}",
            f"Initial Response: {response}",
            f"Critique: {critique}",
            self.refinement_instruction
        ]
        return "\n\n".join(parts)
    
    def build_full_process(self, query: str) -> str:
        """Build complete reflection process template"""
        parts = []
        
        if self.instruction:
            parts.append(self.instruction)
        
        template = f"""Please follow this reflection process:

1. First, provide your initial response to the query
2. Then, critique your response identifying weaknesses or areas for improvement  
3. Finally, provide a refined response based on your critique

Query: {query}

Initial Response:"""
        
        parts.append(template)
        
        # Add existing steps
        for step in self.steps:
            if step.response or step.critique or step.refinement:
                parts.append(step.format())
        
        return "\n\n".join(parts)
    
    def build(self, query: str = None) -> str:
        """Build reflection prompt"""
        if query:
            return self.build_full_process(query)
        
        parts = []
        if self.instruction:
            parts.append(self.instruction)
        
        for step in self.steps:
            parts.append(step.format())
        
        return "\n\n".join(parts)