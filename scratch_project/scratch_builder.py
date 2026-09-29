import json
import uuid

def gen_id():
    return str(uuid.uuid4()).replace('-', '')[:20]

class BlockBuilder:
    def __init__(self):
        self.blocks = {}

    def hat_flag(self, next_block=None, x=100, y=100):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "event_whenflagclicked",
            "next": next_block,
            "parent": None,
            "inputs": {},
            "fields": {},
            "shadow": False,
            "topLevel": True,
            "x": x,
            "y": y
        }
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def hat_broadcast(self, broadcast_name, broadcast_id, next_block=None, x=100, y=100):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "event_whenbroadcastreceived",
            "next": next_block,
            "parent": None,
            "inputs": {},
            "fields": {
                "BROADCAST_OPTION": [broadcast_name, broadcast_id]
            },
            "shadow": False,
            "topLevel": True,
            "x": x,
            "y": y
        }
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def hat_clicked(self, next_block=None, x=100, y=100):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "event_whenthisspriteclicked",
            "next": next_block,
            "parent": None,
            "inputs": {},
            "fields": {},
            "shadow": False,
            "topLevel": True,
            "x": x,
            "y": y
        }
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def hat_key(self, key_name, next_block=None, x=100, y=100):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "event_whenkeypressed",
            "next": next_block,
            "parent": None,
            "inputs": {},
            "fields": {
                "KEY_OPTION": [key_name, None]
            },
            "shadow": False,
            "topLevel": True,
            "x": x,
            "y": y
        }
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def broadcast(self, broadcast_name, broadcast_id, next_block=None, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "event_broadcast",
            "next": next_block,
            "parent": parent,
            "inputs": {
                "BROADCAST_INPUT": [1, [11, broadcast_name, broadcast_id]]
            },
            "fields": {},
            "shadow": False,
            "topLevel": False
        }
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def wait(self, secs, next_block=None, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "control_wait",
            "next": next_block,
            "parent": parent,
            "inputs": {
                "DURATION": [1, [4, secs]]
            },
            "fields": {},
            "shadow": False,
            "topLevel": False
        }
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def say_for(self, message, secs, next_block=None, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "looks_sayforsecs",
            "next": next_block,
            "parent": parent,
            "inputs": {
                "MESSAGE": [1, [10, str(message)]],
                "SECS": [1, [4, secs]]
            },
            "fields": {},
            "shadow": False,
            "topLevel": False
        }
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def show(self, next_block=None, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "looks_show",
            "next": next_block,
            "parent": parent,
            "inputs": {},
            "fields": {},
            "shadow": False,
            "topLevel": False
        }
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def hide(self, next_block=None, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "looks_hide",
            "next": next_block,
            "parent": parent,
            "inputs": {},
            "fields": {},
            "shadow": False,
            "topLevel": False
        }
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def switch_costume(self, costume_name, next_block=None, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "looks_switchcostumeto",
            "next": next_block,
            "parent": parent,
            "inputs": {
                "COSTUME": [1, [10, costume_name]]
            },
            "fields": {},
            "shadow": False,
            "topLevel": False
        }
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def switch_backdrop(self, backdrop_name, next_block=None, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "looks_switchbackdropto",
            "next": next_block,
            "parent": parent,
            "inputs": {
                "BACKDROP": [1, [10, backdrop_name]]
            },
            "fields": {},
            "shadow": False,
            "topLevel": False
        }
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def goto_xy(self, x, y, next_block=None, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "motion_gotoxy",
            "next": next_block,
            "parent": parent,
            "inputs": {
                "X": [1, [4, x]],
                "Y": [1, [4, y]]
            },
            "fields": {},
            "shadow": False,
            "topLevel": False
        }
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def play_sound(self, sound_name, next_block=None, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "sound_play",
            "next": next_block,
            "parent": parent,
            "inputs": {
                "SOUND_MENU": [1, [10, sound_name]]
            },
            "fields": {},
            "shadow": False,
            "topLevel": False
        }
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def set_var(self, var_name, var_id, value, next_block=None, parent=None):
        bid = gen_id()
        val_prim = [4, value] if isinstance(value, (int, float)) else [10, str(value)]
        self.blocks[bid] = {
            "opcode": "data_setvariableto",
            "next": next_block,
            "parent": parent,
            "inputs": {
                "VALUE": [1, val_prim]
            },
            "fields": {
                "VARIABLE": [var_name, var_id]
            },
            "shadow": False,
            "topLevel": False
        }
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def change_var(self, var_name, var_id, delta, next_block=None, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "data_changevariableby",
            "next": next_block,
            "parent": parent,
            "inputs": {
                "VALUE": [1, [4, delta]]
            },
            "fields": {
                "VARIABLE": [var_name, var_id]
            },
            "shadow": False,
            "topLevel": False
        }
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def repeat(self, times, substack_head, next_block=None, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "control_repeat",
            "next": next_block,
            "parent": parent,
            "inputs": {
                "TIMES": [1, [6, times]],
                "SUBSTACK": [2, substack_head]
            },
            "fields": {},
            "shadow": False,
            "topLevel": False
        }
        if substack_head and substack_head in self.blocks:
            self.blocks[substack_head]["parent"] = bid
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def forever(self, substack_head, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "control_forever",
            "next": None,
            "parent": parent,
            "inputs": {
                "SUBSTACK": [2, substack_head]
            },
            "fields": {},
            "shadow": False,
            "topLevel": False
        }
        if substack_head and substack_head in self.blocks:
            self.blocks[substack_head]["parent"] = bid
        return bid

    def repeat_until(self, cond_id, substack_head, next_block=None, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "control_repeat_until",
            "next": next_block,
            "parent": parent,
            "inputs": {
                "CONDITION": [2, cond_id],
                "SUBSTACK": [2, substack_head]
            },
            "fields": {},
            "shadow": False,
            "topLevel": False
        }
        if cond_id and cond_id in self.blocks:
            self.blocks[cond_id]["parent"] = bid
        if substack_head and substack_head in self.blocks:
            self.blocks[substack_head]["parent"] = bid
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def if_then(self, cond_id, substack_head, next_block=None, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "control_if",
            "next": next_block,
            "parent": parent,
            "inputs": {
                "CONDITION": [2, cond_id],
                "SUBSTACK": [2, substack_head]
            },
            "fields": {},
            "shadow": False,
            "topLevel": False
        }
        if cond_id and cond_id in self.blocks:
            self.blocks[cond_id]["parent"] = bid
        if substack_head and substack_head in self.blocks:
            self.blocks[substack_head]["parent"] = bid
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def if_else(self, cond_id, substack1_head, substack2_head, next_block=None, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "control_if_else",
            "next": next_block,
            "parent": parent,
            "inputs": {
                "CONDITION": [2, cond_id],
                "SUBSTACK": [2, substack1_head],
                "SUBSTACK2": [2, substack2_head]
            },
            "fields": {},
            "shadow": False,
            "topLevel": False
        }
        if cond_id and cond_id in self.blocks:
            self.blocks[cond_id]["parent"] = bid
        if substack1_head and substack1_head in self.blocks:
            self.blocks[substack1_head]["parent"] = bid
        if substack2_head and substack2_head in self.blocks:
            self.blocks[substack2_head]["parent"] = bid
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def op_equals_var(self, var_name, var_id, target_val, parent=None):
        bid = gen_id()
        val_prim = [4, target_val] if isinstance(target_val, (int, float)) else [10, str(target_val)]
        self.blocks[bid] = {
            "opcode": "operator_equals",
            "next": None,
            "parent": parent,
            "inputs": {
                "OPERAND1": [3, [12, var_name, var_id], [10, ""]],
                "OPERAND2": [1, val_prim]
            },
            "fields": {},
            "shadow": False,
            "topLevel": False
        }
        return bid

    def op_gt_var(self, var_name, var_id, threshold, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "operator_gt",
            "next": None,
            "parent": parent,
            "inputs": {
                "OPERAND1": [3, [12, var_name, var_id], [10, ""]],
                "OPERAND2": [1, [4, threshold]]
            },
            "fields": {},
            "shadow": False,
            "topLevel": False
        }
        return bid

    def op_lt_var(self, var_name, var_id, threshold, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "operator_lt",
            "next": None,
            "parent": parent,
            "inputs": {
                "OPERAND1": [3, [12, var_name, var_id], [10, ""]],
                "OPERAND2": [1, [4, threshold]]
            },
            "fields": {},
            "shadow": False,
            "topLevel": False
        }
        return bid

    def turn_right(self, degrees, next_block=None, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "motion_turnright",
            "next": next_block,
            "parent": parent,
            "inputs": {
                "DEGREES": [1, [4, degrees]]
            },
            "fields": {},
            "shadow": False,
            "topLevel": False
        }
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def change_y(self, dy, next_block=None, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "motion_changeyby",
            "next": next_block,
            "parent": parent,
            "inputs": {
                "DY": [1, [4, dy]]
            },
            "fields": {},
            "shadow": False,
            "topLevel": False
        }
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def change_x(self, dx, next_block=None, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "motion_changexby",
            "next": next_block,
            "parent": parent,
            "inputs": {
                "DX": [1, [4, dx]]
            },
            "fields": {},
            "shadow": False,
            "topLevel": False
        }
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def set_size(self, pct, next_block=None, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "looks_setsizeto",
            "next": next_block,
            "parent": parent,
            "inputs": {
                "SIZE": [1, [4, pct]]
            },
            "fields": {},
            "shadow": False,
            "topLevel": False
        }
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def goto_front(self, next_block=None, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "looks_gotofrontback",
            "next": next_block,
            "parent": parent,
            "inputs": {},
            "fields": {
                "FRONT_BACK": ["front", None]
            },
            "shadow": False,
            "topLevel": False
        }
    def stop_other_scripts(self, next_block=None, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "control_stop",
            "next": next_block,
            "parent": parent,
            "inputs": {},
            "fields": {
                "STOP_OPTION": ["other scripts in sprite", None]
            },
            "mutation": {
                "tagName": "mutation",
                "children": [],
                "hasnext": "true"
            },
            "shadow": False,
            "topLevel": False
        }
        if next_block and next_block in self.blocks:
            self.blocks[next_block]["parent"] = bid
        return bid

    def stop_this_script(self, parent=None):
        bid = gen_id()
        self.blocks[bid] = {
            "opcode": "control_stop",
            "next": None,
            "parent": parent,
            "inputs": {},
            "fields": {
                "STOP_OPTION": ["this script", None]
            },
            "mutation": {
                "tagName": "mutation",
                "children": [],
                "hasnext": "false"
            },
            "shadow": False,
            "topLevel": False
        }
        return bid

print("BlockBuilder fully operational!")
