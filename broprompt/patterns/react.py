from typing import List, Optional


class ReACTStep:
    """Single step in ReACT pattern"""
    
    def __init__(self, thought: str = "", action: str = "", observation: str = ""):
        self.thought = thought
        self.action = action
        self.observation = observation
    
    def format(self) -> str:
        """Format step as text"""
        parts = []
        if self.thought:
            parts.append(f"Thought: {self.thought}")
        if self.action:
            parts.append(f"Action: {self.action}")
        if self.observation:
            parts.append(f"Observation: {self.observation}")
        return "\n".join(parts)


class ReACT:
    """ReACT (Reasoning and Acting) pattern builder"""
    
    def __init__(self):
        self.steps: List[ReACTStep] = []
        self.instruction = ""
        self.final_answer_prefix = "Final Answer:"
    
    def set_instruction(self, instruction: str) -> 'ReACT':
        """Set the instruction for the ReACT process"""
        self.instruction = instruction
        return self
    
    def add_step(self, thought: str = "", action: str = "", observation: str = "") -> 'ReACT':
        """Add a complete ReACT step"""
        self.steps.append(ReACTStep(thought, action, observation))
        return self
    
    def thought(self, text: str) -> 'ReACT':
        """Add thought to current or new step"""
        if not self.steps or self.steps[-1].thought:
            self.steps.append(ReACTStep())
        self.steps[-1].thought = text
        return self
    
    def action(self, text: str) -> 'ReACT':
        """Add action to current step"""
        if not self.steps:
            self.steps.append(ReACTStep())
        self.steps[-1].action = text
        return self
    
    def observation(self, text: str) -> 'ReACT':
        """Add observation to current step"""
        if not self.steps:
            self.steps.append(ReACTStep())
        self.steps[-1].observation = text
        return self
    
    def build(self, query: str = None, include_template: bool = True) -> str:
        """Build the ReACT prompt"""
        parts = []
        
        if self.instruction:
            parts.append(self.instruction)
        
        if include_template:
            template = """You should use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take
Observation: the result of the action
... (this Thought/Action/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question"""
            parts.append(template)
        
        if query:
            parts.append(f"Question: {query}")
        
        # Add existing steps
        for step in self.steps:
            if step.thought or step.action or step.observation:
                parts.append(step.format())
        
        return "\n\n".join(parts)
    
    def build_template(self) -> str:
        """Build just the ReACT template"""
        return self.build(include_template=True)
    
    def continue_reasoning(self) -> str:
        """Get prompt to continue reasoning"""
        if not self.steps:
            return "Thought:"
        
        last_step = self.steps[-1]
        if last_step.observation and not last_step.thought:
            return "Thought:"
        elif last_step.thought and not last_step.action:
            return "Action:"
        elif last_step.action and not last_step.observation:
            return "Observation:"
        else:
            return "Thought:"