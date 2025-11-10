#!/usr/bin/env python3
"""Simple smoke-runner for environments without pytest installed.

This script calls the async endpoint function directly and exits with 0 on success.
"""
import asyncio
import sys

from backend.main import read_root


def main():
    try:
        result = asyncio.run(read_root())
        expected = {"Hello": "World"}
        if result == expected:
            print("SMOKE TEST PASSED: read_root returned expected value")
            return 0
        else:
            print("SMOKE TEST FAILED: unexpected return value:", result)
            return 2
    except Exception as e:
        print("SMOKE TEST ERROR:", e)
        return 3


if __name__ == "__main__":
    sys.exit(main())
