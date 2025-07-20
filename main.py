from fastapi import FastAPI, Query
from jobspy import scrape_jobs
from typing import Optional, List
import pandas as pd

app = FastAPI(title="JobSpy API", description="Scrape jobs from multiple job boards using JobSpy")

@app.get("/")
def home():
    return {"status": "JobSpy API is running!"}

@app.get("/jobs")
def get_jobs(
    query: str = Query(..., description="Job title or keyword"),
    location: str = Query(..., description="Job location"),
    sites: str = Query("linkedin,indeed,glassdoor,zip_recruiter", description="Comma-separated job boards"),
    hours_old: int = Query(72, description="Filter jobs posted in last X hours"),
    results: int = Query(20, description="Number of results per site"),
    job_type: Optional[str] = Query(None, description="fulltime, parttime, contract, internship"),
    is_remote: Optional[bool] = Query(False, description="True for remote jobs only")
):
    try:
        # Parse sites into list
        site_list = [s.strip() for s in sites.split(",")]

        # Perform scraping
        jobs = scrape_jobs(
            site_name=site_list,
            search_term=query,
            location=location,
            results_wanted=results,
            hours_old=hours_old,
            job_type=job_type,
            is_remote=is_remote,
            country_indeed="USA"
        )

        # Replace NaN with None for valid JSON
        jobs = jobs.replace({float("nan"): None})

        return {
            "status": "success",
            "query": query,
            "location": location,
            "total_jobs": len(jobs),
            "sites": site_list,
            "jobs": jobs.to_dict(orient="records")
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }