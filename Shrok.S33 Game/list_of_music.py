import random

nick_effects = ['s33/nick1.mp3', 's33/nick2.mp3', 's33/nick3.mp3', 's33/nick4.mp3', 's33/nick5.mp3', 's33/nick6.mp3', 's33/nick7.mp3',
's33/nick8.mp3', 's33/nick9.mp3', 's33/nick10.mp3', 's33/nick11.mp3', 's33/nick12.mp3', 's33/nick13.mp3', 's33/nick14.mp3',
's33/nick15.mp3', 's33/nick16.mp3', 's33/nick17.mp3', 's33/nick18.mp3', 's33/nick19.mp3', 's33/nick20.mp3', 's33/nick21.mp3',
's33/nick22.mp3', 's33/nick23.mp3', 's33/nick24.mp3', 's33/nick25.mp3', 's33/nick26.mp3']

rand_n = random.randrange(1,27)

effect_to_play = nick_effects[rand_n]
print(effect_to_play)
