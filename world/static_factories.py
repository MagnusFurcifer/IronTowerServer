def get_static_entity(id):
    if id == 1:
        tmp_entity = {
            "X"             :       8,
            "Y"             :       8,
            "CHAR"          :       "@",
            "COLOR"         :       libtcod.yellow,
            "NAME"          :       "Jeff",
            "BLOCKS"        :       True,
            "FIGHTER"       :       False,
            "STAIRS"        :       False,
            "DIALOG"        :       True,
            "DIALOG_LINE"   :       "Please take these items before heading into the tower."
        }
        return tmp_entity
    elif id == 2:
        tmp_entity = {
            "X"                 :       7,
            "Y"                 :       5,
            "CHAR"              :       "r",
            "COLOR"             :       libtcod.white,
            "NAME"              :       "Plain Ring",
            "BLOCKS"            :       False,
            "FIGHTER"           :       False,
            "STAIRS"            :       False,
            "EQUIPMENT"         :       True,
            "EQ_TYPE"           :       2, #weapon
            "EQ_STAT"           :       "HP",
            "EQ_STAT_CHANGE"    :       0,
            "DESCRIPTION"       :       "A normal ring"
        }
        return tmp_entity
    elif id == 3:
        tmp_entity = {
            "X"                 :       8,
            "Y"                 :       5,
            "CHAR"              :       "w",
            "COLOR"             :       libtcod.white,
            "NAME"              :       "Plain Sword",
            "BLOCKS"            :       False,
            "FIGHTER"           :       False,
            "STAIRS"            :       False,
            "EQUIPMENT"         :       True,
            "EQ_TYPE"           :       1, #weapon
            "EQ_STAT"           :       "ATTACK",
            "EQ_STAT_CHANGE"    :       0,
            "DESCRIPTION"       :       "A normal sword"
        }
        return tmp_entity
    elif id == 4:
        tmp_entity = {
            "X"                 :       9,
            "Y"                 :       5,
            "CHAR"              :       "n",
            "COLOR"             :       libtcod.white,
            "NAME"              :       "Plain Amulet",
            "BLOCKS"            :       False,
            "FIGHTER"           :       False,
            "STAIRS"            :       False,
            "EQUIPMENT"         :       True,
            "EQ_TYPE"           :       3, #weapon
            "EQ_STAT"           :       "HP",
            "EQ_STAT_CHANGE"    :       0,
            "DESCRIPTION"       :       "A normal amulet"

        }
        return tmp_entity
    elif id == 5:
        tmp_entity = {
            "X"                 :       10,
            "Y"                 :       5,
            "CHAR"              :       "a",
            "COLOR"             :       libtcod.white,
            "NAME"              :       "Plain Leather Cuirass",
            "BLOCKS"            :       False,
            "FIGHTER"           :       False,
            "STAIRS"            :       False,
            "EQUIPMENT"         :       True,
            "EQ_TYPE"           :       4, #weapon
            "EQ_STAT"           :       "DEFENSE",
            "EQ_STAT_CHANGE"    :       0,
            "DESCRIPTION"       :       "A normal leather armor peice"

        }
        return tmp_entity
    elif id == 6:
        tmp_entity = {
            "X"             :       6,
            "Y"             :       20,
            "CHAR"          :       "@",
            "COLOR"         :       libtcod.yellow,
            "NAME"          :       "Lizzy",
            "BLOCKS"        :       True,
            "FIGHTER"       :       False,
            "STAIRS"        :       False,
            "DIALOG"        :       True,
            "DIALOG_LINE"   :       "Be careful in the tower. Monsters turn red just before they attack!"
        }
        return tmp_entity
