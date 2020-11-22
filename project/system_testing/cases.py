"""
The package contains steps to reproduce real game situations and the
result that we want to have after bot turn.

It will help us to be sure that new changes in logic don't change
the old fixed bugs with decisions.

Also, this package contains tools to generate documentation and unit tests
from the description of the situations.
"""
from mahjong.tile import TilesConverter
from utils.decisions_logger import MeldPrint

ACTION_DISCARD = "discard"
ACTION_MELD = "meld"
ACTION_CRASH = "crash"

SYSTEM_TESTING_CASES = [
    {
        "index": 1,
        "description": "Bot discarded 2s by suji because of 2 additional ukeire in ryanshanten, instead of discarding the safe tile.",
        "reproducer_command": "python reproducer.py --log 2020102200gm-0001-7994-1143916f --player 0 --wind 2 --honba 3 --tile=1s --n 2 --action=draw",
        "action": ACTION_DISCARD,
        "allowed_discards": ["3s", "5s"],
        "with_riichi": False,
    },
    {
        "index": 2,
        "description": "6m and 8m have equal ukeire, but 6m is safe.",
        "reproducer_command": "python reproducer.py --log 2020102204gm-0001-7994-fb636348 --player 3 --wind 7 --honba 0  --action=draw --tile=6z",
        "action": ACTION_DISCARD,
        "allowed_discards": ["6m", "3s"],
        "with_riichi": False,
    },
    {
        "index": 3,
        "description": "It was a bad meld. We don't want to open hand here.",
        "reproducer_command": "python reproducer.py --log 2020102208gm-0009-0000-40337c9c --player Xenia --wind 3 --honba 0  --action enemy_discard --tile 1s",
        "action": ACTION_MELD,
        "meld": None,
        "tile_after_meld": None,
    },
    {
        "index": 4,
        "description": "It was a bad meld. We don't want to open hand here.",
        "reproducer_command": "python reproducer.py --log 2020102208gm-0009-0000-40337c9c --player Xenia --wind 4 --honba 0  --action enemy_discard --tile 5s",
        "action": ACTION_MELD,
        "meld": None,
        "tile_after_meld": None,
    },
    {
        "index": 5,
        "description": "Riichi dora tanki is a better move here.",
        "reproducer_command": "python reproducer.py --log 2020102517gm-0009-0000-67fd5f29 --player Xenia --wind 2 --honba 0 --action draw --n 1 --tile 7s",
        "action": ACTION_DISCARD,
        "allowed_discards": ["1p", "4p"],
        "with_riichi": True,
    },
    {
        "index": 6,
        "description": "Let's defend here.",
        "reproducer_command": "python reproducer.py --log 2020102602gm-0009-0000-ba58220e --player Kaavi --wind 6 --honba 1 --action draw --n 2 --tile 1s",
        "action": ACTION_DISCARD,
        "allowed_discards": ["1s"],
        "with_riichi": False,
    },
    {
        "index": 7,
        "description": "7p was wrongly detected as dangerous tile, it is not like this",
        "reproducer_command": "python reproducer.py --log 2020102608gm-0009-0000-ff33fd82 --player Wanjirou --wind 4 --honba 0 --action draw --n 1 --tile 7p",
        "action": ACTION_DISCARD,
        "allowed_discards": ["7p"],
        "with_riichi": False,
    },
    {
        "index": 8,
        "description": "Honors are dangerous on this late stage of the game. And we have 2 shanten. Let's fold with 6s",
        "reproducer_command": "python reproducer.py --log 2020102619gm-0089-0000-dfaf5b1d --player Xenia --wind 4 --honba 0 --action draw --n 1 --tile 2m",
        "action": ACTION_DISCARD,
        "allowed_discards": ["6s"],
        "with_riichi": False,
        "skip_reason": "Need to investigate it.",
    },
    {
        "index": 9,
        "description": "",
        "reproducer_command": "python reproducer.py --log 2020102701gm-0089-0000-8572de24 --player Ichihime --wind 7 --honba 1 --action draw --n 1 --tile 7s",
        "action": ACTION_DISCARD,
        "allowed_discards": ["3p"],
        "with_riichi": False,
    },
    {
        "index": 10,
        "description": "",
        "reproducer_command": "python reproducer.py --log 2020102710gm-0009-7994-88f45f2d --player 3 --wind 5 --honba 0 --tile 4m --action enemy_discard",
        "action": ACTION_MELD,
        "meld": None,
        "tile_after_meld": None,
    },
    {
        "index": 11,
        "description": "There is no need in damaten. Let's riichi.",
        "reproducer_command": "python reproducer.py --log 2020102720gm-0089-0000-65eb30bf --player Xenia --wind 8 --honba 2 --action draw --n 1 --tile 4m",
        "action": ACTION_DISCARD,
        "allowed_discards": ["7s"],
        "with_riichi": True,
    },
    {
        "index": 12,
        "description": "Chun is too dangerous to discard.",
        "reproducer_command": "python reproducer.py --log 2020102721gm-0089-0000-67865130 --player Xenia --wind 5 --honba 0 --action draw --n 1 --tile 4m",
        "action": ACTION_DISCARD,
        "allowed_discards": ["7s"],
        "with_riichi": False,
    },
    {
        "index": 13,
        "description": "Hatsu is too dangerous to discard.",
        "reproducer_command": "python reproducer.py --log 2020102821gm-0089-0000-49e1d208 --player Ichihime --wind 1 --honba 2 --action draw --n 1 --tile 6z",
        "action": ACTION_DISCARD,
        "allowed_discards": ["7m"],
        "with_riichi": False,
    },
    {
        "index": 14,
        "description": "3p is genbutsu",
        "reproducer_command": "python reproducer.py --log 2020102908gm-0089-0000-e1512a30 --player Ichihime --wind 7 --honba 0 --action draw --n 2 --tile 6p",
        "action": ACTION_DISCARD,
        "allowed_discards": ["3p"],
        "with_riichi": False,
    },
    {
        "index": 15,
        "description": "5p is too dangerous to discard",
        "reproducer_command": "python reproducer.py --log 2020102900gm-0089-0000-5cc13112 --player Xenia --wind 2 --honba 2 --tile 5p --n 2 --action draw",
        "action": ACTION_DISCARD,
        "allowed_discards": ["5s"],
        "with_riichi": False,
    },
    {
        "index": 16,
        "description": "We need to fold here",
        "reproducer_command": "python reproducer.py --log 2020102921gm-0089-0000-764321f0 --player Xenia --wind 1 --honba 0 --action draw --n 1 --tile 3m",
        "action": ACTION_DISCARD,
        "allowed_discards": ["7s", "3m"],
        "with_riichi": False,
    },
    {
        "index": 17,
        "description": "Bad meld for honitsu.",
        "reproducer_command": "python reproducer.py --log 2020102922gm-0089-0000-d3c4e90b --player Xenia --wind 1 --honba 0 --action enemy_discard --n 1 --tile 8p",
        "action": ACTION_MELD,
        "meld": None,
        "tile_after_meld": None,
    },
    {
        "index": 18,
        "description": "",
        "reproducer_command": "python reproducer.py --log 2020103005gm-0089-0000-01fc4f4d --player Kaavi --wind 3 --honba 0 --action draw --n 3 --tile 6s",
        "action": ACTION_DISCARD,
        "allowed_discards": ["3p", "6s"],
        "with_riichi": False,
    },
    {
        "index": 19,
        "description": "",
        "reproducer_command": "python reproducer.py --log 2020111101gm-0009-7994-f22b8c57 --wind 4 --honba 2 --player 2 --tile 8m --action enemy_discard",
        "action": ACTION_MELD,
        "meld": None,
        "tile_after_meld": None,
    },
    {
        "index": 20,
        "description": "",
        "reproducer_command": "python reproducer.py --log 2020111111gm-0009-7994-5550ade1 --wind 8 --honba 1 --player 0 --tile 7z --action enemy_discard",
        "action": ACTION_MELD,
        "meld": {"type": MeldPrint.PON, "tiles": TilesConverter.string_to_136_array(honors="777")},
        "tile_after_meld": "3p",
        "skip_reason": "Need to investigate it.",
    },
    {
        "index": 21,
        "description": "",
        "reproducer_command": "python reproducer.py --log 2020111401gm-0009-7994-7429e8e0 --wind 1 --honba 1 --action draw --tile 3s --player 3",
        "action": ACTION_CRASH,
    },
    {
        "index": 22,
        "description": "",
        "reproducer_command": "python reproducer.py --log 2020111402gm-0009-7994-41f6c1a1 --wind 3 --honba 0 --action enemy_discard --tile 5p --player 1",
        "action": ACTION_CRASH,
    },
    {
        "index": 23,
        "description": "",
        "reproducer_command": "python reproducer.py --file failed_2020-11-11_13_06_26_885.txt --wind 3 --honba 0 --tile 1z --n 2 --player 3",
        "action": ACTION_CRASH,
    },
    {
        "index": 24,
        "description": "",
        "reproducer_command": "python reproducer.py --file failed_2020-11-11_12_52_06_023.txt --wind 8 --honba 0 --action enemy_discard --tile 3s --player 0",
        "action": ACTION_CRASH,
    },
    {
        "index": 25,
        "description": "",
        "reproducer_command": "python reproducer.py --file failed_2020-11-11_12_19_20_515.txt --wind 3 --honba 1 --tile 6s --player 2",
        "action": ACTION_CRASH,
    },
    {
        "index": 26,
        "description": "",
        "reproducer_command": "python reproducer.py --log 2020102620gm-0089-0000-c558d68c --player Kaavi --wind 1 --honba 2 --action draw --n 2 --tile 4p",
        "action": ACTION_DISCARD,
        "allowed_discards": ["3s"],
        "with_riichi": False,
    },
    {
        "index": 27,
        "description": "",
        "reproducer_command": "python reproducer.py --log 2020102208gm-0009-0000-1d3d08c8 --player Ichihime --wind 5 --honba 1 --tile 1z --action draw",
        "action": ACTION_CRASH,
    },
    {
        "index": 28,
        "description": "",
        "reproducer_command": "python reproducer.py --log 2020102008gm-0001-7994-9438a8f4 --player Wanjirou --wind 3 --honba 0 --tile 7p --action enemy_discard",
        "action": ACTION_MELD,
        "meld": None,
        "tile_after_meld": None,
    },
    {
        "index": 29,
        "description": "There was crash after open kan in the real game.",
        "reproducer_command": "python reproducer.py --log 2020112003gm-0089-0000-72c1d092 --player Xenia --wind 7 --honba 0 --tile 1s",
        "action": ACTION_CRASH,
    },
    {
        "index": 30,
        "description": "We are pushing here, even if it is karaten we still want to keep tempai.",
        "reproducer_command": "python reproducer.py --log 2020112215gm-0009-0000-9c894eca --player 1 --wind 8 --honba 0 --action draw --n 1 --tile 7m",
        "action": ACTION_DISCARD,
        "allowed_discards": ["5m"],
        "with_riichi": False,
    },
    {
        "index": 31,
        "description": "Regression with honitsu and chinitsu detection",
        "reproducer_command": "python reproducer.py --log 2020112219gm-0089-0000-8de03653 --player 安提洛科斯 --wind 1 --honba 0 --action draw --n 1 --tile 1s",
        "action": ACTION_DISCARD,
        "allowed_discards": ["3z"],
        "with_riichi": False,
    },
]
