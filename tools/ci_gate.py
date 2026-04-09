"""Fail-closed CI gates for Cognitive Lab."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]


class GateFailure(RuntimeError):
    """Raised when a CI gate must fail closed."""

    def __init__(
        self,
        gate: str,
        violation_type: str,
        reason: str,
        file: str | None = None,
        violation_id: str | None = None,
    ) -> None:
        super().__init__(reason)
        self.gate = gate
        self.violation_type = violation_type
        self.reason = reason
        self.file = file
        self.violation_id = violation_id or gate


def _emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def _pass(gate: str, details: dict[str, Any] | None = None) -> int:
    payload = {"gate": gate, "status": "PASS"}
    if details:
        payload["details"] = details
    _emit(payload)
    return 0


def _fail(gate: str, error: GateFailure) -> int:
    _emit(
        {
            "gate": gate,
            "status": "FAIL",
            "violations": [
                {
                    "type": error.violation_type,
                    "id": error.violation_id,
                    "file": error.file or "",
                    "reason": error.reason,
                }
            ],
        }
    )
    return 1


def _run(command: list[str], gate: str, violation_id: str, file: str) -> str:
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        reason = (completed.stdout + "\n" + completed.stderr).strip()
        raise GateFailure(
            gate=gate,
            violation_type="COMMAND_FAILURE",
            violation_id=violation_id,
            file=file,
            reason=reason or f"Command failed: {' '.join(command)}",
        )
    return completed.stdout


def run_validate_leap_analysis() -> int:
    gate = "validate-leap-analysis"
    _run(
        [sys.executable, "leap_analysis/test_leap_analysis.py"],
        gate=gate,
        violation_id="leap-analysis",
        file="leap_analysis/test_leap_analysis.py",
    )
    return _pass(gate, {"command": "python leap_analysis/test_leap_analysis.py"})


def run_validate_post_alignment_lab() -> int:
    gate = "validate-post-alignment-lab"
    _run(
        [sys.executable, "post_alignment_lab/test_post_alignment_phase2.py"],
        gate=gate,
        violation_id="post-alignment-lab",
        file="post_alignment_lab/test_post_alignment_phase2.py",
    )
    return _pass(gate, {"command": "python post_alignment_lab/test_post_alignment_phase2.py"})


def run_validate_intuition_layer() -> int:
    gate = "validate-intuition-layer"
    _run(
        [sys.executable, "intuition-layer/test_intuition_router.py"],
        gate=gate,
        violation_id="intuition-layer",
        file="intuition-layer/test_intuition_router.py",
    )
    return _pass(gate, {"command": "python intuition-layer/test_intuition_router.py"})


def run_validate_governance() -> int:
    gate = "validate-governance"
    required_paths = [
        "README.md",
        ".github/workflows/test.yml",
        "leap_analysis/test_leap_analysis.py",
        "post_alignment_lab/test_post_alignment_phase2.py",
        "intuition-layer/test_intuition_router.py",
        "intuition-layer/test_memory_bank.py",
    ]
    missing = [path for path in required_paths if not (REPO_ROOT / path).is_file()]
    if missing:
        raise GateFailure(
            gate=gate,
            violation_type="GOVERNANCE_VIOLATION",
            violation_id="required-paths",
            file="",
            reason="Missing maintained pillar files: " + ", ".join(missing),
        )
    return _pass(gate, {"required_paths": required_paths})


def run_unit_tests() -> int:
    gate = "unit-tests"
    _run(
        [sys.executable, "-m", "pytest", "-q"],
        gate=gate,
        violation_id="pytest",
        file=".",
    )
    return _pass(gate, {"command": "python -m pytest -q"})


GATES = {
    "validate-leap-analysis": run_validate_leap_analysis,
    "validate-post-alignment-lab": run_validate_post_alignment_lab,
    "validate-intuition-layer": run_validate_intuition_layer,
    "validate-governance": run_validate_governance,
    "unit-tests": run_unit_tests,
}


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] not in GATES:
        print("Usage: python tools/ci_gate.py <gate>", file=sys.stderr)
        print("Available gates:", ", ".join(sorted(GATES.keys())), file=sys.stderr)
        return 2
    gate = argv[1]
    try:
        return GATES[gate]()
    except GateFailure as error:
        return _fail(gate, error)
    except Exception as error:
        return _fail(
            gate,
            GateFailure(
                gate=gate,
                violation_type="INTERNAL_CI_ERROR",
                violation_id=gate,
                reason=str(error) or "Unexpected CI gate failure.",
            ),
        )


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
