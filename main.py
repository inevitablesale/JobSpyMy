from fastapi import FastAPI, Query
from jobspy import scrape_jobs
from typing import Optional

app = FastAPI(title="JobSpy API", description="Scrape jobs dynamically from multiple boards")

@app.get("/")
def home():
    return {"status": "JobSpy API is running!"}

@app.get("/jobs")
def get_jobs(
    query: str = Query(..., description="Job title or keyword"),
    location: str = Query(..., description="Job location"),
    sites: str = Query("linkedin,indeed,glassdoor", description="Comma-separated job boards"),
    hours_old: int = Query(72),
    results: int = Query(20)
):
    jobs = scrape_jobs(
        site_name=[s.strip() for s in sites.split(",")],
        search_term=query,
        location=location,
        results_wanted=results,
        hours_old=hours_old,
        country_indeed="USA"
    )
    return {"total_jobs": len(jobs), "jobs": jobs.to_dict(orient="records")}