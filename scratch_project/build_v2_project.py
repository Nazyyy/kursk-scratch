import json
import os
import zipfile
import hashlib
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
    "var_brake": ["BrakeActive", 0],
    "var_flywheel": ["FlywheelActive", 0],
    "var_focus": ["FocusDist", 60],
    "var_distkma": ["DistKMA", 90],
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
    "bc_lock_focus": "lock_focus",
    "bc_level1_complete": "level1_complete",
    "bc_goto_level2": "goto_level2",
    "bc_start_level2_game": "start_level2_game",
    "bc_activate_brake": "activate_brake",
    "bc_activate_flywheel": "activate_flywheel",
    "bc_level2_complete": "level2_complete",
    "bc_goto_level3": "goto_level3",
    "bc_start_level3_game": "start_level3_game",
    "bc_drill_core": "drill_core",
    "bc_level3_complete": "level3_complete",
    "bc_goto_hall_quiz": "goto_hall_quiz",
    "bc_start_quiz_game": "start_quiz_game",
    "bc_ans_a": "ans_a",
    "bc_ans_b": "ans_b",
    "bc_ans_c": "ans_c",
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
s_init_kma = stage_bb.set_var("DistKMA", "var_distkma", 90, s_init_q)
s_init_foc = stage_bb.set_var("FocusDist", "var_focus", 60, s_init_kma)
s_init_fly = stage_bb.set_var("FlywheelActive", "var_flywheel", 0, s_init_foc)
s_init_brk = stage_bb.set_var("BrakeActive", "var_brake", 0, s_init_fly)
s_init_wnd = stage_bb.set_var("WindSpeed", "var_wind", 35, s_init_brk)
s_init_en = stage_bb.set_var("Energy", "var_energy", 0, s_init_wnd)
s_init_sc = stage_bb.set_var("Score", "var_score", 0, s_init_en)
s_init_st = stage_bb.set_var("GameState", "var_gamestate", "TITLE", s_init_sc)
s_bg_title = stage_bb.switch_backdrop("bg_title", s_init_st)
s_bc_title = stage_bb.broadcast("start_title", "bc_start_title", s_bg_title)
stage_bb.hat_flag(s_bc_title, 50, 50)

# Goto Level 1
l1_snd = stage_bb.play_sound("snd_teleport", None)
l1_bg = stage_bb.switch_backdrop("bg_semenov", l1_snd)
l1_miss = stage_bb.set_var("MissionText", "var_mission", "Эпоха 1: Обсерватория Семёнова (1853 г.) • Настройка оптики", l1_bg)
l1_st = stage_bb.set_var("GameState", "var_gamestate", "LEVEL1", l1_miss)
stage_bb.hat_broadcast("goto_level1", "bc_goto_level1", l1_st, 50, 240)

# Goto Level 2
l2_snd = stage_bb.play_sound("snd_teleport", None)
l2_bg = stage_bb.switch_backdrop("bg_ufimtsev", l2_snd)
l2_miss = stage_bb.set_var("MissionText", "var_mission", "Эпоха 2: Ветростанция Уфимцева (1931 г.) • Баланс маховика", l2_bg)
l2_st = stage_bb.set_var("GameState", "var_gamestate", "LEVEL2", l2_miss)
stage_bb.hat_broadcast("goto_level2", "bc_goto_level2", l2_st, 50, 420)

# Goto Level 3
l3_snd = stage_bb.play_sound("snd_teleport", None)
l3_bg = stage_bb.switch_backdrop("bg_kma_aes", l3_snd)
l3_miss = stage_bb.set_var("MissionText", "var_mission", "Эпоха 3: КМА и Энергия Атома (г. Курчатов) • Гео-поиск", l3_bg)
l3_st = stage_bb.set_var("GameState", "var_gamestate", "LEVEL3", l3_miss)
stage_bb.hat_broadcast("goto_level3", "bc_goto_level3", l3_st, 50, 600)

