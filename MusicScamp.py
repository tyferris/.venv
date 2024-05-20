from scamp import *
from math import *
import random

s = Session()
n = s.new_part("Cello")
n.set_max_pitch_bend(100)
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
    returnable.append(end)
    returnable.append(end)
    return returnable

def tenuto (start, end, time):
    step = 3*((start-end)/time)
    returnable = []
    p = start
    while p > end:
        returnable.append(p)
        p = p - step
        returnable.append(p)
        returnable.append(p)
    returnable.append(end)
    returnable.append(end)
    return returnable

def jump (start, end, time):
    step = ((start-end)/time)*2
    returnable = [start]
    p = start
    while p > end:
        returnable.append(end)
        p = p - step
        returnable.append(p)
    returnable.append(end)
    returnable.append(end)
    return returnable

def degrade (start, end, time, function):
    pitches = function(start, end, time) #allows different functions to work in code
    n.play_note(pitches, 0.6, time)

def bass (pitch, time):
    n.play_note(pitch, cresc, time)

def demo0 ():
    bass(50,3)
    s.fork(degrade,args=(90, 50, 10, chrom))
    bass(50,3)
    s.fork(degrade,args=(90, 50, 10, osci))
    bass(50,3)
    s.fork(degrade,args=(90, 50, 10, tenuto))
    bass(50,3)
    s.fork(degrade,args=(90, 50, 10, jump))
    bass(50,100)

def demo1 ():
    bass(50,8)
    s.fork(degrade,args=(90, 50, 10, chrom))
    s.fork(degrade,args=(90, 50, 30, chrom))
    bass(50,100)

def demo2 ():
    bass(50,5)
    s.fork(degrade,args=(90, 50, 10, osci))
    s.fork(degrade,args=(96, 50, 10, osci))
    bass(50,5)
    s.fork(degrade,args=(90, 50, 10, osci))
    s.fork(degrade,args=(90, 50, 20, osci))
    s.fork(degrade,args=(90, 50, 30, osci))
    bass(50,5)
    s.fork(degrade,args=(90, 50, 10, osci))
    s.fork(degrade,args=(90, 50, 10, chrom))
    bass(50,100)

def demo3 ():
    bass(50,5)
    s.fork(degrade,args=(90, 50, 10, osci))
    s.fork(degrade,args=(96, 50, 10, chrom))
    bass(50,5)
    s.fork(degrade,args=(80, 50, 10, osci))
    s.fork(degrade,args=(70, 50, 20, jump))
    s.fork(degrade,args=(90, 50, 30, tenuto))
    bass(50,100)

def demo4 ():
    bass(50,3) # major
    s.fork(degrade,args=(82, 50, 15, tenuto))
    s.fork(degrade,args=(79, 50, 30, tenuto))
    s.fork(degrade,args=(76, 50, 30, tenuto))
    s.fork(degrade,args=(72, 50, 30, tenuto))
    # bass(50,5) # minor
    # s.fork(degrade,args=(89, 50, 10, osci))
    # s.fork(degrade,args=(85, 50, 10, osci))
    # s.fork(degrade,args=(82, 50, 10, osci))
    # bass(50,5) # 7th
    # s.fork(degrade,args=(92, 50, 10, tenuto))
    # s.fork(degrade,args=(89, 50, 10, tenuto))
    # s.fork(degrade,args=(86, 50, 10, tenuto))
    # s.fork(degrade,args=(82, 50, 10, tenuto))
    bass(50,100)

def note1 (animation_frame):
    start = 70 - (5*(animation_frame-1)) # indexing starts at 1
    end = 70 - (5*(animation_frame)) # indexing starts at 1
    b = s.new_part("Bird")

    s.fork(b.play_note,args=(70, 0.5, 10))
    s.fork(degrade,args=(start, end, 10, tenuto))
    s.fork(bass,args=[50,10])
    s.wait(10)

# demo0()
# demo1()
# demo2()
# demo3()
# demo4()
# s.print_default_soundfont_presets()

# def scale1 ():
#     n.play_note(80,1,1)
#     n.play_note(82,1,1)
#     n.play_note(84,1,1)
#     n.play_note(86,1,1)

# def scale2 ():
#     n.play_note(84,1,1)
#     n.play_note(86,1,1)
#     n.play_note(88,1,1)
#     n.play_note(90,1,1)

# def scale3 ():
#     n.play_note([60,70,80,60],1,5)

# sprint 1 demo notes
    # need to see audio and visual together in the same scene to figure out the ideas better
    # audio should be more different
    # audio should match up with shapes more + vibes (plastic bottle sounds different than bag etc)
    # music feels ominous but should feel more naturelike, bird/flute, calming, serene
    # background color should be changed to something that works better with the visuals
    # work in large rough strokes to make it easy to show off