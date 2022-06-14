import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []

questions = [
     "what is han jisung's english name \n a.peter\n b.chris\n c.bob\n d.sam",
     "who is the main vocalist of dreamcatcher \n a.lee siyeon\n b.jeon soyeon\n c.kim siyoon\n d.ah sullyoon",
     "who did the whisper in ateez's to the beat \n a.seonghwa\n b.hongjoong\n c.yunho\n d.san",
     "what was the first group i stanned \n a.blackpink\n b.stray kids\n c.dreamcatcher\n d.ateez"
]

answers = ['a', 'a', 'b', 'a']

print("vroom vroom...")

def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions) - 1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def clientthread(conn):
    score = 0
    conn.send("slay".encode('utf-8'))
    conn.send("welcome to the quiz slay\n".encode('utf-8'))
    conn.send("good luck uwu\n\n".encode('utf-8'))
    index, question, answer = get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send(f"SLAY YOU GOT {score}\n\n".encode('utf-8'))
                else:
                    conn.send("no\n\n".encode('utf-8'))
                remove_question(index)
                index, question, answer = get_random_question_answer(conn)
            else:
                remove(conn)
        except:
            continue

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print (addr[0] + " connected")
    new_thread = Thread(target= clientthread,args=(conn))
    new_thread.start()