# Goto Hall Quiz
lh_snd = stage_bb.play_sound("snd_fanfare", None)
lh_bg = stage_bb.switch_backdrop("bg_hall_of_fame", lh_snd)
lh_miss = stage_bb.set_var("MissionText", "var_mission", "Финал: Инженерный Экзамен Зала Научной Славы", lh_bg)
lh_st = stage_bb.set_var("GameState", "var_gamestate", "HALL_QUIZ", lh_miss)
stage_bb.hat_broadcast("goto_hall_quiz", "bc_goto_hall_quiz", lh_st, 50, 780)

# Show Victory
lv_snd = stage_bb.play_sound("snd_fanfare", None)
lv_miss = stage_bb.set_var("MissionText", "var_mission", "ТРИУМФ: Присвоение Золотого Инженерного Паспорта Первопроходца!", lv_snd)
lv_st = stage_bb.set_var("GameState", "var_gamestate", "VICTORY", lv_miss)
stage_bb.hat_broadcast("show_victory", "bc_show_victory", lv_st, 50, 960)

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
# 1. DIALOG BOX (Контроллер сюжета и диалогов)
# =========================================================================
dlg_bb = BlockBuilder()

# Green flag hide
dlg_bb.hat_flag(dlg_bb.hide(None), 50, 50)

# Intro sequence
di_bc = dlg_bb.broadcast("goto_level1", "bc_goto_level1", None)
di_h = dlg_bb.hide(di_bc)
di_w2 = dlg_bb.wait(3.0, di_h)
di_c2 = dlg_bb.switch_costume("dlg_intro_2", di_w2)
di_w1 = dlg_bb.wait(3.0, di_c2)
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
dl4_w = dlg_bb.wait(3.0, dl4_h)
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

for ev in ["start_level1_game", "start_level2_game", "start_level3_game", "start_quiz_game"]:
    dlg_bb.hat_broadcast(ev, f"bc_{ev}", dlg_bb.hide(None), 50, 1500)

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
# 2. HERO (Инженер-стажер IT-ЦОПП)
# =========================================================================
hero_bb = BlockBuilder()
hero_bb.hat_flag(hero_bb.hide(None), 50, 50)

# intro
h_i_show = hero_bb.show(None)
h_i_pos = hero_bb.goto_xy(-140, -40, h_i_show)
h_i_cost = hero_bb.switch_costume("hero_copt", h_i_pos)
hero_bb.hat_broadcast("start_intro", "bc_start_intro", h_i_cost, 50, 160)

# Level 1
h_l1_show = hero_bb.show(None)
h_l1_pos = hero_bb.goto_xy(-150, -40, h_l1_show)
h_l1_cost = hero_bb.switch_costume("hero_astronomer", h_l1_pos)
hero_bb.hat_broadcast("goto_level1", "bc_goto_level1", h_l1_cost, 50, 320)

# Level 2
h_l2_show = hero_bb.show(None)
h_l2_pos = hero_bb.goto_xy(150, -40, h_l2_show)
h_l2_cost = hero_bb.switch_costume("hero_aviator", h_l2_pos)
hero_bb.hat_broadcast("goto_level2", "bc_goto_level2", h_l2_cost, 50, 480)

# Level 3
h_l3_show = hero_bb.show(None)
h_l3_pos = hero_bb.goto_xy(150, -40, h_l3_show)
h_l3_cost = hero_bb.switch_costume("hero_physicist", h_l3_pos)
hero_bb.hat_broadcast("goto_level3", "bc_goto_level3", h_l3_cost, 50, 640)

# Level 4 Quiz
h_l4_show = hero_bb.show(None)
h_l4_pos = hero_bb.goto_xy(-150, -40, h_l4_show)
h_l4_cost = hero_bb.switch_costume("hero_copt", h_l4_pos)
hero_bb.hat_broadcast("goto_hall_quiz", "bc_goto_hall_quiz", h_l4_cost, 50, 800)

