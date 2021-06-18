from models.db_handler import DBHandler
from models.user import UserBean, get as get_user
from models.helpers import parse_timestamp


def ReportBean(params):
    return {
        "id": params[0],
        "plaintiff": get_user(params[1]),
        "defendant": get_user(params[2]),
        "reason": params[3],
        "status": params[4],
        "created_at": parse_timestamp(params[5])
    }


def get(report_id):
    with DBHandler() as db:
        db.execute("""
            SELECT *
            FROM reports
            WHERE id = %s;
        """, [report_id])
        report = db.one()
    return ReportBean(report)


def new(plaintiff_id, defendant, reason):
    with DBHandler() as db:
        db.execute("""
            SELECT id
            FROM users
            WHERE username = %s;
        """, [defendant])
        tmp = db.one()
        if tmp:
            defendant_id = tmp[0]
            db.execute("""
                INSERT INTO reports(plaintiff_id, defendant_id, reason, status, created_at)
                VALUES(%s, %s, %s, 'pending', 'now')
                RETURNING id;
            """, [plaintiff_id, defendant_id, reason])
            id = db.one()[0]
        else:
            return "No user with that name"
    return get(id)


def update_status(report_id, status):
    with DBHandler() as db:
        db.execute("""
            UPDATE reports
            SET status = %s
            WHERE id = %s;
        """, [status, report_id])
    return "Report updated"


def delete(report_id):
    with DBHandler() as db:
        db.execute("""
            DELETE FROM reports
            WHERE id = %s;
        """, [report_id])
    return "Report deleted"


def get_all():
    with DBHandler() as db:
        db.execute("""
            SELECT *
            FROM reports;
        """)
        from_db = db.all()
    reports = []
    for report in from_db:
        reports.append(ReportBean(report))
    return reports
