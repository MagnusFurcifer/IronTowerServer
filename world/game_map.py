import random
import it_config
from world.rectangle import Rect
from world.tile import Tile
from world.enums import EquipmentType
import libtcodpy as libtcod
from world.entity_factories import MonsterFactory, EquipmentFactory, NPCFactory
from world.static_factories import get_static_entity

class GameMap:
    def __init__(self, width, height, type, tiles, playerX, playerY):
        self.width = width
        self.height = height
        self.type = type
        self.tiles = tiles
        self.playerX = playerX
        self.playerY = playerY


class MapGenerator:
    def __init__(self, width, height, type, level):
        self.width = width
        self.height = height
        self.type = type
        self.level = level
        self.tiles = self.initialize_tiles()
        self.entities = []
        self.playerStartX = int(self.width / 2)
        self.playerStartY = int(self.height / 2)
        random.seed(it_config.random_seed)

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles

    def generate_map(self, max_rooms, room_min_size, room_max_size):
        if self.type == "DUNGEON":
            return self.gen_dungeon(max_rooms, room_min_size, room_max_size)
        elif self.type == "TOWN":
            return self.gen_town()

    def gen_town(self):

        #Move PC up a bit to the park
        self.playerStartY = self.playerStartY - 10
        self.playerStartX = self.playerStartX + 30

        self.tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]
        for x in range(self.width):
            self.tiles[x][0] = Tile(True)
            self.tiles[x][self.height - 1] = Tile(True)
        for y in range(self.height):
            self.tiles[0][y] = Tile(True)
            self.tiles[self.width - 1][y] = Tile(True)

        rooms = []

        #Item Shop
        new_room = Rect(3, 3, 10, 10)
        self.create_building(new_room, "bottom")
        rooms.append(new_room)
        self.entities.append(get_static_entity(1)) #Jeff the item man
        self.entities.append(get_static_entity(2)) #Plan Ring
        self.entities.append(get_static_entity(3)) #Plain Sword
        self.entities.append(get_static_entity(4)) #Plan Amulet
        self.entities.append(get_static_entity(5)) #Plain armor

        #Fighter Trainer
        new_room = Rect(3, 17, 6, 9)
        self.create_building(new_room, "top")
        rooms.append(new_room)
        self.entities.append(get_static_entity(6)) #Lizzy tells you about stuff


        new_room = Rect(16, 5, 12, 8)
        self.create_building(new_room, "bottom")
        rooms.append(new_room)
        self.entities.append(get_static_entity(7)) #So does John

        new_room = Rect(12, 17, 8, 14)
        self.create_building(new_room, "top")
        rooms.append(new_room)

        new_room = Rect(40, 10, 10, 10)
        self.create_building(new_room, "left")
        rooms.append(new_room)
        new_room = Rect(30, 20, 30, 20)
        self.create_building(new_room, "top")
        rooms.append(new_room)

        stairs_entity = {
            "X"             :       45,
            "Y"             :       30,
            "CHAR"          :       ">",
            "COLOR"         :       libtcod.white,
            "NAME"          :       "Stairs",
            "BLOCKS"        :       False,
            "STAIRS"        :       True,
            "STAIRS_TYPE"   :       "DUNGEON",
            "STAIRS_LEVEL"  :       1
            }
        self.entities.append(stairs_entity)
        map = self.encode_map()
        return map

    def gen_dungeon(self, max_rooms, room_min_size, room_max_size):

        max_monsters_per_room = 3
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # random width and height
            w = random.randint(room_min_size, room_max_size)
            h = random.randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = random.randint(0, self.width - w - 1)
            y = random.randint(0, self.height - h - 1)

            # "Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()
                center_last_room_x = new_x
                center_last_room_y = new_y

                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    self.playerStartX = new_x
                    self.playerStartY = new_y
                else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 0 or 1)
                    if random.randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                        # finally, append the new room to the list
                self.place_monsters(new_room, max_monsters_per_room)
                self.place_equipment(new_room, 1) #Place items
                rooms.append(new_room)
                num_rooms += 1

        stairs_entity = {
            "X"             :       center_last_room_x,
            "Y"             :       center_last_room_y,
            "CHAR"          :       ">",
            "COLOR"         :       libtcod.white,
            "NAME"          :       "Stairs",
            "BLOCKS"        :       False,
            "STAIRS"        :       True,
            "STAIRS_TYPE"   :       "DUNGEON",
            "STAIRS_LEVEL"  :       self.level + 1
            }
        self.entities.append(stairs_entity)
        map = self.encode_map()
        return map


    def place_equipment(self, room, max_kit):

        equipgen = EquipmentFactory(self.type, self.level)

        for i in range(max_kit):
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)
            if not any([entity for entity in self.entities if entity.get("X") == x and entity.get("Y") == y]):
                self.entities.append(equipgen.get_random_equipment(x, y))

    def place_monsters(self, room, max_monsters_per_room):
        # Get a random number of monsters
        number_of_monsters = random.randint(0, max_monsters_per_room)

        mongen = MonsterFactory(self.type, self.level)

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in self.entities if entity.get("X") == x and entity.get("Y") == y]):
                manster = mongen.get_monster(x, y)
                print(manster)
                self.entities.append(manster)

    def encode_map(self):
        map = {
            "COMMAND"   :   "MAPDATA",
            "WIDTH"     :   self.width,
            "HEIGHT"    :   self.height,
            "TYPE"      :   self.type,
            "ENTITIES"  :   self.entities,
            "PLAYERX"   :   self.playerStartX,
            "PLAYERY"   :   self.playerStartY
            }

        for x in range(self.width):
            map['TR_' + str(x)] = []
            for y in range(self.height):
                if self.tiles[x][y].blocked:
                    map['TR_' + str(x)].append(0)
                else:
                    map['TR_' + str(x)].append(1)

        return map

    def create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_building(self, room, door_dir):
        #Walls
        for x in range(room.x1, room.x2 + 1):
            self.tiles[x][room.y1].blocked = True
            self.tiles[x][room.y1].block_sight = True
            self.tiles[x][room.y2].blocked = True
            self.tiles[x][room.y2].block_sight = True
        for y in range(room.y1, room.y2):
            self.tiles[room.x1][y].blocked = True
            self.tiles[room.x1][y].block_sight = True
            self.tiles[room.x2][y].blocked = True
            self.tiles[room.x2][y].block_sight = True
        #Door
        if door_dir == "bottom":
            self.tiles[room.x1 + int((room.x2 - room.x1) / 2)][room.y2].blocked = False
            self.tiles[room.x1 + int((room.x2 - room.x1) / 2)][room.y2].block_sight = False
        if door_dir == "top":
            self.tiles[room.x1 + int((room.x2 - room.x1) / 2)][room.y1].blocked = False
            self.tiles[room.x1 + int((room.x2 - room.x1) / 2)][room.y1].block_sight = False
        if door_dir == "left":
            self.tiles[room.x1][room.y1 + int((room.y2 - room.y1) / 2)].blocked = False
            self.tiles[room.x1][room.y1 + int((room.y2 - room.y1) / 2)].block_sight = False
        if door_dir == "right":
            self.tiles[room.x2][room.y1 + int((room.y2 - room.y1) / 2)].blocked = False
            self.tiles[room.x2][room.y1 + int((room.y2 - room.y1) / 2)].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