# Victory with 3-level deep nested condition
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
# 3. KURSIK (Кибер-соловей робот-маскот)
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
# 4. CHAR_SEMENOV (Ф.А. Семёнов, 1853 г.)
# =========================================================================
sem_bb = BlockBuilder()
sem_bb.hat_flag(sem_bb.hide(None), 50, 50)
sem_bb.hat_broadcast("goto_level1", "bc_goto_level1", sem_bb.show(sem_bb.goto_xy(150, -40, None)), 50, 160)
sem_bb.hat_broadcast("goto_level2", "bc_goto_level2", sem_bb.hide(None), 50, 300)
sem_bb.hat_broadcast("goto_level3", "bc_goto_level3", sem_bb.hide(None), 50, 420)
sem_bb.hat_broadcast("goto_hall_quiz", "bc_goto_hall_quiz", sem_bb.hide(None), 50, 540)
sem_bb.hat_broadcast("show_victory", "bc_show_victory", sem_bb.hide(None), 50, 660)

targets.append(create_sprite(
    "CharSemenov",
    ["char_semenov"],
    sem_bb,
    [],
    x=150, y=-40, size=85, visible=False, layer=7
))

# =========================================================================
# 5. CHAR_UFIMTSEV (А.Г. Уфимцев, 1931 г.)
# =========================================================================
uf_bb = BlockBuilder()
uf_bb.hat_flag(uf_bb.hide(None), 50, 50)
uf_bb.hat_broadcast("goto_level1", "bc_goto_level1", uf_bb.hide(None), 50, 160)
uf_bb.hat_broadcast("goto_level2", "bc_goto_level2", uf_bb.show(uf_bb.goto_xy(-150, -40, None)), 50, 280)
uf_bb.hat_broadcast("goto_level3", "bc_goto_level3", uf_bb.hide(None), 50, 420)
uf_bb.hat_broadcast("goto_hall_quiz", "bc_goto_hall_quiz", uf_bb.hide(None), 50, 540)
uf_bb.hat_broadcast("show_victory", "bc_show_victory", uf_bb.hide(None), 50, 660)

targets.append(create_sprite(
    "CharUfimtsev",
    ["char_ufimtsev"],
    uf_bb,
    [],
    x=-150, y=-40, size=85, visible=False, layer=7
))

# =========================================================================
# 6. CHAR_LAZAREV (Академик П.П. Лазарев, КМА)
# =========================================================================
laz_bb = BlockBuilder()
laz_bb.hat_flag(laz_bb.hide(None), 50, 50)
laz_bb.hat_broadcast("goto_level1", "bc_goto_level1", laz_bb.hide(None), 50, 160)
laz_bb.hat_broadcast("goto_level2", "bc_goto_level2", laz_bb.hide(None), 50, 280)
laz_bb.hat_broadcast("goto_level3", "bc_goto_level3", laz_bb.show(laz_bb.goto_xy(-150, -40, None)), 50, 400)
laz_bb.hat_broadcast("goto_hall_quiz", "bc_goto_hall_quiz", laz_bb.hide(None), 50, 540)
laz_bb.hat_broadcast("show_victory", "bc_show_victory", laz_bb.hide(None), 50, 660)

targets.append(create_sprite(
    "CharLazarev",
    ["char_lazarev"],
    laz_bb,
    [],
    x=-150, y=-40, size=85, visible=False, layer=7
))

# =========================================================================
# 7. TITLE BUTTONS (BtnStart, BtnRules, BtnAuthors) - NO OVERLAP!
# =========================================================================
# BtnStart: 192x42 at (0, 10)
b_start_bb = BlockBuilder()
bs_show = b_start_bb.show(None)
bs_pos = b_start_bb.goto_xy(0, 10, bs_show)
b_start_bb.hat_flag(bs_pos, 50, 50)

bs_bc = b_start_bb.broadcast("start_intro", "bc_start_intro", None)
bs_hide = b_start_bb.hide(bs_bc)
bs_snd = b_start_bb.play_sound("snd_click", bs_hide)
b_start_bb.hat_clicked(bs_snd, 50, 180)

