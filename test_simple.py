#!/usr/bin/env python3
"""
Simple test client for Cognee API - Test with minimal text
"""

import asyncio
import sys
from client import CogneeClient, SearchType


async def main():
    COGNEE_URL = "http://eva_cognee:8181"

    print("Testing Cognee with simple text...")
    client = CogneeClient(base_url=COGNEE_URL, timeout=600.0)

    try:
        # Test with simple text
        print("\n1. Adding simple text...")
        simple_text = "The packer machine groups containers into packs. It uses a virtual conveyor system with NumPy arrays."

        add_result = await client.add(
            text=simple_text,
            dataset_name="test_simple"
        )
        print(f"✓ Add result: {add_result}")

        print("\n2. Building knowledge graph...")
        cognify_result = await client.cognify(datasets=["test_simple"])
        print(f"✓ Cognify result: {cognify_result}")

        print("\n3. Searching...")
        search_result = await client.search(
            query_text="What does the packer do?",
            query_type=SearchType.GRAPH_COMPLETION
        )
        print(f"✓ Search result: {search_result}")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        await client.close()

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
