import unittest
from datetime import datetime

from raconteur.analysis import classify, compare_countries
from raconteur.data import Record


def rec(year, hours, country):
    return Record(datetime(year, 6, 1), hours, country)


RECORDS = [
    rec(1999, 9.0, "A"),
    rec(2000, 1.0, "A"),
    rec(2001, 2.0, "A"),
    rec(2001, 2.0, "B"),
    rec(2002, 9.0, "B"),
]


class TestCompareCountries(unittest.TestCase):
    def test_known_answers(self):
        result = compare_countries(RECORDS, "A", "B", 2000, 2001)
        a, b = result["countries"]
        self.assertEqual((a["count"], a["total"], a["average"]), (2, 3.0, 1.5))
        self.assertEqual((b["count"], b["total"], b["average"]), (1, 2.0, 2.0))
        self.assertEqual(result["leader"], "A")

    def test_no_evas_is_unavailable_and_tie(self):
        result = compare_countries(RECORDS, "A", "B", 1990, 1995)
        a, b = result["countries"]
        self.assertEqual((a["count"], a["total"], a["average"]), (0, 0, None))
        self.assertEqual((b["count"], b["total"], b["average"]), (0, 0, None))
        self.assertIsNone(result["leader"])

    def test_invalid_input_raises(self):
        with self.assertRaises(ValueError):
            compare_countries(RECORDS, "A", "B", 2001, 2000)
        with self.assertRaises(ValueError):
            compare_countries(RECORDS, "A", "Narnia", 2000, 2001)


class TestClassify(unittest.TestCase):
    def test_boundaries(self):
        self.assertEqual(classify(3.99), "short")
        self.assertEqual(classify(4), "standard")
        self.assertEqual(classify(6.99), "standard")
        self.assertEqual(classify(7), "long")


if __name__ == "__main__":
    unittest.main()