for ev in ["start_intro", "goto_level1", "goto_level2", "goto_level3", "goto_hall_quiz", "show_victory"]:
    b_start_bb.hat_broadcast(ev, f"bc_{ev}", b_start_bb.hide(None), 50, 300)

targets.append(create_sprite("BtnStart", ["btn_start"], b_start_bb, ["snd_click"], x=0, y=10, size=100, visible=True, layer=12))

# BtnRules: 144x34 at (-100, -70) -> X spans -172 to -28
b_rules_bb = BlockBuilder()
br_show = b_rules_bb.show(None)
br_pos = b_rules_bb.goto_xy(-100, -70, br_show)
b_rules_bb.hat_flag(br_pos, 50, 50)
b_rules_bb.hat_clicked(b_rules_bb.play_sound("snd_click", None), 50, 180)
for ev in ["start_intro", "goto_level1", "goto_level2", "goto_level3", "goto_hall_quiz", "show_victory"]:
    b_rules_bb.hat_broadcast(ev, f"bc_{ev}", b_rules_bb.hide(None), 50, 300)

targets.append(create_sprite("BtnRules", ["btn_rules"], b_rules_bb, ["snd_click"], x=-100, y=-70, size=100, visible=True, layer=12))

# BtnAuthors: 144x34 at (100, -70) -> X spans +28 to +172 (Gap = 56px between rules and authors!)
b_auth_bb = BlockBuilder()
ba_show = b_auth_bb.show(None)
ba_pos = b_auth_bb.goto_xy(100, -70, ba_show)
b_auth_bb.hat_flag(ba_pos, 50, 50)
b_auth_bb.hat_clicked(b_auth_bb.play_sound("snd_click", None), 50, 180)
for ev in ["start_intro", "goto_level1", "goto_level2", "goto_level3", "goto_hall_quiz", "show_victory"]:
    b_auth_bb.hat_broadcast(ev, f"bc_{ev}", b_auth_bb.hide(None), 50, 300)

targets.append(create_sprite("BtnAuthors", ["btn_authors"], b_auth_bb, ["snd_click"], x=100, y=-70, size=100, visible=True, layer=12))

# =========================================================================
# 8. LEVEL 1: TELESCOPE & ECLIPSE
# =========================================================================
# Eclipse Target: 60x60 at (70, 50)
ecl_bb = BlockBuilder()
ecl_bb.hat_flag(ecl_bb.hide(None), 50, 50)
ecl_bb.hat_broadcast("start_level1_game", "bc_start_level1_game", ecl_bb.show(ecl_bb.goto_xy(70, 50, None)), 50, 160)
for ev in ["goto_level2", "goto_level3", "goto_hall_quiz", "show_victory"]:
    ecl_bb.hat_broadcast(ev, f"bc_{ev}", ecl_bb.hide(None), 50, 300)

targets.append(create_sprite("EclipseTarget", ["eclipse_target"], ecl_bb, [], x=70, y=50, size=100, visible=False, layer=4))

# Telescope Lens: 112x112 at (-40, -10)
lens_bb = BlockBuilder()
lens_bb.hat_flag(lens_bb.hide(None), 50, 50)

# Move controls
lens_bb.hat_key("right arrow", lens_bb.change_x(15, None), 50, 160)
lens_bb.hat_key("left arrow", lens_bb.change_x(-15, None), 50, 260)
lens_bb.hat_key("up arrow", lens_bb.change_y(15, None), 50, 360)
lens_bb.hat_key("down arrow", lens_bb.change_y(-15, None), 50, 460)

