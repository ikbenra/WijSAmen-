#!/usr/bin/env python3
"""Validate a bounded, pre-registered response-variant calibration card."""

from __future__ import annotations

import json
import sys
from pathlib import Path


OUTCOMES = {"matched", "missed", "unclear"}


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate(card: dict) -> list[str]:
    errors: list[str] = []

    require(card.get("schema_version") == 1, "schema_version must be 1", errors)
    require(bool(card.get("card_id")), "card_id is required", errors)
    require(bool(card.get("preregistered_at")), "preregistered_at is required", errors)
    require(bool(card.get("observed_at")), "observed_at is required", errors)
    require(card.get("interpretation_disclosed") is True,
            "interpretation_disclosed must be true", errors)
    require(card.get("permission_to_test") is True,
            "permission_to_test must be true", errors)
    require(card.get("virtual_lines_labeled_unverified") is True,
            "virtual lines must remain explicitly unverified", errors)
    require(card.get("persistent_learning_claimed") is False,
            "persistent learning may not be claimed", errors)
    require(bool(card.get("observed_line_3")), "observed_line_3 is required", errors)

    predictions = card.get("predictions")
    require(isinstance(predictions, list) and len(predictions) == 3,
            "exactly three predictions are required", errors)
    if isinstance(predictions, list):
        for index, prediction in enumerate(predictions):
            require(isinstance(prediction, dict),
                    f"prediction {index} must be an object", errors)
            if isinstance(prediction, dict):
                for field in ("feature", "expected", "disconfirming_observation"):
                    require(bool(prediction.get(field)),
                            f"prediction {index}.{field} is required", errors)

    scores = card.get("scores")
    require(isinstance(scores, list) and len(scores) == 3,
            "exactly three scores are required", errors)
    if isinstance(scores, list):
        seen_indexes: set[int] = set()
        for score in scores:
            require(isinstance(score, dict), "each score must be an object", errors)
            if not isinstance(score, dict):
                continue
            prediction_index = score.get("prediction_index")
            require(prediction_index in {0, 1, 2},
                    "prediction_index must be 0, 1 or 2", errors)
            if prediction_index in {0, 1, 2}:
                require(prediction_index not in seen_indexes,
                        "each prediction_index may be scored only once", errors)
                seen_indexes.add(prediction_index)
            require(score.get("outcome") in OUTCOMES,
                    "score outcome must be matched, missed or unclear", errors)
            require(bool(score.get("evidence_excerpt")),
                    "each score needs an evidence_excerpt", errors)

    questions = card.get("clarification_questions", [])
    require(isinstance(questions, list), "clarification_questions must be a list", errors)
    if isinstance(questions, list):
        require(len(questions) <= 1, "at most one clarification question is allowed", errors)
        if questions:
            require(any(s.get("outcome") == "missed" for s in scores if isinstance(s, dict)) if isinstance(scores, list) else False,
                    "a clarification question requires at least one material miss", errors)

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_card.py CARD.json", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        card = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    errors = validate(card)
    if errors:
        for error in errors:
            print(f"INVALID: {error}", file=sys.stderr)
        return 1
    print("VALID: pre-registered, permission-bounded and non-persistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
