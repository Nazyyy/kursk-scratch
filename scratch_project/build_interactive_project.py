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

# Global broadcasts
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

print("Configuring Stage & Sprites...")

# =========================================================================
# 0. STAGE
# =========================================================================
stage_bb = BlockBuilder()

# Green flag initialization
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
lv_miss = stage_bb.set_var("MissionText", "var_mission", "ТРИУМФ: Присвоение Инженерного Паспорта Первопроходца!", lv_snd)
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
    "layerOrder": 0,
    "tempo": 60,
    "videoTransparency": 50,
    "videoState": "on",
    "textToSpeechLanguage": None
})

# =========================================================================
# 1. HERO (Инженер-стажер IT-ЦОПП)
# =========================================================================
hero_bb = BlockBuilder()

h_hide = hero_bb.hide(None)
hero_bb.hat_flag(h_hide, 50, 50)

# start_intro:
h_i_bc = hero_bb.broadcast("goto_level1", "bc_goto_level1", None)
h_i_s2 = hero_bb.say_for("Архив чертежей поврежден! Исследуем открытия первопроходцев!", 2.5, h_i_bc)
h_i_s1 = hero_bb.say_for("Инженерный корпус IT-ЦОПП! Запуск модуля исторической верификации!", 2.5, h_i_s2)
h_i_show = hero_bb.show(h_i_s1)
h_i_pos = hero_bb.goto_xy(-140, -60, h_i_show)
h_i_cost = hero_bb.switch_costume("hero_copt", h_i_pos)
hero_bb.hat_broadcast("start_intro", "bc_start_intro", h_i_cost, 50, 160)

# goto_level1:
h_l1_say = hero_bb.say_for("Курск, 1853 год! Обсерватория астронома-самоучки Фёдора Семёнова!", 2.5, None)
h_l1_show = hero_bb.show(h_l1_say)
h_l1_pos = hero_bb.goto_xy(-140, -60, h_l1_show)
h_l1_cost = hero_bb.switch_costume("hero_astronomer", h_l1_pos)
hero_bb.hat_broadcast("goto_level1", "bc_goto_level1", h_l1_cost, 50, 360)

# goto_level2:
h_l2_say = hero_bb.say_for("1931 год, улица Семёновская! Мы у ветроэлектростанции Уфимцева!", 2.5, None)
h_l2_show = hero_bb.show(h_l2_say)
h_l2_pos = hero_bb.goto_xy(-140, -60, h_l2_show)
h_l2_cost = hero_bb.switch_costume("hero_aviator", h_l2_pos)
hero_bb.hat_broadcast("goto_level2", "bc_goto_level2", h_l2_cost, 50, 560)

# goto_level3:
h_l3_say = hero_bb.say_for("Бассейн Курской магнитной аномалии и энергоблок Курской АЭС!", 2.5, None)
h_l3_show = hero_bb.show(h_l3_say)
h_l3_pos = hero_bb.goto_xy(-140, -60, h_l3_show)
h_l3_cost = hero_bb.switch_costume("hero_physicist", h_l3_pos)
hero_bb.hat_broadcast("goto_level3", "bc_goto_level3", h_l3_cost, 50, 760)

# show_victory with deep nested evaluation
say_gold_max = hero_bb.say_for("Абсолютный триумф (95+ баллов)! Золотая Демидовская Медаль РАН с отличием!", 3.5, None)
say_gold = hero_bb.say_for("Блестящий результат! Звание «Академик Соловьиного Края»!", 3.5, None)
cond_gt_95 = hero_bb.op_gt_var("Score", "var_score", 94, None)
nested_gold = hero_bb.if_else(cond_gt_95, say_gold_max, say_gold, None)
set_award_gold = hero_bb.set_var("AwardName", "var_award", "Золотая Демидовская Медаль РАН", nested_gold)
set_stat_gold = hero_bb.set_var("StatusRank", "var_status", "Академик Соловьиного Края", set_award_gold)

say_silver = hero_bb.say_for("Отличная квалификация! Звание «Инженер-первопроходец Курска»!", 3.5, None)
set_award_silv = hero_bb.set_var("AwardName", "var_award", "Серебряный знак Уфимцева", say_silver)
set_stat_silv = hero_bb.set_var("StatusRank", "var_status", "Инженер-первопроходец Курска", set_award_silv)

say_bronze = hero_bb.say_for("Экспедиция пройдена! Звание «Стажер-испытатель IT-ЦОПП»!", 3.5, None)
set_award_brz = hero_bb.set_var("AwardName", "var_award", "Свидетельство исследователя", say_bronze)
set_stat_brz = hero_bb.set_var("StatusRank", "var_status", "Стажер-испытатель IT-ЦОПП", set_award_brz)

