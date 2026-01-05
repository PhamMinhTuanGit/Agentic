




from typing import List, Dict, Optional, Generator
from dataclasses import dataclass
from enum import Enum
import json


class TaskType(Enum):
    """Task types for planning"""
    QUERY = "query"  # Simple question answering
    CONFIGURATION = "configuration"  # Configure device/service
    TROUBLESHOOTING = "troubleshooting"  # Troubleshoot issues
    RETRIEVAL = "retrieval"  # Retrieve information
    MULTI_STEP = "multi_step"  # Multiple steps required
    TOOL_CALL = "tool_call"  # Requires tool invocation


@dataclass
class PlanStep:
    """Single step in a plan"""
    step_id: int
    description: str
    task_type: TaskType
    required_tools: List[str]
    dependencies: List[int]  # IDs of steps that must complete first
    estimated_tokens: int
    priority: int = 1


@dataclass
class TaskPlan:
    """Complete plan for a user query"""
    query: str
    intent: str
    steps: List[PlanStep]
    total_estimated_tokens: int
    requires_rag: bool
    requires_memory: bool


class AgentPlanning:
    """
    Responsible for task decomposition and planning.
    Analyzes user queries and breaks them down into executable steps.
    """
    
    def __init__(self, llm_client=None, max_steps: int = 5):
        """
        Args:
            llm_client: LLM client for planning analysis (optional)
            max_steps: Maximum number of planning steps
        """
        self.llm_client = llm_client
        self.max_steps = max_steps
    
    def analyze_query(self, query: str) -> TaskType:
        """
        Analyze query to determine task type.
        
        Args:
            query: User query string
            
        Returns:
            TaskType enum indicating the type of task
        """
        query_lower = query.lower()
        
        # Pattern matching for task type detection
        if any(word in query_lower for word in ["configure", "setup", "set", "enable", "disable"]):
            return TaskType.CONFIGURATION
        elif any(word in query_lower for word in ["troubleshoot", "debug", "issue", "problem", "error", "fix"]):
            return TaskType.TROUBLESHOOTING
        elif any(word in query_lower for word in ["what", "how", "where", "when", "why", "list", "show", "get"]):
            return TaskType.RETRIEVAL
        elif any(word in query_lower for word in ["multiple", "step", "then", "first", "second", "also"]):
            return TaskType.MULTI_STEP
        else:
            return TaskType.QUERY
    
    def extract_intent(self, query: str) -> str:
        """
        Extract main intent from query.
        
        Args:
            query: User query string
            
        Returns:
            Intent description
        """
        # Simple keyword-based intent extraction
        if "configure" in query.lower():
            return "configure_device"
        elif "troubleshoot" in query.lower():
            return "diagnose_issue"
        elif "show" in query.lower() or "list" in query.lower():
            return "retrieve_info"
        elif "help" in query.lower():
            return "provide_assistance"
        else:
            return "general_query"
    
    def decompose_task(self, query: str) -> TaskPlan:
        """
        Decompose a user query into executable steps.
        
        Args:
            query: User query to decompose
            
        Returns:
            TaskPlan with structured steps
        """
        task_type = self.analyze_query(query)
        intent = self.extract_intent(query)
        
        steps = []
        
        if task_type == TaskType.CONFIGURATION:
            steps = self._plan_configuration_task(query)
        elif task_type == TaskType.TROUBLESHOOTING:
            steps = self._plan_troubleshooting_task(query)
        elif task_type == TaskType.MULTI_STEP:
            steps = self._plan_multi_step_task(query)
        elif task_type == TaskType.RETRIEVAL:
            steps = self._plan_retrieval_task(query)
        else:
            steps = self._plan_simple_query(query)
        
        # Calculate total estimated tokens
        total_tokens = sum(step.estimated_tokens for step in steps)
        
        # Determine if RAG and memory are needed
        requires_rag = len(steps) > 0
        requires_memory = task_type in [TaskType.TROUBLESHOOTING, TaskType.CONFIGURATION, TaskType.MULTI_STEP]
        
        return TaskPlan(
            query=query,
            intent=intent,
            steps=steps,
            total_estimated_tokens=total_tokens,
            requires_rag=requires_rag,
            requires_memory=requires_memory
        )
    
    def _plan_simple_query(self, query: str) -> List[PlanStep]:
        """Plan for simple query/question answering"""
        return [
            PlanStep(
                step_id=1,
                description=f"Answer query: {query[:100]}",
                task_type=TaskType.QUERY,
                required_tools=[],
                dependencies=[],
                estimated_tokens=500,
                priority=1
            )
        ]
    
    def _plan_retrieval_task(self, query: str) -> List[PlanStep]:
        """Plan for information retrieval task"""
        return [
            PlanStep(
                step_id=1,
                description="Search for relevant documentation",
                task_type=TaskType.RETRIEVAL,
                required_tools=["search"],
                dependencies=[],
                estimated_tokens=300,
                priority=1
            ),
            PlanStep(
                step_id=2,
                description="Synthesize retrieved information",
                task_type=TaskType.RETRIEVAL,
                required_tools=[],
                dependencies=[1],
                estimated_tokens=400,
                priority=1
            )
        ]
    
    def _plan_configuration_task(self, query: str) -> List[PlanStep]:
        """Plan for configuration task"""
        return [
            PlanStep(
                step_id=1,
                description="Understand current state and requirements",
                task_type=TaskType.CONFIGURATION,
                required_tools=["memory_retrieve"],
                dependencies=[],
                estimated_tokens=300,
                priority=1
            ),
            PlanStep(
                step_id=2,
                description="Search for configuration guidelines",
                task_type=TaskType.CONFIGURATION,
                required_tools=["search"],
                dependencies=[1],
                estimated_tokens=400,
                priority=1
            ),
            PlanStep(
                step_id=3,
                description="Generate configuration steps",
                task_type=TaskType.CONFIGURATION,
                required_tools=[],
                dependencies=[1, 2],
                estimated_tokens=600,
                priority=1
            ),
            PlanStep(
                step_id=4,
                description="Provide configuration with examples",
                task_type=TaskType.CONFIGURATION,
                required_tools=[],
                dependencies=[3],
                estimated_tokens=500,
                priority=1
            )
        ]
    
    def _plan_troubleshooting_task(self, query: str) -> List[PlanStep]:
        """Plan for troubleshooting task"""
        return [
            PlanStep(
                step_id=1,
                description="Retrieve relevant past issues and solutions",
                task_type=TaskType.TROUBLESHOOTING,
                required_tools=["memory_retrieve"],
                dependencies=[],
                estimated_tokens=300,
                priority=2
            ),
            PlanStep(
                step_id=2,
                description="Search for similar issues in documentation",
                task_type=TaskType.TROUBLESHOOTING,
                required_tools=["search"],
                dependencies=[],
                estimated_tokens=400,
                priority=1
            ),
            PlanStep(
                step_id=3,
                description="Analyze symptoms and identify root cause",
                task_type=TaskType.TROUBLESHOOTING,
                required_tools=[],
                dependencies=[1, 2],
                estimated_tokens=600,
                priority=1
            ),
            PlanStep(
                step_id=4,
                description="Propose solutions with steps",
                task_type=TaskType.TROUBLESHOOTING,
                required_tools=[],
                dependencies=[3],
                estimated_tokens=500,
                priority=1
            )
        ]
    
    def _plan_multi_step_task(self, query: str) -> List[PlanStep]:
        """Plan for multi-step task"""
        return [
            PlanStep(
                step_id=1,
                description="Break down complex task into sub-steps",
                task_type=TaskType.MULTI_STEP,
                required_tools=[],
                dependencies=[],
                estimated_tokens=400,
                priority=1
            ),
            PlanStep(
                step_id=2,
                description="Execute step 1: Retrieve context",
                task_type=TaskType.RETRIEVAL,
                required_tools=["search"],
                dependencies=[1],
                estimated_tokens=400,
                priority=1
            ),
            PlanStep(
                step_id=3,
                description="Execute step 2: Process and analyze",
                task_type=TaskType.MULTI_STEP,
                required_tools=[],
                dependencies=[2],
                estimated_tokens=500,
                priority=1
            ),
            PlanStep(
                step_id=4,
                description="Execute step 3: Generate response",
                task_type=TaskType.MULTI_STEP,
                required_tools=[],
                dependencies=[3],
                estimated_tokens=400,
                priority=1
            )
        ]
    
    def optimize_plan(self, plan: TaskPlan) -> TaskPlan:
        """
        Optimize plan by reordering steps or removing redundancies.
        
        Args:
            plan: Original task plan
            
        Returns:
            Optimized task plan
        """
        # Sort by priority and dependencies
        sorted_steps = sorted(plan.steps, key=lambda s: (s.priority, s.step_id))
        plan.steps = sorted_steps
        return plan
    
    def estimate_token_cost(self, plan: TaskPlan) -> int:
        """
        Estimate total token cost for executing the plan.
        
        Args:
            plan: Task plan to estimate
            
        Returns:
            Estimated number of tokens needed
        """
        return plan.total_estimated_tokens
    
    def get_execution_order(self, plan: TaskPlan) -> List[int]:
        """
        Get execution order based on dependencies.
        
        Args:
            plan: Task plan
            
        Returns:
            List of step IDs in execution order
        """
        executed = set()
        order = []
        
        while len(executed) < len(plan.steps):
            for step in plan.steps:
                if step.step_id not in executed:
                    # Check if all dependencies are satisfied
                    if all(dep in executed for dep in step.dependencies):
                        order.append(step.step_id)
                        executed.add(step.step_id)
                        break
        
        return order
    
    def format_plan_for_display(self, plan: TaskPlan) -> str:
        """
        Format plan as human-readable string.
        
        Args:
            plan: Task plan to format
            
        Returns:
            Formatted plan string
        """
        output = []
        output.append(f"Query: {plan.query}")
        output.append(f"Intent: {plan.intent}")
        output.append(f"Task Type: {plan.steps[0].task_type.value if plan.steps else 'N/A'}")
        output.append(f"Requires RAG: {plan.requires_rag}")
        output.append(f"Requires Memory: {plan.requires_memory}")
        output.append(f"Estimated Tokens: {plan.total_estimated_tokens}\n")
        
        output.append("Execution Plan:")
        execution_order = self.get_execution_order(plan)
        for idx, step_id in enumerate(execution_order, 1):
            step = next(s for s in plan.steps if s.step_id == step_id)
            output.append(f"  Step {idx}: {step.description}")
            if step.required_tools:
                output.append(f"    Tools: {', '.join(step.required_tools)}")
            output.append(f"    Tokens: {step.estimated_tokens}")
        
        return "\n".join(output)


# Example usage and testing
if __name__ == "__main__":
    planner = AgentPlanning()
    
    # Test different query types
    test_queries = [
        "How do I configure OSPF on ZebOS?",
        "Troubleshoot BGP convergence issues",
        "Show me the steps to configure PIM Sparse Mode",
        "What is MPLS and how do I enable it?",
        "Configure AAA authentication then setup TACACS+ server"
    ]
    
    for query in test_queries:
        print("=" * 80)
        plan = planner.decompose_task(query)
        plan = planner.optimize_plan(plan)
        print(planner.format_plan_for_display(plan))
        print()

    