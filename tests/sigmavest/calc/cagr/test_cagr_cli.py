from unittest.mock import patch
import pytest
import typer
from typer.testing import CliRunner
from sigmavest.calc.cagr.cli import app

runner = CliRunner()


@pytest.fixture(name="test_app")
def test_app_fixture():
    test_app = typer.Typer()
    test_app.add_typer(app, name="cagr")
    yield test_app

class TestCalculateCLI:
    def test_valid_input(self, test_app):
        result = runner.invoke(test_app, ["cagr", "calculate", "1000", "2000", "3"])
        assert result.exit_code == 0
        assert "CAGR" in result.output
        assert "25.99%" in result.output

    def test_quiet_mode(self, test_app):
        result = runner.invoke(test_app, ["cagr", "calculate", "1000", "2000", "3", "--quiet"])
        assert result.exit_code == 0
        assert result.output.strip() == "0.2599210498948732"

    def test_zero_periods(self, test_app):
        result = runner.invoke(test_app, ["cagr", "calculate", "1000", "2000", "0"])
        assert result.exit_code == 1
        assert "Error: Investment periods must be more than" in result.output

    def test_negative_start_value(self, test_app):
        # "--" is used to separate options from arguments indicating that the following are positional arguments
        # this is a workaround for the CLI to not interpret them as options when starting with a dash
        result = runner.invoke(test_app, ["cagr", "calculate", "--", "-1000", "2000", "3"])
        assert result.exit_code == 1
        assert "Error: Starting value must be positive" in result.output

    def test_edge_case_same_start_end(self, test_app):
        result = runner.invoke(test_app, ["cagr", "calculate", "1000", "1000", "3"])
        assert result.exit_code == 0
        assert "CAGR" in result.output
        assert "0.00%" in result.output

    def test_gui_sub_command(self, test_app):
        with patch("sigmavest.calc.cagr.cli.run_gui") as mock_run_gui:
            result = runner.invoke(test_app, ["cagr", "gui"])
            mock_run_gui.assert_called_once()
            assert result.exit_code == 0