cond_gt_70 = hero_bb.op_gt_var("Score", "var_score", 69, None)
nested_lower = hero_bb.if_else(cond_gt_70, set_stat_silv, set_stat_brz, None)

cond_gt_85 = hero_bb.op_gt_var("Score", "var_score", 84, None)
main_branch = hero_bb.if_else(cond_gt_85, set_stat_gold, nested_lower, None)

h_v_sz = hero_bb.set_size(120, main_branch)
h_v_show = hero_bb.show(h_v_sz)
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
# 2. KURSIK (Геодезический модуль «Соловей-46»)
# =========================================================================
kursik_bb = BlockBuilder()

k_hide = kursik_bb.hide(None)
kursik_bb.hat_flag(k_hide, 50, 50)

# Continuous smooth hover animation loop
k_dy_dn = kursik_bb.change_y(-2, None)
k_w_dn = kursik_bb.wait(0.08, k_dy_dn)
k_rep_dn = kursik_bb.repeat(5, k_w_dn, None)

k_dy_up = kursik_bb.change_y(2, None)
k_w_up = kursik_bb.wait(0.08, k_dy_up)
k_rep_up = kursik_bb.repeat(5, k_w_up, k_rep_dn)

k_forever = kursik_bb.forever(k_rep_up, None)

k_show = kursik_bb.show(k_forever)
k_pos = kursik_bb.goto_xy(-70, 15, k_show)
k_cost = kursik_bb.switch_costume("kursik_hover", k_pos)
kursik_bb.hat_broadcast("start_intro", "bc_start_intro", k_cost, 50, 160)

# Level prompts
k_l1_c2 = kursik_bb.switch_costume("kursik_hover", None)
k_l1_say = kursik_bb.say_for("Стрелками клавиатуры наведите визир на координаты затмения!", 2.8, k_l1_c2)
k_l1_c1 = kursik_bb.switch_costume("kursik_scan", k_l1_say)
kursik_bb.hat_broadcast("start_level1_game", "bc_start_level1_game", k_l1_c1, 50, 360)

k_l2_c2 = kursik_bb.switch_costume("kursik_hover", None)
k_l2_say = kursik_bb.say_for("Следите за тахометром! Тормозите ротор в бурю и запускайте маховик в штиль!", 3.2, k_l2_c2)
k_l2_c1 = kursik_bb.switch_costume("kursik_talk", k_l2_say)
kursik_bb.hat_broadcast("start_level2_game", "bc_start_level2_game", k_l2_c1, 50, 540)

k_l3_c2 = kursik_bb.switch_costume("kursik_hover", None)
k_l3_say = kursik_bb.say_for("Перемещайте зонд по карьеру! Стрелка компаса укажет на пласт магнетита!", 3.2, k_l3_c2)
k_l3_c1 = kursik_bb.switch_costume("kursik_scan", k_l3_say)
kursik_bb.hat_broadcast("start_level3_game", "bc_start_level3_game", k_l3_c1, 50, 720)

k_v_say = kursik_bb.say_for("Телеметрия подтверждена! Научный прорыв Соловьиного края зафиксирован!", 3.5, None)
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

hf_hide = hist_bb.hide(None)
hist_bb.hat_flag(hf_hide, 50, 50)

# Semenov
hf_l1_bc = hist_bb.broadcast("start_level1_game", "bc_start_level1_game", None)
hf_l1_s3 = hist_bb.say_for("Сфокусируйте окуляр телескопа на Солнечное затмение!", 3.0, hf_l1_bc)
hf_l1_s2 = hist_bb.say_for("Я рассчитал затмения до 2001 года и получил Демидовскую премию Академии наук!", 3.2, hf_l1_s3)
hf_l1_s1 = hist_bb.say_for("Приветствую! Я курский купец и астроном-самоучка Фёдор Семёнов.", 3.0, hf_l1_s2)
hf_l1_show = hist_bb.show(hf_l1_s1)
hf_l1_pos = hist_bb.goto_xy(120, -60, hf_l1_show)
hf_l1_cost = hist_bb.switch_costume("char_semenov", hf_l1_pos)
hist_bb.hat_broadcast("goto_level1", "bc_goto_level1", hf_l1_cost, 50, 160)

