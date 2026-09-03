import pytest
import pandas as pd
from scoring_formula import score_dataframe

def test_score_dataframe_success():
    """Test that score_dataframe correctly calculates scores and tiers for valid input."""
    # Given
    df = pd.DataFrame({
        'severity':      [4.0, 2.5, 1.5, 4.5],
        'weather':       [1.3, 1.1, 1.0, 1.4],
        'impact':        [2.5, 1.5, 0.5, 2.8],
        'complaints':    [1.8, 1.0, 0.3, 1.9],
        'accessibility': [1.5, 1.0, 0.5, 1.8],
        'other_column':  ['A', 'B', 'C', 'D'] # Verify extra columns are kept
    })

    # Expected scores: (severity * weather) + impact + complaints + accessibility
    # Row 0: (4.0 * 1.3) + 2.5 + 1.8 + 1.5 = 5.2 + 5.8 = 11.00 (Critical)
    # Row 1: (2.5 * 1.1) + 1.5 + 1.0 + 1.0 = 2.75 + 3.5 = 6.25 (Medium)
    # Row 2: (1.5 * 1.0) + 0.5 + 0.3 + 0.5 = 1.5 + 1.3 = 2.80 (Low)
    # Row 3: (4.5 * 1.4) + 2.8 + 1.9 + 1.8 = 6.3 + 6.5 = 12.80 (Critical)

    # When
    result_df = score_dataframe(df)

    # Then
    assert 'priority_score' in result_df.columns
    assert 'priority_tier' in result_df.columns
    assert 'other_column' in result_df.columns

    assert result_df['priority_score'].tolist() == [11.00, 6.25, 2.80, 12.80]
    assert result_df['priority_tier'].tolist() == ['Critical', 'Medium', 'Low', 'Critical']

def test_score_dataframe_missing_columns():
    """Test that score_dataframe raises ValueError when required columns are missing."""
    # Given a DataFrame missing 'weather' and 'accessibility'
    df = pd.DataFrame({
        'severity':   [4.0],
        'impact':     [2.5],
        'complaints': [1.8],
    })

    # When / Then
    with pytest.raises(ValueError, match="DataFrame is missing columns"):
        score_dataframe(df)

def test_score_dataframe_preserves_original():
    """Test that score_dataframe returns a new DataFrame and does not modify the original."""
    # Given
    original_df = pd.DataFrame({
        'severity':      [4.0],
        'weather':       [1.3],
        'impact':        [2.5],
        'complaints':    [1.8],
        'accessibility': [1.5],
    })

    # When
    result_df = score_dataframe(original_df)

    # Then
    assert 'priority_score' not in original_df.columns
    assert 'priority_tier' not in original_df.columns
    assert id(original_df) != id(result_df)
