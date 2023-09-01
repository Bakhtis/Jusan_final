from flask import Flask, jsonify, send_file
import openpyxl
import psycopg2
import uuid
from datetime import datetime

app = Flask(__name__)

@app.route('/generate-report', methods=['GET'])
def generate_report():
    connection = psycopg2.connect(
        dbname="hackathon",
        user="postgres",
        password="postgres",
        host="jdbc:postgresql://database-1-jusan.co9yxdynjyur.us-west-2.rds.amazonaws.com:5432/hackathon",
        port="5432"
    )
    
    cursor = connection.cursor()
    sql_query = "SELECT * FROM anketas"
    cursor.execute(sql_query)
    results = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    
    sheet.append(column_names)
    
    for row in results:
        sheet.append(row)
    
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_filename = f"/app/reports/report_{timestamp}_{unique_id}.xlsx"
    workbook.save(report_filename)
    
    cursor.close()
    connection.close()
    
    return send_file(report_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

