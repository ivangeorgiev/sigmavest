import pytest
from sigmavest.calc.cagr import calculate_cagr


class TestCalculateCAGR:
    def test_valid(self):
        assert calculate_cagr(1000, 2000, 3) == pytest.approx(0.259921, rel=1e-5)
        assert calculate_cagr(500, 1000, 5) == pytest.approx(0.148698, rel=1e-5)
        assert calculate_cagr(100, 121, 2) == pytest.approx(0.1, rel=1e-5)

    def test_zero_periods(self):
        with pytest.raises(ValueError, match="Investment periods must be more than 0"):
            calculate_cagr(1000, 2000, 0)

    def test_negative_periods(self):
        with pytest.raises(ValueError, match="Investment periods must be more than 0"):
            calculate_cagr(1000, 2000, -1)

    def test_zero_start_value(self):
        with pytest.raises(ValueError, match="Starting value must be positive"):
            calculate_cagr(0, 2000, 3)

    def test_negative_start_value(self):
        with pytest.raises(ValueError, match="Starting value must be positive"):
            calculate_cagr(-1000, 2000, 3)

    def test_edge_case(self):
        assert calculate_cagr(1000, 1000, 3) == 0
