import json
import os
import zipfile
import hashlib
from scratch_builder import BlockBuilder, gen_id

PROJECT_DIR = "/home/dima/Projects/hackathon/scratch_project"
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
MANIFEST_FILE = os.path.join(PROJECT_DIR, "assets_manifest.json")

with open(MANIFEST_FILE, "r") as f:
    manifest = json.load(f)

# Global variables
VARIABLES = {
    "var_gamestate": ["GameState", "TITLE"],
    "var_score": ["Score", 0],
    "var_energy": ["Energy", 0],
    "var_wind": ["WindSpeed", 30],
    "var_brake": ["BrakeActive", 0],
    "var_focus": ["FocusDist", 50],
    "var_question": ["QuestionNum", 1],
    "var_status": ["StatusRank", "Исследователь"],
    "var_award": ["AwardName", "Медаль"],
    "var_mission": ["MissionText", "IT-ЦОПП: Нажмите СТАРТ для начала экспедиции!"]
}

# Global broadcasts
BROADCASTS = {
    "bc_start_title": "start_title",
    "bc_show_rules": "show_rules",
    "bc_show_authors": "show_authors",
    "bc_start_intro": "start_intro",
    "bc_goto_level1": "goto_level1",
    "bc_start_level1_game": "start_level1_game",
    "bc_level1_complete": "level1_complete",
    "bc_goto_level2": "goto_level2",
    "bc_start_level2_game": "start_level2_game",
    "bc_level2_complete": "level2_complete",
    "bc_goto_level3": "goto_level3",
    "bc_start_level3_game": "start_level3_game",
    "bc_level3_complete": "level3_complete",
    "bc_goto_hall_quiz": "goto_hall_quiz",
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
        res["bitmapResolution"] = 1
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

# =========================================================================
# 0. STAGE
# =========================================================================
stage_bb = BlockBuilder()

# Flag clicked
s_init_mission = stage_bb.set_var("MissionText", "var_mission", "IT-ЦОПП: Нажмите СТАРТ для начала экспедиции!", None)
s_init_q = stage_bb.set_var("QuestionNum", "var_question", 1, s_init_mission)
s_init_focus = stage_bb.set_var("FocusDist", "var_focus", 50, s_init_q)
s_init_brake = stage_bb.set_var("BrakeActive", "var_brake", 0, s_init_focus)
s_init_wind = stage_bb.set_var("WindSpeed", "var_wind", 30, s_init_brake)
s_init_energy = stage_bb.set_var("Energy", "var_energy", 0, s_init_wind)
s_init_score = stage_bb.set_var("Score", "var_score", 0, s_init_energy)
s_init_state = stage_bb.set_var("GameState", "var_gamestate", "TITLE", s_init_score)
s_bg_title = stage_bb.switch_backdrop("bg_title", s_init_state)
s_bc_start = stage_bb.broadcast("start_title", "bc_start_title", s_bg_title)
stage_bb.hat_flag(s_bc_start, 50, 50)

# when I receive goto_level1
l1_snd = stage_bb.play_sound("snd_teleport", None)
l1_bg = stage_bb.switch_backdrop("bg_semenov", l1_snd)
l1_miss = stage_bb.set_var("MissionText", "var_mission", "Локация 1: Обсерватория Ф.А. Семёнова (1853 г.)", l1_bg)
l1_state = stage_bb.set_var("GameState", "var_gamestate", "LEVEL1", l1_miss)
stage_bb.hat_broadcast("goto_level1", "bc_goto_level1", l1_state, 50, 250)

# when I receive goto_level2
l2_snd = stage_bb.play_sound("snd_teleport", None)
l2_bg = stage_bb.switch_backdrop("bg_ufimtsev", l2_snd)
l2_miss = stage_bb.set_var("MissionText", "var_mission", "Локация 2: Ветроэлектростанция А.Г. Уфимцева (1931 г.)", l2_bg)
l2_state = stage_bb.set_var("GameState", "var_gamestate", "LEVEL2", l2_miss)
stage_bb.hat_broadcast("goto_level2", "bc_goto_level2", l2_state, 50, 420)

# when I receive goto_level3
l3_snd = stage_bb.play_sound("snd_teleport", None)
l3_bg = stage_bb.switch_backdrop("bg_kma_aes", l3_snd)
l3_miss = stage_bb.set_var("MissionText", "var_mission", "Локация 3: КМА и Энергия Атома (г. Курчатов)", l3_bg)
l3_state = stage_bb.set_var("GameState", "var_gamestate", "LEVEL3", l3_miss)
stage_bb.hat_broadcast("goto_level3", "bc_goto_level3", l3_state, 50, 590)

# when I receive goto_hall_quiz
lh_snd = stage_bb.play_sound("snd_fanfare", None)
lh_bg = stage_bb.switch_backdrop("bg_hall_of_fame", lh_snd)
lh_miss = stage_bb.set_var("MissionText", "var_mission", "Локация 4: Зал Научной Славы Курского Края • Викторина", lh_bg)
lh_state = stage_bb.set_var("GameState", "var_gamestate", "HALL_QUIZ", lh_miss)
stage_bb.hat_broadcast("goto_hall_quiz", "bc_goto_hall_quiz", lh_state, 50, 760)

# when I receive show_victory
lv_snd = stage_bb.play_sound("snd_fanfare", None)
lv_miss = stage_bb.set_var("MissionText", "var_mission", "ФИНАЛ: Торжественное награждение первопроходца!", lv_snd)
lv_state = stage_bb.set_var("GameState", "var_gamestate", "VICTORY", lv_miss)
stage_bb.hat_broadcast("show_victory", "bc_show_victory", lv_state, 50, 930)

stage_target = {
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
    "layerOrder": 0,
    "tempo": 60,
    "videoTransparency": 50,
    "videoState": "on",
    "textToSpeechLanguage": None
}
targets.append(stage_target)

# Helper to create basic sprite target
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
        "sounds": [make_sound(s) for s in (sounds or ["snd_click"])],
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
# 1. HERO (Главный герой / Исследователь)
# =========================================================================
hero_bb = BlockBuilder()

# Green flag: hide
h_hide = hero_bb.hide(None)
hero_bb.hat_flag(h_hide, 50, 50)

# start_intro:
h_i_bc = hero_bb.broadcast("goto_level1", "bc_goto_level1", None)
h_i_say2 = hero_bb.say_for("Архив курских изобретений поврежден. Пора в экспедицию!", 2.5, h_i_bc)
h_i_say1 = hero_bb.say_for("Привет! Мы в квантовой лаборатории IT-ЦОПП Курска!", 2.5, h_i_say2)
h_i_show = hero_bb.show(h_i_say1)
h_i_pos = hero_bb.goto_xy(-140, -60, h_i_show)
h_i_cost = hero_bb.switch_costume("hero_copt", h_i_pos)
hero_bb.hat_broadcast("start_intro", "bc_start_intro", h_i_cost, 50, 160)

# goto_level1:
h_l1_say = hero_bb.say_for("Курск 1853 года! Обсерватория астронома Фёдора Семёнова!", 2.5, None)
h_l1_show = hero_bb.show(h_l1_say)
h_l1_pos = hero_bb.goto_xy(-140, -60, h_l1_show)
h_l1_cost = hero_bb.switch_costume("hero_astronomer", h_l1_pos)
hero_bb.hat_broadcast("goto_level1", "bc_goto_level1", h_l1_cost, 50, 360)

# goto_level2:
h_l2_say = hero_bb.say_for("1931 год, улица Семёновская! Мы у ветростанции Уфимцева!", 2.5, None)
h_l2_show = hero_bb.show(h_l2_say)
h_l2_pos = hero_bb.goto_xy(-140, -60, h_l2_show)
h_l2_cost = hero_bb.switch_costume("hero_aviator", h_l2_pos)
hero_bb.hat_broadcast("goto_level2", "bc_goto_level2", h_l2_cost, 50, 560)

# goto_level3:
h_l3_say = hero_bb.say_for("Курская магнитная аномалия и атомный кластер Курчатова!", 2.5, None)
h_l3_show = hero_bb.show(h_l3_say)
h_l3_pos = hero_bb.goto_xy(-140, -60, h_l3_show)
h_l3_cost = hero_bb.switch_costume("hero_physicist", h_l3_pos)
hero_bb.hat_broadcast("goto_level3", "bc_goto_level3", h_l3_cost, 50, 760)

# show_victory (with deep nested branching!):
# Outer condition: Score >= 85
# Substack 1 (High score):
#   Nested condition: Score >= 100
#     Substack 1.1: say "Идеальный результат! Золотая медаль Демидова наша!"
#     Substack 1.2: say "Великолепный результат! Звание Академика Соловьиного края!"
# Substack 2 (Else):
#   Nested condition: Score >= 55
#     Substack 2.1: say "Отличная экспедиция! Наука Курского края под защитой!"
#     Substack 2.2: say "Хорошая попытка! Пройдите экспедицию снова!"

say_gold_max = hero_bb.say_for("Абсолютный триумф (100+ баллов)! Золотая медаль Демидова!", 3.5, None)
say_gold = hero_bb.say_for("Великолепно! Звание Академика Соловьиного Края!", 3.5, None)
cond_gt_100 = hero_bb.op_gt_var("Score", "var_score", 95, None)
nested_if_gold = hero_bb.if_else(cond_gt_100, say_gold_max, say_gold, None)
set_award_gold = hero_bb.set_var("AwardName", "var_award", "Золотая Демидовская Медаль РАН", nested_if_gold)
set_stat_gold = hero_bb.set_var("StatusRank", "var_status", "Академик Соловьиного Края", set_award_gold)

say_silver = hero_bb.say_for("Отличная экспедиция! Наука Курского края под защитой!", 3.5, None)
set_award_silv = hero_bb.set_var("AwardName", "var_award", "Серебряный знак Уфимцева", say_silver)
set_stat_silv = hero_bb.set_var("StatusRank", "var_status", "Инженер-первопроходец Курска", set_award_silv)

say_bronze = hero_bb.say_for("Хорошая попытка! Пройдите экспедицию снова для максимума!", 3.5, None)
set_award_brz = hero_bb.set_var("AwardName", "var_award", "Сертификат исследователя", say_bronze)
set_stat_brz = hero_bb.set_var("StatusRank", "var_status", "Юный лаборант ЦОПП", set_award_brz)

cond_gt_55 = hero_bb.op_gt_var("Score", "var_score", 54, None)
nested_if_else_lower = hero_bb.if_else(cond_gt_55, set_stat_silv, set_stat_brz, None)

cond_gt_85 = hero_bb.op_gt_var("Score", "var_score", 84, None)
main_branch = hero_bb.if_else(cond_gt_85, set_stat_gold, nested_if_else_lower, None)

h_v_size = hero_bb.set_size(125, main_branch)
h_v_show = hero_bb.show(h_v_size)
h_v_pos = hero_bb.goto_xy(0, -45, h_v_show)
h_v_cost = hero_bb.switch_costume("hero_triumph", h_v_pos)
hero_bb.hat_broadcast("show_victory", "bc_show_victory", h_v_cost, 50, 960)

targets.append(create_sprite(
    "Hero",
    ["hero_copt", "hero_astronomer", "hero_aviator", "hero_physicist", "hero_triumph"],
    hero_bb,
    ["snd_teleport", "snd_correct", "snd_fanfare"],
    x=-140, y=-60, size=100, visible=False, layer=5
))

# =========================================================================
# 2. KURSIK (Дрон-соловей «Курсик»)
# =========================================================================
kursik_bb = BlockBuilder()

# Green flag: hide
k_hide = kursik_bb.hide(None)
kursik_bb.hat_flag(k_hide, 50, 50)

# Hover loop on start_intro
k_loop_dn = kursik_bb.change_y(-2, None)
k_wait_dn = kursik_bb.wait(0.08, k_loop_dn)
k_rep_dn = kursik_bb.repeat(5, k_wait_dn, None)

k_loop_up = kursik_bb.change_y(2, None)
k_wait_up = kursik_bb.wait(0.08, k_loop_up)
k_rep_up = kursik_bb.repeat(5, k_wait_up, k_rep_dn)

k_forever = kursik_bb.forever(k_rep_up, None)

k_show = kursik_bb.show(k_forever)
k_pos = kursik_bb.goto_xy(-70, 15, k_show)
k_cost = kursik_bb.switch_costume("kursik_hover", k_pos)
kursik_bb.hat_broadcast("start_intro", "bc_start_intro", k_cost, 50, 160)

# Prompts on each stage:
# Level 1 Game start
k_l1_c2 = kursik_bb.switch_costume("kursik_hover", None)
k_l1_say = kursik_bb.say_for("Управляй окуляром! Наведи перекрестье на Солнечное затмение!", 2.5, k_l1_c2)
k_l1_c1 = kursik_bb.switch_costume("kursik_scan", k_l1_say)
kursik_bb.hat_broadcast("start_level1_game", "bc_start_level1_game", k_l1_c1, 50, 360)

# Level 2 Game start
k_l2_c2 = kursik_bb.switch_costume("kursik_hover", None)
k_l2_say = kursik_bb.say_for("Следи за ветром! Жми тормоз в бурю и маховик в штиль!", 2.8, k_l2_c2)
k_l2_c1 = kursik_bb.switch_costume("kursik_talk", k_l2_say)
kursik_bb.hat_broadcast("start_level2_game", "bc_start_level2_game", k_l2_c1, 50, 540)

# Level 3 Game start
k_l3_c2 = kursik_bb.switch_costume("kursik_hover", None)
k_l3_say = kursik_bb.say_for("Слушай звук магнитометра! Чем чаще сигнал — тем ближе руда!", 2.8, k_l3_c2)
k_l3_c1 = kursik_bb.switch_costume("kursik_scan", k_l3_say)
kursik_bb.hat_broadcast("start_level3_game", "bc_start_level3_game", k_l3_c1, 50, 720)

# Victory
k_v_say = kursik_bb.say_for("Ура! Наука Соловьиного края прославлена на века!", 3.5, None)
k_v_pos = kursik_bb.goto_xy(100, 35, k_v_say)
k_v_cost = kursik_bb.switch_costume("kursik_celebrate", k_v_pos)
kursik_bb.hat_broadcast("show_victory", "bc_show_victory", k_v_cost, 50, 900)

targets.append(create_sprite(
    "Kursik",
    ["kursik_hover", "kursik_talk", "kursik_scan", "kursik_celebrate"],
    kursik_bb,
    ["snd_correct", "snd_click"],
    x=-70, y=15, size=90, visible=False, layer=6
))

# =========================================================================
# 3. HISTORICAL FIGURES (Персоналии курян)
# =========================================================================
hist_bb = BlockBuilder()

# Green flag: hide
hf_hide = hist_bb.hide(None)
hist_bb.hat_flag(hf_hide, 50, 50)

# goto_level1: Fedor Semenov
hf_l1_bc = hist_bb.broadcast("start_level1_game", "bc_start_level1_game", None)
hf_l1_s3 = hist_bb.say_for("Помогите мне сфокусировать окуляр и зафиксировать затмение!", 3.0, hf_l1_bc)
hf_l1_s2 = hist_bb.say_for("Без школ и академий я рассчитал затмения Солнца до 2001 года!", 3.0, hf_l1_s3)
hf_l1_s1 = hist_bb.say_for("Приветствую! Я курский купец и астроном Фёдор Семёнов.", 3.0, hf_l1_s2)
hf_l1_show = hist_bb.show(hf_l1_s1)
hf_l1_pos = hist_bb.goto_xy(120, -60, hf_l1_show)
hf_l1_cost = hist_bb.switch_costume("char_semenov", hf_l1_pos)
hist_bb.hat_broadcast("goto_level1", "bc_goto_level1", hf_l1_cost, 50, 160)

# goto_level2: Anatoly Ufimtsev
hf_l2_bc = hist_bb.broadcast("start_level2_game", "bc_start_level2_game", None)
hf_l2_s3 = hist_bb.say_for("Ветростанция питает дом даже в штиль благодаря маховику! Запустим её!", 3.0, hf_l2_bc)
hf_l2_s2 = hist_bb.say_for("Я создал первую в мире ветростанцию с инерционным накопителем!", 3.0, hf_l2_s3)
hf_l2_s1 = hist_bb.say_for("Здравствуйте! Я изобретатель Анатолий Уфимцев, внук Семёнова!", 3.0, hf_l2_s2)
hf_l2_show = hist_bb.show(hf_l2_s1)
hf_l2_pos = hist_bb.goto_xy(120, -60, hf_l2_show)
hf_l2_cost = hist_bb.switch_costume("char_ufimtsev", hf_l2_pos)
hist_bb.hat_broadcast("goto_level2", "bc_goto_level2", hf_l2_cost, 50, 420)

# goto_level3: Academician Petr Lazarev
hf_l3_bc = hist_bb.broadcast("start_level3_game", "bc_start_level3_game", None)
hf_l3_s3 = hist_bb.say_for("Найдите эпицентр магнетита нашим гео-магнитометром!", 3.0, hf_l3_bc)
hf_l3_s2 = hist_bb.say_for("Мы доказали: здесь крупнейший в мире бассейн железных руд!", 3.0, hf_l3_s3)
hf_l3_s1 = hist_bb.say_for("Приветствую! Я академик Пётр Лазарев, исследователь КМА.", 3.0, hf_l3_s2)
hf_l3_show = hist_bb.show(hf_l3_s1)
hf_l3_pos = hist_bb.goto_xy(120, -60, hf_l3_show)
hf_l3_cost = hist_bb.switch_costume("char_lazarev", hf_l3_pos)
hist_bb.hat_broadcast("goto_level3", "bc_goto_level3", hf_l3_cost, 50, 680)

# In hall of fame:
hf_h_say = hist_bb.say_for("В Зале Славы вы сдаете экзамен по науке Курского Края!", 2.5, None)
hf_h_show = hist_bb.show(hf_h_say)
hf_h_pos = hist_bb.goto_xy(170, -60, hf_h_show)
hf_h_cost = hist_bb.switch_costume("char_semenov", hf_h_pos)
hist_bb.hat_broadcast("goto_hall_quiz", "bc_goto_hall_quiz", hf_h_cost, 50, 940)

# On victory:
hf_v_hide = hist_bb.hide(None)
hist_bb.hat_broadcast("show_victory", "bc_show_victory", hf_v_hide, 50, 1140)

targets.append(create_sprite(
    "HistoricalFigures",
    ["char_semenov", "char_ufimtsev", "char_lazarev"],
    hist_bb,
    ["snd_correct"],
    x=120, y=-60, size=100, visible=False, layer=4
))

# =========================================================================
# 4. TELESCOPE LENS (Мини-игра 1: Окуляр Семёнова)
# =========================================================================
lens_bb = BlockBuilder()
tl_hide = lens_bb.hide(None)
lens_bb.hat_flag(tl_hide, 50, 50)

# Gameplay loop in level 1
tl_bc_comp = lens_bb.broadcast("level1_complete", "bc_level1_complete", None)
tl_hide_done = lens_bb.hide(tl_bc_comp)
tl_say_win = lens_bb.say_for("Фокус пойман! Затмение зафиксировано в таблицах! (+25)", 2.5, tl_hide_done)
tl_add_score = lens_bb.change_var("Score", "var_score", 25, tl_say_win)
tl_snd_win = lens_bb.play_sound("snd_correct", tl_add_score)

# Loop body to focus:
# moves lens closer to eclipse target and clicks
tl_snd_foc = lens_bb.play_sound("snd_focus", None)
tl_dy = lens_bb.change_y(6, tl_snd_foc)
tl_dx = lens_bb.change_x(18, tl_dy)
tl_chg_foc = lens_bb.change_var("FocusDist", "var_focus", -12, tl_dx)
tl_wait = lens_bb.wait(0.35, tl_chg_foc)

cond_foc_done = lens_bb.op_lt_var("FocusDist", "var_focus", 10, None)
tl_rep_until = lens_bb.repeat_until(cond_foc_done, tl_wait, tl_snd_win)

tl_init_foc = lens_bb.set_var("FocusDist", "var_focus", 50, tl_rep_until)
tl_show = lens_bb.show(tl_init_foc)
tl_pos = lens_bb.goto_xy(-40, 40, tl_show)
lens_bb.hat_broadcast("start_level1_game", "bc_start_level1_game", tl_pos, 50, 160)

# Advance to level 2 after completion:
tl_wait_l2 = lens_bb.wait(1.5, None)
tl_bc_l2 = lens_bb.broadcast("goto_level2", "bc_goto_level2", tl_wait_l2)
lens_bb.hat_broadcast("level1_complete", "bc_level1_complete", tl_bc_l2, 50, 420)

targets.append(create_sprite(
    "TelescopeLens",
    ["telescope_lens"],
    lens_bb,
    ["snd_focus", "snd_correct"],
    x=-40, y=40, size=100, visible=False, layer=8
))

# =========================================================================
# 5. ECLIPSE TARGET (Солнечное затмение)
# =========================================================================
ecl_bb = BlockBuilder()
ecl_hide = ecl_bb.hide(None)
ecl_bb.hat_flag(ecl_hide, 50, 50)

ecl_show = ecl_bb.show(None)
ecl_pos = ecl_bb.goto_xy(50, 70, ecl_show)
ecl_bb.hat_broadcast("start_level1_game", "bc_start_level1_game", ecl_pos, 50, 160)

ecl_h2 = ecl_bb.hide(None)
ecl_bb.hat_broadcast("level1_complete", "bc_level1_complete", ecl_h2, 50, 320)

targets.append(create_sprite(
    "EclipseTarget",
    ["eclipse_target"],
    ecl_bb,
    [],
    x=50, y=70, size=100, visible=False, layer=7
))

# =========================================================================
# 6. WIND TURBINE (Ветроэлектростанция Уфимцева)
# =========================================================================
wind_bb = BlockBuilder()
wt_hide = wind_bb.hide(None)
wind_bb.hat_flag(wt_hide, 50, 50)

# Show on goto_level2
wt_show = wind_bb.show(None)
wt_pos = wind_bb.goto_xy(100, 70, wt_show)
wind_bb.hat_broadcast("goto_level2", "bc_goto_level2", wt_pos, 50, 160)

# Hide on level3
wt_h3 = wind_bb.hide(None)
wind_bb.hat_broadcast("goto_level3", "bc_goto_level3", wt_h3, 50, 320)

# Gameplay loop on start_level2_game:
# Contains 3-level deep nested conditional branching!
# Outer: repeat until (Energy >= 100)
# Inside loop:
#   if (WindSpeed > 60):
#     if (BrakeActive == 1):
#       Energy += 15, Score += 5, BrakeActive = 0, say "Тормоз защитил маховик от бури!"
#     else:
#       Energy -= 5, Score -= 2, say "Шторм без тормоза! Перегрузка!"
#   else:
#     if (WindSpeed < 25):
#       if (Energy > 15):
#         Energy += 10, say "Штиль! Но вакуумный маховик Уфимцева дает ток!"
#       else:
#         Energy += 5, say "Штиль. Накопите энергию маховика!"
#     else:
#       Energy += 15, Score += 5, say "Ровный курский ветер! Генератор Уфимцева дает ток!"

# Branch 1.1: Storm + Brake
s_brk_msg = wind_bb.say_for("Тормоз защитил маховик от бури! Ток сохранен! (+5)", 1.2, None)
s_brk_rst = wind_bb.set_var("BrakeActive", "var_brake", 0, s_brk_msg)
s_brk_sc = wind_bb.change_var("Score", "var_score", 5, s_brk_rst)
s_brk_en = wind_bb.change_var("Energy", "var_energy", 15, s_brk_sc)

# Branch 1.2: Storm without Brake
s_ovr_msg = wind_bb.say_for("Шторм без тормоза! Перегрузка ротора!", 1.2, None)
s_ovr_sc = wind_bb.change_var("Score", "var_score", -2, s_ovr_msg)
s_ovr_en = wind_bb.change_var("Energy", "var_energy", -5, s_ovr_sc)

cond_brake = wind_bb.op_equals_var("BrakeActive", "var_brake", 1, None)
nested_storm = wind_bb.if_else(cond_brake, s_brk_en, s_ovr_en, None)

# Branch 2.1: Calm + Flywheel stored
s_calm_msg1 = wind_bb.say_for("Штиль! Но вакуумный маховик Уфимцева отдает ток!", 1.2, None)
s_calm_en1 = wind_bb.change_var("Energy", "var_energy", 10, s_calm_msg1)

# Branch 2.2: Calm + Low energy
s_calm_msg2 = wind_bb.say_for("Штиль. Накопите инерцию в маховике!", 1.2, None)
s_calm_en2 = wind_bb.change_var("Energy", "var_energy", 5, s_calm_msg2)

cond_en_stored = wind_bb.op_gt_var("Energy", "var_energy", 15, None)
nested_calm = wind_bb.if_else(cond_en_stored, s_calm_en1, s_calm_en2, None)

# Branch 2.3: Optimal normal wind
s_opt_msg = wind_bb.say_for("Ровный курский ветер! Генератор Уфимцева работает! (+5)", 1.2, None)
s_opt_sc = wind_bb.change_var("Score", "var_score", 5, s_opt_msg)
s_opt_en = wind_bb.change_var("Energy", "var_energy", 15, s_opt_sc)

cond_calm = wind_bb.op_lt_var("WindSpeed", "var_wind", 25, None)
nested_normal_or_calm = wind_bb.if_else(cond_calm, nested_calm, s_opt_en, None)

cond_storm = wind_bb.op_gt_var("WindSpeed", "var_wind", 60, None)
step_nested_physics = wind_bb.if_else(cond_storm, nested_storm, nested_normal_or_calm, None)

# Cycle wind variations: 20 -> 70 -> 35 -> 80
turn_blades = wind_bb.turn_right(30, step_nested_physics)
cycle_wait = wind_bb.wait(0.6, turn_blades)

# Victory after 100% energy
wt_bc_done = wind_bb.broadcast("level2_complete", "bc_level2_complete", None)
wt_say_win = wind_bb.say_for("100% энергии получено! Фонари Курска зажглись! (+25)", 3.0, wt_bc_done)
wt_sc_win = wind_bb.change_var("Score", "var_score", 25, wt_say_win)
wt_snd_win = wind_bb.play_sound("snd_correct", wt_sc_win)

cond_en_done = wind_bb.op_gt_var("Energy", "var_energy", 99, None)
wt_rep_until = wind_bb.repeat_until(cond_en_done, cycle_wait, wt_snd_win)

wt_init_en = wind_bb.set_var("Energy", "var_energy", 10, wt_rep_until)
wind_bb.hat_broadcast("start_level2_game", "bc_start_level2_game", wt_init_en, 50, 480)

# Advance to level 3
wt_w_l3 = wind_bb.wait(1.5, None)
wt_bc_l3 = wind_bb.broadcast("goto_level3", "bc_goto_level3", wt_w_l3)
wind_bb.hat_broadcast("level2_complete", "bc_level2_complete", wt_bc_l3, 50, 780)

targets.append(create_sprite(
    "WindTurbine",
    ["wind_rotor"],
    wind_bb,
    ["snd_wind", "snd_correct"],
    x=100, y=70, size=100, visible=False, layer=8
))

# =========================================================================
# 7. FLYWHEEL METER (Маховик-аккумулятор)
# =========================================================================
fly_bb = BlockBuilder()
fly_hide = fly_bb.hide(None)
fly_bb.hat_flag(fly_hide, 50, 50)

fly_show = fly_bb.show(None)
fly_pos = fly_bb.goto_xy(-60, 70, fly_show)
fly_bb.hat_broadcast("goto_level2", "bc_goto_level2", fly_pos, 50, 160)

fly_h3 = fly_bb.hide(None)
fly_bb.hat_broadcast("goto_level3", "bc_goto_level3", fly_h3, 50, 320)

targets.append(create_sprite(
    "FlywheelMeter",
    ["flywheel_meter"],
    fly_bb,
    [],
    x=-60, y=70, size=90, visible=False, layer=7
))

# =========================================================================
# 8. MAGNETOMETER (Гео-магнитометр КМА Лазарева)
# =========================================================================
mag_bb = BlockBuilder()
mag_hide = mag_bb.hide(None)
mag_bb.hat_flag(mag_hide, 50, 50)

# Search gameplay: moves across quarry terraces, sounds beep, discovers ore
mag_bc_done = mag_bb.broadcast("level3_complete", "bc_level3_complete", None)
mag_h_done = mag_bb.hide(mag_bc_done)
mag_say_win = mag_bb.say_for("Залежь магнетита найдена! Атомный кластер запущен! (+25)", 3.0, mag_h_done)
mag_sc_win = mag_bb.change_var("Score", "var_score", 25, mag_say_win)
mag_snd_win = mag_bb.play_sound("snd_correct", mag_sc_win)

# 4 search steps with sound
step_say = mag_bb.say_for("Стрелка реагирует на магнетит! Сигнал растет!", 0.8, None)
step_snd = mag_bb.play_sound("snd_magnet", step_say)
step_dy = mag_bb.change_y(-10, step_snd)
step_dx = mag_bb.change_x(30, step_dy)
step_w = mag_bb.wait(0.5, step_dx)

mag_rep = mag_bb.repeat(4, step_w, mag_snd_win)

mag_show = mag_bb.show(mag_rep)
mag_pos = mag_bb.goto_xy(-50, -10, mag_show)
mag_bb.hat_broadcast("start_level3_game", "bc_start_level3_game", mag_pos, 50, 160)

# Advance to Quiz
mag_w_q = mag_bb.wait(1.5, None)
mag_bc_q = mag_bb.broadcast("goto_hall_quiz", "bc_goto_hall_quiz", mag_w_q)
mag_bb.hat_broadcast("level3_complete", "bc_level3_complete", mag_bc_q, 50, 420)

targets.append(create_sprite(
    "Magnetometer",
    ["magneto_sensor"],
    mag_bb,
    ["snd_magnet", "snd_correct"],
    x=-50, y=-10, size=90, visible=False, layer=8
))

# =========================================================================
# 9. ORE VEIN (Пласт магнетита КМА)
# =========================================================================
ore_bb = BlockBuilder()
ore_hide = ore_bb.hide(None)
ore_bb.hat_flag(ore_hide, 50, 50)

ore_show = ore_bb.show(None)
ore_pos = ore_bb.goto_xy(70, -50, ore_show)
ore_bb.hat_broadcast("start_level3_game", "bc_start_level3_game", ore_pos, 50, 160)

ore_hq = ore_bb.hide(None)
ore_bb.hat_broadcast("goto_hall_quiz", "bc_goto_hall_quiz", ore_hq, 50, 320)

targets.append(create_sprite(
    "OreVein",
    ["ore_vein"],
    ore_bb,
    [],
    x=70, y=-50, size=100, visible=False, layer=6
))

# =========================================================================
# 10. DIALOG BOX & HUD
# =========================================================================
dlg_bb = BlockBuilder()
dlg_hide = dlg_bb.hide(None)
dlg_bb.hat_flag(dlg_hide, 50, 50)

dlg_show = dlg_bb.show(None)
dlg_pos = dlg_bb.goto_xy(0, -125, dlg_show)
dlg_bb.hat_broadcast("start_intro", "bc_start_intro", dlg_pos, 50, 160)

dlg_h_l1 = dlg_bb.hide(None)
dlg_bb.hat_broadcast("start_level1_game", "bc_start_level1_game", dlg_h_l1, 50, 300)

dlg_s_l2 = dlg_bb.show(None)
dlg_bb.hat_broadcast("goto_level2", "bc_goto_level2", dlg_s_l2, 50, 420)

dlg_h_l2 = dlg_bb.hide(None)
dlg_bb.hat_broadcast("start_level2_game", "bc_start_level2_game", dlg_h_l2, 50, 540)

dlg_s_l3 = dlg_bb.show(None)
dlg_bb.hat_broadcast("goto_level3", "bc_goto_level3", dlg_s_l3, 50, 660)

dlg_h_l3 = dlg_bb.hide(None)
dlg_bb.hat_broadcast("start_level3_game", "bc_start_level3_game", dlg_h_l3, 50, 780)

dlg_h_vic = dlg_bb.hide(None)
dlg_bb.hat_broadcast("show_victory", "bc_show_victory", dlg_h_vic, 50, 900)

targets.append(create_sprite(
    "DialogBox",
    ["dialog_plate"],
    dlg_bb,
    [],
    x=0, y=-125, size=100, visible=False, layer=3
))

# HUD
hud_bb = BlockBuilder()
hud_show = hud_bb.show(None)
hud_pos = hud_bb.goto_xy(0, 165, hud_show)
hud_bb.hat_flag(hud_pos, 50, 50)

targets.append(create_sprite(
    "HUD",
    ["hud_bar"],
    hud_bb,
    [],
    x=0, y=165, size=100, visible=True, layer=10
))

# =========================================================================
# 11. BUTTONS (Меню и Управление)
# =========================================================================
# BtnStart
b_start_bb = BlockBuilder()
bs_show = b_start_bb.show(None)
bs_pos = b_start_bb.goto_xy(0, -15, bs_show)
b_start_bb.hat_flag(bs_pos, 50, 50)

bs_bc = b_start_bb.broadcast("start_intro", "bc_start_intro", None)
bs_hide = b_start_bb.hide(bs_bc)
bs_snd = b_start_bb.play_sound("snd_click", bs_hide)
b_start_bb.hat_clicked(bs_snd, 50, 180)

bs_h2 = b_start_bb.hide(None)
b_start_bb.hat_broadcast("start_intro", "bc_start_intro", bs_h2, 50, 340)

targets.append(create_sprite("BtnStart", ["btn_start"], b_start_bb, ["snd_click"], x=0, y=-15, size=100, visible=True, layer=12))

# BtnRules
b_rules_bb = BlockBuilder()
br_show = b_rules_bb.show(None)
br_pos = b_rules_bb.goto_xy(-90, -75, br_show)
b_rules_bb.hat_flag(br_pos, 50, 50)

br_say = b_rules_bb.say_for("Цель: пройти 3 эпохи науки Курска, решить инженерные задачи и победить в викторине!", 4.0, None)
br_snd = b_rules_bb.play_sound("snd_click", br_say)
b_rules_bb.hat_clicked(br_snd, 50, 180)

br_h2 = b_rules_bb.hide(None)
b_rules_bb.hat_broadcast("start_intro", "bc_start_intro", br_h2, 50, 360)

targets.append(create_sprite("BtnRules", ["btn_rules"], b_rules_bb, ["snd_click"], x=-90, y=-75, size=95, visible=True, layer=12))

# BtnAuthors
b_auth_bb = BlockBuilder()
ba_show = b_auth_bb.show(None)
ba_pos = b_auth_bb.goto_xy(90, -75, ba_show)
b_auth_bb.hat_flag(ba_pos, 50, 50)

ba_say = b_auth_bb.say_for("Проект 'Код Первопроходцев' создан для открытого регионального конкурса IT-ЦОПП!", 4.0, None)
ba_snd = b_auth_bb.play_sound("snd_click", ba_say)
b_auth_bb.hat_clicked(ba_snd, 50, 180)

ba_h2 = b_auth_bb.hide(None)
b_auth_bb.hat_broadcast("start_intro", "bc_start_intro", ba_h2, 50, 360)

targets.append(create_sprite("BtnAuthors", ["btn_authors"], b_auth_bb, ["snd_click"], x=90, y=-75, size=95, visible=True, layer=12))

# BtnBrake (Level 2 Turbine Control)
b_brk_bb = BlockBuilder()
bb_hide = b_brk_bb.hide(None)
b_brk_bb.hat_flag(bb_hide, 50, 50)

bb_show = b_brk_bb.show(None)
bb_pos = b_brk_bb.goto_xy(-65, -15, bb_show)
b_brk_bb.hat_broadcast("start_level2_game", "bc_start_level2_game", bb_pos, 50, 160)

bb_h2 = b_brk_bb.hide(None)
b_brk_bb.hat_broadcast("level2_complete", "bc_level2_complete", bb_h2, 50, 300)

bb_say = b_brk_bb.say_for("Тормоз включен!", 0.8, None)
bb_set = b_brk_bb.set_var("BrakeActive", "var_brake", 1, bb_say)
bb_snd = b_brk_bb.play_sound("snd_click", bb_set)
b_brk_bb.hat_clicked(bb_snd, 50, 420)

targets.append(create_sprite("BtnBrake", ["btn_brake"], b_brk_bb, ["snd_click"], x=-65, y=-15, size=95, visible=False, layer=12))

# BtnGear (Level 2 Flywheel Connect)
b_gear_bb = BlockBuilder()
bg_hide = b_gear_bb.hide(None)
b_gear_bb.hat_flag(bg_hide, 50, 50)

bg_show = b_gear_bb.show(None)
bg_pos = b_gear_bb.goto_xy(65, -15, bg_show)
b_gear_bb.hat_broadcast("start_level2_game", "bc_start_level2_game", bg_pos, 50, 160)

bg_h2 = b_gear_bb.hide(None)
b_gear_bb.hat_broadcast("level2_complete", "bc_level2_complete", bg_h2, 50, 300)

bg_say = b_gear_bb.say_for("Ток направлен в накопитель!", 0.8, None)
bg_chg = b_gear_bb.change_var("Energy", "var_energy", 8, bg_say)
bg_snd = b_gear_bb.play_sound("snd_click", bg_chg)
b_gear_bb.hat_clicked(bg_snd, 50, 420)

targets.append(create_sprite("BtnGear", ["btn_gear"], b_gear_bb, ["snd_click"], x=65, y=-15, size=95, visible=False, layer=12))

# Quiz Option Buttons [A], [B], [C]
b_opta_bb = BlockBuilder()
boa_hide = b_opta_bb.hide(None)
b_opta_bb.hat_flag(boa_hide, 50, 50)

boa_show = b_opta_bb.show(None)
boa_pos = b_opta_bb.goto_xy(0, 40, boa_show)
b_opta_bb.hat_broadcast("goto_hall_quiz", "bc_goto_hall_quiz", boa_pos, 50, 160)

boa_bc = b_opta_bb.broadcast("ans_a", "bc_ans_a", None)
boa_snd = b_opta_bb.play_sound("snd_click", boa_bc)
b_opta_bb.hat_clicked(boa_snd, 50, 300)

boa_hvic = b_opta_bb.hide(None)
b_opta_bb.hat_broadcast("show_victory", "bc_show_victory", boa_hvic, 50, 440)

targets.append(create_sprite("BtnOptA", ["btn_opt_a"], b_opta_bb, ["snd_click"], x=0, y=40, size=90, visible=False, layer=12))

b_optb_bb = BlockBuilder()
bob_hide = b_optb_bb.hide(None)
b_optb_bb.hat_flag(bob_hide, 50, 50)

bob_show = b_optb_bb.show(None)
bob_pos = b_optb_bb.goto_xy(0, -5, bob_show)
b_optb_bb.hat_broadcast("goto_hall_quiz", "bc_goto_hall_quiz", bob_pos, 50, 160)

bob_bc = b_optb_bb.broadcast("ans_b", "bc_ans_b", None)
bob_snd = b_optb_bb.play_sound("snd_click", bob_bc)
b_optb_bb.hat_clicked(bob_snd, 50, 300)

bob_hvic = b_optb_bb.hide(None)
b_optb_bb.hat_broadcast("show_victory", "bc_show_victory", bob_hvic, 50, 440)

targets.append(create_sprite("BtnOptB", ["btn_opt_b"], b_optb_bb, ["snd_click"], x=0, y=-5, size=90, visible=False, layer=12))

b_optc_bb = BlockBuilder()
boc_hide = b_optc_bb.hide(None)
b_optc_bb.hat_flag(boc_hide, 50, 50)

boc_show = b_optc_bb.show(None)
boc_pos = b_optc_bb.goto_xy(0, -50, boc_show)
b_optc_bb.hat_broadcast("goto_hall_quiz", "bc_goto_hall_quiz", boc_pos, 50, 160)

boc_bc = b_optc_bb.broadcast("ans_c", "bc_ans_c", None)
boc_snd = b_optc_bb.play_sound("snd_click", boc_bc)
b_optc_bb.hat_clicked(boc_snd, 50, 300)

boc_hvic = b_optc_bb.hide(None)
b_optc_bb.hat_broadcast("show_victory", "bc_show_victory", boc_hvic, 50, 440)

targets.append(create_sprite("BtnOptC", ["btn_opt_c"], b_optc_bb, ["snd_click"], x=0, y=-50, size=90, visible=False, layer=12))

# =========================================================================
# 12. QUIZ MASTER (Логика вопросов викторины с вложенными ветвлениями)
# =========================================================================
qm_bb = BlockBuilder()
qm_hide = qm_bb.hide(None)
qm_bb.hat_flag(qm_hide, 50, 50)

qm_miss = qm_bb.set_var("MissionText", "var_mission", "ВОПРОС 1: Награда астронома Фёдора Семёнова? [A] Демидовская премия [B] Нобелевская", None)
qm_q1 = qm_bb.set_var("QuestionNum", "var_question", 1, qm_miss)
qm_show = qm_bb.show(qm_q1)
qm_pos = qm_bb.goto_xy(0, 100, qm_show)
qm_bb.hat_broadcast("goto_hall_quiz", "bc_goto_hall_quiz", qm_pos, 50, 160)

# Nested branch on Correct Answer [A]:
# Q5 completion
q5_vic = qm_bb.broadcast("show_victory", "bc_show_victory", None)
q5_say = qm_bb.say_for("Блестяще! Город Курчатов и Курская АЭС! Викторина пройдена! (+10)", 2.5, q5_vic)
q5_sc = qm_bb.change_var("Score", "var_score", 10, q5_say)
q5_snd = qm_bb.play_sound("snd_correct", q5_sc)

# Q4 completion -> Q5
q4_say = qm_bb.say_for("Верно! Курская магнитная аномалия Лазарева! (+10)", 2.0, None)
q4_sc = qm_bb.change_var("Score", "var_score", 10, q4_say)
q4_snd = qm_bb.play_sound("snd_correct", q4_sc)
q4_miss = qm_bb.set_var("MissionText", "var_mission", "ВОПРОС 5: Город мирного атома Курской области? [A] г. Курчатов [B] г. Фатеж", q4_snd)
q4_next = qm_bb.set_var("QuestionNum", "var_question", 5, q4_miss)

# Q3 completion -> Q4
q3_say = qm_bb.say_for("Точно! Первая в мире ВЭС с вакуумным маховиком! (+10)", 2.0, None)
q3_sc = qm_bb.change_var("Score", "var_score", 10, q3_say)
q3_snd = qm_bb.play_sound("snd_correct", q3_sc)
q3_miss = qm_bb.set_var("MissionText", "var_mission", "ВОПРОС 4: Что исследовал академик П.П. Лазарев? [A] Руду КМА [B] Алмазы", q3_snd)
q3_next = qm_bb.set_var("QuestionNum", "var_question", 4, q3_miss)

# Q2 completion -> Q3
q2_say = qm_bb.say_for("Правильно! Уфимцев — родной внук астронома Семёнова! (+10)", 2.0, None)
q2_sc = qm_bb.change_var("Score", "var_score", 10, q2_say)
q2_snd = qm_bb.play_sound("snd_correct", q2_sc)
q2_miss = qm_bb.set_var("MissionText", "var_mission", "ВОПРОС 3: Главная инновация ВЭС Уфимцева 1931 г.? [A] Маховик в вакууме [B] Паровой котел", q2_snd)
q2_next = qm_bb.set_var("QuestionNum", "var_question", 3, q2_miss)

# Q1 completion -> Q2
q1_say = qm_bb.say_for("Верно! Золотая Демидовская премия 1858 года! (+10)", 2.0, None)
q1_sc = qm_bb.change_var("Score", "var_score", 10, q1_say)
q1_snd = qm_bb.play_sound("snd_correct", q1_sc)
q1_miss = qm_bb.set_var("MissionText", "var_mission", "ВОПРОС 2: Кем приходился Уфимцев Семёнову? [A] Родным внуком [B] Соседом", q1_snd)
q1_next = qm_bb.set_var("QuestionNum", "var_question", 2, q1_miss)

# Chain nested if-else statements for questions 1 to 5:
cond_q4 = qm_bb.op_equals_var("QuestionNum", "var_question", 4, None)
if_q4 = qm_bb.if_else(cond_q4, q4_next, q5_snd, None)

cond_q3 = qm_bb.op_equals_var("QuestionNum", "var_question", 3, None)
if_q3 = qm_bb.if_else(cond_q3, q3_next, if_q4, None)

cond_q2 = qm_bb.op_equals_var("QuestionNum", "var_question", 2, None)
if_q2 = qm_bb.if_else(cond_q2, q2_next, if_q3, None)

cond_q1 = qm_bb.op_equals_var("QuestionNum", "var_question", 1, None)
if_q1 = qm_bb.if_else(cond_q1, q1_next, if_q2, None)

qm_bb.hat_broadcast("ans_a", "bc_ans_a", if_q1, 50, 360)

# Wrong answers [B] and [C]:
w_say = qm_bb.say_for("Не совсем так! Вспомните историю первопроходцев!", 1.5, None)
w_sc = qm_bb.change_var("Score", "var_score", -2, w_say)
w_snd = qm_bb.play_sound("snd_wrong", w_sc)
qm_bb.hat_broadcast("ans_b", "bc_ans_b", w_snd, 50, 720)

w_say_c = qm_bb.say_for("Попробуйте другой вариант ответа!", 1.5, None)
w_sc_c = qm_bb.change_var("Score", "var_score", -2, w_say_c)
w_snd_c = qm_bb.play_sound("snd_wrong", w_sc_c)
qm_bb.hat_broadcast("ans_c", "bc_ans_c", w_snd_c, 50, 920)

qm_hvic = qm_bb.hide(None)
qm_bb.hat_broadcast("show_victory", "bc_show_victory", qm_hvic, 50, 1120)

targets.append(create_sprite(
    "QuizMaster",
    ["dialog_plate"],
    qm_bb,
    ["snd_correct", "snd_wrong"],
    x=0, y=100, size=95, visible=False, layer=11
))

# =========================================================================
# 13. FX (Золотая Медаль Демидова & Салют)
# =========================================================================
fx_bb = BlockBuilder()
fx_hide = fx_bb.hide(None)
fx_bb.hat_flag(fx_hide, 50, 50)

# Victory floating animation loop
fx_loop_dn = fx_bb.change_y(-1, None)
fx_w_dn = fx_bb.wait(0.06, fx_loop_dn)
fx_rep_dn = fx_bb.repeat(8, fx_w_dn, None)

fx_loop_up = fx_bb.change_y(1, None)
fx_w_up = fx_bb.wait(0.06, fx_loop_up)
fx_rep_up = fx_bb.repeat(8, fx_w_up, fx_rep_dn)

fx_forever = fx_bb.forever(fx_rep_up, None)

fx_snd = fx_bb.play_sound("snd_fanfare", fx_forever)
fx_size = fx_bb.set_size(130, fx_snd)
fx_show = fx_bb.show(fx_size)
fx_pos = fx_bb.goto_xy(0, 65, fx_show)
fx_cost = fx_bb.switch_costume("fx_medal", fx_pos)
fx_bb.hat_broadcast("show_victory", "bc_show_victory", fx_cost, 50, 160)

targets.append(create_sprite(
    "FX",
    ["fx_medal", "fx_spark"],
    fx_bb,
    ["snd_fanfare"],
    x=0, y=65, size=130, visible=False, layer=13
))

# Monitors
monitors = [
    {
        "id": "var_score",
        "mode": "default",
        "opcode": "data_variable",
        "params": {"VARIABLE": "Score"},
        "spriteName": None,
        "value": 0,
        "width": 0,
        "height": 0,
        "x": 8,
        "y": 8,
        "visible": True,
        "sliderMin": 0,
        "sliderMax": 100,
        "isDiscrete": True
    },
    {
        "id": "var_energy",
        "mode": "default",
        "opcode": "data_variable",
        "params": {"VARIABLE": "Energy"},
        "spriteName": None,
        "value": 0,
        "width": 0,
        "height": 0,
        "x": 8,
        "y": 38,
        "visible": True,
        "sliderMin": 0,
        "sliderMax": 100,
        "isDiscrete": True
    }
]

# Meta
meta = {
    "semver": "3.0.0",
    "vm": "0.2.0",
    "agent": "Mozilla/5.0 (X11; Linux x86_64) Scratch/3.0 IT-COPP Kursk Edition"
}

project_json = {
    "targets": targets,
    "monitors": monitors,
    "extensions": [],
    "meta": meta
}

# Write project.json to disk
with open(os.path.join(PROJECT_DIR, "project.json"), "w", encoding="utf-8") as f:
    json.dump(project_json, f, ensure_ascii=False, indent=2)

print("project.json successfully written!")
print(f"Total targets: {len(targets)}")

# Pack .sb3 file
sb3_out_path = "/home/dima/Projects/hackathon/kursk_heroes.sb3"
sb3_copy_path = "/home/dima/Projects/hackathon/kursk_pioneers_science.sb3"

for out_p in [sb3_out_path, sb3_copy_path]:
    with zipfile.ZipFile(out_p, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("project.json", json.dumps(project_json, ensure_ascii=False))
        for asset_key, item in manifest.items():
            fpath = os.path.join(ASSETS_DIR, item["md5ext"])
            z.write(fpath, arcname=item["md5ext"])
    print(f"Generated SB3: {out_p} ({os.path.getsize(out_p)} bytes)")

