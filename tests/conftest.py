import json
import re
from pathlib import Path
import pytest

test_results = []


def pytest_addoption(parser):
    """Adds custom command-line options to pytest."""
    parser.addoption(
        "--report",
        action="store_true",
        default=False,
        help="Generate a custom JSON report with test docstring metadata."
    )


def parse_docstring_metadata(docstring: str) -> dict:
    """Extracts ID, TYPE, and SUMMARY fields from formatted test docstrings."""
    if not docstring:
        return {"id": "N/A", "type": "N/A", "summary": "No docstring provided."}

    metadata = {}

    id_match = re.search(r"ID:\s*(.+)", docstring)
    metadata["id"] = id_match.group(1).strip() if id_match else "UNKNOWN-ID"

    type_match = re.search(r"TYPE:\s*(.+)", docstring)
    metadata["type"] = type_match.group(1).strip() if type_match else "UNKNOWN-TYPE"

    summary_match = re.search(r"SUMMARY:\s*(.+)", docstring, re.DOTALL)
    if summary_match:
        metadata["summary"] = summary_match.group(1).strip().replace("\n", " ")
    else:
        metadata["summary"] = "No summary provided."

    return metadata


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Collects metadata only if --report option is supplied."""
    outcome = yield
    report = outcome.get_result()

    if not item.config.getoption("--report"):
        return

    if report.when == "call":
        docstring = item.obj.__doc__ or ""
        metadata = parse_docstring_metadata(docstring)

        test_results.append({
            "test_id": metadata["id"],
            "test_type": metadata["type"],
            "summary": metadata["summary"],
            "test_function": item.name,
            "file": str(item.fspath),
            "outcome": report.outcome.upper(),
            "duration_seconds": round(report.duration, 4),
        })


def pytest_sessionfinish(session, exitstatus):
    """Generates JSON report on session finish ONLY if --report flag was used."""
    if not session.config.getoption("--report"):
        return

    reports_dir = Path(session.rootdir) / "reports"
    reports_dir.mkdir(exist_ok=True)

    report_file = reports_dir / "test_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(test_results, f, indent=2)

    print(f"\n[REPORT GENERATED] Metadata test report saved at: {report_file}")