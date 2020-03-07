import libtcodpy as libtcod
import os

random_seed = "IRONTOWER"

screen_width = 80
screen_height = 50

# Size of the map
map_width = 80
map_height = 43

# Some variables for the rooms in the map
room_max_size = 7
room_min_size = 3
max_rooms = 60
max_spread = 5
max_monsters_per_room = 3

colors = {
    'dark_wall': libtcod.Color(0, 0, 100),
    'dark_ground': libtcod.Color(50, 50, 150),
    'light_wall': libtcod.Color(130, 110, 50),
    'light_ground': libtcod.Color(200, 180, 50)
}

ironserver_host = '0.0.0.0'  # The server's hostname or IP address
ironserver_port = 8080        # The port used by the server
ironweb_port = 8000 #Web server to display logs
ironweb_path = "./httpd/"
db_path = os.getcwd() + "/ironserver.db"
