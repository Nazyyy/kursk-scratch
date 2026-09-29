import json
import os
import zipfile
import sys

sys.path.insert(0, "/home/dima/Projects/hackathon/scratch_project")
from scratch_builder import BlockBuilder, gen_id

PROJECT_DIR = "/home/dima/Projects/hackathon/scratch_project"
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
MANIFEST_FILE = os.path.join(PROJECT_DIR, "assets_manifest.json")

with open(MANIFEST_FILE, "r") as f:
    manifest = json.load(f)

VARIABLES = {
    "var_gamestate": ["GameState", "TITLE"],
    "var_score": ["Score", 0],
    "var_energy": ["Energy", 0],
    "var_wind": ["WindSpeed", 35],
    "var_rpm": ["FlywheelRPM", 60],
    "var_focus": ["FocusDist", 30],
    "var_focus_lock": ["FocusLocked", 0],
    "var_distkma": ["DistKMA", 45],
    "var_candrill": ["CanDrill", 0],
    "var_question": ["QuestionNum", 1],
    "var_status": ["StatusRank", "Инженер-исследователь"],
    "var_award": ["AwardName", "Демидовская Медаль"],
    "var_mission": ["MissionText", "IT-ЦОПП: Нажмите [НАЧАТЬ ЭКСПЕДИЦИЮ]"]
}

BROADCASTS = {
    "bc_start_title": "start_title",
    "bc_show_rules": "show_rules",
    "bc_show_authors": "show_authors",
    "bc_start_intro": "start_intro",
    "bc_goto_level1": "goto_level1",
    "bc_start_level1_game": "start_level1_game",
    "bc_goto_level2": "goto_level2",
    "bc_start_level2_game": "start_level2_game",
    "bc_goto_level3": "goto_level3",
    "bc_start_level3_game": "start_level3_game",
    "bc_goto_hall_quiz": "goto_hall_quiz",
    "bc_start_quiz_game": "start_quiz_game",
    "bc_next_question": "next_question",
    "bc_show_victory": "show_victory"
}

def make_costume(name):
    item = manifest[name]
    res = {
        "assetId": item["assetId"],
        "name": name,
        "md5ext": item["md5ext"],
        "dataFormat": item["dataFormat"],
        "rotationCenterX": item.get("rotationCenterX", 240),
        "rotationCenterY": item.get("rotationCenterY", 180)
    }
    if item["dataFormat"] == "png":
        res["bitmapResolution"] = item.get("bitmapResolution", 1)
    return res

def make_sound(name):
    item = manifest[name]
    return {
        "assetId": item["assetId"],
        "name": name,
        "dataFormat": item["dataFormat"],
        "format": "",
        "rate": item.get("rate", 44100),
        "sampleCount": item.get("sampleCount", 1000),
        "md5ext": item["md5ext"]
    }

ALL_SOUND_NAMES = [
    "snd_click", "snd_teleport", "snd_focus", "snd_wind",
    "snd_magnet", "snd_correct", "snd_wrong", "snd_fanfare"
]
ALL_SOUNDS = [make_sound(s) for s in ALL_SOUND_NAMES]

targets = []

def create_sprite(name, costumes, bb, sounds=None, x=0, y=0, size=100, visible=True, layer=1):
    return {
        "isStage": False,
        "name": name,
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": bb.blocks,
        "comments": {},
        "currentCostume": 0,
        "costumes": [make_costume(c) for c in costumes],
        "sounds": [make_sound(s) for s in (sounds or [])],
        "volume": 100,
        "layerOrder": layer,
        "visible": visible,
        "x": x,
        "y": y,
        "size": size,
        "direction": 90,
        "draggable": False,
        "rotationStyle": "all around"
    }

# =========================================================================
# STAGE
# =========================================================================
stage_bb = BlockBuilder()

# Flag init
s_init_miss = stage_bb.set_var("MissionText", "var_mission", "IT-ЦОПП: Нажмите [НАЧАТЬ ЭКСПЕДИЦИЮ]", None)
s_init_q = stage_bb.set_var("QuestionNum", "var_question", 1, s_init_miss)
s_init_kma = stage_bb.set_var("DistKMA", "var_distkma", 45, s_init_q)
s_init_dr = stage_bb.set_var("CanDrill", "var_candrill", 0, s_init_kma)
s_init_foc = stage_bb.set_var("FocusDist", "var_focus", 30, s_init_dr)
s_init_flock = stage_bb.set_var("FocusLocked", "var_focus_lock", 0, s_init_foc)
s_init_rpm = stage_bb.set_var("FlywheelRPM", "var_rpm", 60, s_init_flock)
s_init_wnd = stage_bb.set_var("WindSpeed", "var_wind", 35, s_init_rpm)
s_init_en = stage_bb.set_var("Energy", "var_energy", 0, s_init_wnd)
s_init_sc = stage_bb.set_var("Score", "var_score", 0, s_init_en)
s_init_st = stage_bb.set_var("GameState", "var_gamestate", "TITLE", s_init_sc)
s_bg_title = stage_bb.switch_backdrop("bg_title", s_init_st)
s_bc_title = stage_bb.broadcast("start_title", "bc_start_title", s_bg_title)
stage_bb.hat_flag(s_bc_title, 50, 50)

# Level transitions
stage_bb.hat_broadcast("goto_level1", "bc_goto_level1", 
    stage_bb.set_var("GameState", "var_gamestate", "LEVEL1",
    stage_bb.switch_backdrop("bg_semenov", 
    stage_bb.play_sound("snd_teleport", None))), 50, 240)

stage_bb.hat_broadcast("goto_level2", "bc_goto_level2", 
    stage_bb.set_var("GameState", "var_gamestate", "LEVEL2",
    stage_bb.switch_backdrop("bg_ufimtsev", 
    stage_bb.play_sound("snd_teleport", None))), 50, 420)

stage_bb.hat_broadcast("goto_level3", "bc_goto_level3", 
    stage_bb.set_var("GameState", "var_gamestate", "LEVEL3",
    stage_bb.switch_backdrop("bg_kma_aes", 
    stage_bb.play_sound("snd_teleport", None))), 50, 600)

stage_bb.hat_broadcast("goto_hall_quiz", "bc_goto_hall_quiz", 
    stage_bb.set_var("GameState", "var_gamestate", "HALL_QUIZ",
    stage_bb.switch_backdrop("bg_hall_of_fame", 
    stage_bb.play_sound("snd_fanfare", None))), 50, 780)