# Ufimtsev
hf_l2_bc = hist_bb.broadcast("start_level2_game", "bc_start_level2_game", None)
hf_l2_s3 = hist_bb.say_for("Маховик весом 3.5 тонны в вакууме дает ток даже в полный штиль! Запустим агрегат!", 3.2, hf_l2_bc)
hf_l2_s2 = hist_bb.say_for("Я создал первую в мире ветростанцию с инерционным накопителем!", 3.0, hf_l2_s3)
hf_l2_s1 = hist_bb.say_for("Здравствуйте! Я изобретатель Анатолий Уфимцев, внук астронома Семёнова!", 3.0, hf_l2_s2)
hf_l2_show = hist_bb.show(hf_l2_s1)
hf_l2_pos = hist_bb.goto_xy(120, -60, hf_l2_show)
hf_l2_cost = hist_bb.switch_costume("char_ufimtsev", hf_l2_pos)
hist_bb.hat_broadcast("goto_level2", "bc_goto_level2", hf_l2_cost, 50, 420)

# Lazarev
hf_l3_bc = hist_bb.broadcast("start_level3_game", "bc_start_level3_game", None)
hf_l3_s3 = hist_bb.say_for("Найдите эпицентр залежи магнетита нашим геофизическим магнитометром!", 3.0, hf_l3_bc)
hf_l3_s2 = hist_bb.say_for("Экспедиция доказала: недра Курского края хранят 30 миллиардов тонн руды!", 3.2, hf_l3_s3)
hf_l3_s1 = hist_bb.say_for("Приветствую исследователей! Я академик Пётр Лазарев, руководитель экспедиции КМА.", 3.0, hf_l3_s2)
hf_l3_show = hist_bb.show(hf_l3_s1)
hf_l3_pos = hist_bb.goto_xy(120, -60, hf_l3_show)
hf_l3_cost = hist_bb.switch_costume("char_lazarev", hf_l3_pos)
hist_bb.hat_broadcast("goto_level3", "bc_goto_level3", hf_l3_cost, 50, 680)

# Hall of Fame
hf_h_say = hist_bb.say_for("В Зале Научной Славы подтвердите знания в итоговом инженерном экзамене!", 2.8, None)
hf_h_show = hist_bb.show(hf_h_say)
hf_h_pos = hist_bb.goto_xy(170, -60, hf_h_show)
hf_h_cost = hist_bb.switch_costume("char_semenov", hf_h_pos)
hist_bb.hat_broadcast("goto_hall_quiz", "bc_goto_hall_quiz", hf_h_cost, 50, 940)

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
# 4. TELESCOPE LENS (Интерактивный оптический прицел Семёнова)
# =========================================================================
# Target Eclipse is at (x: 80, y: 60).
# Player moves reticle with Arrow Keys!
lens_bb = BlockBuilder()

tl_hide = lens_bb.hide(None)
lens_bb.hat_flag(tl_hide, 50, 50)

# On start_level1_game:
# Set FocusDist = 60, pos (-40, 30), show
tl_cost1 = lens_bb.switch_costume("telescope_lens", None)
tl_set_foc = lens_bb.set_var("FocusDist", "var_focus", 60, tl_cost1)
tl_show = lens_bb.show(tl_set_foc)
tl_pos = lens_bb.goto_xy(-40, 30, tl_show)
lens_bb.hat_broadcast("start_level1_game", "bc_start_level1_game", tl_pos, 50, 160)

# Real Player Keyboard Arrow Controls:
# Right Arrow:
k_r_chg = lens_bb.change_var("FocusDist", "var_focus", -10, None)
k_r_snd = lens_bb.play_sound("snd_focus", k_r_chg)
k_r_dx = lens_bb.change_x(18, k_r_snd)
lens_bb.hat_key("right arrow", k_r_dx, 50, 340)

# Left Arrow:
k_l_chg = lens_bb.change_var("FocusDist", "var_focus", 10, None)
k_l_snd = lens_bb.play_sound("snd_focus", k_l_chg)
k_l_dx = lens_bb.change_x(-18, k_l_snd)
lens_bb.hat_key("left arrow", k_l_dx, 50, 480)

# Up Arrow:
k_u_chg = lens_bb.change_var("FocusDist", "var_focus", -10, None)
k_u_snd = lens_bb.play_sound("snd_focus", k_u_chg)
k_u_dy = lens_bb.change_y(15, k_u_snd)
lens_bb.hat_key("up arrow", k_u_dy, 50, 620)

# Down Arrow:
k_d_chg = lens_bb.change_var("FocusDist", "var_focus", 10, None)
k_d_snd = lens_bb.play_sound("snd_focus", k_d_chg)
k_d_dy = lens_bb.change_y(-15, k_d_snd)
lens_bb.hat_key("down arrow", k_d_dy, 50, 760)

# Lock focus check (via broadcast lock_focus from button or Space key):
# If FocusDist <= 20: Success! Else: Warning!
succ_bc = lens_bb.broadcast("level1_complete", "bc_level1_complete", None)
succ_say = lens_bb.say_for("Оптический фокус 100%! Затмение зафиксировано в таблицах Семёнова! (+30)", 3.0, succ_bc)
succ_sc = lens_bb.change_var("Score", "var_score", 30, succ_say)
succ_snd = lens_bb.play_sound("snd_correct", succ_sc)
succ_cost = lens_bb.switch_costume("telescope_lens_sharp", succ_snd)

