import unittest

from ecc.curve import (
    P256, secp256k1, Curve25519, M383, E222, E382, Point
)

CURVES = [P256, secp256k1, Curve25519, M383, E222, E382]


class PointAndCurveTestCase(unittest.TestCase):
    def test_operator(self):
        for curve in CURVES:
            with self.subTest(curve=curve):
                P = curve.G
                self.assertEqual(P + P, 2 * P)
                self.assertEqual(P - P, curve.INF)
                self.assertEqual(P + (-P), curve.INF)
                self.assertEqual(P + P + P + P + P, P * 5)
                self.assertEqual(-P - P - P - P - P, -5 * P)
                self.assertEqual(P - 2 * P, -P)
                self.assertEqual(20 * P + 4 * P, 10 * P + 14 * P)
                self.assertEqual(curve.INF + 10 * P, 10 * P)
                self.assertEqual(curve.INF - 3 * P, -3 * P)
                self.assertEqual(curve.INF + curve.INF, curve.INF)
                self.assertEqual(0 * P, curve.INF)
                self.assertEqual(1000 * curve.INF, curve.INF)

    def test_double_points_y_equals_to_0(self):
        P = Point(x=0, y=0, curve=Curve25519)
        self.assertEqual(P + P, Curve25519.INF)
        self.assertEqual(2 * P, Curve25519.INF)
        self.assertEqual(-2 * P, Curve25519.INF)
