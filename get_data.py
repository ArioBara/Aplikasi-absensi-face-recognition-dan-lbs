from config import db_connection, db_cursor

def get_positions():
    query = "SELECT * FROM position ORDER BY position_name ASC"
    db_cursor.execute(query)
    positions = db_cursor.fetchall()
    return positions

def get_shift():
    query = "SELECT * FROM shift ORDER BY shift_name ASC"
    db_cursor.execute(query)
    shifts = db_cursor.fetchall()
    return shifts

def get_one_presence(id_employees, presence_date):
    query = "SELECT * FROM presence WHERE id_employees = %s AND presence_date = %s"
    db_cursor.execute(query, (id_employees, presence_date))
    presence = db_cursor.fetchone()
    return presence

def get_presence(id_employees):
    query = "SELECT * FROM presence WHERE id_employees = %s"
    db_cursor.execute(query, (id_employees,))
    presence = db_cursor.fetchall()
    return presence

def get_presence_status():
    query = "SELECT * from present_status order by present_name ASC"
    db_cursor.execute(query)
    presence_status = db_cursor.fetchall()
    return presence_status

def get_position_name(id_employees):
    query = '''
            SELECT e.id_position, p.position_name 
            FROM employees as e
            JOIN position as p ON e.id_position = p.id_position
            WHERE e.id_employees = %s
            ORDER BY p.id_position ASC
            '''
    db_cursor.execute(query, (id_employees,))
    result = db_cursor.fetchone()
    if result:
        position = result['id_position']
        return position
    else:
        return None
    
def get_shift_name(id_employees):
    query = '''
            SELECT e.id_shift, s.shift_name 
            FROM employees as e
            JOIN shift as s ON e.id_shift = s.id_shift
            WHERE e.id_employees = %s
            ORDER BY s.id_shift ASC
            '''
    db_cursor.execute(query, (id_employees,))
    result = db_cursor.fetchone()
    if result:
        shift = result['id_shift']
        return shift
    else:
        return None

def get_presence_employees(id_employees):
    query = '''
            SELECT p.id_presence, p.presence_date, p.time_in, p.time_out, ps.id_present, ps.present_name
            FROM presence as p
            JOIN employees as e ON p.id_employees = e.id_employees
            JOIN present_status as ps ON p.id_present = ps.id_present
            WHERE e.id_employees = %s
            '''
    db_cursor.execute(query, (id_employees,))
    results = db_cursor.fetchall()  # Menggunakan fetchall() untuk mengambil semua hasil
    return results

def get_present_name(id_presence):
    query = '''
            SELECT p.id_presence, ps.id_present, ps.present_name
            FROM presence as p
            JOIN present_status as ps ON p.id_present = ps.id_present
            WHERE p.id_presence = %s
            '''
    db_cursor.execute(query,(id_presence,))
    result = db_cursor.fetchone()
    return result

def get_date_presence(id_employees, start_date, end_date):
    query = '''
            SELECT p.id_presence, p.presence_date, p.time_in, p.time_out, ps.id_present, ps.present_name
            FROM presence as p
            JOIN employees as e ON p.id_employees = e.id_employees
            JOIN present_status as ps ON p.id_present = ps.id_present
            WHERE e.id_employees = %s AND p.presence_date BETWEEN %s AND %s
            '''
    db_cursor.execute(query, (id_employees, start_date, end_date))
    result = db_cursor.fetchall()
    return result

def get_employees_cuty(id_employees):
    query = '''
            SELECT e.name, c.id_cuty, c.id_employees, c.cuty_start, c.cuty_end, c.date_work, c.cuty_description, c.cuty_status
            FROM cuty as c
            JOIN employees as e ON c.id_employees = e.id_employees
            WHERE e.id_employees = %s
            ORDER BY c.id_cuty DESC
            '''
    db_cursor.execute(query, (id_employees,))
    result = db_cursor.fetchall()
    return result

def get_date_cuty(id_employees, start_date, end_date):
    query = '''
            SELECT c.id_cuty, c.cuty_start, c.cuty_end, c.date_work, c.cuty_description, c.cuty_status, e.name
            FROM cuty AS c
            JOIN employees AS e ON c.id_employees = e.id_employees
            WHERE e.id_employees = %s AND c.cuty_start AND c.cuty_end BETWEEN %s AND %s
            '''
    db_cursor.execute(query, (id_employees, start_date, end_date))
    result = db_cursor.fetchall()
    return result

def get_employees():
    query = 'SELECT * FROM employees'
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    return result

def get_employees_count():
    query = 'SELECT * FROM employees'
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    return len(result)

def get_employees_data():
    query = '''
            SELECT e.id_employees, e.employees_code, e.name, e.photo, p.id_position, p.position_name, s.id_shift, s.shift_name
            FROM employees as e
            JOIN position as p ON e.id_position = p.id_position
            JOIN shift as s ON s.id_shift = e.id_shift
            '''
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    return result

def get_position_count():
    query = 'SELECT * FROM position'
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    return len(result)

def get_shift_count():
    query = 'SELECT * FROM shift'
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    return len(result)

def get_employees_cuty_admin():
    query = '''
            SELECT c.id_cuty, e.name, c.cuty_start, c.cuty_end, c.date_work, c.cuty_description, c.cuty_status
            FROM cuty AS c, employees AS e
            WHERE c.id_employees = e.id_employees
            '''
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    return result

def get_cuty_count():
    query = 'SELECT * FROM cuty'
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    return len(result)

def get_presence_admin():
    query = '''
            SELECT p.id_presence, e.name, p.presence_date, p.time_in, p.time_out, ps.present_name, p.keterangan, p.picture_in, p.picture_out
            FROM presence AS p
            JOIN employees AS e ON p.id_employees = e.id_employees
            JOIN present_status AS ps ON p.id_present = ps.id_present
            '''
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    return result

def get_admin():
    query = 'SELECT * FROM admin'
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    return result