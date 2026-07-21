"""Guards the Azure (F1/Oryx) deploy step, which builds from a requirements.txt
exported from uv.lock. If this export breaks, the deploy build breaks."""

import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

EXPORT_CMD = [
    "uv",
    "export",
    "--frozen",
    "--no-dev",
    "--no-emit-project",
    "--format",
    "requirements-txt",
]


@pytest.mark.skipif(shutil.which("uv") is None, reason="uv not on PATH")
def test_requirements_export_includes_runtime_server_deps() -> None:
    result = subprocess.run(
        EXPORT_CMD,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    output = result.stdout.lower()

    # The startup command runs uvicorn serving the FastAPI app, so both must
    # be present and version-pinned in the exported requirements.
    assert "fastapi==" in output
    assert "uvicorn==" in output
    # Export must be hash-pinned for reproducible Oryx builds.
    assert "--hash=sha256:" in output
