from typer.testing import CliRunner
from sigmavest.calc.cli import app

runner = CliRunner()


class TestCalcCLI:
    def test_summary_command(self):
        result = runner.invoke(app, ["summary"])
        assert result.exit_code == 0
        assert "This is the `calc` command summary." in result.output

    def test_cagr_command_registered(self):
        subcommand_names = [cmd_info.name for cmd_info in app.registered_groups]
        assert "cagr" in subcommand_names
