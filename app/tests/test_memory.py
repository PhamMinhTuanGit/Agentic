"""
Tests for Memory Agent
"""
import pytest
from app.memory.agent import MemoryAgent
from app.memory.schemas import MemoryItem
from app.memory.store import MemoryStore


def test_memory_agent_basic():
    """Test basic memory agent operations"""
    agent = MemoryAgent()
    session_id = "test_session_1"
    
    # Add memory
    agent.update(session_id, "Tôi là John", "Xin chào John!")
    
    # Retrieve
    memories = agent.retrieve(session_id, "tên tôi")
    assert len(memories) > 0
    assert "John" in memories[0]


def test_memory_agent_should_not_store():
    """Test that irrelevant queries are not stored"""
    agent = MemoryAgent()
    session_id = "test_session_2"
    
    # This should not be stored
    agent.update(session_id, "What is BGP?", "BGP is a routing protocol")
    
    # Check no memories
    count = agent.get_memory_count(session_id)
    assert count == 0


def test_memory_agent_force_store():
    """Test forcing memory storage"""
    agent = MemoryAgent()
    session_id = "test_session_3"
    
    # Force store
    agent.update(session_id, "Random query", "Random answer", force=True)
    
    # Should be stored
    count = agent.get_memory_count(session_id)
    assert count == 1


def test_memory_agent_summary():
    """Test summary memory"""
    agent = MemoryAgent()
    session_id = "test_session_4"
    
    # Add summary
    agent.add_summary(session_id, "User is working on FastAPI project", ["project"])
    
    # Retrieve by tag
    memories = agent.retrieve_by_tags(session_id, ["project"])
    assert len(memories) == 1
    assert "FastAPI" in memories[0]


def test_memory_agent_clear():
    """Test clearing session"""
    agent = MemoryAgent()
    session_id = "test_session_5"
    
    # Add memory
    agent.update(session_id, "Tôi là Alice", "Hi Alice!", force=True)
    assert agent.get_memory_count(session_id) == 1
    
    # Clear
    agent.clear_session(session_id)
    assert agent.get_memory_count(session_id) == 0


def test_memory_agent_multi_session():
    """Test multiple sessions isolation"""
    agent = MemoryAgent()
    
    # Session 1
    agent.update("session_1", "Tôi là Bob", "Hi Bob!", force=True)
    
    # Session 2
    agent.update("session_2", "Tôi là Charlie", "Hi Charlie!", force=True)
    
    # Check isolation
    mem1 = agent.retrieve("session_1", "Bob")
    mem2 = agent.retrieve("session_2", "Charlie")
    
    assert "Bob" in mem1[0]
    assert "Charlie" in mem2[0]
    assert "Bob" not in str(mem2)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
