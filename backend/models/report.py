from models.db_handler import DBHandler

def ReportBean(params):
    return {
        "id": params[0],
        "plaintiffId": params[1],
        "defendantId": params[2],
        "reason": params[3],
        "status": params[4]
    }

def get(id):
    with DBHandler() as db:
        db.execute("""
            SELECT *
            FROM reports
            WHERE id = %s;
        """, [id])
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

def update(id, status):
    with DBHandler() as db:
        db.execute("""
            UPDATE reports
            SET status = %s
            WHERE id = %s;
        """, [status, id])
    return "Report updated"

def delete(id):
    with DBHandler() as db:
        db.execute("""
            DELETE FROM reports
            WHERE id = %s;
        """)
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