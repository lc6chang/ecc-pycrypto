import unittest

from ecc import curve
from ecc import registry


CURVES: list[curve.Curve] = [
    registry.P256,
    registry.secp256k1,
    registry.Curve25519,
    registry.M383,
    registry.E222,
    registry.E382,
]


class TestCasePointAndCurve(unittest.TestCase):
    def test_operator(self):
        for curve_ in CURVES:
            with self.subTest(name=curve_.name):
                P = curve_.G
                self.assertEqual(P + P, 2 * P)
                self.assertEqual(P - P, curve_.INF)
                self.assertEqual(P + (-P), curve_.INF)
                self.assertEqual(P + P + P + P + P, P * 5)
                self.assertEqual(-P - P - P - P - P, -5 * P)
                self.assertEqual(P - 2 * P, -P)
                self.assertEqual(20 * P + 4 * P, 10 * P + 14 * P)
                self.assertEqual(curve_.INF + 10 * P, 10 * P)
                self.assertEqual(curve_.INF - 3 * P, -3 * P)
                self.assertEqual(curve_.INF + curve_.INF, curve_.INF)
                self.assertEqual(0 * P, curve_.INF)
                self.assertEqual(1000 * curve_.INF, curve_.INF)

    def test_double_points_y_equals_to_0(self):
        P = curve.Point(curve=registry.Curve25519, x=0, y=0)
        self.assertEqual(P + P, registry.Curve25519.INF)
        self.assertEqual(2 * P, registry.Curve25519.INF)
        self.assertEqual(-2 * P, registry.Curve25519.INF)

    def test_point_not_on_curve(self):
        with self.assertRaises(ValueError):
            curve.Point(curve=registry.Curve25519, x=1, y=0)