stage_bb.hat_broadcast("show_victory", "bc_show_victory", 
    stage_bb.set_var("GameState", "var_gamestate", "VICTORY",
    stage_bb.play_sound("snd_fanfare", None)), 50, 960)

targets.append({
    "isStage": True,
    "name": "Stage",
    "variables": VARIABLES,
    "lists": {},
    "broadcasts": BROADCASTS,
    "blocks": stage_bb.blocks,
    "comments": {},
    "currentCostume": 0,
    "costumes": [
        make_costume("bg_title"),
        make_costume("bg_semenov"),
        make_costume("bg_ufimtsev"),
        make_costume("bg_kma_aes"),
        make_costume("bg_hall_of_fame")
    ],
    "sounds": ALL_SOUNDS,
    "volume": 100,
    "layerOrder": 0
})

# =========================================================================
# 1. HUD BAR (Верхняя панель: 368x29 at 0, 162)
# =========================================================================
hud_bb = BlockBuilder()
hud_bb.hat_flag(hud_bb.hide(None), 50, 50)
for ev in ["goto_level1", "goto_level2", "goto_level3", "goto_hall_quiz", "show_victory"]:
    hud_bb.hat_broadcast(ev, f"bc_{ev}", hud_bb.show(hud_bb.goto_xy(0, 162, None)), 50, 160)

targets.append(create_sprite("HUD", ["hud_bar"], hud_bb, [], x=0, y=162, size=100, visible=False, layer=10))

# =========================================================================
# 2. DIALOG BOX (Центрированные карточки, авто-прогресс и пропуск по клику/пробелу)
# =========================================================================
dlg_bb = BlockBuilder()
dlg_bb.hat_flag(dlg_bb.hide(None), 50, 50)

# Intro
di_bc = dlg_bb.broadcast("goto_level1", "bc_goto_level1", None)
di_h = dlg_bb.hide(di_bc)
di_w2 = dlg_bb.wait(3.2, di_h)
di_c2 = dlg_bb.switch_costume("dlg_intro_2", di_w2)
di_w1 = dlg_bb.wait(3.2, di_c2)
di_c1 = dlg_bb.switch_costume("dlg_intro_1", di_w1)
di_show = dlg_bb.show(di_c1)
di_pos = dlg_bb.goto_xy(0, -115, di_show)
di_stop = dlg_bb.stop_other_scripts(di_pos)
dlg_bb.hat_broadcast("start_intro", "bc_start_intro", di_stop, 50, 160)

# Level 1 sequence (Semenov)
dl1_bc = dlg_bb.broadcast("start_level1_game", "bc_start_level1_game", None)
dl1_h = dlg_bb.hide(dl1_bc)
dl1_w3 = dlg_bb.wait(3.2, dl1_h)
dl1_c3 = dlg_bb.switch_costume("dlg_semenov_task", dl1_w3)
dl1_w2 = dlg_bb.wait(3.0, dl1_c3)
dl1_c2 = dlg_bb.switch_costume("dlg_semenov_2", dl1_w2)
dl1_w1 = dlg_bb.wait(3.0, dl1_c2)
dl1_c1 = dlg_bb.switch_costume("dlg_semenov_1", dl1_w1)
dl1_show = dlg_bb.show(dl1_c1)
dl1_pos = dlg_bb.goto_xy(0, -115, dl1_show)
dl1_stop = dlg_bb.stop_other_scripts(dl1_pos)
dlg_bb.hat_broadcast("goto_level1", "bc_goto_level1", dl1_stop, 50, 420)

# Level 2 sequence (Ufimtsev)
dl2_bc = dlg_bb.broadcast("start_level2_game", "bc_start_level2_game", None)
dl2_h = dlg_bb.hide(dl2_bc)
dl2_w3 = dlg_bb.wait(3.2, dl2_h)
dl2_c3 = dlg_bb.switch_costume("dlg_ufimtsev_task", dl2_w3)
dl2_w2 = dlg_bb.wait(3.0, dl2_c3)
dl2_c2 = dlg_bb.switch_costume("dlg_ufimtsev_2", dl2_w2)
dl2_w1 = dlg_bb.wait(3.0, dl2_c2)
dl2_c1 = dlg_bb.switch_costume("dlg_ufimtsev_1", dl2_w1)
dl2_show = dlg_bb.show(dl2_c1)
dl2_pos = dlg_bb.goto_xy(0, -115, dl2_show)
dl2_stop = dlg_bb.stop_other_scripts(dl2_pos)
dlg_bb.hat_broadcast("goto_level2", "bc_goto_level2", dl2_stop, 50, 680)

# Level 3 sequence (Lazarev)
dl3_bc = dlg_bb.broadcast("start_level3_game", "bc_start_level3_game", None)
dl3_h = dlg_bb.hide(dl3_bc)
dl3_w3 = dlg_bb.wait(3.2, dl3_h)
dl3_c3 = dlg_bb.switch_costume("dlg_lazarev_task", dl3_w3)
dl3_w2 = dlg_bb.wait(3.0, dl3_c3)
dl3_c2 = dlg_bb.switch_costume("dlg_lazarev_2", dl3_w2)
dl3_w1 = dlg_bb.wait(3.0, dl3_c2)
dl3_c1 = dlg_bb.switch_costume("dlg_lazarev_1", dl3_w1)
dl3_show = dlg_bb.show(dl3_c1)
dl3_pos = dlg_bb.goto_xy(0, -115, dl3_show)
dl3_stop = dlg_bb.stop_other_scripts(dl3_pos)
dlg_bb.hat_broadcast("goto_level3", "bc_goto_level3", dl3_stop, 50, 940)

# Level 4 Quiz intro
dl4_bc = dlg_bb.broadcast("start_quiz_game", "bc_start_quiz_game", None)
dl4_h = dlg_bb.hide(dl4_bc)
dl4_w = dlg_bb.wait(3.2, dl4_h)
dl4_c = dlg_bb.switch_costume("dlg_quiz_intro", dl4_w)
dl4_show = dlg_bb.show(dl4_c)
dl4_pos = dlg_bb.goto_xy(0, -115, dl4_show)
dl4_stop = dlg_bb.stop_other_scripts(dl4_pos)
dlg_bb.hat_broadcast("goto_hall_quiz", "bc_goto_hall_quiz", dl4_stop, 50, 1200)

# Victory sequence
dv_show = dlg_bb.show(None)
dv_c = dlg_bb.switch_costume("dlg_victory", dv_show)
dv_pos = dlg_bb.goto_xy(0, -115, dv_c)
dv_stop = dlg_bb.stop_other_scripts(dv_pos)
dlg_bb.hat_broadcast("show_victory", "bc_show_victory", dv_stop, 50, 1360)

