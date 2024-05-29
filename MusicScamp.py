from scamp import *
from math import *
import random

s = Session().run_as_server()
n1 = s.new_part("Cello")
n2 = s.new_part("Oboe")
n3 = s.new_part("Flute")
n1.set_max_pitch_bend(100)
n2.set_max_pitch_bend(100)
n3.set_max_pitch_bend(100)
cresc = Envelope.from_levels([0.6,0.8,1.0])

def chrom (start, end, time):
    step = ((start-end)/time)
    return [start - (step * x) for x in range(0,time+1)]

def osci (start, end, time):
    step = ((start-end)/time)*2
    returnable = [start]
    p = start
    while p > end:
        p = p + step
        returnable.append(p)
        p = p - step*2
        returnable.append(p)
    #returnable.append(end)
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
    # returnable.append(end)
    # returnable.append(end)
    return returnable

def jump (start, end, time):
    step = ((start-end)/time)*2
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
    p = round(start)
    while p != end:
        returnable.append(p)
        p = harm_func(p, end)
    returnable.append(end)
    return returnable

def harm_func(note, end):
    print(type(note))
    print(type(end))
    degree = (note-end)%8
    print (degree)
    if degree == 0:
        return end
    if degree == 1:
        return end
    if degree == 2:
        return random(end+1, end+3)
    if degree == 3:
        return end + 5
    if degree == 4:
        return random(end+3, end+5)
    if degree == 5:
        return end
    if degree == 6:
        return end + 5
    if degree == 7:
        return random(end+8, end +6)
    return 90

def degrade_smooth (start, end, time, function, part):
    pitches = function(start, end, time) #allows different functions to work in code
    print(function, pitches)
    part.play_note(pitches, 0.6, time)

def degrade_list (start, end, time, function, part):
    pitches = function(start, end, time)
    print(function, pitches)
    for pitch in pitches:
        part.play_note(pitch, 0.6, (time/len(pitches)))

def bass (pitch, time):
    n1.play_note(pitch, 0.5, time)

def bass_inf (pitch):
    while True:
        bass(pitch,100)

def trash_bag_sound (time):
    b = s.new_part("Bird")
    s.fork(b.play_note,args=(70, 0.5, time))

    #note = random.randint(61,71)
    s.fork(degrade_smooth,args=(70, 50, time, random_function([chrom, jump, osci, tenuto]),random_function([n1,n2,n3]))) # swap between list and smooth / differing functions

def random_function(options): # takes input list
    return options[random.randint(0,len(options)-1)]

# sprint 1 demo notes
    # need to see audio and visual together in the same scene to figure out the ideas better
    # audio should be more different
    # audio should match up with shapes more + vibes (plastic bottle sounds different than bag etc)
    # music feels ominous but should feel more naturelike, bird/flute, calming, serene
    # background color should be changed to something that works better with the visuals
    # work in large rough strokes to make it easy to show off

# spring 2 demo notes
    # ?
    # ?
    # ?
    # ?
    # ?