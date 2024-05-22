from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MySQL configurations
app.config['MYSQL_HOST'] = 'nebula.c9ewiciweyd6.eu-north-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'nebula'
app.config['MYSQL_PASSWORD'] = 'Mangi1979'
app.config['MYSQL_DB'] = 'Nebula_Admin1'

mysql = MySQL(app)

@app.route('/')
def index():
    return "Welcome to Nebula"

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Return no content for favicon.ico requests

@app.route('/api/health-check', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/test-db-connection', methods=['GET', 'POST'])
def test_db_connection():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        cur.close()
        return jsonify({"status": "success", "result": result}), 200
    except Exception as e:
        print(f"Error connecting to the database: {e}")  # Detailed error logging
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/admins', methods=['GET'])
def get_admins():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Nebula_Admin1")
    admins = cur.fetchall()
    cur.close()
    return jsonify(admins)

@app.route('/api/admin', methods=['POST'])
def add_admin():
    data = request.get_json()
    name = data['name']
    email = data['email']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Nebula_Admin1 (name, email) VALUES (%s, %s)", (name, email))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Admin added successfully'})

@app.route('/api/admin/<int:id>', methods=['PUT'])
def update_admin(id):
    data = request.get_json()
    name = data['name']
    email = data['email']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE Nebula_Admin1 SET name = %s, email = %s WHERE id = %s", (name, email, id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Admin updated successfully'})

@app.route('/api/admin/<int:id>', methods=['DELETE'])
def delete_admin(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Nebula_Admin1 WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Admin deleted successfully'})

if __name__ == '__master__':
    app.run(debug=True)