import re
from pathlib import Path
from typing import Dict, Any, Optional


class PromptTemplate:
    """Enhanced template management with variable substitution"""
    
    def __init__(self, template: str):
        self.template = template
    
    @classmethod
    def from_file(cls, file_path: str) -> 'PromptTemplate':
        """Load template from file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return cls(f.read().strip())
    
    def format(self, **kwargs) -> str:
        """Format template with variables"""
        return self.template.format(**kwargs)
    
    def safe_format(self, **kwargs) -> str:
        """Format template, leaving unmatched placeholders intact"""
        def replace_func(match):
            key = match.group(1)
            return str(kwargs.get(key, match.group(0)))
        
        return re.sub(r'\{([^}]+)\}', replace_func, self.template)
    
    def get_variables(self) -> set:
        """Extract all variable names from template"""
        return set(re.findall(r'\{([^}]+)\}', self.template))


class Prompt:
    """Fluent API for building prompts"""
    
    def __init__(self):
        self._system = ""
        self._user = ""
        self._assistant = ""
        self._messages = []
    
    @classmethod
    def system(cls, content: str, **kwargs) -> 'Prompt':
        """Set system message"""
        instance = cls()
        if Path(content).exists():
            template = PromptTemplate.from_file(content)
            instance._system = template.format(**kwargs)
        else:
            instance._system = content.format(**kwargs) if kwargs else content
        return instance
    
    def user(self, content: str, **kwargs) -> 'Prompt':
        """Add user message"""
        formatted = content.format(**kwargs) if kwargs else content
        self._user = formatted
        return self
    
    def assistant(self, content: str, **kwargs) -> 'Prompt':
        """Add assistant message"""
        formatted = content.format(**kwargs) if kwargs else content
        self._assistant = formatted
        return self
    
    def add_message(self, role: str, content: str, **kwargs) -> 'Prompt':
        """Add custom message"""
        formatted = content.format(**kwargs) if kwargs else content
        self._messages.append({"role": role, "content": formatted})
        return self
    
    def build(self) -> list:
        """Build message list for API"""
        messages = []
        
        if self._system:
            messages.append({"role": "system", "content": self._system})
        
        if self._user:
            messages.append({"role": "user", "content": self._user})
        
        if self._assistant:
            messages.append({"role": "assistant", "content": self._assistant})
        
        messages.extend(self._messages)
        return messages
    
    def build_string(self, separator: str = "\n\n") -> str:
        """Build as single string"""
        parts = []
        
        if self._system:
            parts.append(f"System: {self._system}")
        
        if self._user:
            parts.append(f"User: {self._user}")
        
        if self._assistant:
            parts.append(f"Assistant: {self._assistant}")
        
        for msg in self._messages:
            parts.append(f"{msg['role'].title()}: {msg['content']}")
        
        return separator.join(parts)