fail_say = lens_bb.say_for("Расфокусировка! Наведите перекрестье точнее на центр затмения!", 1.8, None)
fail_snd = lens_bb.play_sound("snd_wrong", fail_say)

cond_foc_ok = lens_bb.op_lt_var("FocusDist", "var_focus", 25, None)
foc_branch = lens_bb.if_else(cond_foc_ok, succ_cost, fail_snd, None)
lens_bb.hat_broadcast("lock_focus", "bc_lock_focus", foc_branch, 50, 920)

# Also support Space key for lock
lens_bb.hat_key("space", foc_branch, 50, 1080)

# Hide after level 1 complete
tl_w_l2 = lens_bb.wait(1.5, None)
tl_bc_l2 = lens_bb.broadcast("goto_level2", "bc_goto_level2", tl_w_l2)
tl_h_done = lens_bb.hide(tl_bc_l2)
lens_bb.hat_broadcast("level1_complete", "bc_level1_complete", tl_h_done, 50, 1220)

targets.append(create_sprite(
    "TelescopeLens",
    ["telescope_lens", "telescope_lens_sharp"],
    lens_bb,
    ["snd_focus", "snd_correct", "snd_wrong"],
    x=-40, y=30, size=100, visible=False, layer=8
))

# =========================================================================
# 5. ECLIPSE TARGET (Солнечное затмение)
# =========================================================================
ecl_bb = BlockBuilder()

ecl_hide = ecl_bb.hide(None)
ecl_bb.hat_flag(ecl_hide, 50, 50)

ecl_show = ecl_bb.show(None)
ecl_pos = ecl_bb.goto_xy(80, 60, ecl_show)
ecl_bb.hat_broadcast("start_level1_game", "bc_start_level1_game", ecl_pos, 50, 160)

ecl_h2 = ecl_bb.hide(None)
ecl_bb.hat_broadcast("level1_complete", "bc_level1_complete", ecl_h2, 50, 320)

targets.append(create_sprite(
    "EclipseTarget",
    ["eclipse_target"],
    ecl_bb,
    [],
    x=80, y=60, size=100, visible=False, layer=7
))

# =========================================================================
# 6. WIND TURBINE (Симулятор ВЭС-1 Уфимцева с маховиком)
# =========================================================================
wind_bb = BlockBuilder()

wt_hide = wind_bb.hide(None)
wind_bb.hat_flag(wt_hide, 50, 50)

wt_show = wind_bb.show(None)
wt_pos = wind_bb.goto_xy(100, 70, wt_show)
wind_bb.hat_broadcast("goto_level2", "bc_goto_level2", wt_pos, 50, 160)

wt_h3 = wind_bb.hide(None)
wind_bb.hat_broadcast("goto_level3", "bc_goto_level3", wt_h3, 50, 320)

# Active dynamic simulation loop with deep nested branching!
# Storm with brake:
brk_msg = wind_bb.say_for("Тормоз защитил маховик от разрушения! Энергия запасена! (+5)", 1.2, None)
brk_rst = wind_bb.set_var("BrakeActive", "var_brake", 0, brk_msg)
brk_sc = wind_bb.change_var("Score", "var_score", 5, brk_rst)
brk_en = wind_bb.change_var("Energy", "var_energy", 16, brk_sc)

# Storm without brake:
ovr_msg = wind_bb.say_for("Шторм без тормоза! Аварийный сброс ротора!", 1.2, None)
ovr_sc = wind_bb.change_var("Score", "var_score", -3, ovr_msg)
ovr_en = wind_bb.change_var("Energy", "var_energy", -8, ovr_sc)

cond_brk = wind_bb.op_equals_var("BrakeActive", "var_brake", 1, None)
nested_storm = wind_bb.if_else(cond_brk, brk_en, ovr_en, None)

# Calm with flywheel discharge:
fly_msg1 = wind_bb.say_for("Штиль! Но вакуумный маховик Уфимцева питает фонари Курска! (+5)", 1.2, None)
fly_rst = wind_bb.set_var("FlywheelActive", "var_flywheel", 0, fly_msg1)
fly_sc = wind_bb.change_var("Score", "var_score", 5, fly_rst)
fly_en = wind_bb.change_var("Energy", "var_energy", 14, fly_sc)

# Calm without flywheel:
calm_msg2 = wind_bb.say_for("Штиль! Жмите [ВАКУУМНЫЙ МАХОВИК] для отдачи тока из инерции!", 1.2, None)
calm_en2 = wind_bb.change_var("Energy", "var_energy", 3, calm_msg2)

