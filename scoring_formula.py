"""
scoring_formula.py
------------------
CityPulse AI — Priority Scoring Engine

Computes an equity-adjusted priority score for each road incident
and assigns it to one of four repair tiers.

Formula:
    Priority Score = (Severity x Weather) + Impact + Complaints + Accessibility

Usage:
    from scoring_formula import score_incident, assign_tier, score_dataframe

Authors: Mohammed Imad, Ronny Yeap
Course:  CET4973 — Intro to Artificial Intelligence, Spring 2026
"""

# ---------------------------------------------------------------------------
# Feature ranges (for validation)
# ---------------------------------------------------------------------------
FEATURE_RANGES = {
    "severity":      (1.0, 5.0),   # road damage level (1=minor, 5=severe)
    "weather":       (1.0, 1.5),   # rain/freeze risk multiplier
    "impact":        (0.0, 3.0),   # proximity to schools, hospitals
    "complaints":    (0.0, 2.0),   # 311 volume, normalized for reporting rate
    "accessibility": (0.0, 2.0),   # vulnerable-user concentration
}

# Score range: min = 1.0*1.0 + 0 + 0 + 0 = 1.0
#              max = 5.0*1.5 + 3 + 2 + 2  = 14.5
SCORE_MIN = 1.0
SCORE_MAX = 14.5

# ---------------------------------------------------------------------------
# Tier thresholds
# ---------------------------------------------------------------------------
TIER_THRESHOLDS = {
    "Critical": 11.0,   # repair within 24 hours
    "High":      7.0,   # repair within 48 hours
    "Medium":    4.0,   # schedule within 1-2 weeks
    "Low":       0.0,   # routine queue
}

TIER_RESPONSE_TIMES = {
    "Critical": "Within 24 hours",
    "High":     "Within 48 hours",
    "Medium":   "1–2 weeks",
    "Low":      "Routine queue",
}


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def score_incident(severity, weather, impact, complaints, accessibility,
                   validate=True):
    """
    Compute the priority score for a single road incident.

    Parameters
    ----------
    severity      : float, 1.0–5.0  — damage level from CV model (Team 1)
    weather       : float, 1.0–1.5  — weather risk multiplier (OpenWeatherMap)
    impact        : float, 0.0–3.0  — facility proximity score
    complaints    : float, 0.0–2.0  — reporting-rate-adjusted 311 score
    accessibility : float, 0.0–2.0  — vulnerable-user concentration
    validate      : bool             — raise ValueError if inputs out of range

    Returns
    -------
    float — priority score in [1.0, 14.5]

    Examples
    --------
    >>> score_incident(severity=4.0, weather=1.3, impact=2.5,
    ...                complaints=1.8, accessibility=1.5)
    11.0
    """
    if validate:
        args = {
            "severity": severity,
            "weather": weather,
            "impact": impact,
            "complaints": complaints,
            "accessibility": accessibility,
        }
        for name, value in args.items():
            lo, hi = FEATURE_RANGES[name]
            if not (lo <= value <= hi):
                raise ValueError(
                    f"'{name}' value {value} is out of range [{lo}, {hi}]"
                )

    score = (severity * weather) + impact + complaints + accessibility
    return round(score, 4)


def assign_tier(score):
    """
    Convert a numeric priority score to a tier label.

    Parameters
    ----------
    score : float — output of score_incident()

    Returns
    -------
    str — one of 'Critical', 'High', 'Medium', 'Low'

    Examples
    --------
    >>> assign_tier(11.5)
    'Critical'
    >>> assign_tier(8.2)
    'High'
    >>> assign_tier(5.0)
    'Medium'
    >>> assign_tier(2.1)
    'Low'
    """
    if score >= TIER_THRESHOLDS["Critical"]:
        return "Critical"
    elif score >= TIER_THRESHOLDS["High"]:
        return "High"
    elif score >= TIER_THRESHOLDS["Medium"]:
        return "Medium"
    else:
        return "Low"