# Tracking loop
l_sw_sharp = lens_bb.switch_costume("telescope_lens_sharp", None)
l_sw_norm = lens_bb.switch_costume("telescope_lens", None)
l_cond = lens_bb.op_lt_var("FocusDist", "var_focus", 28, None)
l_branch = lens_bb.if_else(l_cond, l_sw_sharp, l_sw_norm, None)
l_set_foc = lens_bb.set_var("FocusDist", "var_focus", 20, l_branch)
l_loop = lens_bb.forever(l_set_foc, None)
l_show = lens_bb.show(l_loop)
l_pos = lens_bb.goto_xy(-40, -10, l_show)
lens_bb.hat_broadcast("start_level1_game", "bc_start_level1_game", l_pos, 50, 600)

for ev in ["goto_level2", "goto_level3", "goto_hall_quiz", "show_victory"]:
    l_stop = lens_bb.stop_other_scripts(lens_bb.hide(None))
    lens_bb.hat_broadcast(ev, f"bc_{ev}", l_stop, 50, 800)

targets.append(create_sprite(
    "TelescopeLens",
    ["telescope_lens", "telescope_lens_sharp"],
    lens_bb,
    ["snd_focus", "snd_correct"],
    x=-40, y=-10, size=100, visible=False, layer=6
))

# BtnLockFocus: 184x38.5 at (0, -125) -> Spans X: -92 to +92 (Hero at -150, Semenov at +150, ZERO overlap!)
blf_bb = BlockBuilder()
blf_bb.hat_flag(blf_bb.hide(None), 50, 50)
blf_bb.hat_broadcast("start_level1_game", "bc_start_level1_game", blf_bb.show(blf_bb.goto_xy(0, -125, None)), 50, 160)

blf_bc = blf_bb.broadcast("goto_level2", "bc_goto_level2", None)
blf_wait = blf_bb.wait(1.2, blf_bc)
blf_sc = blf_bb.change_var("Score", "var_score", 25, blf_wait)
blf_snd_ok = blf_bb.play_sound("snd_correct", blf_sc)
blf_snd_err = blf_bb.play_sound("snd_wrong", None)
blf_check = blf_bb.if_else(blf_bb.op_lt_var("FocusDist", "var_focus", 35, None), blf_snd_ok, blf_snd_err, None)
blf_bb.hat_clicked(blf_check, 50, 320)

for ev in ["goto_level2", "goto_level3", "goto_hall_quiz", "show_victory"]:
    blf_bb.hat_broadcast(ev, f"bc_{ev}", blf_bb.hide(None), 50, 500)

targets.append(create_sprite("BtnLockFocus", ["btn_lock_focus"], blf_bb, ["snd_click", "snd_correct", "snd_wrong"], x=0, y=-125, size=100, visible=False, layer=12))

# =========================================================================
# 9. LEVEL 2: WIND TURBINE & FLYWHEEL
# =========================================================================
# WindTurbine Rotor: 70x70 at (0, 35)
wt_bb = BlockBuilder()
wt_bb.hat_flag(wt_bb.hide(None), 50, 50)

wt_rot = wt_bb.forever(wt_bb.turn_right(15, wt_bb.wait(0.04, None)), None)
wt_show = wt_bb.show(wt_rot)
wt_pos = wt_bb.goto_xy(0, 35, wt_show)
wt_bb.hat_broadcast("start_level2_game", "bc_start_level2_game", wt_pos, 50, 160)

for ev in ["goto_level1", "goto_level3", "goto_hall_quiz", "show_victory"]:
    wt_stop = wt_bb.stop_other_scripts(wt_bb.hide(None))
    wt_bb.hat_broadcast(ev, f"bc_{ev}", wt_stop, 50, 350)

targets.append(create_sprite("WindTurbine", ["wind_rotor"], wt_bb, ["snd_wind"], x=0, y=35, size=100, visible=False, layer=5))

# FlywheelMeter: 104x104 at (-65, 55) -> Beside wind turbine, away from characters!
fwm_bb = BlockBuilder()
fwm_bb.hat_flag(fwm_bb.hide(None), 50, 50)
fwm_bb.hat_broadcast("start_level2_game", "bc_start_level2_game", fwm_bb.show(fwm_bb.goto_xy(-90, 35, None)), 50, 160)
for ev in ["goto_level1", "goto_level3", "goto_hall_quiz", "show_victory"]:
    fwm_stop = fwm_bb.stop_other_scripts(fwm_bb.hide(None))
    fwm_bb.hat_broadcast(ev, f"bc_{ev}", fwm_stop, 50, 350)