# Hide on mini-game starts
for ev in ["start_level1_game", "start_level2_game", "start_level3_game", "start_quiz_game"]:
    dlg_bb.hat_broadcast(ev, f"bc_{ev}", dlg_bb.stop_other_scripts(dlg_bb.hide(None)), 50, 1500)

# Interactive Skip on Space key
sk_q = dlg_bb.if_then(dlg_bb.op_equals_var("GameState", "var_gamestate", "HALL_QUIZ", None), dlg_bb.broadcast("start_quiz_game", "bc_start_quiz_game", None), None)
sk_l3 = dlg_bb.if_then(dlg_bb.op_equals_var("GameState", "var_gamestate", "LEVEL3", None), dlg_bb.broadcast("start_level3_game", "bc_start_level3_game", None), sk_q)
sk_l2 = dlg_bb.if_then(dlg_bb.op_equals_var("GameState", "var_gamestate", "LEVEL2", None), dlg_bb.broadcast("start_level2_game", "bc_start_level2_game", None), sk_l3)
sk_l1 = dlg_bb.if_then(dlg_bb.op_equals_var("GameState", "var_gamestate", "LEVEL1", None), dlg_bb.broadcast("start_level1_game", "bc_start_level1_game", None), sk_l2)
sk_intro = dlg_bb.if_then(dlg_bb.op_equals_var("GameState", "var_gamestate", "INTRO", None), dlg_bb.broadcast("goto_level1", "bc_goto_level1", None), sk_l1)
sk_action = dlg_bb.play_sound("snd_click", sk_intro)

dlg_bb.hat_key("space", sk_action, 50, 1700)
dlg_bb.hat_clicked(sk_action, 50, 1850)

targets.append(create_sprite(
    "DialogBox",
    [
        "dialog_plate", "dlg_intro_1", "dlg_intro_2",
        "dlg_semenov_1", "dlg_semenov_2", "dlg_semenov_task",
        "dlg_ufimtsev_1", "dlg_ufimtsev_2", "dlg_ufimtsev_task",
        "dlg_lazarev_1", "dlg_lazarev_2", "dlg_lazarev_task",
        "dlg_quiz_intro", "dlg_victory"
    ],
    dlg_bb,
    ["snd_click"],
    x=0, y=-115, size=100, visible=False, layer=15
))

# =========================================================================
# 3. HERO (Инженер-стажер IT-ЦОПП)
# =========================================================================
hero_bb = BlockBuilder()
hero_bb.hat_flag(hero_bb.hide(None), 50, 50)

hero_bb.hat_broadcast("start_intro", "bc_start_intro", 
    hero_bb.switch_costume("hero_copt", hero_bb.goto_xy(-140, -40, hero_bb.show(None))), 50, 160)

hero_bb.hat_broadcast("goto_level1", "bc_goto_level1", 
    hero_bb.switch_costume("hero_astronomer", hero_bb.goto_xy(-150, -40, hero_bb.show(None))), 50, 320)

hero_bb.hat_broadcast("goto_level2", "bc_goto_level2", 
    hero_bb.switch_costume("hero_aviator", hero_bb.goto_xy(150, -40, hero_bb.show(None))), 50, 480)

hero_bb.hat_broadcast("goto_level3", "bc_goto_level3", 
    hero_bb.switch_costume("hero_physicist", hero_bb.goto_xy(150, -40, hero_bb.show(None))), 50, 640)

hero_bb.hat_broadcast("goto_hall_quiz", "bc_goto_hall_quiz", 
    hero_bb.switch_costume("hero_copt", hero_bb.goto_xy(-150, -40, hero_bb.show(None))), 50, 800)

# Victory calculation
set_award_gold = hero_bb.set_var("AwardName", "var_award", "Золотая Демидовская Медаль РАН с отличием", None)
set_stat_gold = hero_bb.set_var("StatusRank", "var_status", "Академик Соловьиного Края", set_award_gold)

set_award_silv = hero_bb.set_var("AwardName", "var_award", "Серебряный знак Уфимцева", None)
set_stat_silv = hero_bb.set_var("StatusRank", "var_status", "Инженер-первопроходец Курска", set_award_silv)

set_award_brz = hero_bb.set_var("AwardName", "var_award", "Свидетельство исследователя", None)
set_stat_brz = hero_bb.set_var("StatusRank", "var_status", "Стажер-испытатель IT-ЦОПП", set_award_brz)

cond_gt_70 = hero_bb.op_gt_var("Score", "var_score", 69, None)
nested_lower = hero_bb.if_else(cond_gt_70, set_stat_silv, set_stat_brz, None)
cond_gt_90 = hero_bb.op_gt_var("Score", "var_score", 89, None)
nested_top = hero_bb.if_else(cond_gt_90, set_stat_gold, nested_lower, None)

h_v_eval = hero_bb.show(nested_top)
h_v_pos = hero_bb.goto_xy(0, -45, h_v_eval)
h_v_cost = hero_bb.switch_costume("hero_triumph", h_v_pos)
hero_bb.hat_broadcast("show_victory", "bc_show_victory", h_v_cost, 50, 960)

targets.append(create_sprite(
    "Hero",
    ["hero_copt", "hero_astronomer", "hero_aviator", "hero_physicist", "hero_triumph"],
    hero_bb,
    ["snd_correct", "snd_fanfare"],
    x=-140, y=-40, size=85, visible=False, layer=8
))

# =========================================================================
# 4. KURSIK (Кибер-соловей робот-маскот)
# =========================================================================
kurs_bb = BlockBuilder()

# Floating loop
k_w2 = kurs_bb.wait(0.25, None)
k_y2 = kurs_bb.change_y(-4, k_w2)
k_w1 = kurs_bb.wait(0.25, k_y2)
k_y1 = kurs_bb.change_y(4, k_w1)
k_loop = kurs_bb.forever(k_y1, None)
k_show = kurs_bb.show(k_loop)
k_pos = kurs_bb.goto_xy(0, 75, k_show)
kurs_bb.hat_flag(k_pos, 50, 50)

