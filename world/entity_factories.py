import libtcodpy as libtcod
import random
import it_config

class NPCFactory:
    def __init__(self, type, level):
        self.type = type
        self.level = level
        random.seed(it_config.random_seed)

    def get_monster(self, x, y):
        monster_types = ["GOB", "ZOM", "MUSH"]
        tmp_entity = {
                    "X"             :       x,
                    "Y"             :       y,
                    "CHAR"          :       "G",
                    "COLOR"         :       libtcod.green,
                    "NAME"          :       "Goblin",
                    "BLOCKS"        :       True,
                    "FIGHTER"       :       True,
                    "FIGHTER_HP"    :       2,
                    "FIGHTER_DEF"   :       0,
                    "FIGHTER_ATK" :       1,
                    "AI"            :       True,
                    "AI_PACKAGE"    :       "Chase"
                    }
        return tmp_entity



class MonsterFactory:
    def __init__(self, type, level):
        self.type = type
        self.level = level
        random.seed(it_config.random_seed)

    def get_monster(self, x, y):
        monster_types = ["GOB", "ZOM", "MUSH", "KOB"]
        tmp_entity = {
                    "X"             :       x,
                    "Y"             :       y,
                    "CHAR"          :       "G",
                    "COLOR"         :       libtcod.green,
                    "NAME"          :       "Goblin",
                    "BLOCKS"        :       True,
                    "FIGHTER"       :       True,
                    "FIGHTER_HP"    :       2,
                    "FIGHTER_DEF"   :       0,
                    "FIGHTER_ATK" :       1,
                    "AI"            :       True,
                    "AI_PACKAGE"    :       "Chase"
                    }
        mon_type = random.choice(monster_types)
        if mon_type == "GOB":
            print("Goblin")
            tmp_entity["NAME"] = "Goblin"
            tmp_entity["AI_PACKAGE"] = "Chase"
            tmp_entity["CHAR"] = "G"
        elif mon_type == "ZOM":
            print("Zom")
            tmp_entity["NAME"] = "Zombie"
            tmp_entity["AI_PACKAGE"] = "Bounce"
            tmp_entity["CHAR"] = "Z"
        elif mon_type == "MUSH":
            print("Mush")
            tmp_entity["NAME"] = "Mushroom"
            tmp_entity["AI_PACKAGE"] = "Static"
            tmp_entity["CHAR"] = "M"
        elif mon_type == "KOB":
            print("Mush")
            tmp_entity["NAME"] = "Kobold"
            tmp_entity["AI_PACKAGE"] = "LongRNGBounce"
            tmp_entity["CHAR"] = "K"
        return tmp_entity

class ItemFactory():
    def __init__(self, type, level):
        self.type = type
        self.level = level
        random.seed(it_config.random_seed)


    def get_random_item(self, x, y):
        tmp_entity = {
                    "X"                 :       x,
                    "Y"                 :       y,
                    "CHAR"              :       "!",
                    "COLOR"             :       libtcod.purple,
                    "NAME"              :       "Potion",
                    "BLOCKS"            :       False,
                    "FIGHTER"           :       False,
                    "STAIRS"            :       False,
                    "ITEM"              :       True,
                    "IT_TYPE"           :       "POTION", #weapon
                    "IT_STAT"           :       "HP",
                    "IT_STAT_CHANGE"    :       random.randint(1, 1 + int(self.level * .3)),
                    "DESCRIPTION"       :       "A potion of health"
                    }
        if random.randint(0, 100) < 5: #5% chance for a stat potion
            tmp_entity["IT_STAT"] = random.choice(["ATTACK", "DEFENSE", "MAXHP"])
            tmp_entity["IT_STAT_CHANGE"] = random.randint(0, self.level)
            tmp_entity["NAME"] = "Stat Potion"
            tmp_entity["DESCRIPTION"] = "Permantley raise " + tmp_entity["IT_STAT"] + " by " + str(tmp_entity["IT_STAT_CHANGE"])

        return tmp_entity

class EquipmentFactory:
    def __init__(self, type, level):
        self.type = type
        self.level = level
        random.seed(it_config.random_seed)

    def get_random_equipment(self, x, y):
        tmp_entity = {
                    "X"                 :       x,
                    "Y"                 :       y,
                    "CHAR"              :       "s",
                    "COLOR"             :       libtcod.white,
                    "NAME"              :       "Plain Sword",
                    "BLOCKS"            :       False,
                    "FIGHTER"           :       False,
                    "STAIRS"            :       False,
                    "EQUIPMENT"         :       True,
                    "EQ_TYPE"           :       1, #weapon
                    "EQ_STAT"           :       "ATTACK",
                    "EQ_STAT_CHANGE"    :       0,
                    "DESCRIPTION"       :       "A normal Sword"
                    }

        kit_adj = ['blessed', 'shiny', 'dark', 'dirty', 'golden', 'smelly', 'steel', 'iron', 'wooden', 'glass', 'metal', 'slimey']
        kit_wp_noun = ['sword', 'axe', 'mace', 'staff', 'dagger']
        kit_rn_noun = ['ring', 'band']
        kit_am_noun = ['amulet', 'necklace', 'chain', 'choker', 'pendant', 'locket']
        kit_ar_noun = ['cuirass', 'plate armor', 'chainmail', 'leathers']
        kit_stats = ["ATTACK", "HP", "DEFENSE"]
        kit_types = [1, 2, 3, 4] #Sword, Ring, Amulet, Armor
        kit_type = random.choice(kit_types)
        tmp_entity["EQ_TYPE"]= kit_type
        equipment_name = random.choice(kit_adj) + " "
        if kit_type ==  1:
            tmp_entity["EQ_STAT"] = "ATTACK"
            equipment_name = equipment_name + random.choice(kit_wp_noun)
            tmp_entity["CHAR"] = "w"
            tmp_entity["DESCRIPTION"] = "A Weapon"
        if kit_type ==  2:
            tmp_entity["EQ_STAT"] = random.choice(kit_stats)
            equipment_name = equipment_name + random.choice(kit_rn_noun)
            tmp_entity["CHAR"] = "r"
            tmp_entity["DESCRIPTION"] = "A Ring"
        if kit_type ==  3:
            tmp_entity["EQ_STAT"] = random.choice(kit_stats)
            equipment_name = equipment_name + random.choice(kit_am_noun)
            tmp_entity["CHAR"] = "n"
            tmp_entity["DESCRIPTION"] = "A Amulet"
        if kit_type ==  4:
            tmp_entity["EQ_STAT"] = random.choice(kit_stats)
            equipment_name = equipment_name + random.choice(kit_ar_noun)
            tmp_entity["CHAR"] = "a"
            tmp_entity["DESCRIPTION"] = "A Peice of Armor"

        tmp_entity["EQ_STAT_CHANGE"] = random.randint(0, int(self.level * 1.5))
        equipment_name = equipment_name + " of " + tmp_entity["EQ_STAT"].lower() + " + " + str(tmp_entity["EQ_STAT_CHANGE"])
        tmp_entity['NAME'] = equipment_name
        return tmp_entity
