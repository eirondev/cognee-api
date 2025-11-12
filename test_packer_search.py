#!/usr/bin/env python3
"""
Test client for Cognee API - Search only test for packer priming
Assumes packer.md has already been added and cognified
"""

import asyncio
import sys
from client import CogneeClient, SearchType


async def main():
    # Configuration
    COGNEE_URL = "http://eva_cognee:8181"
    DATASET_NAME = "DesconSim"

    print("=" * 80)
    print("Cognee API Test - Search Packer Priming and Downstream Control")
    print("=" * 80)
    print()

    # Initialize Cognee client
    print(f"Connecting to Cognee API at {COGNEE_URL}...")
    client = CogneeClient(base_url=COGNEE_URL, timeout=300.0)
    print("✓ Client initialized")
    print()

    try:
        # Health check
        print("Checking server health...")
        health_result = await client.health()
        print(f"✓ Server is healthy: {health_result}")
        print()

        # Search for packer priming and downstream control
        print("=" * 80)
        print("SEARCH: 'Explain packer priming and downstream control'")
        print("=" * 80)
        print()

        search_result = await client.search(
            query_text="Explain packer priming and downstream control",
            query_type=SearchType.GRAPH_COMPLETION
        )

        if search_result.get("success"):
            print("✓ Search completed successfully")
            print()
            print("-" * 80)
            print("RESULTS:")
            print("-" * 80)
            print()

            # Display the search results
            search_data = search_result.get("data", [])

            if isinstance(search_data, list):
                if len(search_data) == 0:
                    print("No results returned")
                else:
                    for i, item in enumerate(search_data, 1):
                        print(f"Result {i}:")
                        print(item)
                        print()
            elif isinstance(search_data, dict):
                for key, value in search_data.items():
                    print(f"{key}:")
                    print(f"  {value}")
                    print()
            else:
                print(search_data)

            print("-" * 80)
        else:
            print(f"ERROR: Search failed: {search_result}")
            return 1

    except Exception as e:
        print(f"ERROR: Operation failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        # Cleanup
        await client.close()
        print()
        print("✓ Client connection closed")

    print()
    print("Search test completed!")
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
