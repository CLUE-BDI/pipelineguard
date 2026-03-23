import json
import os
import psycopg2

DB_HOST = os.getenv("PGHOST", "localhost")
DB_NAME = os.getenv("PGDATABASE", "pipelineguard")
DB_USER = os.getenv("PGUSER", "postgres")
DB_PASS = os.getenv("PGPASSWORD", "postgres")
DB_PORT = os.getenv("PGPORT", "5432")

def main():
    with open("outputs/correlated_findings.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
    )
    cur = conn.cursor()

    for item in data["correlated_findings"]:
        cur.execute("""
            INSERT INTO findings (
                finding_id, repo, branch, commit_sha, pipeline_id, file_path, line_start, line_end,
                title, severity, mitre_technique, mitre_name, confidence, matched_by, evidence
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s::jsonb)
            ON CONFLICT (finding_id) DO NOTHING
        """, (
            item["finding_id"],
            item["repo"],
            item["branch"],
            item["commit_sha"],
            item["pipeline_id"],
            item["file_path"],
            item["line_start"],
            item["line_end"],
            item["title"],
            item["severity"],
            item["mitre"]["technique"],
            item["mitre"]["name"],
            item["confidence"],
            json.dumps(item["matched_by"]),
            json.dumps(item["evidence"]),
        ))

    conn.commit()
    cur.close()
    conn.close()
    print("Findings loaded into PostgreSQL")

if __name__ == "__main__":
    main()