targets.append(create_sprite("FlywheelMeter", ["flywheel_meter"], fwm_bb, [], x=-90, y=35, size=100, visible=False, layer=6))

# BtnBrake: 144x38.5 at (-90, -125) -> Spans X: -162 to -18
bb_bb = BlockBuilder()
bb_bb.hat_flag(bb_bb.hide(None), 50, 50)
bb_bb.hat_broadcast("start_level2_game", "bc_start_level2_game", bb_bb.show(bb_bb.goto_xy(-90, -125, None)), 50, 160)
bb_click = bb_bb.change_var("Energy", "var_energy", 25, bb_bb.change_var("Score", "var_score", 10, bb_bb.play_sound("snd_click", None)))
bb_bb.hat_clicked(bb_click, 50, 300)
for ev in ["goto_level1", "goto_level3", "goto_hall_quiz", "show_victory"]:
    bb_stop = bb_bb.stop_other_scripts(bb_bb.hide(None))
    bb_bb.hat_broadcast(ev, f"bc_{ev}", bb_stop, 50, 480)

targets.append(create_sprite("BtnBrake", ["btn_brake"], bb_bb, ["snd_click"], x=-90, y=-125, size=100, visible=False, layer=12))

# BtnGear: 152x38.5 at (+90, -125) -> Spans X: +14 to +166 (Gap = 32px between Brake and Gear!)
bg_bb = BlockBuilder()
bg_bb.hat_flag(bg_bb.hide(None), 50, 50)
bg_bb.hat_broadcast("start_level2_game", "bc_start_level2_game", bg_bb.show(bg_bb.goto_xy(90, -125, None)), 50, 160)

# Check energy >= 100 to finish level 2
bg_next = bg_bb.broadcast("goto_level3", "bc_goto_level3", None)
bg_wait = bg_bb.wait(1.2, bg_next)
bg_snd_win = bg_bb.play_sound("snd_correct", bg_wait)
bg_check = bg_bb.if_then(bg_bb.op_gt_var("Energy", "var_energy", 99, None), bg_snd_win, None)
bg_add_en = bg_bb.change_var("Energy", "var_energy", 25, bg_check)
bg_add_sc = bg_bb.change_var("Score", "var_score", 10, bg_add_en)
bg_snd = bg_bb.play_sound("snd_click", bg_add_sc)
bg_bb.hat_clicked(bg_snd, 50, 300)

for ev in ["goto_level1", "goto_level3", "goto_hall_quiz", "show_victory"]:
    bg_stop = bg_bb.stop_other_scripts(bg_bb.hide(None))
    bg_bb.hat_broadcast(ev, f"bc_{ev}", bg_stop, 50, 520)

targets.append(create_sprite("BtnGear", ["btn_gear"], bg_bb, ["snd_click", "snd_correct"], x=90, y=-125, size=100, visible=False, layer=12))

# =========================================================================
# 10. LEVEL 3: MAGNETOMETER & KMA CORE
# =========================================================================
# Ore Vein: 112x40 at (50, 0)
ov_bb = BlockBuilder()
ov_bb.hat_flag(ov_bb.hide(None), 50, 50)
ov_bb.hat_broadcast("start_level3_game", "bc_start_level3_game", ov_bb.show(ov_bb.goto_xy(50, 0, None)), 50, 160)
for ev in ["goto_level1", "goto_level2", "goto_hall_quiz", "show_victory"]:
    ov_bb.hat_broadcast(ev, f"bc_{ev}", ov_bb.hide(None), 50, 350)

targets.append(create_sprite("OreVein", ["ore_vein"], ov_bb, [], x=50, y=0, size=100, visible=False, layer=4))

