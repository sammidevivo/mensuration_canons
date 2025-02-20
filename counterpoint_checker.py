from scamp import *
import os

class Melody():
    def __init__(self, notes: list, durations: list):
        self.notes = notes
        self.durations = durations

        self.times = []
        for i in range(len(durations)):
            self.times.append(sum(durations[:i]))

        self.max_time = sum(durations)
    
    def get_time(self, note):
        return self.times[note]
    
    def get_note_at_time(self, time):
        if time > self.max_time:
            return -1
        note = self.notes[0]
        for i in range(len(self.times)):
            note = self.notes[i]
            if time < self.times[i]:
                break
        return note

    def play(self, part: ScampInstrument):
        for note, dur in zip(self.notes, self.durations):
            part.play_note(note, 0.8, dur)

    def get_prev_note(self, note):
        if note == 0:
            return None
        return self.notes[note - 1]
    
    def get_next_note(self, note):
        if note == len(self.notes) - 1:
            return None
        return self.notes[note + 1]

def consonant(p1, p2):
    value = abs(p1 - p2) % 12
    ranges = [(0, 0.14), (2.9564, 3.3564), (3.7231, 4.0531), (6.8796, 7.1596), (7.9469, 8.2769), (8.6436, 9.0436)]

    # Check if value is within any of the given ranges
    for low, high in ranges:
        if low <= value <= high:
            return True
    return False

def check_passing_tone(passing: Melody, base: Melody, passing_ptr):
    # is the next thing the passing pointer is going to gonna be consonant?
    next_time = passing.get_time(passing_ptr + 1)

    if not consonant(passing.get_note_at_time(next_time), base.get_note_at_time(next_time)):
        return False

    # approached and resolved by step?
    before_interval = passing.notes[passing_ptr] - passing.notes[passing_ptr - 1]
    after_interval = passing.notes[passing_ptr + 1] - passing.notes[passing_ptr]

    same_direction = before_interval * after_interval > 0
    if 0.25 <= abs(before_interval) <= 2.5 and 0.25 <= abs(after_interval) <= 2.5 and same_direction:
        return True

    return False

def check_neighboring_tone(neighbor: Melody, base: Melody, neighbor_ptr):
    # is the next thing the neighbor pointer is going to gonna be consonant?
    next_time = neighbor.get_time(neighbor_ptr + 1)
    if not consonant(neighbor.get_note_at_time(next_time), base.get_note_at_time(next_time)):
        return False

    # approached and resolved by step?
    before_interval = neighbor.notes[neighbor_ptr] - neighbor.notes[neighbor_ptr - 1]
    after_interval = neighbor.notes[neighbor_ptr + 1] - neighbor.notes[neighbor_ptr]

    same_direction = before_interval * after_interval > 0
    if 0.25 <= abs(before_interval) <= 3.5 and 0.25 <= abs(after_interval) <= 3.5 and not same_direction:
        return True

    return False

def check_suspension(suspension: Melody, base: Melody, suspension_ptr, base_ptr):
    # does the top note stay the same?
    next_time = suspension.get_time(suspension_ptr + 1)
    if base.get_note_at_time(next_time) != base.notes[base_ptr]:
        print("Top note does not stay the same")
        return False

    # does it resolve?
    if not consonant(suspension.get_note_at_time(next_time), base.get_note_at_time(next_time)):
        print("Does not resolve")
        return False

    # does it resolve down?
    interval = suspension.notes[suspension_ptr + 1] - suspension.notes[suspension_ptr]
    if interval > 0:
        print("Does not resolve down")
        return False

    return True

def counterpoint_checker(melody_1: Melody, melody_2: Melody):
    ptr1 = 0
    ptr2 = 0
    time = 0

    while (ptr1 < len(melody_1.notes) - 1) and (ptr2 < len(melody_2.notes) - 1):
        # check for disoncance
        if not consonant(melody_1.notes[ptr1], melody_2.notes[ptr2]):
            print("Dissonance at time: ", time)
            if melody_1.get_time(ptr1) > melody_2.get_time(ptr2):
                faster_melody = melody_1
                slower_melody = melody_2
                fast_ptr = ptr1
            else:
                faster_melody = melody_2
                slower_melody = melody_1
                fast_ptr = ptr2
                slow_ptr = ptr1
            if check_passing_tone(faster_melody, slower_melody, fast_ptr): print("resolved with passing tone")
            elif check_neighboring_tone(faster_melody, slower_melody, fast_ptr): print("resolved with neighboring tone")
            elif check_suspension(faster_melody, slower_melody, fast_ptr, slow_ptr): print("resolved with suspension")
            else: 
                print("not resolved")
                return time
                    
        # move the pointer of the next note
        if melody_1.get_time(ptr1 + 1) < melody_2.get_time(ptr2 + 1):
            ptr1 += 1
            time = melody_1.get_time(ptr1)
        elif melody_1.get_time(ptr1 + 1) > melody_2.get_time(ptr2 + 1):
            ptr2 += 1
            time = melody_2.get_time(ptr2)
        else:
            ptr1 += 1
            ptr2 += 1
            time = melody_1.get_time(ptr1)

    return time
    

melody_1 = Melody([76,74,72,74], [2,4,2,4])
melody_2 = Melody([67,64,62], [4,4,4])

melody_3 = Melody([62,62,62,65,62,65,67,69], [1,1,1,1.5,0.5,0.75,0.25,2])
melody_4 = Melody([i for i in melody_3.notes], [x * 1.5 for x in melody_3.durations])

counterpoint_checker(melody_3, melody_4)