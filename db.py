import sqlite3
 
def close():
    global connect, cursor
    connect.commit()
    cursor.close()
    connect.close()
 
def open():
    global connect, cursor
    connect = sqlite3.connect("test.db")
    cursor = connect.cursor()
 
def create():
    global connect, cursor
    open()
 
    cursor.execute('''PRAGMA foreign_keys=on''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS quizes 
                    (id INTEGER PRIMARY KEY, name VARCHAR)''')
 
    cursor.execute('''CREATE TABLE IF NOT EXISTS questions 
                    (id INTEGER PRIMARY KEY, text VARCHAR,
                    right VARCHAR, answer_1 VARCHAR, answer_2 VARCHAR)''')
 
    cursor.execute('''CREATE TABLE IF NOT EXISTS links
                    (id INTEGER PRIMARY KEY, quiz_id INTEGER, quest_id INTEGER,
                    FOREIGN KEY (quiz_id) REFERENCES quizes(id),
                    FOREIGN KEY (quest_id) REFERENCES questions(id))''')
 
    close()
 
def set_quizes():
    global connect, cursor
    quiz_list = [("про майкрафт",),
                ("про г. Владимир",)]
 
    open()
    cursor.executemany('''INSERT INTO quizes (name) 
                            VALUES (?)''',quiz_list)
    close()
 
def set_questions():
    global connect, cursor
    quest_list = [("На какой высоте спавнились алмазы","от 12","от 26","от 77"),
                ("Какая версия майкрафта наиболее поздняя из предлженых?","1.5.2","1.7.10","1.12.2"),
                ("кто основал Владимир?","Владимир","Юрий Долгорукий","Чингисхан"),
                ("год создания MineCraft","2011","2013","2017"),
                ("в каком измерении материалы для шалкер-сундука","Эндер-мир","Незер","Простой мир"),
                ("какая река во Владимире?","Клязьма","Обь","Дон"),
                ("в каком году украли ворота золотых ворот?","не известно","вчера","1337")]
 
    open()
    cursor.executemany('''INSERT INTO questions (text,right,answer_1,answer_2) 
                            VALUES (?,?,?,?)''',quest_list)
    close()
 
def set_links():
    global connect, cursor
    open()
    links = [(1,1),
            (1,2),
            (1,4),
            (1,5),]
    cursor.executemany('''INSERT INTO links (quiz_id,quest_id) 
                            VALUES (?,?)''',links)
    close()
 
def clear():
    global connect, cursor
    open()
    cursor.execute('''DROP TABLE IF EXISTS quizes''')
    cursor.execute('''DROP TABLE IF EXISTS questions''')
    cursor.execute('''DROP TABLE IF EXISTS links''')
    close()

def get_next_question(nummer_victor,now_quest):
    global connect, cursor
    open()
    cursor.execute('''SELECT quest_id FROM links WHERE quiz_id==(?) ''',[nummer_victor])
    data = cursor.fetchall()
    return int(data[now_quest][0])

def get_max_question(nummer_victor):
    global connect, cursor
    open()
    cursor.execute('''SELECT quest_id FROM links WHERE quiz_id==(?) ''',[nummer_victor])
    data = cursor.fetchall()
    return len(data)


def get_vopros_by_id(id):
    global connect, cursor
    open()
    cursor.execute('''SELECT * FROM questions WHERE id==(?)''',[id])
    data = cursor.fetchone()
    return data

def get_all_quest():
    global connect, cursor
    open()
    cursor.execute('''SELECT * FROM quizes''')
    data = cursor.fetchall()
    return data

if __name__ == "__main__": 
    clear()
    create()
    set_quizes()
    set_questions()
    set_links()
    print(get_next_question(1,1))
    #open()
    #cursor.execute('''SELECT * FROM links''')
    #data = cursor.fetchall()
    #print(data)
    #print(get_all_quest())