from scamp import *
from math import *
import random


# basic set up
s = Session().run_as_server()
s.tempo = 60
s.synchronization_policy = "no synchronization"

n1 = s.new_part("Cello")
n2 = s.new_part("Oboe")
n3 = s.new_part("Flute")
n4 = s.new_part("Piano")

n1.set_max_pitch_bend(100)
n2.set_max_pitch_bend(100)
n3.set_max_pitch_bend(100)
n4.set_max_pitch_bend(100)

cresc = Envelope.from_levels([0.6,0.8,1.0])
cresc_small = Envelope.from_levels([0.4,0.6,0.8])


# algorithmic music generation functions
def chrom (start, end, time):
    step = round(((start-end)/time))
    return [start - (step * x) for x in range(0,round(time)+1)]

def osci (start, end, time):
    step = (2*(start-end)/time)
    returnable = [start]
    p = start
    while p > end:
        p = p + step
        returnable.append(p)
        p = p - step*2
        returnable.append(p)
    returnable.append(end)
    return returnable

def tenuto (start, end, time):
    step = 3*((start-end)/time)
    p = start
    returnable = []
    while p > end:
        returnable.append(p)
        returnable.append(p)
        returnable.append(p)
        p = p - step
    returnable.append(end)
    returnable.append(end)
    return returnable

def jump (start, end, time):
    step = 2*((start-end)/time)
    returnable = []
    p = start
    while p > end:
        returnable.append(p)
        returnable.append(end)
        p = p - step
    returnable.append(end)
    returnable.append(end)
    return returnable

def harm (start, end, time):
    returnable = []
    p = start
    while p != end:
        returnable.append(p)
        p = random.randint(end, p+3)
    returnable.append(end)
    return returnable

def bottle (start, end, time):
    returnable = []
    print(start, end)
    p = start
    i = 0
    while i <= start-end-2:
        returnable.append(p)
        returnable.append(p)
        p = random.randint(end, round(start-(i/2)))
        i+=1
    returnable.append(end)
    return returnable

def single (start, end, time):
    return ([70])

def harm_func(note, end):
    print(type(note))
    print(type(end))
    # degree = (note-end)%8
    # print (degree)
    # return random.randrange()
    # if degree == 0:
    #     return end
    # if degree == 1:
    #     return end
    # if degree == 2:
    #     return random(end+1, end+3)
    # if degree == 3:
    #     return end + 5
    # if degree == 4:
    #     return random(end+3, end+5)
    # if degree == 5:
    #     return end
    # if degree == 6:
    #     return end + 5
    # if degree == 7:
    #     return random(end+8, end +6)
    return 90


# basic helper functions for all music
def degrade_smooth (start, end, time, function, part):
    time = time/16
    pitches = function(start, end, time)
    print(function, pitches, "time = ", time, time/len(pitches))
    part.play_note(pitches, 0.6, time)

def degrade_list (start, end, time, function, part):
    time = time/16
    pitches = function(start, end, time)
    print(function, pitches, "time = ", time, time/len(pitches))
    for pitch in pitches:
        part.play_note(pitch, 0.35, (time/len(pitches)))

def bass (pitch, time):
    n1.play_note(pitch, cresc_small, time)

def bass_inf (pitch):
    while True:
        bass(pitch,100)

def random_function(options): # takes input list
    return options[random.randint(0,len(options)-1)]


# object sound functions
def bottle_sound (time):
    s.fork(degrade_list,args=(82, 62, time, bottle, n3))

def paperbag_sound (time):
    note = 70 # random.randint(64,71)
    s.fork(degrade_smooth,args=(note, 50, time, random_function([osci, tenuto, jump]), random_function([n1,n2,n3])))

def plasticbag_sound (time):
    note = 70 # random.randint(64,71)
    s.fork(degrade_smooth,args=(note, 50, time, random_function([osci, tenuto, jump]), random_function([n1,n2,n3])))

def trashbag_sound (time):
    note = 70 # random.randint(64,71)
    s.fork(degrade_smooth,args=(note, 50, time, random_function([osci, tenuto, jump]), random_function([n1,n2,n3])))

def can_sound (time):
    note = 70 # random.randint(64,71)
    s.fork(degrade_smooth,args=(note, 50, time, random_function([osci, tenuto, jump]), n4))