# Movement per level
kurs_bb.hat_broadcast("start_intro", "bc_start_intro", kurs_bb.goto_xy(-70, 45, kurs_bb.switch_costume("kursik_talk", None)), 50, 240)
kurs_bb.hat_broadcast("goto_level1", "bc_goto_level1", kurs_bb.goto_xy(0, 85, kurs_bb.switch_costume("kursik_hover", None)), 50, 380)
kurs_bb.hat_broadcast("goto_level2", "bc_goto_level2", kurs_bb.goto_xy(0, 85, kurs_bb.switch_costume("kursik_hover", None)), 50, 520)
kurs_bb.hat_broadcast("goto_level3", "bc_goto_level3", kurs_bb.goto_xy(0, 85, kurs_bb.switch_costume("kursik_scan", None)), 50, 660)
kurs_bb.hat_broadcast("goto_hall_quiz", "bc_goto_hall_quiz", kurs_bb.goto_xy(-150, 65, kurs_bb.switch_costume("kursik_hover", None)), 50, 800)
kurs_bb.hat_broadcast("show_victory", "bc_show_victory", kurs_bb.goto_xy(120, 65, kurs_bb.switch_costume("kursik_celebrate", None)), 50, 940)

targets.append(create_sprite(
    "Kursik",
    ["kursik_hover", "kursik_talk", "kursik_scan", "kursik_celebrate"],
    kurs_bb,
    ["snd_correct"],
    x=0, y=75, size=60, visible=True, layer=10
))

# =========================================================================
# 5. CHARACTERS: Semenov, Ufimtsev, Lazarev
# =========================================================================
# Semenov
sem_bb = BlockBuilder()
sem_bb.hat_flag(sem_bb.hide(None), 50, 50)
sem_bb.hat_broadcast("goto_level1", "bc_goto_level1", sem_bb.show(sem_bb.goto_xy(150, -40, None)), 50, 160)
for ev in ["goto_level2", "goto_level3", "goto_hall_quiz", "show_victory"]:
    sem_bb.hat_broadcast(ev, f"bc_{ev}", sem_bb.hide(None), 50, 300)
targets.append(create_sprite("CharSemenov", ["char_semenov"], sem_bb, [], x=150, y=-40, size=85, visible=False, layer=7))

# Ufimtsev
uf_bb = BlockBuilder()
uf_bb.hat_flag(uf_bb.hide(None), 50, 50)
uf_bb.hat_broadcast("goto_level2", "bc_goto_level2", uf_bb.show(uf_bb.goto_xy(-150, -40, None)), 50, 160)
for ev in ["goto_level1", "goto_level3", "goto_hall_quiz", "show_victory"]:
    uf_bb.hat_broadcast(ev, f"bc_{ev}", uf_bb.hide(None), 50, 300)
targets.append(create_sprite("CharUfimtsev", ["char_ufimtsev"], uf_bb, [], x=-150, y=-40, size=85, visible=False, layer=7))

# Lazarev
laz_bb = BlockBuilder()
laz_bb.hat_flag(laz_bb.hide(None), 50, 50)
laz_bb.hat_broadcast("goto_level3", "bc_goto_level3", laz_bb.show(laz_bb.goto_xy(-150, -40, None)), 50, 160)
for ev in ["goto_level1", "goto_level2", "goto_hall_quiz", "show_victory"]:
    laz_bb.hat_broadcast(ev, f"bc_{ev}", laz_bb.hide(None), 50, 300)
targets.append(create_sprite("CharLazarev", ["char_lazarev"], laz_bb, [], x=-150, y=-40, size=85, visible=False, layer=7))

# =========================================================================
# 6. TITLE BUTTONS (BtnStart, BtnRules, BtnAuthors)
# =========================================================================
# BtnStart: (0, 10)
b_start_bb = BlockBuilder()
b_start_bb.hat_flag(b_start_bb.show(b_start_bb.goto_xy(0, 10, None)), 50, 50)
b_start_click = b_start_bb.play_sound("snd_click", b_start_bb.hide(b_start_bb.broadcast("start_intro", "bc_start_intro", None)))
b_start_bb.hat_clicked(b_start_click, 50, 180)
for ev in ["start_intro", "goto_level1", "goto_level2", "goto_level3", "goto_hall_quiz", "show_victory"]:
    b_start_bb.hat_broadcast(ev, f"bc_{ev}", b_start_bb.hide(None), 50, 300)
targets.append(create_sprite("BtnStart", ["btn_start"], b_start_bb, ["snd_click"], x=0, y=10, size=100, visible=True, layer=12))

# BtnRules: (-100, -70)
b_rules_bb = BlockBuilder()
b_rules_bb.hat_flag(b_rules_bb.show(b_rules_bb.goto_xy(-100, -70, None)), 50, 50)
b_rules_bb.hat_clicked(b_rules_bb.play_sound("snd_click", None), 50, 180)
for ev in ["start_intro", "goto_level1", "goto_level2", "goto_level3", "goto_hall_quiz", "show_victory"]:
    b_rules_bb.hat_broadcast(ev, f"bc_{ev}", b_rules_bb.hide(None), 50, 300)
targets.append(create_sprite("BtnRules", ["btn_rules"], b_rules_bb, ["snd_click"], x=-100, y=-70, size=100, visible=True, layer=12))

# BtnAuthors: (100, -70)
b_auth_bb = BlockBuilder()
b_auth_bb.hat_flag(b_auth_bb.show(b_auth_bb.goto_xy(100, -70, None)), 50, 50)
b_auth_bb.hat_clicked(b_auth_bb.play_sound("snd_click", None), 50, 180)
for ev in ["start_intro", "goto_level1", "goto_level2", "goto_level3", "goto_hall_quiz", "show_victory"]:
    b_auth_bb.hat_broadcast(ev, f"bc_{ev}", b_auth_bb.hide(None), 50, 300)
targets.append(create_sprite("BtnAuthors", ["btn_authors"], b_auth_bb, ["snd_click"], x=100, y=-70, size=100, visible=True, layer=12))

# =========================================================================
# 7. GAME 1: TELESCOPE & ECLIPSE (Реальное наведение линзы на затмение)
# =========================================================================
# Eclipse Target: (80, 40)
ecl_bb = BlockBuilder()
ecl_bb.hat_flag(ecl_bb.hide(None), 50, 50)
ecl_bb.hat_broadcast("start_level1_game", "bc_start_level1_game", ecl_bb.show(ecl_bb.goto_xy(80, 40, None)), 50, 160)
for ev in ["goto_level2", "goto_level3", "goto_hall_quiz", "show_victory"]:
    ecl_bb.hat_broadcast(ev, f"bc_{ev}", ecl_bb.hide(None), 50, 300)
targets.append(create_sprite("EclipseTarget", ["eclipse_target"], ecl_bb, [], x=80, y=40, size=100, visible=False, layer=4))