# Magnetometer: 88x51.5 at (-50, 0)
mag_bb = BlockBuilder()
mag_bb.hat_flag(mag_bb.hide(None), 50, 50)

mag_bb.hat_key("right arrow", mag_bb.change_x(15, None), 50, 160)
mag_bb.hat_key("left arrow", mag_bb.change_x(-15, None), 50, 260)
mag_bb.hat_key("up arrow", mag_bb.change_y(15, None), 50, 360)
mag_bb.hat_key("down arrow", mag_bb.change_y(-15, None), 50, 460)

mag_dist = mag_bb.forever(mag_bb.set_var("DistKMA", "var_distkma", 20, None), None)
mag_show = mag_bb.show(mag_dist)
mag_pos = mag_bb.goto_xy(-50, 0, mag_show)
mag_bb.hat_broadcast("start_level3_game", "bc_start_level3_game", mag_pos, 50, 600)

for ev in ["goto_level1", "goto_level2", "goto_hall_quiz", "show_victory"]:
    mag_stop = mag_bb.stop_other_scripts(mag_bb.hide(None))
    mag_bb.hat_broadcast(ev, f"bc_{ev}", mag_stop, 50, 800)

targets.append(create_sprite("Magnetometer", ["magneto_sensor"], mag_bb, ["snd_magnet"], x=-50, y=0, size=100, visible=False, layer=6))

# BtnDrill: 168x38.5 at (0, -125) -> Spans X: -84 to +84 (Lazarev at -150, Hero at +150, ZERO overlap!)
dr_bb = BlockBuilder()
dr_bb.hat_flag(dr_bb.hide(None), 50, 50)
dr_bb.hat_broadcast("start_level3_game", "bc_start_level3_game", dr_bb.show(dr_bb.goto_xy(0, -125, None)), 50, 160)

dr_bc = dr_bb.broadcast("goto_hall_quiz", "bc_goto_hall_quiz", None)
dr_w = dr_bb.wait(1.2, dr_bc)
dr_sc = dr_bb.change_var("Score", "var_score", 30, dr_w)
dr_snd_ok = dr_bb.play_sound("snd_correct", dr_sc)
dr_snd_err = dr_bb.play_sound("snd_wrong", None)
dr_check = dr_bb.if_else(dr_bb.op_lt_var("DistKMA", "var_distkma", 35, None), dr_snd_ok, dr_snd_err, None)
dr_bb.hat_clicked(dr_check, 50, 320)

for ev in ["goto_level1", "goto_level2", "goto_hall_quiz", "show_victory"]:
    dr_bb.hat_broadcast(ev, f"bc_{ev}", dr_bb.hide(None), 50, 500)

targets.append(create_sprite("BtnDrill", ["btn_drill"], dr_bb, ["snd_click", "snd_correct", "snd_wrong"], x=0, y=-125, size=100, visible=False, layer=12))

# =========================================================================
# 11. QUIZ BUTTONS (BtnOptA, BtnOptB, BtnOptC) - NO OVERLAP!
# =========================================================================
# Each is 224x34 units. Placed at X = +50 (Spans X: -62 to +162; Hero is at -150; Gap = 48px!)
# BtnOptA at Y = 40 (Spans Y: 23 to 57)
oa_bb = BlockBuilder()
oa_bb.hat_flag(oa_bb.hide(None), 50, 50)
oa_bb.hat_broadcast("start_quiz_game", "bc_start_quiz_game", oa_bb.show(oa_bb.goto_xy(50, 40, None)), 50, 160)
for ev in ["goto_level1", "goto_level2", "goto_level3", "show_victory"]:
    oa_bb.hat_broadcast(ev, f"bc_{ev}", oa_bb.hide(None), 50, 300)

oa_win = oa_bb.broadcast("show_victory", "bc_show_victory", None)
oa_w = oa_bb.wait(1.0, oa_win)
oa_sc = oa_bb.change_var("Score", "var_score", 20, oa_w)
oa_snd = oa_bb.play_sound("snd_correct", oa_sc)
oa_bb.hat_clicked(oa_snd, 50, 480)

