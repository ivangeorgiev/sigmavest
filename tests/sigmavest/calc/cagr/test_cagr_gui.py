import pytest
from unittest.mock import MagicMock, patch
from sigmavest.calc.cagr.gui import CAGRCalculatorGUI

# filepath: src/sigmavest/calc/cagr/test_gui.py


@pytest.fixture
def mock_ctk():
    with patch("sigmavest.calc.cagr.gui.ctk") as mock_ctk:
        yield mock_ctk


@pytest.fixture
def gui_app(mock_ctk):
    root = MagicMock()
    app = CAGRCalculatorGUI(root)
    app.start_value = MagicMock()
    app.end_value = MagicMock()
    app.years = MagicMock()
    return app


class TestCAGRCalculatorGUI:
    def test_calculate_valid_input(self, gui_app):
        # Simulate valid user inputs
        gui_app.start_value.get = MagicMock(return_value="1000")
        gui_app.end_value.get = MagicMock(return_value="2000")
        gui_app.years.get = MagicMock(return_value="3")

        # Call the calculate method
        gui_app.calculate()

        # Assert the result label is updated with the correct CAGR value
        gui_app.result_label.configure.assert_called_once_with(
            text="CAGR: 25.99%",
            text_color="#2ECC71"
        )

    def test_calculate_invalid_input(self, gui_app):
        # Simulate invalid user inputs (non-numeric values)
        gui_app.start_value.get = MagicMock(return_value="abc")
        gui_app.end_value.get = MagicMock(return_value="2000")
        gui_app.years.get = MagicMock(return_value="3")

        # Call the calculate method
        gui_app.calculate()

        # Assert the result label is updated with an error message
        gui_app.result_label.configure.assert_called_once_with(
            text="Error: could not convert string to float: 'abc'",
            text_color="#E74C3C"
        )

    def test_calculate_zero_years(self, gui_app):
        # Simulate zero years input
        gui_app.start_value.get = MagicMock(return_value="1000")
        gui_app.end_value.get = MagicMock(return_value="2000")
        gui_app.years.get = MagicMock(return_value="0")

        # Call the calculate method
        gui_app.calculate()

        # Assert the result label is updated with an error message
        gui_app.result_label.configure.assert_called_once_with(
            text="Error: Investment periods must be more than 0",
            text_color="#E74C3C"
        )