# Telescope Lens: starts at (-50, -20)
lens_bb = BlockBuilder()
lens_bb.hat_flag(lens_bb.hide(None), 50, 50)

# Movement via arrow keys
lens_bb.hat_key("right arrow", lens_bb.change_x(15, None), 50, 160)
lens_bb.hat_key("left arrow", lens_bb.change_x(-15, None), 50, 260)
lens_bb.hat_key("up arrow", lens_bb.change_y(15, None), 50, 360)
lens_bb.hat_key("down arrow", lens_bb.change_y(-15, None), 50, 460)

# Interactive loop with real collision detection & focus lock!
l_miss_sharp = lens_bb.set_var("MissionText", "var_mission", "ФОКУС 100%: ЗАТМЕНИЕ ПОЙМАНО! НАЖМИТЕ [ЗАФИКСИРОВАТЬ ФОКУС]", None)
l_set_flock = lens_bb.set_var("FocusLocked", "var_focus_lock", 1, l_miss_sharp)
l_set_f100 = lens_bb.set_var("FocusDist", "var_focus", 100, l_set_flock)
l_sw_sharp = lens_bb.switch_costume("telescope_lens_sharp", l_set_f100)

l_miss_blur = lens_bb.set_var("MissionText", "var_mission", "НАВЕДИТЕ ЛИНЗУ ТЕЛЕСКОПА МЫШКОЙ ИЛИ СТРЕЛКАМИ НА ДИСК ЗАТМЕНИЯ", None)
l_set_funlock = lens_bb.set_var("FocusLocked", "var_focus_lock", 0, l_miss_blur)
l_set_f30 = lens_bb.set_var("FocusDist", "var_focus", 30, l_set_funlock)
l_sw_norm = lens_bb.switch_costume("telescope_lens", l_set_f30)

l_touch = lens_bb.sensing_touching("EclipseTarget", None)
l_check = lens_bb.if_else(l_touch, l_sw_sharp, l_sw_norm, None)
l_wait = lens_bb.wait(0.05, l_check)
l_loop = lens_bb.forever(l_wait, None)
l_show = lens_bb.show(l_loop)
l_pos = lens_bb.goto_xy(-50, -20, l_show)
lens_bb.hat_broadcast("start_level1_game", "bc_start_level1_game", l_pos, 50, 600)

# Mouse drag support: when clicked, follow mouse
lens_drag = lens_bb.forever(lens_bb.if_then(lens_bb.sensing_mousedown(None), lens_bb.goto_mouse(None), None), None)
lens_bb.hat_clicked(lens_drag, 50, 750)

for ev in ["goto_level2", "goto_level3", "goto_hall_quiz", "show_victory"]:
    lens_bb.hat_broadcast(ev, f"bc_{ev}", lens_bb.stop_other_scripts(lens_bb.hide(None)), 50, 900)

targets.append(create_sprite(
    "TelescopeLens",
    ["telescope_lens", "telescope_lens_sharp"],
    lens_bb,
    ["snd_focus", "snd_correct"],
    x=-50, y=-20, size=100, visible=False, layer=6
))

# BtnLockFocus: (0, -125)
blf_bb = BlockBuilder()
blf_bb.hat_flag(blf_bb.hide(None), 50, 50)
blf_bb.hat_broadcast("start_level1_game", "bc_start_level1_game", blf_bb.show(blf_bb.goto_xy(0, -125, None)), 50, 160)

blf_win_bc = blf_bb.broadcast("goto_level2", "bc_goto_level2", None)
blf_win_w = blf_bb.wait(1.5, blf_win_bc)
blf_win_miss = blf_bb.set_var("MissionText", "var_mission", "ОТЛИЧНО! Таблицы затмений Семёнова подтверждены!", blf_win_w)
blf_win_sc = blf_bb.change_var("Score", "var_score", 30, blf_win_miss)
blf_win_snd = blf_bb.play_sound("snd_correct", blf_win_sc)

blf_fail_miss = blf_bb.set_var("MissionText", "var_mission", "НЕТ ФОКУСА! Совместите линзу с темным диском затмения!", None)
blf_fail_snd = blf_bb.play_sound("snd_wrong", blf_fail_miss)

blf_click = blf_bb.if_else(
    blf_bb.op_gt_var("FocusDist", "var_focus", 80, None),
    blf_win_snd,
    blf_fail_snd,
    None
)
blf_bb.hat_clicked(blf_click, 50, 320)

for ev in ["goto_level2", "goto_level3", "goto_hall_quiz", "show_victory"]:
    blf_bb.hat_broadcast(ev, f"bc_{ev}", blf_bb.hide(None), 50, 500)

targets.append(create_sprite("BtnLockFocus", ["btn_lock_focus"], blf_bb, ["snd_click", "snd_correct", "snd_wrong"], x=0, y=-125, size=100, visible=False, layer=12))

# =========================================================================
# 8. GAME 2: WIND TURBINE & VACUUM FLYWHEEL (Живая физика балансировки)
# =========================================================================
# WindTurbine Rotor: (0, 35)
wt_bb = BlockBuilder()
wt_bb.hat_flag(wt_bb.hide(None), 50, 50)
wt_rot = wt_bb.forever(wt_bb.turn_right(18, wt_bb.wait(0.04, None)), None)
wt_bb.hat_broadcast("start_level2_game", "bc_start_level2_game", wt_bb.goto_xy(0, 35, wt_bb.show(wt_rot)), 50, 160)
for ev in ["goto_level1", "goto_level3", "goto_hall_quiz", "show_victory"]:
    wt_bb.hat_broadcast(ev, f"bc_{ev}", wt_bb.stop_other_scripts(wt_bb.hide(None)), 50, 350)
targets.append(create_sprite("WindTurbine", ["wind_rotor"], wt_bb, ["snd_wind"], x=0, y=35, size=100, visible=False, layer=5))

# FlywheelMeter: (-90, 35)
fwm_bb = BlockBuilder()
fwm_bb.hat_flag(fwm_bb.hide(None), 50, 50)

# Wind and Flywheel dynamics loop
fwm_win_bc = fwm_bb.broadcast("goto_level3", "bc_goto_level3", None)
fwm_win_w = fwm_bb.wait(1.5, fwm_win_bc)
fwm_win_miss = fwm_bb.set_var("MissionText", "var_mission", "ТРИУМФ! Ветростанция Уфимцева накопила 100% энергии!", fwm_win_w)
fwm_win_sc = fwm_bb.change_var("Score", "var_score", 35, fwm_win_miss)
fwm_win_snd = fwm_bb.play_sound("snd_correct", fwm_win_sc)
fwm_check_win = fwm_bb.if_then(fwm_bb.op_gt_var("Energy", "var_energy", 99, None), fwm_win_snd, None)

