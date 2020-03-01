import libtcodpy as libtcod

screen_width = 80
screen_height = 50

# Size of the map
map_width = 80
map_height = 43

# Some variables for the rooms in the map
room_max_size = 10
room_min_size = 6
max_rooms = 30

fov_algorithm = 0
fov_light_walls = True
fov_radius = 10

colors = {
    'dark_wall': libtcod.Color(0, 0, 100),
    'dark_ground': libtcod.Color(50, 50, 150),
    'light_wall': libtcod.Color(130, 110, 50),
    'light_ground': libtcod.Color(200, 180, 50)
}

ironserver_host = '127.0.0.1'  # The server's hostname or IP address
ironserver_port = 8080        # The port used by the server
