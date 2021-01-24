import sqlite3
DB_PATH = 'todo.db'
NOTSTARTED = 'Not Started'
INPROGRESS = 'In Progress'
COMPLETED = 'Completed'
status_list =[NOTSTARTED,INPROGRESS,COMPLETED]

def add_item_to_todo_list(item):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('insert into items(item, status) values(?,?)', (item, NOTSTARTED))
        conn.commit()
        return {"item": item, "status": NOTSTARTED}
    except Exception as e:
        print('Error', e)
        return None

def get_all_todo_items():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('select * FROM items')
        rows =c.fetchall()
        return { "count": len(rows), "items": rows }
    except Exception as e:
        print('Error', e)
        return None


def update_item(item, status):
    if status not in status_list:
        print("Invalid Status: " + status)
        return None

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('update items set status=? where item=?', (status, item))
        conn.commit()
        return {"item": item, "status": status}
    except Exception as e:
        print('Error', e)
        return None

def get_status(item):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("select status from items where item='%s'" % item)   
        status = c.fetchone()[0]
        return status
    except Exception as e:
        print('Error: ', e)
        return None

def delete_item(item):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("delete from items where item='%s'" % item)
        conn.commit()
        return {'item': item}
    except Exception as e:
        print('Error: ', e)
        return None
        