cond_fly = wind_bb.op_equals_var("FlywheelActive", "var_flywheel", 1, None)
nested_calm = wind_bb.if_else(cond_fly, fly_en, calm_en2, None)

# Optimal wind:
opt_msg = wind_bb.say_for("Оптимальный курский ветер! Генератор Уфимцева заряжает сеть! (+3)", 1.2, None)
opt_sc = wind_bb.change_var("Score", "var_score", 3, opt_msg)
opt_en = wind_bb.change_var("Energy", "var_energy", 12, opt_sc)

cond_is_calm = wind_bb.op_lt_var("WindSpeed", "var_wind", 25, None)
nested_calm_or_opt = wind_bb.if_else(cond_is_calm, nested_calm, opt_en, None)

cond_is_storm = wind_bb.op_gt_var("WindSpeed", "var_wind", 60, None)
sim_branch = wind_bb.if_else(cond_is_storm, nested_storm, nested_calm_or_opt, None)

# Wind variation cycle
rot_turn = wind_bb.turn_right(28, sim_branch)
sim_wait = wind_bb.wait(0.7, rot_turn)

# Loop completion
wt_bc_done = wind_bb.broadcast("level2_complete", "bc_level2_complete", None)
wt_say_win = wind_bb.say_for("100% энергии получено! Фонари улицы Семёновской зажглись! (+30)", 3.0, wt_bc_done)
wt_sc_win = wind_bb.change_var("Score", "var_score", 30, wt_say_win)
wt_snd_win = wind_bb.play_sound("snd_correct", wt_sc_win)

cond_en_100 = wind_bb.op_gt_var("Energy", "var_energy", 99, None)
wt_rep_loop = wind_bb.repeat_until(cond_en_100, sim_wait, wt_snd_win)

wt_init_en = wind_bb.set_var("Energy", "var_energy", 15, wt_rep_loop)
wind_bb.hat_broadcast("start_level2_game", "bc_start_level2_game", wt_init_en, 50, 480)

# Advance to Level 3
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
# Magnetite Target is at (x: 80, y: -50).
# Player moves probe across the quarry grid with Arrow keys or clicks!
mag_bb = BlockBuilder()

mg_hide = mag_bb.hide(None)
mag_bb.hat_flag(mg_hide, 50, 50)

# On start_level3_game:
mg_init_d = mag_bb.set_var("DistKMA", "var_distkma", 90, None)
mg_show = mag_bb.show(mg_init_d)
mg_pos = mag_bb.goto_xy(-70, 0, mg_show)
mag_bb.hat_broadcast("start_level3_game", "bc_start_level3_game", mg_pos, 50, 160)

# Keyboard controls for Magnetometer:
# Right:
m_r_chg = mag_bb.change_var("DistKMA", "var_distkma", -15, None)
m_r_snd = mag_bb.play_sound("snd_magnet", m_r_chg)
m_r_dx = mag_bb.change_x(25, m_r_snd)
mag_bb.hat_key("right arrow", m_r_dx, 50, 320)

# Left:
m_l_chg = mag_bb.change_var("DistKMA", "var_distkma", 15, None)
m_l_snd = mag_bb.play_sound("snd_magnet", m_l_chg)
m_l_dx = mag_bb.change_x(-25, m_l_snd)
mag_bb.hat_key("left arrow", m_l_dx, 50, 460)

# Down:
m_d_chg = mag_bb.change_var("DistKMA", "var_distkma", -15, None)
m_d_snd = mag_bb.play_sound("snd_magnet", m_d_chg)
m_d_dy = mag_bb.change_y(-15, m_d_snd)
mag_bb.hat_key("down arrow", m_d_dy, 50, 600)

# Up:
m_u_chg = mag_bb.change_var("DistKMA", "var_distkma", 15, None)
m_u_snd = mag_bb.play_sound("snd_magnet", m_u_chg)
m_u_dy = mag_bb.change_y(15, m_u_snd)
mag_bb.hat_key("up arrow", m_u_dy, 50, 740)

# Drill Core Action (broadcast drill_core from button or Space key)
drill_bc = mag_bb.broadcast("level3_complete", "bc_level3_complete", None)
drill_say = mag_bb.say_for("Керн магнетита извлечен! Энергоблоки Курской АЭС синхронизированы! (+30)", 3.0, drill_bc)
drill_sc = mag_bb.change_var("Score", "var_score", 30, drill_say)
drill_snd = mag_bb.play_sound("snd_correct", drill_sc)

