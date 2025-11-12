#!/usr/bin/env python3
"""
Cognee RAG workflow - Retrieve relevant chunks
This retrieves context that Claude Code can then read and use to answer questions
"""

import asyncio
import sys
from pathlib import Path
from client import CogneeClient, SearchType


async def main():
    COGNEE_URL = "http://eva_cognee:8181"
    PACKER_DOC_PATH = "/home/steve/DevOps/workspaces/DesconSimGui/docs/packer.md"
    DATASET_NAME = "DesconSim_Packer"

    print("=" * 80)
    print("Cognee RAG Test - Retrieve Context for Claude Code")
    print("=" * 80)
    print()

    # Read document
    print("[1/4] Reading packer.md...")
    packer_content = Path(PACKER_DOC_PATH).read_text()
    print(f"✓ Loaded ({len(packer_content)} characters)")
    print()

    # Initialize Cognee client
    print("[2/4] Connecting to Cognee...")
    cognee_client = CogneeClient(base_url=COGNEE_URL, timeout=1800.0)
    print("✓ Connected")
    print()

    try:
        # Reset and add document
        print("[3/4] Resetting and adding document...")
        await cognee_client.prune()
        print("  ✓ Memory cleared")
        await cognee_client.add(text=packer_content, dataset_name=DATASET_NAME)
        print("  ✓ Document added")
        await cognee_client.cognify(datasets=[DATASET_NAME])
        print("  ✓ Knowledge graph built")
        print()

        # Perform retrieval queries
        print("[4/4] Retrieving context for questions...")
        print()

        queries = [
            "What is priming and downstream control in the packer?",
            "Explain the speed control hierarchy",
            "How does the virtual conveyor system work?"
        ]

        for query_num, question in enumerate(queries, 1):
            print("=" * 80)
            print(f"QUERY {query_num}/{len(queries)}: {question}")
            print("=" * 80)
            print()

            # Retrieve context from Cognee
            search_result = await cognee_client.search(
                query_text=question,
                query_type=SearchType.CHUNKS
            )

            if not search_result.get("success"):
                print(f"ERROR: Search failed: {search_result}")
                continue

            # Extract text from chunks
            chunks = search_result.get("data", [])
            context_parts = []

            for chunk in chunks[:2]:  # Use top 2 chunks
                if isinstance(chunk, dict) and 'text' in chunk:
                    context_parts.append(chunk['text'])

            if not context_parts:
                print("No context retrieved")
                continue

            # Display retrieved context
            print(f"Retrieved {len(context_parts)} relevant chunk(s):")
            print()
            print("-" * 80)
            print("RETRIEVED CONTEXT:")
            print("-" * 80)

            for i, context in enumerate(context_parts, 1):
                print(f"\n[Chunk {i}]")
                print(context)
                print()

            print("-" * 80)
            print()
            print("Claude Code: Please read the above context and answer the question.")
            print()

        print("=" * 80)
        print("Retrieval complete!")
        print("=" * 80)

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        await cognee_client.close()

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