fwm_in_green = fwm_bb.change_var("Energy", "var_energy", 5, 
    fwm_bb.set_var("MissionText", "var_mission", "СТАБИЛЬНО: ВАКУУМНЫЙ МАХОВИК ЗАРЯЖАЕТ АККУМУЛЯТОР!", fwm_check_win))

fwm_rpm_high = fwm_bb.set_var("MissionText", "var_mission", "ОПАСНОСТЬ: ПЕРЕГРЕВ РОТОРА! ЖМИТЕ [ТОРМОЗ РОТОРА]!", None)
fwm_rpm_low = fwm_bb.set_var("MissionText", "var_mission", "МАЛО ОБОРОТОВ! ПОДКЛЮЧИТЕ [ВАКУУМНЫЙ МАХОВИК]!", None)
fwm_check_sub = fwm_bb.if_else(fwm_bb.op_gt_var("FlywheelRPM", "var_rpm", 84, None), fwm_rpm_high, fwm_rpm_low, None)

# Green condition: RPM > 54 and RPM < 85
fwm_cond_min = fwm_bb.op_gt_var("FlywheelRPM", "var_rpm", 54, None)
fwm_cond_max = fwm_bb.op_lt_var("FlywheelRPM", "var_rpm", 85, None)
fwm_cond_green = fwm_bb.op_and(fwm_cond_min, fwm_cond_max, None)
fwm_eval_zone = fwm_bb.if_else(fwm_cond_green, fwm_in_green, fwm_check_sub, None)

# Wind fluctuates and drags RPM
fwm_wind_high = fwm_bb.change_var("FlywheelRPM", "var_rpm", 3, fwm_eval_zone)
fwm_wind_low = fwm_bb.change_var("FlywheelRPM", "var_rpm", -3, fwm_eval_zone)
fwm_eval_wind = fwm_bb.if_else(fwm_bb.op_gt_var("WindSpeed", "var_wind", 60, None), fwm_wind_high, fwm_wind_low, None)

fwm_set_wnd = fwm_bb.set_var("WindSpeed", "var_wind", fwm_bb.op_random(30, 85, None), fwm_eval_wind)
fwm_tick_wait = fwm_bb.wait(0.35, fwm_set_wnd)
fwm_sim_loop = fwm_bb.forever(fwm_tick_wait, None)

fwm_init_sim = fwm_bb.set_var("Energy", "var_energy", 0, 
    fwm_bb.set_var("FlywheelRPM", "var_rpm", 65, 
    fwm_bb.show(fwm_bb.goto_xy(-90, 35, fwm_sim_loop))))
fwm_bb.hat_broadcast("start_level2_game", "bc_start_level2_game", fwm_init_sim, 50, 160)

for ev in ["goto_level1", "goto_level3", "goto_hall_quiz", "show_victory"]:
    fwm_bb.hat_broadcast(ev, f"bc_{ev}", fwm_bb.stop_other_scripts(fwm_bb.hide(None)), 50, 350)

targets.append(create_sprite("FlywheelMeter", ["flywheel_meter"], fwm_bb, ["snd_wind", "snd_correct"], x=-90, y=35, size=100, visible=False, layer=6))

# BtnBrake: (-90, -125)
bb_bb = BlockBuilder()
bb_bb.hat_flag(bb_bb.hide(None), 50, 50)
bb_bb.hat_broadcast("start_level2_game", "bc_start_level2_game", bb_bb.show(bb_bb.goto_xy(-90, -125, None)), 50, 160)

bb_click = bb_bb.play_sound("snd_click", bb_bb.change_var("FlywheelRPM", "var_rpm", -12, None))
bb_bb.hat_clicked(bb_click, 50, 300)
bb_bb.hat_key("down arrow", bb_click, 50, 420)

for ev in ["goto_level1", "goto_level3", "goto_hall_quiz", "show_victory"]:
    bb_bb.hat_broadcast(ev, f"bc_{ev}", bb_bb.hide(None), 50, 540)
targets.append(create_sprite("BtnBrake", ["btn_brake"], bb_bb, ["snd_click"], x=-90, y=-125, size=100, visible=False, layer=12))

# BtnGear: (+90, -125)
bg_bb = BlockBuilder()
bg_bb.hat_flag(bg_bb.hide(None), 50, 50)
bg_bb.hat_broadcast("start_level2_game", "bc_start_level2_game", bg_bb.show(bg_bb.goto_xy(90, -125, None)), 50, 160)

bg_click = bg_bb.play_sound("snd_click", bg_bb.change_var("FlywheelRPM", "var_rpm", 12, None))
bg_bb.hat_clicked(bg_click, 50, 300)
bg_bb.hat_key("up arrow", bg_click, 50, 420)

for ev in ["goto_level1", "goto_level3", "goto_hall_quiz", "show_victory"]:
    bg_bb.hat_broadcast(ev, f"bc_{ev}", bg_bb.hide(None), 50, 540)
targets.append(create_sprite("BtnGear", ["btn_gear"], bg_bb, ["snd_click"], x=90, y=-125, size=100, visible=False, layer=12))

# =========================================================================
# 9. GAME 3: KMA MAGNETOMETER SURVEY (Геомагнитный сонар и бурение керна)
# =========================================================================
# Ore Vein: (70, -20)
ov_bb = BlockBuilder()
ov_bb.hat_flag(ov_bb.hide(None), 50, 50)
ov_bb.hat_broadcast("start_level3_game", "bc_start_level3_game", ov_bb.show(ov_bb.goto_xy(70, -20, None)), 50, 160)
for ev in ["goto_level1", "goto_level2", "goto_hall_quiz", "show_victory"]:
    ov_bb.hat_broadcast(ev, f"bc_{ev}", ov_bb.hide(None), 50, 350)
targets.append(create_sprite("OreVein", ["ore_vein"], ov_bb, [], x=70, y=-20, size=100, visible=False, layer=4))

# Magnetometer: starts at (-70, 0)
mag_bb = BlockBuilder()
mag_bb.hat_flag(mag_bb.hide(None), 50, 50)

# Movement
mag_bb.hat_key("right arrow", mag_bb.change_x(15, None), 50, 160)
mag_bb.hat_key("left arrow", mag_bb.change_x(-15, None), 50, 260)
mag_bb.hat_key("up arrow", mag_bb.change_y(15, None), 50, 360)
mag_bb.hat_key("down arrow", mag_bb.change_y(-15, None), 50, 460)

