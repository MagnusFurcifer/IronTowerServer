import libtcodpy as libtcod

class MonsterGenerator:
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
