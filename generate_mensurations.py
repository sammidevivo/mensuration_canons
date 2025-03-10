from scamp import *
import os
from counterpoint_checker import Melody

def generate_score(melody_1: Melody, melody_2: Melody, trans, aug, inst_1: str, inst_2: str):
    # Construct file name and title dynamically
    file_name = f"mensuration-aug[{aug}]trans[{trans}].pdf"
    name = f"Mensuration: aug: {aug}, trans: {trans}"

    # Ensure directory exists
    output_dir = os.path.join("mensuration_canons", "scores")
    os.makedirs(output_dir, exist_ok=True)

    # Generate the score
    s = Session()
    engraving_settings.show_microtonal_annotations = True
    p1 = s.new_part(inst_1, "piano")
    p2 = s.new_part(inst_2, "piano")
    s.start_transcribing()
    s.fast_forward_in_beats(1000)
    s.fork(melody_1.play, args=(p1,))
    s.fork(melody_2.play, args=(p2,))
    wait_for_children_to_finish()

    # Export as PDF
    score = s.stop_transcribing().to_score(title=name)
    file_path = os.path.join(output_dir, file_name)
    # score.show()
    score.export_pdf(file_path)
    

def generate_mensurations(cantus_firmus: Melody):
    transpositions = [0, 3, 4, 7, 8, 9, 12]
    augmentations = [2/1, 3/1, 4/1, 5/1, 6/1, 7/1, 3/2, 5/2, 7/2, 4/3, 5/3, 7/3, 5/4, 7/4, 6/5, 7/5, 7/6]

    for aug in augmentations:
        for trans in transpositions:
            counterpoint = Melody([note + trans for note in cantus_firmus.notes], [dur * aug for dur in cantus_firmus.durations])
            generate_score(cantus_firmus, counterpoint, trans, aug, "cantus firmus", "counterpoint")
    

josqin = Melody([62,62,62,65,62,65,67,69,69,69,67,65], 
                [1,1,1,1.5,0.5,0.75,0.25,2,1,1.5,0.5,1])
josqin_counterpoint = Melody([62,62,62,65,62,65,67,69], [x * 1.5 for x in josqin.durations])

cantus_firmus = Melody([62, 65.5, 63.5, 62, 65.5, 69, 67, 71, 69, 67, 63.5, 65.5, 63.5, 62], [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0])
generate_mensurations(cantus_firmus)