# Scanning loop with real OreVein collision detection!
mag_snd_hit = mag_bb.play_sound("snd_magnet", None)
mag_miss_hit = mag_bb.set_var("MissionText", "var_mission", "МАГНИТНАЯ АНОМАЛИЯ 160 мкТл! ЖМИТЕ [ИЗВЛЕЧЬ КЕРН КМА]!", mag_snd_hit)
mag_hit_can = mag_bb.set_var("CanDrill", "var_candrill", 1, mag_miss_hit)
mag_hit_kma = mag_bb.set_var("DistKMA", "var_distkma", 160, mag_hit_can)

mag_miss_norm = mag_bb.set_var("MissionText", "var_mission", "СКАНИРУЙТЕ КАРЬЕР: Ищите эпицентр аномалии магнетита (>120 мкТл)", None)
mag_norm_can = mag_bb.set_var("CanDrill", "var_candrill", 0, mag_miss_norm)
mag_norm_kma = mag_bb.set_var("DistKMA", "var_distkma", 45, mag_norm_can)

mag_touch = mag_bb.sensing_touching("OreVein", None)
mag_eval = mag_bb.if_else(mag_touch, mag_hit_kma, mag_norm_kma, None)
mag_wait = mag_bb.wait(0.08, mag_eval)
mag_loop = mag_bb.forever(mag_wait, None)

mag_init = mag_bb.set_var("CanDrill", "var_candrill", 0, 
    mag_bb.set_var("DistKMA", "var_distkma", 45, 
    mag_bb.show(mag_bb.goto_xy(-70, 0, mag_loop))))
mag_bb.hat_broadcast("start_level3_game", "bc_start_level3_game", mag_init, 50, 600)

# Mouse drag support
mag_drag = mag_bb.forever(mag_bb.if_then(mag_bb.sensing_mousedown(None), mag_bb.goto_mouse(None), None), None)
mag_bb.hat_clicked(mag_drag, 50, 750)

for ev in ["goto_level1", "goto_level2", "goto_hall_quiz", "show_victory"]:
    mag_bb.hat_broadcast(ev, f"bc_{ev}", mag_bb.stop_other_scripts(mag_bb.hide(None)), 50, 900)

targets.append(create_sprite("Magnetometer", ["magneto_sensor"], mag_bb, ["snd_magnet"], x=-70, y=0, size=100, visible=False, layer=6))

# BtnDrill: (0, -125)
dr_bb = BlockBuilder()
dr_bb.hat_flag(dr_bb.hide(None), 50, 50)
dr_bb.hat_broadcast("start_level3_game", "bc_start_level3_game", dr_bb.show(dr_bb.goto_xy(0, -125, None)), 50, 160)

dr_win_bc = dr_bb.broadcast("goto_hall_quiz", "bc_goto_hall_quiz", None)
dr_win_w = dr_bb.wait(1.5, dr_win_bc)
dr_win_miss = dr_bb.set_var("MissionText", "var_mission", "КЕРН ИЗВЛЕЧЕН: 68% ЖЕЛЕЗА! ЗАПАСЫ КМА ДОКАЗАНЫ!", dr_win_w)
dr_win_sc = dr_bb.change_var("Score", "var_score", 35, dr_win_miss)
dr_win_snd = dr_bb.play_sound("snd_correct", dr_win_sc)

dr_fail_miss = dr_bb.set_var("MissionText", "var_mission", "ЗДЕСЬ ПУСТАЯ ПОРОДА! Подведите зонд к аномалии (>120 мкТл)!", None)
dr_fail_snd = dr_bb.play_sound("snd_wrong", dr_fail_miss)

dr_click = dr_bb.if_else(
    dr_bb.op_gt_var("DistKMA", "var_distkma", 100, None),
    dr_win_snd,
    dr_fail_snd,
    None
)
dr_bb.hat_clicked(dr_click, 50, 320)

for ev in ["goto_level1", "goto_level2", "goto_hall_quiz", "show_victory"]:
    dr_bb.hat_broadcast(ev, f"bc_{ev}", dr_bb.hide(None), 50, 500)

targets.append(create_sprite("BtnDrill", ["btn_drill"], dr_bb, ["snd_click", "snd_correct", "snd_wrong"], x=0, y=-125, size=100, visible=False, layer=12))

# =========================================================================
# 10. GAME 4: QUIZ (3 последовательных вопроса о курских героях)
# =========================================================================
# QuizBanner: (50, 95)
qb_bb = BlockBuilder()
qb_bb.hat_flag(qb_bb.hide(None), 50, 50)
qb_bb.hat_broadcast("start_quiz_game", "bc_start_quiz_game", qb_bb.switch_costume("card_q1", qb_bb.show(qb_bb.goto_xy(50, 95, None))), 50, 160)

# Next question handler
qb_set_q3 = qb_bb.switch_costume("card_q3", None)
qb_set_q2 = qb_bb.switch_costume("card_q2", None)
qb_eval = qb_bb.if_else(qb_bb.op_equals_var("QuestionNum", "var_question", 3, None), qb_set_q3, qb_set_q2, None)
qb_bb.hat_broadcast("next_question", "bc_next_question", qb_eval, 50, 320)

for ev in ["goto_level1", "goto_level2", "goto_level3", "show_victory"]:
    qb_bb.hat_broadcast(ev, f"bc_{ev}", qb_bb.hide(None), 50, 480)

targets.append(create_sprite("QuizBanner", ["card_q1", "card_q2", "card_q3"], qb_bb, [], x=50, y=95, size=100, visible=False, layer=12))

# BtnOptA: (50, 40) - ALWAYS CORRECT ANSWER
oa_bb = BlockBuilder()
oa_bb.hat_flag(oa_bb.hide(None), 50, 50)
oa_bb.hat_broadcast("start_quiz_game", "bc_start_quiz_game", oa_bb.switch_costume("btn_opt_a", oa_bb.show(oa_bb.goto_xy(50, 40, None))), 50, 160)

# Click logic
oa_win_bc = oa_bb.broadcast("show_victory", "bc_show_victory", None)
oa_win_w = oa_bb.wait(1.0, oa_win_bc)

oa_adv_bc = oa_bb.broadcast("next_question", "bc_next_question", None)
oa_adv_inc = oa_bb.change_var("QuestionNum", "var_question", 1, oa_adv_bc)

