from click.testing import CliRunner

from xbot import xbot


def test_ls():
    runner = CliRunner()
    result = runner.invoke(xbot, ["node", "ls", "--all"])
    assert result.exit_code == 0
    assert "Name" in result.output


test_ls()
