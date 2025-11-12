#!/usr/bin/env python3
"""
Cognee Administration Utility
Manage Cognee memory, datasets, and system data
"""

import asyncio
import sys
from client import CogneeClient


async def main():
    COGNEE_URL = "http://eva_cognee:8181"

    if len(sys.argv) < 2:
        print("Cognee Administration Utility")
        print()
        print("Usage: ./cognee_admin.py <command>")
        print()
        print("Commands:")
        print("  health         - Check server health")
        print("  prune          - Clear all data (documents, knowledge graphs)")
        print("  prune_system   - Clear system data (graph, vector, metadata, cache)")
        print("  reset_all      - Clear both data and system (complete reset)")
        print()
        return 1

    command = sys.argv[1].lower()

    client = CogneeClient(base_url=COGNEE_URL, timeout=300.0)

    try:
        if command == "health":
            print("Checking server health...")
            result = await client.health()
            print(f"✓ {result}")

        elif command == "prune":
            print("Clearing all data (documents, knowledge graphs)...")
            print("This will remove all datasets, documents, and processed data.")
            confirm = input("Are you sure? (yes/no): ")
            if confirm.lower() == "yes":
                result = await client.prune()
                print(f"✓ {result.get('message')}")
            else:
                print("Cancelled")

        elif command == "prune_system":
            print("Clearing system data (graph, vector, metadata, cache)...")
            confirm = input("Are you sure? (yes/no): ")
            if confirm.lower() == "yes":
                result = await client.prune_system()
                print(f"✓ {result.get('message')}")
            else:
                print("Cancelled")

        elif command == "reset_all":
            print("COMPLETE RESET - This will clear ALL data and system data!")
            confirm = input("Are you absolutely sure? (yes/no): ")
            if confirm.lower() == "yes":
                print("\n1. Clearing data...")
                result1 = await client.prune()
                print(f"   ✓ {result1.get('message')}")

                print("2. Clearing system...")
                result2 = await client.prune_system()
                print(f"   ✓ {result2.get('message')}")

                print("\n✓ Complete reset finished!")
            else:
                print("Cancelled")

        else:
            print(f"ERROR: Unknown command '{command}'")
            return 1

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
