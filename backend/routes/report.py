from flask import request, jsonify
from app import app, auth
import models.report as Report

@app.post("/api/v1/report")
@auth.login(roles=['user', 'admin'])
def post_report():
    plaintiff_id = auth.get_user()['id']
    defendant = request.json["defendant"]
    reason = request.json["reason"]
    report = Report.new(plaintiff_id, defendant, reason)
    return jsonify(report)


@app.put("/api/v1/report")
@auth.login(roles=['admin'])
def put_report():
    report_id = request.json["report_id"]
    status = request.json["status"]
    return Report.update_status(report_id, status)


@app.delete("/api/v1/report")
@auth.login(roles=['admin'])
def delete_report():
    report_id = request.json["report_id"]
    return Report.delete(report_id)
