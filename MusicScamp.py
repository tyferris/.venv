from scamp import *
from math import *
import random


# basic set up
s = Session().run_as_server()
s.tempo = 60
#s.synchronization_policy = "no synchronization"

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

def rand (start, end, time):
    returnable = []
    p = start
    while p != end:
        returnable.append(p)
        p = random.randint(end, p+3)
    returnable.append(end)
    return returnable

def bottle (start, end, time):
    returnable = []
    p = start
    i = 0
    while i <= start-end-2:
        returnable.append(p)
        returnable.append(p)
        p = random.randint(end, round(start-(i/2)))
        i+=1
    returnable.append(end)
    return returnable

def ostinato (start, end, time):
    # blues_scale = [end, end+3, end+5, end+6, end+7, end+10, end+12, end+15, end+17, end+18, end+19, end+22, end+24]
    returnable = []
    # p = start
    # i = 0
    # while i <= time*4:
    #     returnable.append(p)
    #     p = random.choice(blues_scale)
    #     if i >= time*3:
    #         blues_scale.pop()
    #     i+=1
    # returnable.append(end)
    return returnable

def single (start, end, time):
    return ([70])

def major_harmonic(start, end, time):
    degree = (start-end)%12
    returnable = []
    i = 0
    note = start
    while i <= time*2 and note != end:
        print("degree = ", degree)
        for x in range (1,3):
            returnable.append(note)
            print(x)
        if degree == 0: # 1st
            note = random.choice([end, end+7, end+7, end+12, end+12])
        elif degree == 2: # 2nd
            note = random.choice([end, end+4, end+4, end+14])
        elif degree == 4: # 3rd
            note = random.choice([end+2, end+5, end+5, end+7, end+7])
        elif degree == 5: # 4th
            note = random.choice([end+5, end+7, end+7, end+7, end+9])
        elif degree == 7: # 5th
            note = random.choice([end, end, end+5, end+7, end+9, end+12])        
        elif degree == 9: # 6th
            note = random.choice([end+7, end+7, end+11, end+11, end+11])
        elif degree == 11: # 7th
            note = random.choice([end+5, end+12, end+12, end+12])
        else:
            note = round(note-1)
    returnable.append(end)
    return returnable

def blues (start, end, time):
    blues_scale = [end, end+3, end+5, end+6, end+7, end+10, end+12, end+15, end+17, end+18, end+19, end+22, end+24]
    returnable = []
    p = start
    i = 0
    while i <= time*4:
        if i - time*2 <= 1:
            blues_scale = [end, end+3, end+5, end+6, end+7, end+10, end+12]
            print("it ran")
        returnable.append(p)
        p = random.choice(blues_scale)
        i+=1
    returnable.append(end)
    return returnable


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
    note = random.randint(64,71)
    s.fork(degrade_smooth,args=(note, 50, time, major_harmonic, n1))

def plasticbag_sound (time):
    note = 70 # random.randint(64,71)
    s.fork(degrade_smooth,args=(note, 50, time, random_function([osci, tenuto, jump]), random_function([n1,n2,n3])))

def trashbag_sound (time):
    note = 70 # random.randint(64,71)
    s.fork(degrade_smooth,args=(note, 50, time, random_function([osci, tenuto, jump]), random_function([n1,n2,n3])))

def can_sound (time):
    s.fork(degrade_list,args=(random.choice([77,65,53]), 50, time, blues, n4))
    s.fork(degrade_list,args=(random.choice([74,62,50]), 50, time, blues, n4))