oa_check_final = oa_bb.if_else(
    oa_bb.op_gt_var("QuestionNum", "var_question", 2, None),
    oa_win_w,
    oa_adv_inc,
    None
)
oa_sc = oa_bb.change_var("Score", "var_score", 10, oa_check_final)
oa_snd = oa_bb.play_sound("snd_correct", oa_sc)
oa_bb.hat_clicked(oa_snd, 50, 320)

# Next question costume switch
oa_q3 = oa_bb.switch_costume("btn_opt_a_q3", None)
oa_q2 = oa_bb.switch_costume("btn_opt_a_q2", None)
oa_eval_c = oa_bb.if_else(oa_bb.op_equals_var("QuestionNum", "var_question", 3, None), oa_q3, oa_q2, None)
oa_bb.hat_broadcast("next_question", "bc_next_question", oa_eval_c, 50, 500)

for ev in ["goto_level1", "goto_level2", "goto_level3", "show_victory"]:
    oa_bb.hat_broadcast(ev, f"bc_{ev}", oa_bb.hide(None), 50, 680)

targets.append(create_sprite("BtnOptA", ["btn_opt_a", "btn_opt_a_q2", "btn_opt_a_q3"], oa_bb, ["snd_click", "snd_correct"], x=50, y=40, size=100, visible=False, layer=12))

# BtnOptB: (50, -15) - WRONG
ob_bb = BlockBuilder()
ob_bb.hat_flag(ob_bb.hide(None), 50, 50)
ob_bb.hat_broadcast("start_quiz_game", "bc_start_quiz_game", ob_bb.switch_costume("btn_opt_b", ob_bb.show(ob_bb.goto_xy(50, -15, None))), 50, 160)

ob_err_miss = ob_bb.set_var("MissionText", "var_mission", "НЕВЕРНО! Подумайте и выберите правильный ответ!", None)
ob_click = ob_bb.play_sound("snd_wrong", ob_err_miss)
ob_bb.hat_clicked(ob_click, 50, 320)

ob_q3 = ob_bb.switch_costume("btn_opt_b_q3", None)
ob_q2 = ob_bb.switch_costume("btn_opt_b_q2", None)
ob_eval_c = ob_bb.if_else(ob_bb.op_equals_var("QuestionNum", "var_question", 3, None), ob_q3, ob_q2, None)
ob_bb.hat_broadcast("next_question", "bc_next_question", ob_eval_c, 50, 500)

for ev in ["goto_level1", "goto_level2", "goto_level3", "show_victory"]:
    ob_bb.hat_broadcast(ev, f"bc_{ev}", ob_bb.hide(None), 50, 680)

targets.append(create_sprite("BtnOptB", ["btn_opt_b", "btn_opt_b_q2", "btn_opt_b_q3"], ob_bb, ["snd_click", "snd_wrong"], x=50, y=-15, size=100, visible=False, layer=12))

# BtnOptC: (50, -70) - WRONG
oc_bb = BlockBuilder()
oc_bb.hat_flag(oc_bb.hide(None), 50, 50)
oc_bb.hat_broadcast("start_quiz_game", "bc_start_quiz_game", oc_bb.switch_costume("btn_opt_c", oc_bb.show(oc_bb.goto_xy(50, -70, None))), 50, 160)

oc_err_miss = oc_bb.set_var("MissionText", "var_mission", "НЕВЕРНО! Подумайте и выберите правильный ответ!", None)
oc_click = oc_bb.play_sound("snd_wrong", oc_err_miss)
oc_bb.hat_clicked(oc_click, 50, 320)

oc_q3 = oc_bb.switch_costume("btn_opt_c_q3", None)
oc_q2 = oc_bb.switch_costume("btn_opt_c_q2", None)
oc_eval_c = oc_bb.if_else(oc_bb.op_equals_var("QuestionNum", "var_question", 3, None), oc_q3, oc_q2, None)
oc_bb.hat_broadcast("next_question", "bc_next_question", oc_eval_c, 50, 500)

for ev in ["goto_level1", "goto_level2", "goto_level3", "show_victory"]:
    oc_bb.hat_broadcast(ev, f"bc_{ev}", oc_bb.hide(None), 50, 680)

targets.append(create_sprite("BtnOptC", ["btn_opt_c", "btn_opt_c_q2", "btn_opt_c_q3"], oc_bb, ["snd_click", "snd_wrong"], x=50, y=-70, size=100, visible=False, layer=12))

# =========================================================================
# 11. VICTORY MEDAL (FxMedal)
# =========================================================================
med_bb = BlockBuilder()
med_bb.hat_flag(med_bb.hide(None), 50, 50)

m_w2 = med_bb.wait(0.3, None)
m_s2 = med_bb.set_size(95, m_w2)
m_w1 = med_bb.wait(0.3, m_s2)
m_s1 = med_bb.set_size(105, m_w1)
m_loop = med_bb.forever(m_s1, None)
m_show = med_bb.show(m_loop)
m_pos = med_bb.goto_xy(0, 65, m_show)
med_bb.hat_broadcast("show_victory", "bc_show_victory", m_pos, 50, 160)

for ev in ["goto_level1", "goto_level2", "goto_level3", "goto_hall_quiz"]:
    med_bb.hat_broadcast(ev, f"bc_{ev}", med_bb.stop_other_scripts(med_bb.hide(None)), 50, 350)

targets.append(create_sprite("FxMedal", ["fx_medal"], med_bb, ["snd_fanfare"], x=0, y=65, size=100, visible=False, layer=14))

# =========================================================================
# PACKAGE PROJECT
# =========================================================================
project = {
    "targets": targets,
    "monitors": [],
    "extensions": [],
    "meta": {
        "semver": "3.0.0",
        "vm": "0.2.0",
        "agent": "Antigravity Scratch Engine 3.0"
    }
}

OUT_PROJECT_JSON = os.path.join(PROJECT_DIR, "project.json")
with open(OUT_PROJECT_JSON, "w", encoding="utf-8") as f:
    json.dump(project, f, ensure_ascii=False, indent=2)

OUT_SB3 = "/home/dima/Projects/hackathon/kursk_heroes.sb3"
with zipfile.ZipFile(OUT_SB3, "w", compression=zipfile.ZIP_DEFLATED) as z:
    z.write(OUT_PROJECT_JSON, "project.json")
    for fname in os.listdir(ASSETS_DIR):
        fpath = os.path.join(ASSETS_DIR, fname)
        if os.path.isfile(fpath):
            z.write(fpath, fname)

print(f"Project successfully compiled to {OUT_SB3} ({os.path.getsize(OUT_SB3)} bytes)!")