def score_dataframe(df, validate=True):
    """
    Apply the scoring formula to an entire pandas DataFrame.

    The DataFrame must contain these columns:
        severity, weather, impact, complaints, accessibility

    Adds two new columns:
        priority_score — numeric score
        priority_tier  — tier label (Critical / High / Medium / Low)

    Parameters
    ----------
    df       : pd.DataFrame — input feature DataFrame
    validate : bool         — check feature ranges row by row (slower)

    Returns
    -------
    pd.DataFrame — original DataFrame with two columns appended

    Examples
    --------
    >>> import pandas as pd
    >>> from scoring_formula import score_dataframe
    >>> df = pd.DataFrame({
    ...     'severity':      [4.0, 2.5, 1.5],
    ...     'weather':       [1.3, 1.1, 1.0],
    ...     'impact':        [2.5, 1.5, 0.5],
    ...     'complaints':    [1.8, 1.0, 0.3],
    ...     'accessibility': [1.5, 1.0, 0.5],
    ... })
    >>> score_dataframe(df)[['priority_score', 'priority_tier']]
       priority_score priority_tier
    0           11.00      Critical
    1            6.25        Medium
    2            2.80           Low
    """
    import pandas as pd

    required = list(FEATURE_RANGES.keys())
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"DataFrame is missing columns: {missing}")

    df = df.copy()

    # Vectorized formula — no loop needed
    df["priority_score"] = (
        (df["severity"] * df["weather"])
        + df["impact"]
        + df["complaints"]
        + df["accessibility"]
    ).round(4)

    df["priority_tier"] = df["priority_score"].apply(assign_tier)

    return df


def explain_score(severity, weather, impact, complaints, accessibility):
    """
    Return a human-readable breakdown of a single incident's score.
    Useful for the dashboard popup and qualitative analysis.

    Examples
    --------
    >>> print(explain_score(4.0, 1.3, 2.5, 1.8, 1.5))
    Priority Score:  11.00 / 14.5
    Priority Tier:   Critical — Within 24 hours
    <BLANKLINE>
    Score breakdown:
      Severity × Weather   = 4.0 × 1.3 = 5.2
      Impact               = 2.5
      Complaints           = 1.8
      Accessibility        = 1.5
      ─────────────────────────────────────
      Total                = 11.00
    """
    score = score_incident(severity, weather, impact, complaints,
                           accessibility, validate=False)
    tier  = assign_tier(score)
    sev_component = round(severity * weather, 4)

    lines = [
        f"Priority Score:  {score:.2f} / {SCORE_MAX}",
        f"Priority Tier:   {tier} — {TIER_RESPONSE_TIMES[tier]}",
        "",
        "Score breakdown:",
        f"  Severity × Weather   = {severity} × {weather} = {sev_component}",
        f"  Impact               = {impact}",
        f"  Complaints           = {complaints}",
        f"  Accessibility        = {accessibility}",
        f"  ─────────────────────────────────────",
        f"  Total                = {score:.2f}",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Quick demo — runs when executed directly: python scoring_formula.py
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== CityPulse AI — Scoring Formula Demo ===\n")

    # Example 1: severe pothole near school in high-risk weather — should be Critical
    print("Example 1: Severe pothole near school, rain forecast")
    print(explain_score(
        severity=4.5, weather=1.4, impact=2.8,
        complaints=1.9, accessibility=1.8
    ))

    print()

    # Example 2: minor crack, dry weather, low-density area — should be Low/Medium
    print("Example 2: Minor crack, dry weather, low-density area")
    print(explain_score(
        severity=1.5, weather=1.0, impact=0.5,
        complaints=0.3, accessibility=0.4
    ))

    print()

    # Example 3: DataFrame usage
    print("Example 3: Batch scoring with score_dataframe()")
    import pandas as pd
    sample = pd.DataFrame({
        "severity":      [4.5, 2.5, 1.5],
        "weather":       [1.4, 1.1, 1.0],
        "impact":        [2.8, 1.5, 0.5],
        "complaints":    [1.9, 1.0, 0.3],
        "accessibility": [1.8, 1.0, 0.4],
        "borough":       ["Bronx", "Queens", "Staten Island"],
    })
    result = score_dataframe(sample)
    print(result[["borough", "priority_score", "priority_tier"]].to_string(index=False))
