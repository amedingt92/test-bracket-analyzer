import subprocess


def test_cli_help():
    result = subprocess.run([
        "python",
        "-m",
        "src.cli.main",
        "--help",
    ], capture_output=True, text=True)
    assert result.returncode == 0
    # The help output should mention some subcommands
    assert "ingest" in result.stdout
