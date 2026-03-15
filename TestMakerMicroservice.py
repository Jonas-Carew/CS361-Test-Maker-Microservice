
import zmq
from random import randrange

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5558")

ERRORS = [
    "Too few terms",
    ]

def error(err_num):
    socket.send_string("ERROR: " + ERRORS[err_num])

while True:
    lists = socket.recv_pyobj()
    copy = lists.copy()

    if (len(lists) < 4):
        error(0)
        continue

    leng = len(lists)
    for _ in range(leng):
        n = randrange(len(lists))
        pair = lists.pop(n)

        bad_list = copy.copy()
        bad_list.pop(n)
        bad_terms = []
        for _ in range(3):
            bad_term = bad_list.pop(randrange(len(bad_list)))
            bad_terms.append(bad_term)

        correct = randrange(4)
        qlist = [pair[1]] + bad_terms[:correct] + [pair[0]] + bad_terms[correct:]
        socket.send_pyobj(qlist,zmq.SNDMORE)

