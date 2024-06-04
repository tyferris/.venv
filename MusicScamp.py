from scamp import *
from math import *
import random


# basic set up
s = Session().run_as_server()
s.tempo = 60

cello = s.new_part("Cello")
oboe = s.new_part("Oboe")
flute = s.new_part("Flute")
harp = s.new_part("Harp")
guitar = s.new_part("Guitar")

cello.set_max_pitch_bend(100)
oboe.set_max_pitch_bend(100)
flute.set_max_pitch_bend(100)
harp.set_max_pitch_bend(100)
guitar.set_max_pitch_bend(100)

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
    while i <= 2*(start-end-1):
        returnable.append(p)
        returnable.append(p)
        p = random.randint(end, round(start-(i/2)))
        i+=1
    returnable.append(end)
    returnable.append(end)
    returnable.append(end)
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
    returnable = []
    i = 0
    note = start
    while i <= time:
        degree = (note-end)%12
        returnable.append(note)
        i+=1
        if degree == 0: # 1st
            returnable.append(note)
            note = random.choice([end, end+7, end+7, end+12, end+12])
        elif degree == 2: # 2nd
            note = random.choice([end, end+4, end+4, end+14])
        elif degree == 4: # 3rd
            note = random.choice([end+2, end+5, end+5, end+7, end+7])
        elif degree == 5: # 4th
            returnable.append(note)
            note = random.choice([end+5, end+7, end+7, end+7, end+9])
        elif degree == 7: # 5th
            returnable.append(note)
            note = random.choice([end, end, end+5, end+7, end+9, end+12])        
        elif degree == 9: # 6th
            note = random.choice([end+7, end+7, end+11, end+11, end+11])
        elif degree == 11: # 7th
            note = random.choice([end+5, end+12, end+12, end+12])
        else:
            note = round(note-1)
    returnable.append(end)
    return returnable

def minor_harmonic(start, end, time):
    returnable = []
    i = 0
    note = start
    while i <= time:
        degree = (note-end)%12
        returnable.append(note)
        i+=1
        if degree == 0: # 1st
            returnable.append(note)
            note = random.choice([end, end+7, end+7, end+12, end+12])
        elif degree == 2: # 2nd
            note = random.choice([end, end+3, end+3, end+14])
        elif degree == 3: # 3rd
            note = random.choice([end+2, end+5, end+5, end+7, end+7])
        elif degree == 5: # 4th
            returnable.append(note)
            note = random.choice([end+5, end+7, end+7, end+7, end+8])
        elif degree == 7: # 5th
            returnable.append(note)
            note = random.choice([end, end, end+5, end+7, end+8, end+12])        
        elif degree == 8: # 6th
            note = random.choice([end+7, end+7, end+10, end+10, end+10])
        elif degree == 10: # 7th
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
        if abs(time*2-i) <= 1:
            blues_scale = [end, end+3, end+5, end+6, end+7, end+10, end+12]
        if abs(time*3-i) <= 1:
            blues_scale = [end, end+3, end+5, end+6, end+7]
        returnable.append(p)
        p = random.choice(blues_scale)
        i+=1
    returnable.append(end)
    returnable.append(end)
    returnable.append(end)
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
    cello.play_note(pitch, cresc_small, time)

def bass_inf (pitch):
    while True:
        bass(pitch,100)

def random_function(options): # takes input list
    return options[random.randint(0,len(options)-1)]


# object sound functions
def bottle_sound (time):
    s.fork(degrade_list,args=(86, 62, time, bottle, harp))

def paperbag_sound (time):
    note = random.randint(62,74)
    s.fork(degrade_list,args=(45, 50, time, single, cello))
    s.fork(degrade_list,args=(note, 50, time, major_harmonic, oboe))

def plasticbag_sound (time):
    note = random.randint(58,68)
    s.fork(degrade_smooth,args=(note, 50, time, random_function([tenuto]), cello))

def trashbag_sound (time):
    note = random.randint(62,74)
    s.fork(degrade_list,args=(42, 50, time, single, cello))
    s.fork(degrade_smooth,args=(note, 50, time, minor_harmonic, oboe))

def can_sound (time):
    s.fork(degrade_list,args=(random.choice([77,65,53]), 50, time, blues, guitar))
    s.fork(degrade_list,args=(random.choice([74,62,50]), 50, time, blues, guitar))