import mysql.connector
from mysql.connector import Error

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Shiva123',
    database='mysql'  
)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
 emp_id INT PRIMARY KEY,
 emp_name VARCHAR(100),
 department VARCHAR(50),
 job_name VARCHAR(50),
 manager_id INT NULL,
 hire_date DATE,
 salary DECIMAL(10,2),
 commission DECIMAL(10,2) NULL
);
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
 sale_id INT PRIMARY KEY,
 date DATE NOT NULL,
 amount DECIMAL(12,2) NOT NULL
);
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
 transaction_id INT AUTO_INCREMENT PRIMARY KEY,
 col1 VARCHAR(50) NOT NULL,
 col2 VARCHAR(50) NOT NULL,
 transaction_date DATE,
 amount DECIMAL(12,2)
);
''')

cursor.execute("DELETE FROM employees")
cursor.execute("DELETE FROM sales")
cursor.execute("DELETE FROM transactions")
employees_data = [
    (1, 'Alice', 'HR', 'Manager', None, '2020-01-15', 70000, None),
    (2, 'Bob', 'HR', 'Executive', 1, '2021-03-10', 40000, 2000),
    (3, 'Charlie', 'IT', 'Developer', 4, '2019-07-23', 60000, None),
    (4, 'David', 'IT', 'Manager', None, '2018-11-05', 80000, 5000),
    (5, 'Eve', 'Sales', 'Executive', 6, '2022-02-20', 45000, 1500),
    (6, 'Frank', 'Sales', 'Manager', None, '2017-09-12', 75000, None)
]
cursor.executemany("INSERT INTO employees VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", employees_data)
sales_data = [
    (1, '2024-01-01', 1000),
    (2, '2024-01-02', 1500),
    (3, '2024-01-03', 1200),
    (4, '2024-01-04', 1800)
]
cursor.executemany("INSERT INTO sales VALUES (%s,%s,%s)", sales_data)
transactions_data = [
    ('A', 'X', '2024-01-01', 100),
    ('A', 'X', '2024-01-02', 200),
    ('B', 'Y', '2024-01-03', 150),
    ('A', 'X', '2024-01-04', 300),
    ('B', 'Y', '2024-01-05', 250),
    ('C', 'Z', '2024-01-06', 400)
]
cursor.executemany("INSERT INTO transactions (col1, col2, transaction_date, amount) VALUES (%s,%s,%s,%s)", transactions_data)
conn.commit()

task1 = "SELECT MAX(salary) AS second_highest_salary FROM employees WHERE salary < (SELECT MAX(salary) FROM employees)"
cursor.execute(task1)
print('Second highest salary:', cursor.fetchone()[0])

task2 = '''
SELECT emp_name, department, salary FROM employees e
WHERE salary > (
    SELECT AVG(salary) FROM employees WHERE department = e.department
)
'''
cursor.execute(task2)
print('Employees earning more than department average:')
for row in cursor.fetchall():
    print(row)

task3 = '''
SELECT date, amount, SUM(amount) OVER (ORDER BY date) AS running_total FROM sales ORDER BY date
'''
cursor.execute(task3)
print('Running total of sales:')
for row in cursor.fetchall():
    print(row)

task4 = '''
SELECT col1, col2, COUNT(*) as cnt FROM transactions
GROUP BY col1, col2
HAVING cnt > 1
'''
cursor.execute(task4)
print('Duplicate (col1, col2) combinations:')
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()