def is_remote(location):
    if not location:
        return False
    loc = location.lower()
    return "remote" in loc or "work from home" in loc or "wfh" in loc

def has_stipend(stipend):
    if not stipend:
        return False
    s = stipend.lower()
    return "unpaid" not in s and any(char.isdigit() for char in s)

def filter_jobs(jobs, min_score=0):
    """
    Filter jobs based on minimum score.
    """
    return [job for job in jobs if job.get('score', 0) >= min_score]
