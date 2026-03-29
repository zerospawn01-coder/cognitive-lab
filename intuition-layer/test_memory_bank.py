import unittest

import numpy as np

from memory_bank import FixedMemoryBank


class TestFixedMemoryBankCosineNormalization(unittest.TestCase):
    def test_retrieve_preserves_cosine_ranking_for_non_unit_embeddings(self):
        embeddings = {
            "query": np.array([1.0, 0.0]),
            "aligned": np.array([1.0, 0.0]),
            "large_off_axis": np.array([10.0, 10.0]),
        }

        bank = FixedMemoryBank(embed_fn=lambda text: embeddings[text])
        bank.add_episode("aligned", answer="A", importance=1.0)
        bank.add_episode("large_off_axis", answer="B", importance=1.0)

        results = bank.retrieve("query", k=2)

        self.assertEqual(results[0][0], "aligned")
        self.assertAlmostEqual(results[0][1], 1.0, places=6)
        self.assertLess(results[1][1], results[0][1])

    def test_get_min_distance_stays_non_negative_for_scaled_embeddings(self):
        embeddings = {
            "query": np.array([3.0, 0.0]),
            "stored": np.array([30.0, 0.0]),
        }

        bank = FixedMemoryBank(embed_fn=lambda text: embeddings[text])
        bank.add_episode("stored", answer="A", importance=1.0)

        distance = bank.get_min_distance("query")

        self.assertGreaterEqual(distance, 0.0)
        self.assertAlmostEqual(distance, 0.0, places=6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
