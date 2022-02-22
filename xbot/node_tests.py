"""
    Before running these tests, make sure that you've generated the required auth token by running `xbot config -e <email> -p <password>`.
    The tests will fail without it, and the native error messages are not very explicit about this.
"""
from click.testing import CliRunner

from xbot import xbot


def test_ls():
    runner = CliRunner()
    result = runner.invoke(xbot, ["node", "ls", "--all"])
    assert result.exit_code == 0
    assert "Name" in result.output


test_ls()
