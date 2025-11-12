#!/usr/bin/env python3
"""
Test client for Cognee API - Packer Documentation
Ingests packer.md document and queries about the packer model.
"""

import asyncio
import sys
from pathlib import Path
from client import CogneeClient, SearchType


async def main():
    # Configuration
    COGNEE_URL = "http://eva_cognee:8181"
    PACKER_DOC_PATH = "/home/steve/DevOps/workspaces/DesconSimGui/docs/packer.md"
    DATASET_NAME = "DesconSim"

    print("=" * 80)
    print("Cognee API Test - Packer Documentation")
    print("=" * 80)
    print()

    # Step 1: Read the packer.md file
    print("[1/5] Reading packer.md document...")
    try:
        packer_doc_path = Path(PACKER_DOC_PATH)
        if not packer_doc_path.exists():
            print(f"ERROR: File not found: {PACKER_DOC_PATH}")
            return 1

        packer_content = packer_doc_path.read_text()
        print(f"✓ Document loaded successfully ({len(packer_content)} characters)")
        print()
    except Exception as e:
        print(f"ERROR: Failed to read document: {e}")
        return 1

    # Step 2: Initialize Cognee client and check health
    print(f"[2/6] Connecting to Cognee API at {COGNEE_URL}...")
    client = CogneeClient(base_url=COGNEE_URL, timeout=1800.0)  # 30 minute timeout
    print("✓ Client initialized (timeout: 1800s / 30 minutes)")
    print()

    try:
        # Step 2.5: Health check
        print("[3/6] Checking server health...")
        health_result = await client.health()
        print(f"✓ Server is healthy: {health_result}")
        print()

        # Step 3: Add document to Cognee
        print(f"[4/6] Adding document to Cognee (dataset: '{DATASET_NAME}')...")
        print(f"  Document size: {len(packer_content)} characters")
        print(f"  Sending data: text=<{len(packer_content)} chars>, dataset_name='{DATASET_NAME}'")
        print(f"  Note: This may take several minutes if Cognee needs to download models...")
        add_result = await client.add(
            text=packer_content,
            dataset_name=DATASET_NAME
        )

        if add_result.get("success"):
            data_id = add_result.get("data", {}).get("data_id")
            print(f"✓ Document added successfully")
            print(f"  Data ID: {data_id}")
            print(f"  Message: {add_result.get('message')}")
        else:
            print(f"ERROR: Failed to add document: {add_result}")
            return 1
        print()

        # Step 4: Cognify the data (build knowledge graph)
        print(f"[5/6] Building knowledge graph (cognify)...")
        cognify_result = await client.cognify(datasets=[DATASET_NAME])

        if cognify_result.get("success"):
            print(f"✓ Knowledge graph built successfully")
            print(f"  Message: {cognify_result.get('message')}")
        else:
            print(f"ERROR: Failed to cognify: {cognify_result}")
            return 1
        print()

        # Optional: Memify (enrich the graph)
        # Uncomment if you want to enrich the graph
        # print(f"[5/6] Enriching graph (memify)...")
        # memify_result = await client.memify(dataset=DATASET_NAME)
        # if memify_result.get("success"):
        #     print(f"✓ Graph enriched successfully")
        # print()

        # Step 5: Search for packer model explanation
        print("[6/6] Searching: 'How does the packer model work?'")
        search_result = await client.search(
            query_text="How does the packer model work?",
            query_type=SearchType.GRAPH_COMPLETION
        )

        if search_result.get("success"):
            print("✓ Search completed successfully")
            print()
            print("=" * 80)
            print("SEARCH RESULTS")
            print("=" * 80)
            print()

            # Display the search results
            search_data = search_result.get("data", {})
            if isinstance(search_data, dict):
                # Pretty print the results
                for key, value in search_data.items():
                    print(f"{key}:")
                    print(f"  {value}")
                    print()
            elif isinstance(search_data, list):
                for i, item in enumerate(search_data, 1):
                    print(f"Result {i}:")
                    print(f"  {item}")
                    print()
            else:
                print(search_data)

            print("=" * 80)
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
    print("Test completed successfully!")
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
