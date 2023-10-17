import sys
import base64
import inspect
import os
import io
from submission_sample import SimpleAgent, dotdict, MCTS
import numpy as np
from tqdm import tqdm
from parl.utils import logger
from connectx_try import encode_weight, load_buffer, System, extract
from connect4_game import Connect4Game
from pathlib import Path
from connectx_try import load_data, getCurrentPlayer, getStep, store_data
from feature import DatasetManager
from random import uniform
import random
from time import sleep
from collections import defaultdict
import collections
#パターンの出現場所 v2, h2
#factor = 31

sample_s_path = '/home/student/PARL/benchmark/torch/AlphaZero/best_200.pth.tar'
sample_b_path = '/home/student/PARL/benchmark/torch/AlphaZero/saved_model/checkpoint_1.pth.tar'

game = Connect4Game()
strong_timellimit = 5
weak_timelimit = 0.5
strong_puct = 1
weak_puct = 0.1
sample_system = System(game, sample_s_path, sample_b_path, turn=1, strong_timelimit=strong_timellimit,
                        weak_timelimit=weak_timelimit, strong_puct=strong_puct, weak_puct=weak_puct)

paths1 = sorted(Path('./label/important/important/short').glob('*.board'))
paths2 = sorted(Path('./label/important/trivial/short').glob('*.board'))
paths3 = sorted(Path('./label/trivial/important/short').glob('*.board'))
paths4 = sorted(Path('./label/trivial/trivial/short').glob('*.board'))

paths = [paths1, paths2, paths3, paths4]
height, width = game.getBoardSize()
datas = []
for i in range(len(paths)):
    #print(f"dataset: {i+1}")
    record = defaultdict(lambda: 0)
    dataset = DatasetManager(game, paths[i])
    dataset.make_board_set()
    pattern_paths = dataset.make_pattern_path_set(dataset.pattern_set[1])
    print(len(pattern_paths))
    pdataset = DatasetManager(game, pattern_paths)
    for p in pdataset.path_set:
        content = load_data(p)
        imp, board, branch, fpath, importance = content
        contain_indices, pure_indices = pdataset.match_pattern(board, dataset.pattern_set[1])
        for c in contain_indices:
            h = int(c/width) - 1
            w = c % width
            '''
            if h > 0:
                record[c-width] += 1
            '''

            record[c-width] += 1
            record[c-width+1] += 1
    
    visual = [0 if i not in collections.Counter(record).keys() else collections.Counter(record)[i]
                for i in range(height * width)]
    visual = np.array(visual).reshape(height, width)
    #print(np.sum(visual, axis=0)) #列ごと
    data = np.sum(visual, axis=0)
    data = np.array(data, dtype=np.float64)
    data /= np.sum(data)
    datas.append(data)
    #print(np.sum(visual, axis=1)) #行ごと
    #print(visual)

print(datas)
for i in range(len(datas[0])):
    print(f"{i} {datas[0][i]} {datas[1][i]} {datas[2][i]} {datas[3][i]}")

        

