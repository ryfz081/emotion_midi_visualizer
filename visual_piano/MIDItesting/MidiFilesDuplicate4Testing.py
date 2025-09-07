import mido
mid = mido.MidiFile('rachc.mid')
for msg in mid.play():
    print(msg)
    