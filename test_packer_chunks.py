#!/usr/bin/env python3
"""
Test retrieving actual document chunks with semantic search
This should show the raw content that matches the query
"""

import asyncio
import sys
from client import CogneeClient, SearchType


async def main():
    COGNEE_URL = "http://eva_cognee:8181"

    print("=" * 80)
    print("Packer Documentation - Chunk Retrieval Test")
    print("=" * 80)
    print()

    client = CogneeClient(base_url=COGNEE_URL, timeout=300.0)

    try:
        queries = [
            "priming downstream control",
            "speed control hierarchy configuration",
            "virtual conveyor system",
            "packer configuration properties"
        ]

        for query in queries:
            print("=" * 80)
            print(f"QUERY: {query}")
            print("=" * 80)

            # Try CHUNKS - should return semantically similar document chunks
            result = await client.search(
                query_text=query,
                query_type=SearchType.CHUNKS
            )

            if result.get("success"):
                data = result.get("data", [])

                if isinstance(data, list) and len(data) > 0:
                    # Take first result
                    chunk = data[0]

                    if isinstance(chunk, dict) and 'text' in chunk:
                        text = chunk['text']

                        # Find the relevant section in the text
                        lines = text.split('\n')

                        # Print relevant lines (look for the query terms)
                        query_terms = query.lower().split()
                        relevant_lines = []

                        for i, line in enumerate(lines):
                            line_lower = line.lower()
                            if any(term in line_lower for term in query_terms):
                                # Print context: 2 lines before, the line, and 5 lines after
                                start = max(0, i - 2)
                                end = min(len(lines), i + 6)
                                relevant_lines = lines[start:end]
                                break

                        if relevant_lines:
                            print("\nRelevant section:")
                            print("-" * 80)
                            for line in relevant_lines:
                                print(line)
                            print("-" * 80)
                        else:
                            # If no specific match, show first 20 lines
                            print("\nFirst 20 lines of chunk:")
                            print("-" * 80)
                            for line in lines[:20]:
                                print(line)
                            print("-" * 80)
                    else:
                        print(f"Unexpected chunk format: {chunk}")
                else:
                    print("No results")
            else:
                print(f"Search failed: {result}")

            print()

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
