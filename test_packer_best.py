#!/usr/bin/env python3
"""
Optimized Packer Search Test
Tests different search modes to find the most useful one for querying documentation
"""

import asyncio
import sys
from pathlib import Path
from client import CogneeClient, SearchType


def format_result(result, max_length=500):
    """Format search result, truncating if too long"""
    if isinstance(result, dict):
        if 'text' in result:
            text = result['text']
            if len(text) > max_length:
                return text[:max_length] + f"\n... (truncated {len(text) - max_length} chars)"
            return text
        return str(result)
    elif isinstance(result, str):
        if len(result) > max_length:
            return result[:max_length] + f"\n... (truncated {len(result) - max_length} chars)"
        return result
    return str(result)


async def main():
    COGNEE_URL = "http://eva_cognee:8181"
    PACKER_DOC_PATH = "/home/steve/DevOps/workspaces/DesconSimGui/docs/packer.md"
    DATASET_NAME = "DesconSim_Packer"

    print("=" * 80)
    print("Optimized Packer Documentation Search Test")
    print("=" * 80)
    print()

    # Read document
    print("[1/5] Reading packer.md...")
    packer_content = Path(PACKER_DOC_PATH).read_text()
    print(f"✓ Loaded ({len(packer_content)} characters)")
    print()

    # Initialize
    print("[2/5] Connecting to Cognee...")
    client = CogneeClient(base_url=COGNEE_URL, timeout=1800.0)
    print("✓ Connected")
    print()

    try:
        # Clear and reset
        print("[3/5] Resetting Cognee memory...")
        await client.prune()
        print("✓ Memory cleared")
        print()

        # Add and process
        print("[4/5] Adding and processing document (may take several minutes)...")
        await client.add(text=packer_content, dataset_name=DATASET_NAME)
        print("  ✓ Added")
        await client.cognify(datasets=[DATASET_NAME])
        print("  ✓ Cognified")
        print()

        # Test different search types
        print("[5/5] Testing search types...")
        print()

        query = "What is priming and downstream control in the packer?"

        # Test RAG_COMPLETION - should give focused answers
        print("=" * 80)
        print(f"QUERY: {query}")
        print("=" * 80)
        print()

        search_types_to_test = [
            (SearchType.RAG_COMPLETION, "RAG (Retrieval Augmented Generation) - Best for Q&A"),
            (SearchType.GRAPH_SUMMARY_COMPLETION, "Graph Summary - Summarized graph info"),
            (SearchType.NATURAL_LANGUAGE, "Natural Language - NL query processing"),
        ]

        for search_type, description in search_types_to_test:
            print(f"┌─ {description}")
            print(f"│  Search Type: {search_type.value}")
            print("└─ Result:")

            try:
                result = await client.search(query_text=query, query_type=search_type)

                if result.get("success"):
                    data = result.get("data", [])

                    if isinstance(data, list):
                        if len(data) == 0 or (len(data) == 1 and not data[0]):
                            print("   No results")
                        else:
                            for i, item in enumerate(data[:3], 1):  # Limit to first 3
                                if item:
                                    formatted = format_result(item, max_length=400)
                                    print(f"   [{i}] {formatted}")
                    elif isinstance(data, str):
                        print(f"   {format_result(data, max_length=400)}")
                    else:
                        print(f"   {format_result(data, max_length=400)}")
                else:
                    print(f"   Search failed: {result.get('message', 'Unknown error')}")

            except Exception as e:
                print(f"   ERROR: {e}")

            print()

        # Additional query test
        print("=" * 80)
        print("QUERY: Explain the speed control hierarchy")
        print("=" * 80)
        print()

        try:
            result = await client.search(
                query_text="Explain the speed control hierarchy",
                query_type=SearchType.RAG_COMPLETION
            )

            if result.get("success"):
                data = result.get("data", [])
                print(format_result(data, max_length=600))
            else:
                print(f"Search failed: {result}")

        except Exception as e:
            print(f"ERROR: {e}")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        await client.close()
        print()
        print("✓ Test completed")

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
