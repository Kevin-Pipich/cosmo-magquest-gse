"""
This module hides a secret surprise!
"""

import customtkinter as ctk
import numpy as np
from tkinter import NORMAL, DISABLED
from random import choice, choices

def easter_egg(self):
    """
    Every good program has an Easter egg :) (I know this game is buggy, I did it in a day. This was not my main goal.
    Im sorry)
    """
    # Hi, I'm Kevin. I wrote all this code back in the summer of 2022. If you are still using this code... thanks but
    # honestly why would you, I was just an undergrad when I made this program, and I had no idea what I was doing.
    # I hope you enjoy the Easter egg and think the program is pretty good. Thanks for checking it out!
    global player_keys
    global player_gold

    global player_health
    global player_stamina
    global player_agility
    global player_strength

    global player_kills
    global player_deaths

    # ============ initialize_player ============
    player_keys = 0
    player_gold = 0

    player_health = 100
    player_stamina = 50
    player_agility = 50
    player_strength = 50

    player_kills = 0
    player_deaths = 0

    player_inventory = [" ", " ", " ", " "]

    def close_display():
        game_window.destroy()
        self.play_game.state = NORMAL

    def generate_map():
        places = []
        castle_row = np.random.randint(1, 16)
        castle_col = np.random.randint(1, 29)

        castle = ctk.CTkLabel(master=map_frame,
                              text_font=("kanit", -30),
                              text_color="red",
                              text="🏰")
        castle.grid(row=castle_row, rowspan=2, column=castle_col, columnspan=2)

        places.append([castle_row, castle_col])
        places.append([castle_row, castle_col + 1])
        places.append([castle_row + 1, castle_col])
        places.append([castle_row + 1, castle_col + 1])

        num_bosses = np.random.randint(3, 6)

        choose = []
        for i in range(0, num_bosses):
            for x in range(1, 18):
                for y in range(1, 30):
                    if [x, y] not in places:
                        choose.append([x, y])

            boss_place = choice(choose)

            boss = ctk.CTkLabel(master=map_frame,
                                text_font=("kanit", -10),
                                text_color="black",
                                text="💀")
            boss.grid(row=boss_place[0], column=boss_place[1])

            places.append(boss_place)

        num_caves = np.random.randint(7, 15)
        choose = []
        for i in range(0, num_caves):
            for x in range(1, 18):
                for y in range(1, 30):
                    if [x, y] not in places:
                        choose.append([x, y])

            cave_place = choice(choose)

            cave = ctk.CTkLabel(master=map_frame,
                                text_font=("kanit", -15),
                                text_color="dimgrey",
                                text="🏔")
            cave.grid(row=cave_place[0], column=cave_place[1])

            places.append(cave_place)

        choose = []
        for x in range(1, 18):
            for y in range(1, 30):
                if [x, y] not in places:
                    choose.append([x, y])

        store_place = choice(choose)

        store = ctk.CTkLabel(master=map_frame,
                             text_font=("kanit", -15),
                             text_color="fuchsia",
                             text="🏪")
        store.grid(row=store_place[0], column=store_place[1])

        places.append(store_place)

        choose = []
        for x in range(1, 18):
            for y in range(1, 30):
                if [x, y] not in places:
                    choose.append([x, y])

        player_place = choice(choose)

        global player
        player = ctk.CTkLabel(master=map_frame,
                              text_font=("kanit", -15),
                              text_color="goldenrod",
                              text="👑")
        player.grid(row=player_place[0], column=player_place[1])

        return places, num_bosses, player_place

    def update_stats():
        global player_health
        global player_stamina
        global player_agility
        global player_strength

        global player_kills
        global player_deaths
        global player_keys

        player_health = 100
        player_stamina = 50
        player_agility = 50
        player_strength = 50

        for i in range(0, len(player_inventory)):
            match player_inventory[i]:
                case "🔫":
                    player_strength += 25
                    player_stamina += 10
                case "⚔":
                    player_strength += 20
                    player_agility += 10
                case "🏹":
                    player_strength += 10
                    player_agility += 10
                case "⛏":
                    player_strength += 15
                case "💎":
                    player_stamina += 10
                    player_agility += 10
                    player_stamina += 10
                    player_health += 10
                case "♥":
                    player_health += 25
                case "★":
                    player_stamina += 20
                case _:
                    pass

        player_gold_label.configure(text=str(player_gold))

        player_health_label.configure(text=str(player_health))
        player_stamina_label.configure(text=str(player_stamina))
        player_agility_label.configure(text=str(player_agility))
        player_strength_label.configure(text=str(player_strength))

        player_kills_label.configure(text=str(player_kills))
        player_deaths_label.configure(text=str(player_deaths))
        player_keys_label.configure(text=str(player_keys))

        item_1.configure(text=player_inventory[0])
        item_2.configure(text=player_inventory[1])
        item_3.configure(text=player_inventory[2])
        item_4.configure(text=player_inventory[3])

    def update_player_health():
        global player_health

        if player_health < 0:
            player_health = 0

        player_health_label.configure(text=str(player_health))

    def player_died():
        global player_deaths
        player_deaths += 1
        choose = []
        for x in range(1, 18):
            for y in range(1, 30):
                if [x, y] not in poi:
                    choose.append([x, y])

        player_inventory[0] = " "
        player_inventory[1] = " "
        player_inventory[2] = " "
        player_inventory[3] = " "

        update_stats()
        new_location = choice(choose)
        move(4, new_location)

    def boss_killed():
        global player_kills
        global player_keys

        player_keys += 1
        player_kills += 1
        update_stats()

    def fight_boss():
        global player_keys
        global player_gold

        global player_health
        global player_stamina
        global player_agility
        global player_strength

        global player_kills
        global player_deaths

        global boss_health

        def attack(boss_strength, boss_stamina, boss_agility):
            global player_health
            global boss_health
            global boss_move
            if boss_move == 0:
                if np.random.rand(1)[0] < int(boss_agility / 150):
                    live_updates.configure(text="Boss has dodged your attack!!!")
                else:
                    damage = int(player_strength * np.random.randint(50, 101) / 100 -
                                 (0.5 * boss_stamina) + (0.2 * boss_agility))
                    if damage < 10:
                        damage = np.random.randint(3, 16)
                    live_updates.configure(text="Boss attempted to dodged your attack but failed!!!\n"
                                                "You have inflicted " + str(damage) + " damage!")
                    boss_health -= damage
            elif boss_move == 1:
                damage_to_player = int(boss_strength * np.random.randint(50, 101) / 100 -
                                       (0.5 * player_stamina) + (0.2 * player_agility))
                damage_to_boss = int(player_strength * np.random.randint(50, 101) / 100 -
                                     (0.5 * boss_stamina) + (0.2 * boss_agility))
                if damage_to_boss < 10:
                    damage_to_boss = np.random.randint(3, 16)
                live_updates.configure(text="Both you and the boss have attacked one another!!!\n"
                                            "You have taken " + str(damage_to_player) + " damage!\n"
                                                                                        "You dealt " + str(
                    damage_to_boss) + " damage!")
                player_health -= damage_to_player
                boss_health -= damage_to_boss
                update_player_health()
            boss_turn()

        def dodge(boss_strength, boss_stamina, boss_agility):
            global player_health
            global boss_health
            global boss_move
            if boss_move == 0:
                live_updates.configure(text="Both you and the boss have dodged!!!\n"
                                            "No damage has been dealt.")
            elif boss_move == 1:
                if np.random.rand(1)[0] < int(player_agility / 70):
                    live_updates.configure(text="You dodged the boss attack!!!")
                else:
                    damage = int(boss_strength * np.random.randint(50, 101) / 100 -
                                 (0.5 * player_stamina) + (0.2 * player_agility))
                    live_updates.configure(text="You attempted to dodge the boss attack but failed!!!\n"
                                                "The boss has inflicted " + str(damage) + " damage!")
                    player_health -= damage
                    update_player_health()
            boss_turn()

        def boss_turn():
            global boss_move
            global player_inventory
            boss_health_bar.set(boss_health / max_health)
            if boss_health <= 0:
                attack_button.state = DISABLED
                dodge_button.state = DISABLED
                live_updates.configure(text="You have defeated the boss!!! You have been fully healed!")
                boss_killed()
                for i in range(0, len(boss_positions)):
                    if boss_positions[i] == player_location:
                        boss_positions[i] = [100, 100]
            elif player_health <= 0:
                attack_button.state = DISABLED
                dodge_button.state = DISABLED
                live_updates.configure(text="The boss has defeated you!!!\n You will now respawn, "
                                            "all items have been lost!")
                player_died()
            else:
                boss_move = np.random.randint(0, 2)
                attack_button.state = NORMAL
                dodge_button.state = NORMAL

        boss_display = ctk.CTkToplevel(game_window)
        boss_display.geometry("400x400")
        boss_display.title("Boss Fight!")
        boss_display.resizable(False, False)

        boss_display.columnconfigure((0, 1, 2), weight=1)
        boss_display.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        boss_health = np.random.randint(100, 326)

        max_health = boss_health

        boss_strength = np.random.randint(50, 201)

        boss_agility = np.random.randint(50, 151)

        boss_stamina = np.random.randint(50, 151)

        boss_health_label = ctk.CTkLabel(master=boss_display, text="Boss Health: ")
        boss_health_label.grid(row=0, column=0)

        boss_health_bar = ctk.CTkProgressBar(master=boss_display)
        boss_health_bar.grid(row=0, column=1, columnspan=2)

        boss_health_bar.set(boss_health / max_health)

        boss_image = ctk.CTkLabel(master=boss_display,
                                  text="💀",
                                  text_font=("kanit", -50),
                                  fg_color=("gray75", "gray30"))
        boss_image.grid(row=1, column=0, columnspan=3, rowspan=3, sticky="nsew", padx=40, pady=40)

        live_updates = ctk.CTkLabel(master=boss_display,
                                    text="Boss has made their move! What will you do?")
        live_updates.grid(row=4, column=0, columnspan=3)

        attack_button = ctk.CTkButton(master=boss_display,
                                      text="Attack",
                                      command=lambda: attack(boss_strength, boss_stamina, boss_agility))
        attack_button.grid(row=5, column=0, padx=5, pady=5)

        dodge_button = ctk.CTkButton(master=boss_display,
                                     text="Dodge",
                                     command=lambda: dodge(boss_strength, boss_stamina, boss_agility))
        dodge_button.grid(row=5, column=2, padx=5, pady=5)

        attack_button.state = DISABLED
        dodge_button.state = DISABLED

        boss_turn()

    def enter_cave():

        global player_gold

        def add_item(item):
            cave_item_1.state = DISABLED
            cave_item_2.state = DISABLED
            cave_item_3.state = DISABLED
            cave_item_4.state = DISABLED

            def replace_item(idx):
                player_inventory[idx] = item

                item_1.configure(text=player_inventory[0])
                item_2.configure(text=player_inventory[1])
                item_3.configure(text=player_inventory[2])
                item_4.configure(text=player_inventory[3])

                inventory_display.destroy()

                update_stats()

            counter = 0
            for i in range(0, len(player_inventory)):
                if player_inventory[i] == " ":
                    player_inventory[i] = item
                    break
                else:
                    counter += 1

            if counter == len(player_inventory):
                inventory_display = ctk.CTkToplevel(game_window)
                inventory_display.geometry("350x300")
                inventory_display.title("Player Inventory")
                inventory_display.resizable(False, False)

                inv_label = ctk.CTkLabel(master=inventory_display,
                                         text="Replace an Item in Inventory",
                                         fg_color=("gray75", "gray30"))
                inv_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

                # make 4 frames for each cave item
                inv_item_1 = ctk.CTkButton(master=inventory_display,
                                           text=player_inventory[0],
                                           fg_color=("gray75", "gray30"),
                                           command=lambda: replace_item(0))
                inv_item_1.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

                inv_item_2 = ctk.CTkButton(master=inventory_display,
                                           text=player_inventory[1],
                                           fg_color=("gray75", "gray30"),
                                           command=lambda: replace_item(1))
                inv_item_2.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

                inv_item_3 = ctk.CTkButton(master=inventory_display,
                                           text=player_inventory[2],
                                           fg_color=("gray75", "gray30"),
                                           command=lambda: replace_item(2))
                inv_item_3.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

                inv_item_4 = ctk.CTkButton(master=inventory_display,
                                           text=player_inventory[3],
                                           fg_color=("gray75", "gray30"),
                                           command=lambda: replace_item(3))
                inv_item_4.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

            item_1.configure(text=player_inventory[0])
            item_2.configure(text=player_inventory[1])
            item_3.configure(text=player_inventory[2])
            item_4.configure(text=player_inventory[3])

            cave_display.destroy()

            update_stats()

        weapons = ["🔫", "⚔", "🏹", "⛏"]
        charms = ["💎", "♥", "★"]

        num_weapons = np.random.randint(0, 3)
        num_charms = np.random.randint(0, 2)

        player_gold += np.random.randint(0, 101)

        weapons_found = choices(weapons, cum_weights=(15, 35, 65, 100), k=4)[:num_weapons]
        charms_found = choices(charms, cum_weights=(35, 65, 100), k=3)[:num_charms]

        cave_display = ctk.CTkToplevel(game_window)
        cave_display.geometry("350x300")
        cave_display.title("Cave")
        cave_display.resizable(False, False)

        items = [" ", " ", " ", " "]
        for i in range(0, num_weapons):
            items[i] = weapons_found[i]

        for i in range(0, num_charms):
            items[i + 2] = charms_found[i]

        # labels
        cave_label = ctk.CTkLabel(master=cave_display,
                                  text="Choose 1 Item to\nAdd to Your Inventory",
                                  fg_color=("gray75", "gray30"))
        cave_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        weapons_label = ctk.CTkLabel(master=cave_display,
                                     text="Weapons:",
                                     fg_color=("gray75", "gray30"))
        weapons_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        charms_label = ctk.CTkLabel(master=cave_display,
                                    text="Charms:",
                                    fg_color=("gray75", "gray30"))
        charms_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # make 4 frames for each cave item
        cave_item_1 = ctk.CTkButton(master=cave_display,
                                    text=items[0],
                                    fg_color=("gray75", "gray30"),
                                    command=lambda: add_item(items[0]))
        cave_item_1.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        cave_item_2 = ctk.CTkButton(master=cave_display,
                                    text=items[1],
                                    fg_color=("gray75", "gray30"),
                                    command=lambda: add_item(items[1]))
        cave_item_2.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        cave_item_3 = ctk.CTkButton(master=cave_display,
                                    text=items[2],
                                    fg_color=("gray75", "gray30"),
                                    command=lambda: add_item(items[2]))
        cave_item_3.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        cave_item_4 = ctk.CTkButton(master=cave_display,
                                    text=items[3],
                                    fg_color=("gray75", "gray30"),
                                    command=lambda: add_item(items[3]))
        cave_item_4.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")

        for i in range(0, len(cave_positions)):
            if player_location == cave_positions[i]:
                cave_positions[i] = [100, 100]

    def enter_castle():
        if player_keys < len(boss_positions):
            pop_up = ctk.CTkToplevel(game_window)
            pop_up.geometry("150x50")
            pop_up.title("Announcement!")
            pop_up.resizable(False, False)
            pop_up_label = ctk.CTkLabel(master=pop_up, text="You must collect all\nthe keys before entering!")
            pop_up_label.grid(row=0, column=0)
        else:
            pop_up = ctk.CTkToplevel(game_window)
            pop_up.geometry("150x50")
            pop_up.title("Announcement!")
            pop_up.resizable(False, False)
            pop_up_label = ctk.CTkLabel(master=pop_up, text="Congratulations! You win!")
            pop_up_label.grid(row=0, column=0)

    def enter_store():
        print("Welcome to the store... currently the store is unavailable")

    def move(direction, respawn):
        match direction:
            case 0:
                player_location[0] -= 1
            case 1:
                player_location[0] += 1
            case 2:
                player_location[1] += 1
            case 3:
                player_location[1] -= 1
            case 4:
                player_location[0] = respawn[0]
                player_location[1] = respawn[1]
        for i in range(0, len(boss_positions)):
            if player_location == boss_positions[i]:
                fight_boss()
            else:
                pass
        for i in range(0, len(cave_positions)):
            if player_location == cave_positions[i]:
                enter_cave()
            else:
                pass
        for i in range(0, len(castle_position)):
            if player_location == castle_position[i]:
                enter_castle()
            else:
                pass
        if player_location == store_position:
            enter_store()
        player.grid(row=player_location[0], column=player_location[1])

    # Create game window
    game_window = ctk.CTkToplevel(self)
    game_window.geometry("750x750")
    game_window.title("EASTER EGG!")
    game_window.resizable(False, False)
    game_window.protocol("WM_DELETE_WINDOW", close_display)
    self.play_game.state = DISABLED

    # ============ create two frames for game interface ============

    # configure layout
    game_window.columnconfigure(0, weight=1)
    game_window.rowconfigure(0, weight=100)
    game_window.rowconfigure(1, weight=1, minsize=150)

    # create frames
    map_frame = ctk.CTkFrame(master=game_window,
                             fg_color="mediumseagreen")
    map_frame.grid(row=0, column=0, sticky="nsew")

    command_frame = ctk.CTkFrame(master=game_window,
                                 fg_color="#292929")
    command_frame.grid(row=1, column=0, sticky="nsew")

    # ============ map_frame ============

    map_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                               24, 25, 26, 27, 28, 29, 30, 31), weight=1)

    for i in range(0, 20):
        for j in range(0, 31):
            empty = ctk.CTkLabel(master=map_frame,
                                 text=" ")
            empty.grid(row=i, column=j, sticky="nsew")

    for i in range(0, 31):
        forest = ctk.CTkLabel(master=map_frame,
                              text_font=("kanit", -15),
                              text_color="darkgreen",
                              text="🌳")
        forest.grid(row=0, column=i)

        forest = ctk.CTkLabel(master=map_frame,
                              text_font=("kanit", -15),
                              text_color="darkgreen",
                              text="🌳")
        forest.grid(row=i, column=0)

        forest = ctk.CTkLabel(master=map_frame,
                              text_font=("kanit", -15),
                              text_color="darkgreen",
                              text="🌳")
        forest.grid(row=19, column=i)

        forest = ctk.CTkLabel(master=map_frame,
                              text_font=("kanit", -15),
                              text_color="darkgreen",
                              text="🌳")
        forest.grid(row=i, column=31)

    poi, bosses, player_location = generate_map()

    castle_position = poi[:4]
    boss_positions = poi[4:4 + bosses]
    cave_positions = poi[4 + bosses:-1]
    store_position = poi[-1]

    # ============ command_frame ============

    command_frame.columnconfigure(0, weight=2)
    command_frame.columnconfigure((1, 2), weight=1)
    command_frame.rowconfigure(0, weight=1)

    movement_frame = ctk.CTkFrame(master=command_frame)
    movement_frame.grid(row=0, column=0, sticky="nsew")

    stats_frame = ctk.CTkFrame(master=command_frame)
    stats_frame.grid(row=0, column=1, sticky="nsew")

    inventory_frame = ctk.CTkFrame(master=command_frame)
    inventory_frame.grid(row=0, column=2, sticky="nsew")

    # ============ movement_frame ============

    movement_frame.columnconfigure((0, 1, 2), weight=1)
    movement_frame.rowconfigure((0, 1, 2), weight=1)

    up = ctk.CTkButton(master=movement_frame,
                       text="↑",
                       command=lambda: move(0, [0, 0]))
    up.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    down = ctk.CTkButton(master=movement_frame,
                         text="↓",
                         command=lambda: move(1, [0, 0]))
    down.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

    east = ctk.CTkButton(master=movement_frame,
                         text="→",
                         command=lambda: move(2, [0, 0]))
    east.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

    west = ctk.CTkButton(master=movement_frame,
                         text="←",
                         command=lambda: move(3, [0, 0]))
    west.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    # ============ stats_frame ============

    stats_frame.columnconfigure((0, 1, 2, 3), weight=1)
    stats_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

    character_label = ctk.CTkLabel(master=stats_frame,
                                   text="Character",
                                   fg_color=("gray75", "gray30"))
    character_label.grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=5)

    health_label = ctk.CTkLabel(master=stats_frame,
                                text="Health: ")
    health_label.grid(row=1, column=0, sticky="ew")

    player_health_label = ctk.CTkLabel(master=stats_frame,
                                       text=str(player_health))
    player_health_label.grid(row=1, column=1, sticky="ew")

    stamina_label = ctk.CTkLabel(master=stats_frame,
                                 text="Stamina: ")
    stamina_label.grid(row=1, column=2, sticky="ew")

    player_stamina_label = ctk.CTkLabel(master=stats_frame,
                                        text=str(player_stamina))
    player_stamina_label.grid(row=1, column=3, sticky="ew")

    strength_label = ctk.CTkLabel(master=stats_frame,
                                  text="Strength: ")
    strength_label.grid(row=2, column=0, sticky="ew")

    player_strength_label = ctk.CTkLabel(master=stats_frame,
                                         text=str(player_strength))
    player_strength_label.grid(row=2, column=1, sticky="ew")

    agility_label = ctk.CTkLabel(master=stats_frame,
                                 text="Agility: ")
    agility_label.grid(row=2, column=2, sticky="ew")

    player_agility_label = ctk.CTkLabel(master=stats_frame,
                                        text=str(player_agility))
    player_agility_label.grid(row=2, column=3, sticky="ew")

    stats_label = ctk.CTkLabel(master=stats_frame,
                               text="Game Stats",
                               fg_color=("gray75", "gray30"))
    stats_label.grid(row=3, column=0, columnspan=4, sticky="ew", padx=5, pady=5)

    keys_label = ctk.CTkLabel(master=stats_frame,
                              text="Keys: ")
    keys_label.grid(row=4, column=0, sticky="ew")

    player_keys_label = ctk.CTkLabel(master=stats_frame,
                                     text=str(player_keys))
    player_keys_label.grid(row=4, column=1, sticky="ew")

    gold_label = ctk.CTkLabel(master=stats_frame,
                              text="Gold: ")
    gold_label.grid(row=4, column=2, sticky="ew")

    player_gold_label = ctk.CTkLabel(master=stats_frame,
                                     text=str(player_gold))
    player_gold_label.grid(row=4, column=3, sticky="ew")

    kills_label = ctk.CTkLabel(master=stats_frame,
                               text="Enemies Killed: ")
    kills_label.grid(row=5, column=0, sticky="ew")

    player_kills_label = ctk.CTkLabel(master=stats_frame,
                                      text=str(player_kills))
    player_kills_label.grid(row=5, column=1, sticky="ew")

    deaths_label = ctk.CTkLabel(master=stats_frame,
                                text="Deaths: ")
    deaths_label.grid(row=5, column=2, sticky="ew")

    player_deaths_label = ctk.CTkLabel(master=stats_frame,
                                       text=str(player_deaths))
    player_deaths_label.grid(row=5, column=3, sticky="ew")

    # ============ inventory_frame ============

    inventory_frame.columnconfigure((0, 1), weight=1)
    inventory_frame.rowconfigure((0, 1, 2), weight=1)

    inventory_label = ctk.CTkLabel(master=inventory_frame,
                                   text="Inventory")
    inventory_label.grid(row=0, column=0, columnspan=2, sticky="ew")

    # make 4 frames for each inventory item
    item_1 = ctk.CTkLabel(master=inventory_frame,
                          text=" ",
                          text_font=("kanit", -10),
                          fg_color=("gray75", "gray30"))
    item_1.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    item_2 = ctk.CTkLabel(master=inventory_frame,
                          text=" ",
                          text_font=("kanit", -10),
                          fg_color=("gray75", "gray30"))
    item_2.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    item_3 = ctk.CTkLabel(master=inventory_frame,
                          text=" ",
                          text_font=("kanit", -10),
                          fg_color=("gray75", "gray30"))
    item_3.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    item_4 = ctk.CTkLabel(master=inventory_frame,
                          text=" ",
                          text_font=("kanit", -10),
                          fg_color=("gray75", "gray30"))
    item_4.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
