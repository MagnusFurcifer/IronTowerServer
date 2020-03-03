import libtcodpy as libtcod

screen_width = 80
screen_height = 50

# Size of the map
map_width = 80
map_height = 43
bar_width = 20
panel_height = 7
panel_y = screen_height - panel_height

fov_algorithm = 0
fov_light_walls = True
fov_radius = 10

colors = {
    'dark_wall': libtcod.Color(0, 0, 100),
    'dark_ground': libtcod.Color(50, 50, 150),
    'light_wall': libtcod.Color(130, 110, 50),
    'light_ground': libtcod.Color(200, 180, 50)
}

ironserver_host = 'magbox.australiaeast.cloudapp.azure.com'  # The server's hostname or IP address
ironserver_port = 8080        # The port used by the server
