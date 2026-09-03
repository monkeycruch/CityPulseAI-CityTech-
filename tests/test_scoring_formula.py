import pytest
from scoring_formula import score_incident

def test_score_incident_happy_path():
    # Priority Score = (Severity x Weather) + Impact + Complaints + Accessibility
    # (4.0 * 1.3) + 2.5 + 1.8 + 1.5 = 5.2 + 2.5 + 1.8 + 1.5 = 11.0
    assert score_incident(4.0, 1.3, 2.5, 1.8, 1.5) == 11.0

    # (2.0 * 1.1) + 1.0 + 0.5 + 0.5 = 2.2 + 1.0 + 0.5 + 0.5 = 4.2
    assert score_incident(2.0, 1.1, 1.0, 0.5, 0.5) == 4.2

def test_score_incident_min_values():
    # min values: (1.0 * 1.0) + 0.0 + 0.0 + 0.0 = 1.0
    assert score_incident(1.0, 1.0, 0.0, 0.0, 0.0) == 1.0

def test_score_incident_max_values():
    # max values: (5.0 * 1.5) + 3.0 + 2.0 + 2.0 = 7.5 + 3.0 + 2.0 + 2.0 = 14.5
    assert score_incident(5.0, 1.5, 3.0, 2.0, 2.0) == 14.5

def test_score_incident_validation_errors():
    # severity out of bounds (1.0-5.0)
    with pytest.raises(ValueError, match="'severity' value 0.5 is out of range"):
        score_incident(0.5, 1.0, 0.0, 0.0, 0.0)
    with pytest.raises(ValueError, match="'severity' value 5.1 is out of range"):
        score_incident(5.1, 1.0, 0.0, 0.0, 0.0)

    # weather out of bounds (1.0-1.5)
    with pytest.raises(ValueError, match="'weather' value 0.9 is out of range"):
        score_incident(1.0, 0.9, 0.0, 0.0, 0.0)
    with pytest.raises(ValueError, match="'weather' value 1.6 is out of range"):
        score_incident(1.0, 1.6, 0.0, 0.0, 0.0)

    # impact out of bounds (0.0-3.0)
    with pytest.raises(ValueError, match="'impact' value -0.1 is out of range"):
        score_incident(1.0, 1.0, -0.1, 0.0, 0.0)
    with pytest.raises(ValueError, match="'impact' value 3.1 is out of range"):
        score_incident(1.0, 1.0, 3.1, 0.0, 0.0)

    # complaints out of bounds (0.0-2.0)
    with pytest.raises(ValueError, match="'complaints' value -0.1 is out of range"):
        score_incident(1.0, 1.0, 0.0, -0.1, 0.0)
    with pytest.raises(ValueError, match="'complaints' value 2.1 is out of range"):
        score_incident(1.0, 1.0, 0.0, 2.1, 0.0)

    # accessibility out of bounds (0.0-2.0)
    with pytest.raises(ValueError, match="'accessibility' value -0.1 is out of range"):
        score_incident(1.0, 1.0, 0.0, 0.0, -0.1)
    with pytest.raises(ValueError, match="'accessibility' value 2.1 is out of range"):
        score_incident(1.0, 1.0, 0.0, 0.0, 2.1)

def test_score_incident_disable_validation():
    # Should not raise exception
    assert score_incident(0.0, 0.0, 0.0, 0.0, 0.0, validate=False) == 0.0
    assert score_incident(10.0, 2.0, 5.0, 5.0, 5.0, validate=False) == 35.0