targets.append(create_sprite("BtnOptA", ["btn_opt_a"], oa_bb, ["snd_click", "snd_correct"], x=50, y=40, size=100, visible=False, layer=12))

# BtnOptB at Y = -15 (Spans Y: -32 to +2, Gap = 21px!)
ob_bb = BlockBuilder()
ob_bb.hat_flag(ob_bb.hide(None), 50, 50)
ob_bb.hat_broadcast("start_quiz_game", "bc_start_quiz_game", ob_bb.show(ob_bb.goto_xy(50, -15, None)), 50, 160)
for ev in ["goto_level1", "goto_level2", "goto_level3", "show_victory"]:
    ob_bb.hat_broadcast(ev, f"bc_{ev}", ob_bb.hide(None), 50, 300)
ob_bb.hat_clicked(ob_bb.play_sound("snd_wrong", None), 50, 480)

targets.append(create_sprite("BtnOptB", ["btn_opt_b"], ob_bb, ["snd_click", "snd_wrong"], x=50, y=-15, size=100, visible=False, layer=12))

# BtnOptC at Y = -70 (Spans Y: -87 to -53, Gap = 21px!)
oc_bb = BlockBuilder()
oc_bb.hat_flag(oc_bb.hide(None), 50, 50)
oc_bb.hat_broadcast("start_quiz_game", "bc_start_quiz_game", oc_bb.show(oc_bb.goto_xy(50, -70, None)), 50, 160)
for ev in ["goto_level1", "goto_level2", "goto_level3", "show_victory"]:
    oc_bb.hat_broadcast(ev, f"bc_{ev}", oc_bb.hide(None), 50, 300)
oc_bb.hat_clicked(oc_bb.play_sound("snd_wrong", None), 50, 480)

targets.append(create_sprite("BtnOptC", ["btn_opt_c"], oc_bb, ["snd_click", "snd_wrong"], x=50, y=-70, size=100, visible=False, layer=12))

# =========================================================================
# 12. VICTORY MEDAL (FxMedal)
# =========================================================================
# FxMedal: 90x144.5 at (0, 65)
med_bb = BlockBuilder()
med_bb.hat_flag(med_bb.hide(None), 50, 50)

# Pulsing medal loop
m_w2 = med_bb.wait(0.3, None)
m_s2 = med_bb.set_size(95, m_w2)
m_w1 = med_bb.wait(0.3, m_s2)
m_s1 = med_bb.set_size(105, m_w1)
m_loop = med_bb.forever(m_s1, None)
m_show = med_bb.show(m_loop)
m_pos = med_bb.goto_xy(0, 65, m_show)
med_bb.hat_broadcast("show_victory", "bc_show_victory", m_pos, 50, 160)

for ev in ["goto_level1", "goto_level2", "goto_level3", "goto_hall_quiz"]:
    m_stop = med_bb.stop_other_scripts(med_bb.hide(None))
    med_bb.hat_broadcast(ev, f"bc_{ev}", m_stop, 50, 350)

targets.append(create_sprite("FxMedal", ["fx_medal"], med_bb, ["snd_fanfare"], x=0, y=65, size=100, visible=False, layer=14))

# =========================================================================
# 13. HUD (Верхняя панель: 368x29 at 0, 162)
# =========================================================================
hud_bb = BlockBuilder()
hud_bb.hat_flag(hud_bb.hide(None), 50, 50)
for ev in ["goto_level1", "goto_level2", "goto_level3", "goto_hall_quiz", "show_victory"]:
    hud_bb.hat_broadcast(ev, f"bc_{ev}", hud_bb.show(hud_bb.goto_xy(0, 162, None)), 50, 160)

targets.append(create_sprite("HUD", ["hud_bar"], hud_bb, [], x=0, y=162, size=100, visible=False, layer=10))

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
