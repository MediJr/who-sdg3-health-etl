"""Fixtures partagées par les tests : un extrait réel de l'API de l'OMS (Sénégal, 2020)."""

import copy
import json
from pathlib import Path

import pytest

from src.transform import TransformResult, build_breakdowns, build_indicators, build_locations, validate_observations

FIXTURE = Path(__file__).parent / "fixtures" / "gho_sample.json"


@pytest.fixture
def sample() -> dict:
    """Une copie fraîche de l'échantillon à chaque test : un test ne peut pas en perturber un autre."""
    return copy.deepcopy(json.loads(FIXTURE.read_text(encoding="utf-8")))


@pytest.fixture
def reference(sample):
    """Référentiels (lieux, ventilations) construits à partir de l'échantillon."""
    return build_locations(sample["dimensions"]), build_breakdowns(sample["dimensions"])


@pytest.fixture
def transform_result(sample, reference) -> TransformResult:
    locations, breakdowns = reference
    observations, quarantine = validate_observations(sample["observations"], locations, breakdowns)
    return TransformResult(build_indicators(sample["indicators"]), locations, breakdowns,
                           observations, quarantine, len(sample["observations"]))
