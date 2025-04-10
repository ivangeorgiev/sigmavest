from typer.testing import CliRunner
from sigmavest.cli import app

runner = CliRunner()


class TestSigmavestCLI:
    def test_calc_group_registered(self):
        registered_groups = [group.name for group in app.registered_groups]
        assert "calc" in registered_groups

    def test_calc_summary_command(self):
        result = runner.invoke(app, ["calc", "summary"])
        assert result.exit_code == 0
        assert "This is the `calc` command summary." in result.output
