from flask import Blueprint, Flask, render_template, request, send_file

from src.flask_app.more_insights import (
    build_jobs_urls,
    get_int_from_args,
    get_job,
    slice_jobs,
)
from src.insights.industries import filter_by_industry, get_unique_industries
from src.insights.jobs import filter_by_job_type, get_unique_job_types, read
from src.insights.salaries import (
    filter_by_salary_range,
    get_max_salary,
    get_min_salary,
)

bp = Blueprint("client", __name__, template_folder="templates")


@bp.route("/.images/job.png")
def flask_image():
    return send_file("../../.images/job.png", mimetype="image/png")


@bp.route("/")
def index():
    md = """
<p align="center">
    <img src="/.images/job.png" alt="Logo da Aplicação" width="800"/>
</p>
<h2 align="center">
    Boas-vindas ao Job Insights<br><br>
</h2>
        """
    return render_template("index.jinja2", md=md)


@bp.route("/jobs")
def list_jobs():
    first_job = get_int_from_args("first_job", 0)
    amount = get_int_from_args("amount", 20)
    salary = get_int_from_args("salary", None)
    industry = request.args.get("industry", None)
    job_type = request.args.get("job_type", None)

    jobs = read(path="data/jobs.csv")
    if industry:
        jobs = filter_by_industry(jobs, industry)
    if job_type:
        jobs = filter_by_job_type(jobs, job_type)
    if salary:
        jobs = filter_by_salary_range(jobs, salary)

    jobs = slice_jobs(jobs, first_job, amount)

    build_jobs_urls(jobs)

    ctx = {
        "jobs": jobs,
        "industries": sorted(get_unique_industries("data/jobs.csv")),
        "job_types": sorted(get_unique_job_types("data/jobs.csv")),
        "previous_job_type": job_type,
        "previous_first": first_job,
        "previous_amount": amount,
        "previous_industry": industry,
        "previous_salary": salary,
        "min_salary": get_min_salary("data/jobs.csv"),
        "max_salary": get_max_salary("data/jobs.csv"),
    }

    return render_template("list_jobs.jinja2", ctx=ctx)


@bp.route("/job/<index>")
def job(index):
    jobs_data = read("data/jobs.csv")
    one_job = get_job(jobs_data, index)
    return render_template("job.jinja2", job=one_job)


def init_app(app: Flask):
    app.register_blueprint(bp)
