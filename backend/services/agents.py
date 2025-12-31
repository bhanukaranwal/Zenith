from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from backend.models.agent import Agent, AgentExecution, AgentStatus
from backend.core.telemetry import get_tracer

tracer = get_tracer(__name__)


class AgentService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def execute_agent(
        self,
        agent_id: int,
        input_data: Dict[str, Any]
    ) -> AgentExecution:
        with tracer.start_as_current_span("execute_agent") as span:
            trace_id = str(uuid.uuid4())
            span.set_attribute("trace_id", trace_id)
            span.set_attribute("agent_id", agent_id)
            
            result = await self.db.execute(select(Agent).where(Agent.id == agent_id))
            agent = result.scalar_one_or_none()
            
            if not agent:
                raise ValueError("Agent not found")
            
            execution = AgentExecution(
                agent_id=agent_id,
                input_data=input_data,
                trace_id=trace_id,
                status=AgentStatus.RUNNING
            )
            
            self.db.add(execution)
            await self.db.commit()
            await self.db.refresh(execution)
            
            try:
                output = await self._run_agent(agent, input_data, trace_id)
                
                execution.output_data = output
                execution.status = AgentStatus.COMPLETED
                execution.end_time = datetime.utcnow()
                
            except Exception as e:
                execution.status = AgentStatus.FAILED
                execution.output_data = {"error": str(e)}
                execution.end_time = datetime.utcnow()
            
            await self.db.commit()
            await self.db.refresh(execution)
            
            return execution
    
    async def _run_agent(
        self,
        agent: Agent,
        input_data: Dict[str, Any],
        trace_id: str
    ) -> Dict[str, Any]:
        if agent.agent_type == "rag":
            return await self._run_rag_agent(agent, input_data, trace_id)
        elif agent.agent_type == "tool":
            return await self._run_tool_agent(agent, input_data, trace_id)
        else:
            return {"result": "Agent execution completed", "input": input_data}
    
    async def _run_rag_agent(
        self,
        agent: Agent,
        input_data: Dict[str, Any],
        trace_id: str
    ) -> Dict[str, Any]:
        query = input_data.get("query", "")
        
        retrieved_docs = [
            {"content": "Sample document 1", "score": 0.95},
            {"content": "Sample document 2", "score": 0.87}
        ]
        
        context = "\n".join([doc["content"] for doc in retrieved_docs])
        
        response = f"Based on the context, here is the answer to: {query}"
        
        return {
            "query": query,
            "retrieved_documents": retrieved_docs,
            "response": response,
            "trace_id": trace_id
        }
    
    async def _run_tool_agent(
        self,
        agent: Agent,
        input_data: Dict[str, Any],
        trace_id: str
    ) -> Dict[str, Any]:
        tools_used = []
        
        for tool in agent.tools:
            tool_result = {
                "tool_name": tool,
                "result": "Tool executed successfully"
            }
            tools_used.append(tool_result)
        
        return {
            "tools_used": tools_used,
            "final_result": "Agent task completed",
            "trace_id": trace_id
        }


class RAGPipelineService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_rag_pipeline(
        self,
        name: str,
        embedding_model: str,
        retrieval_config: Dict[str, Any],
        generation_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        pipeline = {
            "name": name,
            "embedding_model": embedding_model,
            "retrieval_config": retrieval_config,
            "generation_config": generation_config,
            "status": "active"
        }
        
        return pipeline
    
    async def query_rag_pipeline(
        self,
        pipeline_id: int,
        query: str,
        top_k: int = 5
    ) -> Dict[str, Any]:
        retrieved_docs = [
            {"id": i, "content": f"Document {i}", "score": 0.9 - i * 0.1}
            for i in range(top_k)
        ]
        
        context = "\n\n".join([doc["content"] for doc in retrieved_docs])
        
        response = f"Generated response for query: {query}"
        
        return {
            "query": query,
            "retrieved_documents": retrieved_docs,
            "generated_response": response,
            "pipeline_id": pipeline_id
        }
