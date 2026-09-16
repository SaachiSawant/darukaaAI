import sys
import unittest

if __name__ == "__main__":
    print("Starting Darukaa Test Suite...", flush=True)
    loader = unittest.TestLoader()
    suite = loader.discover(".", pattern="test_system.py")
    runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("\nALL TESTS PASSED SUCCESSFULLY!", flush=True)
        sys.exit(0)
    else:
        print("\nTESTS FAILED!", flush=True)
        sys.exit(1)
