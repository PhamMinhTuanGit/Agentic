from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel, Field

class ToolParameter(BaseModel):
    """Schema cho tool parameter"""
    name: str
    type: str  # string, number, boolean, array, object
    description: str
    required: bool = False
    enum: List[str] = None  # Cho dropdown values

class ToolDefinition(BaseModel):
    """Schema cho tool definition (OpenAI format)"""
    name: str = Field(..., description="Tên function")
    description: str = Field(..., description="Mô tả function làm gì")
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="JSON Schema cho parameters"
    )
    
    def to_openai_format(self) -> Dict:
        """Convert sang OpenAI tool format"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }

class BaseTool(ABC):
    """Base class cho tất cả tools"""
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.description = self.__doc__ or "No description"
    
    @abstractmethod
    def get_definition(self) -> ToolDefinition:
        """Return tool definition cho LLM"""
        pass
    
    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute tool với parameters"""
        pass
    
    def validate_parameters(self, params: Dict) -> bool:
        """Validate parameters trước khi execute"""
        definition = self.get_definition()
        required = definition.parameters.get("required", [])
        
        for param in required:
            if param not in params:
                raise ValueError(f"Missing required parameter: {param}")
        
        return True