drill_fail = mag_bb.say_for("Магнитная индукция слаба! Переместите зонд ближе к эпицентру стрелки!", 2.0, None)
drill_f_snd = mag_bb.play_sound("snd_wrong", drill_fail)

cond_kma_ok = mag_bb.op_lt_var("DistKMA", "var_distkma", 35, None)
drill_branch = mag_bb.if_else(cond_kma_ok, drill_snd, drill_f_snd, None)
mag_bb.hat_broadcast("drill_core", "bc_drill_core", drill_branch, 50, 900)

# Hide after level 3 complete
mg_w_q = mag_bb.wait(1.5, None)
mg_bc_q = mag_bb.broadcast("goto_hall_quiz", "bc_goto_hall_quiz", mg_w_q)
mg_h_done = mag_bb.hide(mg_bc_q)
mag_bb.hat_broadcast("level3_complete", "bc_level3_complete", mg_h_done, 50, 1080)

targets.append(create_sprite(
    "Magnetometer",
    ["magneto_sensor"],
    mag_bb,
    ["snd_magnet", "snd_correct", "snd_wrong"],
    x=-70, y=0, size=90, visible=False, layer=8
))

# =========================================================================
# 9. ORE VEIN (Пласт магнетита КМА)
# =========================================================================
ore_bb = BlockBuilder()
ore_hide = ore_bb.hide(None)
ore_bb.hat_flag(ore_hide, 50, 50)

ore_show = ore_bb.show(None)
ore_pos = ore_bb.goto_xy(80, -50, ore_show)
ore_bb.hat_broadcast("start_level3_game", "bc_start_level3_game", ore_pos, 50, 160)

ore_hq = ore_bb.hide(None)
ore_bb.hat_broadcast("goto_hall_quiz", "bc_goto_hall_quiz", ore_hq, 50, 320)

