import unittest
from src.parsers.media_parser import PARSER_MAPPING
from src.parsers.format_utils import PARSER_CONFIG

class TestISOPriority(unittest.TestCase):
    def test_mapping_priority(self):
        """Ensures pycdlib comes before isoparser in the .iso mapping."""
        mapping = PARSER_MAPPING.get(".iso", [])
        self.assertIn("pycdlib", mapping)
        self.assertIn("isoparser", mapping)
        
        pycd_idx = mapping.index("pycdlib")
        iso_idx = mapping.index("isoparser")
        
        self.assertLess(pycd_idx, iso_idx, "pycdlib should have higher priority than isoparser in mapping")

    def test_chain_priority(self):
        """Ensures pycdlib comes before isoparser in the global parser chain."""
        print(f"DEBUG: PARSER_CONFIG={PARSER_CONFIG}")
        chain = PARSER_CONFIG.get("parser_chain", [])
        print(f"DEBUG: chain={chain}")
        self.assertIn("pycdlib", chain)
        self.assertIn("isoparser", chain)
        
        pycd_idx = chain.index("pycdlib")
        iso_idx = chain.index("isoparser")
        
        self.assertLess(pycd_idx, iso_idx, "pycdlib should have higher priority than isoparser in chain")

if __name__ == "__main__":
    unittest.main()
