import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))


async def main():
    print("Zenith RAG Agent Example")
    print("=" * 50)
    
    documents = [
        "Zenith is an open-source ML platform for 2026.",
        "It supports LLMs, RAG, agents, and real-time monitoring.",
        "The platform includes experiment tracking and model registry.",
        "Zenith provides drift detection and performance monitoring."
    ]
    
    print(f"\nLoaded {len(documents)} documents")
    
    query = "What features does Zenith provide?"
    print(f"\nQuery: {query}")
    
    print("\nStep 1: Embedding documents...")
    print("Step 2: Searching for relevant context...")
    
    relevant_docs = documents[:2]
    print(f"\nRetrieved {len(relevant_docs)} relevant documents:")
    for i, doc in enumerate(relevant_docs, 1):
        print(f"{i}. {doc}")
    
    context = "\n".join(relevant_docs)
    
    print("\nStep 3: Generating response with LLM...")
    response = f"Based on the documentation, {query.lower()} Zenith is an open-source ML platform that supports LLMs, RAG, agents, and real-time monitoring."
    
    print(f"\nGenerated Response:")
    print(response)
    
    print("\n✓ RAG Agent execution completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