targets.append(create_sprite(
    "OreVein",
    ["ore_vein"],
    ore_bb,
    [],
    x=80, y=-50, size=100, visible=False, layer=6
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
# 11. BUTTONS (Liquid Glass Интерактивные органы управления)
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

br_say = b_rules_bb.say_for("Цель: настроить оптику Семёнова, сбалансировать ВЭС Уфимцева и найти пласт КМА Лазарева!", 4.0, None)
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

ba_say = b_auth_bb.say_for("«Архив Первопроходцев» • Разработано для регионального конкурса «IT-ЦОПП»", 4.0, None)
ba_snd = b_auth_bb.play_sound("snd_click", ba_say)
b_auth_bb.hat_clicked(ba_snd, 50, 180)

ba_h2 = b_auth_bb.hide(None)
b_auth_bb.hat_broadcast("start_intro", "bc_start_intro", ba_h2, 50, 360)

targets.append(create_sprite("BtnAuthors", ["btn_authors"], b_auth_bb, ["snd_click"], x=90, y=-75, size=95, visible=True, layer=12))

# BtnLockFocus (Level 1: Зафиксировать фокус)
b_lf_bb = BlockBuilder()
blf_hide = b_lf_bb.hide(None)
b_lf_bb.hat_flag(blf_hide, 50, 50)

blf_show = b_lf_bb.show(None)
blf_pos = b_lf_bb.goto_xy(0, -15, blf_show)
b_lf_bb.hat_broadcast("start_level1_game", "bc_start_level1_game", blf_pos, 50, 160)

blf_bc = b_lf_bb.broadcast("lock_focus", "bc_lock_focus", None)
blf_snd = b_lf_bb.play_sound("snd_click", blf_bc)
b_lf_bb.hat_clicked(blf_snd, 50, 300)

blf_h2 = b_lf_bb.hide(None)
b_lf_bb.hat_broadcast("level1_complete", "bc_level1_complete", blf_h2, 50, 440)

targets.append(create_sprite("BtnLockFocus", ["btn_lock_focus"], b_lf_bb, ["snd_click"], x=0, y=-15, size=95, visible=False, layer=12))

# BtnBrake (Level 2: Тормоз ротора)
b_brk_bb = BlockBuilder()
bb_hide = b_brk_bb.hide(None)
b_brk_bb.hat_flag(bb_hide, 50, 50)

bb_show = b_brk_bb.show(None)
bb_pos = b_brk_bb.goto_xy(-70, -15, bb_show)
b_brk_bb.hat_broadcast("start_level2_game", "bc_start_level2_game", bb_pos, 50, 160)

bb_h2 = b_brk_bb.hide(None)
b_brk_bb.hat_broadcast("level2_complete", "bc_level2_complete", bb_h2, 50, 300)

bb_say = b_brk_bb.say_for("Тормоз ротора включен!", 0.8, None)
bb_set = b_brk_bb.set_var("BrakeActive", "var_brake", 1, bb_say)
bb_snd = b_brk_bb.play_sound("snd_click", bb_set)
b_brk_bb.hat_clicked(bb_snd, 50, 420)

targets.append(create_sprite("BtnBrake", ["btn_brake"], b_brk_bb, ["snd_click"], x=-70, y=-15, size=95, visible=False, layer=12))

# BtnGear (Level 2: Вакуумный маховик)
b_gear_bb = BlockBuilder()
bg_hide = b_gear_bb.hide(None)
b_gear_bb.hat_flag(bg_hide, 50, 50)

bg_show = b_gear_bb.show(None)
bg_pos = b_gear_bb.goto_xy(70, -15, bg_show)
b_gear_bb.hat_broadcast("start_level2_game", "bc_start_level2_game", bg_pos, 50, 160)

bg_h2 = b_gear_bb.hide(None)
b_gear_bb.hat_broadcast("level2_complete", "bc_level2_complete", bg_h2, 50, 300)

bg_say = b_gear_bb.say_for("Инерция маховика отдана в сеть!", 0.8, None)
bg_set = b_gear_bb.set_var("FlywheelActive", "var_flywheel", 1, bg_say)
bg_snd = b_gear_bb.play_sound("snd_click", bg_set)
b_gear_bb.hat_clicked(bg_snd, 50, 420)

targets.append(create_sprite("BtnGear", ["btn_gear"], b_gear_bb, ["snd_click"], x=70, y=-15, size=95, visible=False, layer=12))

# BtnDrill (Level 3: Извлечь керн КМА)
b_dr_bb = BlockBuilder()
bdr_hide = b_dr_bb.hide(None)
b_dr_bb.hat_flag(bdr_hide, 50, 50)

bdr_show = b_dr_bb.show(None)
bdr_pos = b_dr_bb.goto_xy(0, -15, bdr_show)
b_dr_bb.hat_broadcast("start_level3_game", "bc_start_level3_game", bdr_pos, 50, 160)

bdr_bc = b_dr_bb.broadcast("drill_core", "bc_drill_core", None)
bdr_snd = b_dr_bb.play_sound("snd_click", bdr_bc)
b_dr_bb.hat_clicked(bdr_snd, 50, 300)

bdr_h2 = b_dr_bb.hide(None)
b_dr_bb.hat_broadcast("level3_complete", "bc_level3_complete", bdr_h2, 50, 440)

targets.append(create_sprite("BtnDrill", ["btn_drill"], b_dr_bb, ["snd_click"], x=0, y=-15, size=95, visible=False, layer=12))

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
# 12. QUIZ MASTER (Инженерная аттестация Зала Славы)
# =========================================================================
qm_bb = BlockBuilder()
qm_hide = qm_bb.hide(None)
qm_bb.hat_flag(qm_hide, 50, 50)

qm_miss = qm_bb.set_var("MissionText", "var_mission", "ВОПРОС 1: Награда Семёнова? [A] Демидовская премия РАН [B] Нобелевская премия", None)
qm_q1 = qm_bb.set_var("QuestionNum", "var_question", 1, qm_miss)
qm_show = qm_bb.show(qm_q1)
qm_pos = qm_bb.goto_xy(0, 100, qm_show)
qm_bb.hat_broadcast("goto_hall_quiz", "bc_goto_hall_quiz", qm_pos, 50, 160)

# Nested branch on Correct Answer [A]:
q5_vic = qm_bb.broadcast("show_victory", "bc_show_victory", None)
q5_say = qm_bb.say_for("Блестяще! Город Курчатов и реакторы ВВЭР-ТОИ! Экзамен завершен! (+10)", 2.5, q5_vic)
q5_sc = qm_bb.change_var("Score", "var_score", 10, q5_say)
q5_snd = qm_bb.play_sound("snd_correct", q5_sc)

q4_say = qm_bb.say_for("Верно! Комплексная экспедиция КМА академика Лазарева! (+10)", 2.0, None)
q4_sc = qm_bb.change_var("Score", "var_score", 10, q4_say)
q4_snd = qm_bb.play_sound("snd_correct", q4_sc)
q4_miss = qm_bb.set_var("MissionText", "var_mission", "ВОПРОС 5: Город мирного атома Курской области? [A] г. Курчатов [B] г. Фатеж", q4_snd)
q4_next = qm_bb.set_var("QuestionNum", "var_question", 5, q4_miss)

q3_say = qm_bb.say_for("Точно! Первая в мире ВЭС с инерционным маховиком в вакууме! (+10)", 2.0, None)
q3_sc = qm_bb.change_var("Score", "var_score", 10, q3_say)
q3_snd = qm_bb.play_sound("snd_correct", q3_sc)
q3_miss = qm_bb.set_var("MissionText", "var_mission", "ВОПРОС 4: Что открыл академик П.П. Лазарев в крае? [A] Руду КМА [B] Алмазы", q3_snd)
q3_next = qm_bb.set_var("QuestionNum", "var_question", 4, q3_miss)

q2_say = qm_bb.say_for("Правильно! Анатолий Уфимцев — родной внук астронома Семёнова! (+10)", 2.0, None)
q2_sc = qm_bb.change_var("Score", "var_score", 10, q2_say)
q2_snd = qm_bb.play_sound("snd_correct", q2_sc)
q2_miss = qm_bb.set_var("MissionText", "var_mission", "ВОПРОС 3: Главная инновация ВЭС Уфимцева 1931 г.? [A] Маховик в вакууме [B] Паровой котел", q2_snd)
q2_next = qm_bb.set_var("QuestionNum", "var_question", 3, q2_miss)

q1_say = qm_bb.say_for("Верно! Золотая Демидовская премия 1858 года за таблицы затмений! (+10)", 2.0, None)
q1_sc = qm_bb.change_var("Score", "var_score", 10, q1_say)
q1_snd = qm_bb.play_sound("snd_correct", q1_sc)
q1_miss = qm_bb.set_var("MissionText", "var_mission", "ВОПРОС 2: Кем приходился Уфимцев Семёнову? [A] Родным внуком [B] Соседом", q1_snd)
q1_next = qm_bb.set_var("QuestionNum", "var_question", 2, q1_miss)

cond_q4 = qm_bb.op_equals_var("QuestionNum", "var_question", 4, None)
if_q4 = qm_bb.if_else(cond_q4, q4_next, q5_snd, None)

cond_q3 = qm_bb.op_equals_var("QuestionNum", "var_question", 3, None)
if_q3 = qm_bb.if_else(cond_q3, q3_next, if_q4, None)

cond_q2 = qm_bb.op_equals_var("QuestionNum", "var_question", 2, None)
if_q2 = qm_bb.if_else(cond_q2, q2_next, if_q3, None)

cond_q1 = qm_bb.op_equals_var("QuestionNum", "var_question", 1, None)
if_q1 = qm_bb.if_else(cond_q1, q1_next, if_q2, None)

qm_bb.hat_broadcast("ans_a", "bc_ans_a", if_q1, 50, 360)

w_say = qm_bb.say_for("Неверно! Вспомните инженерную историю первопроходцев!", 1.5, None)
w_sc = qm_bb.change_var("Score", "var_score", -2, w_say)
w_snd = qm_bb.play_sound("snd_wrong", w_sc)
qm_bb.hat_broadcast("ans_b", "bc_ans_b", w_snd, 50, 720)

w_say_c = qm_bb.say_for("Ответ неверен! Изучите архивные данные!", 1.5, None)
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

fx_loop_dn = fx_bb.change_y(-1, None)
fx_w_dn = fx_bb.wait(0.06, fx_loop_dn)
fx_rep_dn = fx_bb.repeat(8, fx_w_dn, None)

fx_loop_up = fx_bb.change_y(1, None)
fx_w_up = fx_bb.wait(0.06, fx_loop_up)
fx_rep_up = fx_bb.repeat(8, fx_w_up, fx_rep_dn)

fx_forever = fx_bb.forever(fx_rep_up, None)

fx_snd = fx_bb.play_sound("snd_fanfare", fx_forever)
fx_sz = fx_bb.set_size(130, fx_snd)
fx_show = fx_bb.show(fx_sz)
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
    "agent": "Mozilla/5.0 Scratch/3.0 IT-COPP Liquid Glass Edition"
}

project_json = {
    "targets": targets,
    "monitors": monitors,
    "extensions": [],
    "meta": meta
}

with open(os.path.join(PROJECT_DIR, "project.json"), "w", encoding="utf-8") as f:
    json.dump(project_json, f, ensure_ascii=False, indent=2)

print("project.json written successfully!")
print(f"Total targets: {len(targets)}")

# Pack .sb3
sb3_out_path = "/home/dima/Projects/hackathon/kursk_heroes.sb3"
sb3_copy_path = "/home/dima/Projects/hackathon/kursk_pioneers_science.sb3"

for out_p in [sb3_out_path, sb3_copy_path]:
    with zipfile.ZipFile(out_p, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("project.json", json.dumps(project_json, ensure_ascii=False))
        for asset_key, item in manifest.items():
            fpath = os.path.join(ASSETS_DIR, item["md5ext"])
            z.write(fpath, arcname=item["md5ext"])
    print(f"Generated Liquid Glass SB3: {out_p} ({os.path.getsize(out_p)} bytes)")

