import libtcodpy as libtcod
import random

class MonsterFactory:
    def __init__(self, type, level):
        self.type = type
        self.level = level

    def get_monster(x, y):
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

class EquipmentFactory:
    def __init__(self, type, level):
        self.type = type
        self.level = level

    def get_random_equipment(x, y):
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

        kit_adj = [blessed, shiny, dark, dirty, golden, smelly, steel, iron, wooden, glass, metal, slimey]
        kit_wp_noun = [sword, axe, mace, staff, dagger]
        kit_rn_noun = [ring, band]
        kit_am_noun = [amulet, necklace, chain, choker, pendant, locket]
        kit_ar_noun = [cuirass, plate armor, chainmail, leathers]
        kit_stats = ["ATTACK", "HP", "DEFENSE"]
        kit_types = [1, 2, 3, 4] #Sword, Ring, Amulet, Armor
        kit_type = random.choice(kit_types)
        tmp_entity.get("EQ_TYPE") = kit_type
        equipment_name = random.choice(kit_adj) + " "
        if kit_type ==  1:
            tmp_entity.get("EQ_STAT") = "ATTACK"
            equipment_name = equipment_name + random.choice(kit_wp_noun)
            tmp_entity.get("CHAR") = "w"
            tmp_entity.get("DESCRIPTION") = "A Weapon"
        if kit_type ==  2:
            tmp_entity.get("EQ_STAT") = random.choice(kit_stats)
            equipment_name = equipment_name + random.choice(kit_rn_noun)
            tmp_entity.get("CHAR") = "r"
            tmp_entity.get("DESCRIPTION") = "A Ring"
        if kit_type ==  3:
            tmp_entity.get("EQ_STAT") = random.choice(kit_stats)
            equipment_name = equipment_name + random.choice(kit_am_noun)
            tmp_entity.get("CHAR") = "n"
            tmp_entity.get("DESCRIPTION") = "A Amulet"
        if kit_type ==  4:
            tmp_entity.get("EQ_STAT") = random.choice(kit_stats)
            equipment_name = equipment_name + random.choice(kit_ar_noun)
            tmp_entity.get("CHAR") = "a"
            tmp_entity.get("DESCRIPTION") = "A Peice of Armor"

        equipment_name = equipment_name + " of " + tmp_entity.get("EQ_STAT").lower()

        return tmp_entity
