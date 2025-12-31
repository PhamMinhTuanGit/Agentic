import json
from typing import List, Dict, Any, Optional

class AgentCore:
    def __init__(self, llm_client, tools: List[Dict], memory_module):
        self.llm = llm_client
        self.tools = tools  # Danh sách định nghĩa tools (JSON schema)
        self.memory = memory_module # Module quản lý hội thoại và ngữ cảnh
        
        # 1. Goal Management System
        self.objectives = []
        self.current_task_priority = 1
        
        # 2. Integration Bus (Giả lập qua các phương thức internal)
        self.bus_log = []

    def _integration_bus(self, module: str, data: Any):
        """Điều phối dữ liệu giữa các thành phần"""
        entry = {"module": module, "data": data}
        self.bus_log.append(entry)
        return data

    def _update_goals(self, reasoning: str):
        """Hệ thống quản lý mục tiêu: Phân tích suy luận để cập nhật task"""
        # Logic AI để tự động điều chỉnh mục tiêu dựa trên tiến trình
        # Ở mức đơn giản, ta lưu vết mục tiêu vào memory
        self._integration_bus("GoalManager", f"Updating goals based on: {reasoning[:50]}...")

    async def execute_cycle(self, user_input: str):
        """Vòng lặp quyết định chính (Decision-making engine)"""
        
        # BƯỚC 1: Tiếp nhận Input & Truy xuất Memory
        context = self.memory.get_context(user_input)
        self._integration_bus("Memory", "Context retrieved")

        # BƯỚC 2: LLM Reasoning (High-level reasoning)
        # Gửi kèm định nghĩa tools cho LLM
        response = await self.llm.chat(
            messages=context,
            tools=self.tools,
            tool_choice="auto"
        )
        
        # BƯỚC 3: Xử lý quyết định (Decision Making)
        message = response.choices[0].message
        self._update_goals(message.content or "Executing tools")

        # Kiểm tra nếu LLM muốn gọi Tool
        if message.tool_calls:
            for tool_call in message.tool_calls:
                # Điều phối qua Integration Bus tới Tools Module
                result = await self._dispatch_tool(tool_call)
                
                # Lưu kết quả vào memory và tiếp tục vòng lặp (Recurse)
                self.memory.add_tool_result(tool_call.id, result)
                return await self.execute_cycle(user_input) # Tiếp tục suy luận sau khi có data

        return message.content

    async def _dispatch_tool(self, tool_call):
        """Thực thi tool và trả về kết quả qua Bus"""
        func_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        
        self._integration_bus("Tools", f"Calling {func_name} with {args}")
        # Giả sử bạn có một registry chứa các hàm thực thi thực tế
        result = await tool_registry.execute(func_name, args)
        return result