import pytest
from scoring_formula import score_incident

def test_score_incident_happy_path():
    # Valid values
    score = score_incident(
        severity=4.0,
        weather=1.3,
        impact=2.5,
        complaints=1.8,
        accessibility=1.5
    )
    assert isinstance(score, float)
    assert score == 11.0

def test_score_incident_invalid_severity():
    with pytest.raises(ValueError, match="'severity' value 0.9 is out of range"):
        score_incident(severity=0.9, weather=1.3, impact=2.5, complaints=1.8, accessibility=1.5)

    with pytest.raises(ValueError, match="'severity' value 5.1 is out of range"):
        score_incident(severity=5.1, weather=1.3, impact=2.5, complaints=1.8, accessibility=1.5)

def test_score_incident_invalid_weather():
    with pytest.raises(ValueError, match="'weather' value 0.9 is out of range"):
        score_incident(severity=4.0, weather=0.9, impact=2.5, complaints=1.8, accessibility=1.5)

    with pytest.raises(ValueError, match="'weather' value 1.6 is out of range"):
        score_incident(severity=4.0, weather=1.6, impact=2.5, complaints=1.8, accessibility=1.5)

def test_score_incident_invalid_impact():
    with pytest.raises(ValueError, match="'impact' value -0.1 is out of range"):
        score_incident(severity=4.0, weather=1.3, impact=-0.1, complaints=1.8, accessibility=1.5)

    with pytest.raises(ValueError, match="'impact' value 3.1 is out of range"):
        score_incident(severity=4.0, weather=1.3, impact=3.1, complaints=1.8, accessibility=1.5)

def test_score_incident_invalid_complaints():
    with pytest.raises(ValueError, match="'complaints' value -0.1 is out of range"):
        score_incident(severity=4.0, weather=1.3, impact=2.5, complaints=-0.1, accessibility=1.5)

    with pytest.raises(ValueError, match="'complaints' value 2.1 is out of range"):
        score_incident(severity=4.0, weather=1.3, impact=2.5, complaints=2.1, accessibility=1.5)

def test_score_incident_invalid_accessibility():
    with pytest.raises(ValueError, match="'accessibility' value -0.1 is out of range"):
        score_incident(severity=4.0, weather=1.3, impact=2.5, complaints=1.8, accessibility=-0.1)

    with pytest.raises(ValueError, match="'accessibility' value 2.1 is out of range"):
        score_incident(severity=4.0, weather=1.3, impact=2.5, complaints=1.8, accessibility=2.1)

def test_score_incident_no_validate():
    # It should not raise an error if validate=False
    score = score_incident(
        severity=5.1,
        weather=1.6,
        impact=3.1,
        complaints=2.1,
        accessibility=2.1,
        validate=False
    )
    assert isinstance(score, float)
