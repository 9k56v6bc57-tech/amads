"""
Implementation of the elim() function from the Matlab MIDI Toolbox.

Eliminates short parts from a score based on their coverage of the
overall score duration.
"""

from amads.core.basics import Part, Score


def elim(score: Score, extent_crit: float = 0.5) -> Score:
    """
    Eliminate parts that are shorter than extent_crit of the score duration.

    Parameters
    ----------
    score : Score
        The score to filter.
    extent_crit : float
        Minimum proportion of the overall score duration that a part
        must cover. Default is 0.5.

    Returns
    -------
    Score
        A score containing only parts meeting the coverage threshold.
    """
    if not 0 <= extent_crit <= 1:
        raise ValueError("extent_crit must be between 0 and 1")

    flat = score if score.is_flat() else score.flatten()

    parts = list(flat.find_all(Part))

    if not parts:
        return flat

    # Overall duration of the score.
    score_start = min(
        note.onset
        for part in parts
        for note in part.content
    )
    score_end = max(
        note.offset
        for part in parts
        for note in part.content
    )
    score_duration = score_end - score_start

    if score_duration <= 0:
        return flat

    # Keep parts whose span covers enough of the overall duration.
    kept_parts = []

    for part in parts:
        if not part.content:
            continue

        part_start = min(note.onset for note in part.content)
        part_end = max(note.offset for note in part.content)

        coverage = (part_end - part_start) / score_duration

        if coverage >= extent_crit:
            kept_parts.append(part)

    result = flat.emptycopy()

    for part in kept_parts:
        result.content.append(part.copy(parent=result))

    return result
