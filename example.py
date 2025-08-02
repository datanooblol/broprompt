#!/usr/bin/env python3
"""Example usage of broprompt library"""

from dataclasses import dataclass
from broprompt import (
    Prompt, FewShot, ReACT, Reflection, 
    StructuredOutput, ToolRegistry, tool
)

# Example 1: Basic prompt building
print("=== Basic Prompt Building ===")
prompt = Prompt.system("You are a helpful assistant").user("What is {topic}?", topic="Python")
messages = prompt.build()
print(messages)

# Example 2: Few-shot learning
print("\n=== Few-shot Learning ===")
few_shot = (FewShot()
    .set_instruction("Classify the sentiment of the following text:")
    .add_example("I love this product!", "positive")
    .add_example("This is terrible", "negative")
    .build_with_query("The movie was amazing"))
print(few_shot)

# Example 3: Structured output
print("\n=== Structured Output ===")
@dataclass
class SentimentAnalysis:
    sentiment: str
    confidence: float
    reasoning: str

structured = StructuredOutput(SentimentAnalysis)
schema_prompt = structured.generate_prompt("Analyze the sentiment of: 'I love this!'")
print(schema_prompt)

# Example 4: ReACT pattern
print("\n=== ReACT Pattern ===")
react = (ReACT()
    .set_instruction("Solve this step by step")
    .thought("I need to calculate 15 * 23")
    .action("multiply 15 by 23")
    .observation("15 * 23 = 345")
    .build("What is 15 multiplied by 23?"))
print(react)

# Example 5: Tool calling
print("\n=== Tool Calling ===")
registry = ToolRegistry()

@tool("Calculate the sum of two numbers")
def add(a: int, b: int) -> int:
    return a + b

@tool("Get weather information")
def get_weather(city: str) -> str:
    return f"Weather in {city}: Sunny, 25°C"

registry.register(add).register(get_weather)
print(registry.generate_tool_prompt())
print("\nTool definitions:", registry.get_tool_definitions())

if __name__ == "__main__":
    print("\nAll examples completed successfully!")