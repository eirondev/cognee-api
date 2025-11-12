#!/usr/bin/env python3
"""
Full test client for Cognee API - Complete packer workflow
Adds, cognifies, and searches with multiple queries
"""

import asyncio
import sys
from pathlib import Path
from client import CogneeClient, SearchType


async def main():
    # Configuration
    COGNEE_URL = "http://eva_cognee:8181"
    PACKER_DOC_PATH = "/home/steve/DevOps/workspaces/DesconSimGui/docs/packer.md"
    DATASET_NAME = "DesconSim_Packer"

    print("=" * 80)
    print("Cognee API Test - Full Packer Documentation Workflow")
    print("=" * 80)
    print()

    # Read the document
    print("[1/7] Reading packer.md document...")
    try:
        packer_doc_path = Path(PACKER_DOC_PATH)
        if not packer_doc_path.exists():
            print(f"ERROR: File not found: {PACKER_DOC_PATH}")
            return 1

        packer_content = packer_doc_path.read_text()
        print(f"✓ Document loaded ({len(packer_content)} characters)")
        print()
    except Exception as e:
        print(f"ERROR: Failed to read document: {e}")
        return 1

    # Initialize client
    print(f"[2/7] Connecting to Cognee API at {COGNEE_URL}...")
    client = CogneeClient(base_url=COGNEE_URL, timeout=1800.0)
    print("✓ Client initialized (30 minute timeout)")
    print()

    try:
        # Health check
        print("[3/7] Checking server health...")
        health_result = await client.health()
        print(f"✓ Server is healthy: {health_result}")
        print()

        # Prune the old dataset first to start fresh
        print("[4/7] Pruning old data (starting fresh)...")
        try:
            prune_result = await client.prune()
            print(f"✓ Old data pruned: {prune_result.get('message')}")
        except Exception as e:
            print(f"Note: Prune may have failed (this is ok): {e}")
        print()

        # Add document
        print(f"[5/7] Adding packer.md to dataset '{DATASET_NAME}'...")
        print(f"  This may take several minutes...")
        add_result = await client.add(
            text=packer_content,
            dataset_name=DATASET_NAME
        )

        if add_result.get("success"):
            print(f"✓ Document added successfully")
        else:
            print(f"ERROR: Failed to add document: {add_result}")
            return 1
        print()

        # Cognify
        print(f"[6/7] Building knowledge graph...")
        print(f"  This may take several minutes...")
        cognify_result = await client.cognify(datasets=[DATASET_NAME])

        if cognify_result.get("success"):
            print(f"✓ Knowledge graph built successfully")
        else:
            print(f"ERROR: Failed to cognify: {cognify_result}")
            return 1
        print()

        # Multiple searches with different queries
        print("[7/7] Performing searches...")
        print()

        queries = [
            ("What is priming and downstream control in the packer?", SearchType.CHUNKS),
            ("Explain the packer speed control system", SearchType.SUMMARIES),
            ("How does the virtual conveyor work?", SearchType.GRAPH_COMPLETION),
            ("What are the packer configuration properties?", SearchType.CHUNKS_LEXICAL)
        ]

        for i, (query, search_type) in enumerate(queries, 1):
            print("=" * 80)
            print(f"SEARCH {i}/{len(queries)}: '{query}'")
            print(f"  Search Type: {search_type.value}")
            print("=" * 80)

            try:
                search_result = await client.search(
                    query_text=query,
                    query_type=search_type
                )

                if search_result.get("success"):
                    search_data = search_result.get("data", [])

                    if isinstance(search_data, list):
                        if len(search_data) == 0 or (len(search_data) == 1 and not search_data[0]):
                            print("  No results returned")
                        else:
                            for j, item in enumerate(search_data, 1):
                                if item:  # Only print non-empty results
                                    print(f"  Result {j}:")
                                    print(f"    {item}")
                    else:
                        print(f"  {search_data}")
                else:
                    print(f"  Search failed: {search_result}")

            except Exception as e:
                print(f"  ERROR: {e}")

            print()

    except Exception as e:
        print(f"ERROR: Operation failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        await client.close()
        print()
        print("✓ Client connection closed")

    print()
    print("=" * 80)
    print("Test completed!")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
