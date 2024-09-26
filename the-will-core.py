"""
Första anteckningar:

Kom ihåg att göra ett choose your own adventure lolzzzz
där du letar efter the will core som är en maguffin av rang

fler programming puns?
- The Will Core
Bossnamn:
- Opera Tor
- Funk Sean
- Basher
    A git who lives in the Hub

Autobattler?
    input() för varje ny handling, default blank rad för att fortsätta
        Hemliga ord som man kan ge buffar?
        typ input("Skriv in ett hejarop till X!") där vissa inputs är kodord för att ge buffs
            cooldown på buffs så man inte behöver spamma?
            permanenta buffs?
            random ord från lista, alternativt generera?
                Loot/treasure kan vara ledtrådar till ord/stavelser
Levels?
    Behövs progression eller är utmaningen autobattler tactics?
    Builds vs grind
Loot?
    oshit, måste göra loot tables
    Definera i csv/excel?
        namn, rarity där större tal => högre chans
        Summera alla chanser, dra en randint(1, max_loot_chance)
Damage types?
    ARPG style; fire, cold, poison etc.
Initiativ/speed?
Companions?
Dialog?
    Speech skill?
    Färgade ord?
        colorama-modulen verkar inte funka
Karta?
    använd print(i, end = "") för att printa utan ny rad
    Spara spelarens position
        Använd för att avgöra vilket håll man kan gå åt
        Typ nåt sånt här?
    ..... ..... .....
    | o |-|   | | ? |
    ''''' ''''' '''''
            |     | 
    ..... ..... .....
    | x |-|   |-|   |
    ''''' ''''' '''''
    Om rummet är upptäckt, sätt värde på sträng till väggarna, typ
        print(f{room00}, {room01}, {room02})
        print(f{room10}, {room11}, {room12})
        print(f{room20}, {room21}, {room22})
    Tre rader per rum, efter varandra i x-led

Combat moves
    Aimed attack X
    Defense X
    Disarm
    Relentless attack X
    Turtle X

Rum-attribut
    Kan jag generera en lista objekt som rummet innehåller och skriva som desc?
"""
from random import choice
from random import randint
from msvcrt import getch
from sys import stdout
from time import sleep

#CLASSES
class player:
    def __init__(self, hp, speed, attack, defense, armor, inventory, name, exp, level):
        self.hp = hp
        self.speed = speed
        self.attack = attack
        self.defense = defense
        self.armor = armor
        self.inventory = inventory
        self.name = name
        self.exp = exp
        self.level = level
class enemy:
    def __init__(self, hp, speed, attack, defense, armor, name, inventory, loot, level):
        self.hp = hp
        self.speed = speed
        self.attack = attack
        self.defense = defense
        self.armor = armor
        self.name = name
        self.inventory = inventory
        self.loot = loot
        self.level = level
class item:
    def __init__(self, hp, speed, attack, defense, min_dmg, max_dmg, armor, slot, name):
        self.hp = hp
        self.speed = speed
        self.attack = attack
        self.defense = defense
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        self.armor = armor
        self.slot = slot
        self.name = name
class consumable:
    def __init__(self, name):
        self.name = name
class potion(consumable):
    def function():
        player_char.hp += 5
class scroll(consumable):
    def __init__(self, name, text):
        self.name = name
        self.text = text
class key(consumable): #fix parent class
    def __init__(self, name, lock):
        self.name = name
        self.lock = lock
class container:
    def __init__(self, *loot_table):
        self.loot_table = loot_table
        self.items = []
class room:
    def __init__(self, xpos, ypos, vis, line1, line2, line3, items, desc, enemy, lock, lockvis):
        self.xpos = xpos
        self.ypos = ypos
        self.vis = vis
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3
        self.items = items
        self.desc = desc
        self.enemy = enemy
        self.lock = lock
        self.lockvis = lockvis

#INVENTORY ITEMS "Helmet", "Armor", "Main Hand", "Off Hand", "Necklace"
# HP, SPEED, ATTACK, DEFENSE, MIN-DMG, MAX-DMG, ARMOR, SLOT, NAME
item_dagger      = item(0, 1, 0, 0, 1, 2, 0, "Main Hand", "Dagger")
item_short_sword = item(0, 0, 1, 0, 2, 3, 0, "Main Hand", "Short Sword")
item_shield      = item(0, 0, 0, 2, 0, 0, 1, "Off Hand", "Shield")
item_cloak       = item(1, 2, 0, 1, 0, 0, 1, "Armor", "Cloak")
item_dummy       = item(0, 0, 0, 0, 1, 1, 0, "None", "Nothing")
item_shotgun     = item(0, 4, 10, 10, 5, 5, 0, "Main Hand", "SHOTGUN SON")

item_key1 = key("Key A", "A")
item_key2 = key("Key B", "B")

#CONTAINERS
#fixaaaaaa
container_chest = container(item_cloak, 5, item_dagger, 10, item_shield, 10, item_short_sword, 1)

#HOUSEKEEPING
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

#SPELL KEYWORDS
relentless_attack_keyword = 0
relentless_attack_discovered = False
disarm_keyword = 0
disarm_discovered = False
turtle_keyword = 0
turtle_discovered = False
spell_hp_keyword = 0
spell_speed_keyword = 0

#FUNCTIONS
def generate_items(how_many, *items):
    i = 0
    incoming_item_list = list(items)
    outgoing_item_list = []
    while i < how_many:
        item = choice(incoming_item_list)
        outgoing_item_list.append(item)
        incoming_item_list.remove(item)
        i += 1
    return outgoing_item_list
def generate_enemy(hp, speed, attack, defense, armor, name, inventory, loot, exp): #FIXA! basera lvl på j i worldgen?
    gen_enemy = enemy(hp, speed, attack, defense, armor, name, inventory, loot, exp)
    return gen_enemy
def generate_world(xsize, ysize):
    global map_xsize
    global map_ysize
    global relentless_attack_keyword
    global disarm_keyword
    room_list = []
    room_n = 0
    j = 0
    while j < ysize:
        i = 0
        while i < xsize:
            new_room = room(i, j, 0, "     ", "     ", "     ", generate_items(randint(0,2), item_dagger, item_key1, item_key2), generate_room_description(), generate_enemy(3, 2, 1, 1, 0, "Gobbo", {"Helmet": item_dummy, "Armor": item_dummy, "Main Hand": item_dummy, "Off Hand": item_dummy, "Necklace": item_dummy}, [], 1,), choice(["", "", "", "", "", "A", "B"]), 0)
            room_n += 1
            room_list.append(new_room)
            i += 1
        j += 1
    map_xsize = xsize
    map_ysize = ysize
    return room_list
def render_map():
    for x in room_list:
        if player_xpos == x.xpos and player_ypos == x.ypos:
            x.vis = 1

    for x in room_list:
        if x.lockvis == 1:
            x.line1 = ".KEY."
            x.line2 = "  " + x.lock + "  "
            x.line3 = "'REQ'"
    
    for x in room_list:
        if x.vis == 1:
            x.line1 = "....."
            x.line2 = "|   |"
            x.line3 = "'''''"
            if x.items != []:
                x.line1 = "..?.."
        if x.xpos == player_xpos and x.ypos == player_ypos:
            x.line2 = "| @ |"
    
    i = 0
    j = 0
    while j < map_ysize:
        while i < map_xsize:
            for x in room_list[i*map_xsize:i*map_xsize + map_xsize]:
                print(x.line1, end = " ")
            print("")
            for x in room_list[i*map_xsize:i*map_xsize + map_xsize]:
                print(x.line2, end = " ")
            print("")
            for x in room_list[i*map_xsize:i*map_xsize + map_xsize]:
                print(x.line3, end = " ")
            print("")
            i += 1
        j += 1
    for x in room_list:
        if player_xpos == x.xpos and player_ypos == x.ypos:
            print(x.desc)
def delete_rows(rows):
    i = 0
    while i < rows:
        stdout.write(CURSOR_UP_ONE) 
        stdout.write(ERASE_LINE)         
        i += 1
def player_navigation():
    global player_xpos
    global player_ypos
    global room_list
    global current_room
    nav = True
    locked_door = 0
    needed_key = ""
    first = 1
    render_map()
    while nav:
        player_nav = str(getch(), encoding="utf-8")
        if player_nav.lower() == "d" and player_xpos < map_xsize - 1:
            if check_lock(player_xpos + 1, player_ypos):
                player_xpos += 1
                locked_door = 0
            else:
                for x in room_list:
                    if x.xpos == player_xpos + 1 and x.ypos == player_ypos:
                        needed_key = x.lock
                        locked_door = 1
                        x.lockvis = 1
        if player_nav.lower() == "a" and player_xpos > 0:
            if check_lock(player_xpos - 1, player_ypos):
                player_xpos -= 1
                locked_door = 0
            else:
                for x in room_list:
                    if x.xpos == player_xpos - 1 and x.ypos == player_ypos:
                        needed_key = x.lock
                        locked_door = 1
                        x.lockvis = 1
        if player_nav.lower() == "s" and player_ypos < map_ysize - 1:
            if check_lock(player_xpos, player_ypos + 1):
                player_ypos += 1
                locked_door = 0
            else:
                for x in room_list:
                    if x.xpos == player_xpos and x.ypos == player_ypos + 1:
                        needed_key = x.lock
                        locked_door = 1
                        x.lockvis = 1
        if player_nav.lower() == "w" and player_ypos > 0:
            if check_lock(player_xpos, player_ypos - 1):
                player_ypos -= 1
                locked_door = 0
            else:
                for x in room_list:
                    if x.xpos == player_xpos and x.ypos == player_ypos - 1:
                        needed_key = x.lock
                        locked_door = 1
                        x.lockvis = 1
        if player_nav.lower() == "e":
            nav = False
            break
        for x in room_list:
            if x.xpos == player_xpos and x.ypos == player_ypos:
                current_room = x
        if locked_door == 0:
            delete_rows(map_ysize*3 + 3 - first)
            first = 0
            render_map()
        else:
            delete_rows(map_ysize*3 + 3)
            input("\n" * round((map_ysize*3/2)) + (" "*round((map_xsize*3/2)))  + "Locked! You need key " + needed_key + "\n" * round((map_ysize*3/2)))
            delete_rows(map_ysize*3 + 2)
            render_map()
        print("Navigate with WASD, exit with E")
def check_lock(xpos, ypos):
    for x in room_list:
        if x.xpos == xpos and x.ypos == ypos:
            if x.lock != "":
                lock = x.lock
                for i in player_backpack:
                    if type(i) == key:
                        if i.lock == lock:
                            return True
                return False
            else:
                return True
def menu(*choices):
    valid_choice = True
    print("---------------")
    while valid_choice:
        for x, choice in enumerate(choices):
            parse_list = choice.split(" ")
            text = parse_list[0]
            shortcut = parse_list[1]
            print(str(x + 1) + " " + text + " [" + shortcut + "]")
        print("---------------")
        menu_choice= input("What do you wish to do?\n>>>")
        for x, choice in enumerate(choices):
            parse_list = choice.split(" ")
            text = parse_list[0]
            shortcut = parse_list[1]
            if menu_choice.lower() == text.lower() or menu_choice.lower() == shortcut.lower() or menu_choice.lower() == str(x + 1).lower():
                valid_choice = False
                break
        if valid_choice:
            input("Hörru.")
    return shortcut
def inventory():
    print("..............\nYour Inventory\n''''''''''''''")
    for x in player_char.inventory:
        if player_char.inventory[x] == "Nothing":
            print("• " + x + ": Nothing")
        else:
            print("• " + x + ": " + player_char.inventory[x].name)
    print("")
    if player_backpack == []:
        print("Thy backpack is empty.")
    else:
        print("Your backpack contains: ")
        for x in player_backpack:
            print(x.name)
    parse_text("Whassup? (\"help\" for command list)\n>>>", "in")
def explore(): #use parse_text() here to allow for looting etc
    print("...........\nExploration\n'''''''''''")
    print("..\\.............................../..")
    print("...\\............................./...")
    print("....\\.........................../....")
    print(".....i'''''''''''''''''''''''''i.....")
    print(".....|                         |.....")
    print(".....|                         |.....")
    print(".....|    ___        ___       |.....")
    print(".....|   |   |       |+|       |.....")
    print(".....|   |o  |       '''       |.....")
    print(".....|___|___|_________________|.....")
    print("..../...........................\\....")
    print(".../.............................\\...")
    print("../...............................\\..")
    print(current_room.desc)
    if type(current_room.enemy) == enemy:
        print("There is a " + current_room.enemy.name + " in the room. Ew.")
    if current_room.items != []:
        print("The room contains: ", end = "")
        list_len = len(current_room.items)
        for i, x in enumerate(current_room.items):
            if i < list_len - 1:
                print("a " + x.name.lower(), end = ", ")
            elif list_len - 1 == 0:
                print("a " + x.name.lower() + ".")
            else:
                print("and a " + x.name.lower() + ".")
    else:
        print("Nothing in the room to explore")
    parse_text("How will you explore the room? (\"help\" for command list)\n", "ex")
def calculate_combat_speed(instance):
    combat_value = instance.speed
    for x in instance.inventory.values():
        if x.speed != 0:
            combat_value += x.speed
    return combat_value
def combat():
    print("Prepare to fight a mighty " + current_room.enemy.name + "!")
    global player_char
    global relentless_attack_keyword
    global relentless_attack_discovered
    global turtle_keyword
    global turtle_discovered
    global disarm_keyword
    global disarm_discovered
    global player_move
    combat = True
    while combat:
        player_turn = 0
        enemy_turn = 0
        player_speed = calculate_combat_speed(player_char)
        print("Player speed: " + str(player_speed))
        enemy_speed = calculate_combat_speed(current_room.enemy)
        print("Enemy speed: " + str(enemy_speed))
        combat_threshold = max(player_speed, enemy_speed) * 4
        print("Combat Threshold: " +str(combat_threshold))
        player_move = ""
        enemy_move = ""
        if combat_move():
            pass
        else:
            break
        delete_row = False
        while player_char.hp > 0 and current_room.enemy.hp > 0: #-------------------- PLAYER TURN         
            if player_turn >= combat_threshold:
                print(player_char.name + " takes a swing!")
                sleep(1)
                if player_move != turtle_keyword:
                    attack(player_char, player_move, current_room.enemy, enemy_move)
                else:
                    print("You curled up like a turtle.")
                player_move = ""
                player_turn = 0
                delete_row = False
                if current_room.enemy.hp <= 0:
                    current_room.enemy.hp = 0
                    print("You have defeated " + current_room.enemy.name + "!")
                    break
                if combat_move():
                    pass
                else:
                    break

            if enemy_turn >= combat_threshold and current_room.enemy.hp > 0:
                print(current_room.enemy.name + " takes a swing!")
                sleep(1)
                attack(current_room.enemy, enemy_move, player_char, player_move)
                enemy_move = ""
                enemy_turn = 0
                delete_row = False
                if player_char.hp <= 0:
                    print("lol u die")
                    death()
            if player_turn < combat_threshold and enemy_turn < combat_threshold:
                player_turn += player_speed
                if player_turn > combat_threshold:
                    player_turn = combat_threshold
                enemy_turn += enemy_speed
                if enemy_turn > combat_threshold:
                    enemy_turn = combat_threshold
                if delete_row:
                    delete_rows(2)
                delete_row = True
                print("Player: " + "█" * player_turn + "-" * (combat_threshold - player_turn) + " " + str(player_char.hp) + " HP")
                print("Enemy : " + "█" * enemy_turn + "-" * (combat_threshold - enemy_turn) + " " + str(current_room.enemy.hp) + " HP")
                sleep(.5)
        combat = False
def combat_move():
    global turtle_discovered
    global relentless_attack_discovered
    global disarm_discovered
    loop = True
    while loop:
        player_move = input("Press enter to continue, A/D for moves, or type something to cheer " + player_char.name + " on!\n")
        if player_move.lower() == "f":
            print("You flee the battle!")
            return False
        if player_move.lower() == "a": 
            print(player_char.name + " will do an aimed attack (+5 ATK, -5 DEF)")
            return True
        if player_move.lower() == "d": 
            print(player_char.name + " will defend (+5 DEF, -5 ATK)")
            return True
        if player_move.lower() == "": 
            return True
        if player_move.lower() == "move":
            if relentless_attack_discovered == True:
                print("Relentless Attack: " + relentless_attack_keyword + "[" + ra_shortcut + "]")
                print("Lunge at your foe for massive damage while sacrificing safety! (+2 Damage, +1 Damage taken)")
            if turtle_discovered == True:
                print("Turtle: " + turtle_keyword + "[" + turtle_shortcut + "]")
                print("Give up your next attack in order to defend yourself. (+3 Armor, no attacking)")
            if disarm_discovered == True:
                print("Disarm: " + disarm_keyword + "[" + disarm_shortcut + "]")
                print("Aim for your opponent's weapon to disarm them. (-8 attack, hit disarms enemy)")
        if player_move.lower() == relentless_attack_keyword: #------------------------------ SPECIAL MOVES
            if relentless_attack_discovered == False:
                relentless_attack_discovered = True
                print("You have discovered Relentless Attack!\nSay again to use it, otherwise use a different command or press Enter to continue.")
            else:
                print(player_char.name + " will do a relentless attack! (+2 Damage, +1 Damage taken)")
                return True
        if player_move.lower() == turtle_keyword:
            if turtle_discovered == False:
                turtle_discovered = True
                print("You have discovered Turtle!\nSay again to use it, otherwise use a different command or press Enter to continue.")
            else:
                print(player_char.name + " will turtle up this time. (+3 Armor, no attacking)")
                return True
        if player_move == disarm_keyword or player_move.lower() == disarm_shortcut:
            if disarm_discovered == False:
                disarm_discovered = True
                print("You have discovered Disarm!\nSay again to use it, otherwise use a different command or press Enter to continue.")
            else:
                print(player_char.name + " will turtle up this time. (+3 Armor, no attacking)")
                return True
def attack(attacker, attacker_move, defender, defender_move):
    attacker_bonus = 0
    defender_bonus = 0
    defender_armor = defender.inventory["Helmet"].armor - defender.inventory["Armor"].armor
    attack_damage = randint(attacker.inventory["Main Hand"].min_dmg, attacker.inventory["Main Hand"].max_dmg) + attacker.level - defender_armor
    if attacker_move.lower() == "a":
        attacker_bonus = 5
    if attacker_move.lower() == "d":
        attacker_bonus = -5
    if attacker_move.lower() == relentless_attack_keyword:
        attack_damage += 2
    
    if defender_move.lower() == "d":
        defender_bonus = 5
    if defender_move.lower() == "a":
        defender_bonus = -5
    if defender_move.lower() == relentless_attack_keyword:
        defender_armor -= 1
    if defender_move.lower() == turtle_keyword:
        defender_armor += 3
    chance_to_hit = 10 + attacker_bonus + attacker.attack + attacker.inventory["Helmet"].attack + attacker.inventory["Main Hand"].attack + attacker.inventory["Off Hand"].attack + attacker.inventory["Armor"].attack + attacker.inventory["Necklace"].attack -  defender_bonus - defender.defense - defender.inventory["Helmet"].defense - defender.inventory["Main Hand"].defense - defender.inventory["Off Hand"].defense - defender.inventory["Armor"].defense - defender.inventory["Necklace"].defense
    attack_roll = randint(1, 20)
    if attack_roll <= chance_to_hit:
        defender.hp -= attack_damage 
        print(attacker.name + " did " + str(attack_damage) + " damage")
    else: 
        print(attacker.name + " missed!")
def generate_spell_name():
    syl1 = choice(["Ans", "Alt", "Ap", "Bur", "Bos", "Beal", "Cri", "Cal", "Dree", "Dou", "Fle", "Fnu", "Fot", "FF", "Grrrra", "Hesh", "Hal", "Ils", "Jyrr", "Jask", "Klaa", "Lor", "Laf", "Mie", "Mlo", "Neh", "Ny", "Naf", "Oo", "Of", "Pir", "Phon", "Qua", "Qir", "Rhy", "Rac", "Stae", "Sloo", "Thuus", "Tah", "Uuv", "Vex", "Vahl", "Wath", "Xyx", "Xor", "Xeeg", "Yym", "Yrg", "Zwo", "Zae", "Zoth"])
    syl2 = choice(["aa", "al", "ath", "bot", "brith", "cho", "cleh", "der", "don", "dwes", "eir", "eet", "ens", "fro", "for", "fnu", "FN", "gath", "glom", "geb", "hae", "hom", "iel", "iim", "jok", "jar", "khe", "klo", "lith", "lyng", "loe", "mav", "moo", "nia", "nalt", "negh", "ol", "oagh", "oo", "prak", "phe", "quo", "rhea", "ril", "shy", "sul", "tha", "tig", "uu", "vex", "wah", "xa", "yat", "zool", "yoh", "zyz"])
    syl3 = choice(["alg", "aer", "bel", "bah", "cer", "col", "dof", "dae", "eec", "eie", "fay", "fnu", "gab", "goo", "hef", "hau", "ilt", "ine", "joh", "jank", "ka", "kob", "leed", "lan", "mar", "molk", "murn", "nargh", "noeh", "orl", "ooth", "om", "paf", "pip", "que", "ras", "rekk", "som", "seng", "tan", "tel", "thu", "uuv", "uer", "vog", "vex", "wyh", "wee", "wel", "xo", "xed", "yl", "yoof", "zel", "zzzy", "zaelael"])
    name = syl1 + syl2 + syl3
    return name
def death(): #Use sick logo here
    with open("willcore_gameover.txt") as f:
        print(f.read())
    exit()
def generate_room_description():
    adjective = choice(["musty", "clean", "tattered", "lumpy", "putrid", "impressive", "improper"])
    color = choice(["mold", "a unicorn", "off meat", "confetti", "sludge", "sludge that's blue", "a red house", "you know, whatever"])
    center = choice(["table", "man. A man screaming forever", "a minidisc player", "nothing", "something", "THE VOID"])
    string = ("The room is " + adjective + " and the walls are the color of " + color + ".\nIn the center of the room there is " + center + ".")
    return string
def generate_loot():
    loot_list = container_chest.loot_table
    total_chance = 0
    for x in loot_list:
        if type(x) != item:
            total_chance += x
    print("Total chance: " + str(total_chance))
    loot_roll = randint(1, total_chance)
    print("Roll: " + str(loot_roll))
    loot_number = 0
    loot_item = 0
    for x in loot_list:
        if type(x) == item:
            loot_item = x
        else:
            loot_number += x
        if loot_number >= loot_roll:
            print(loot_item.name)
            return(loot_item)
    print("Roll: " + str(loot_roll))
def item_description(_item): #add attack/defense
    if type(_item) == item:
        print(_item.name + ":")
        print("Equip to: " + _item.slot)
        if _item.hp != 0:
            print("• " + str(_item.hp) + " HP")
        if _item.speed > 0:
            print("• + " + str(_item.speed) + " speed")
        elif _item.speed < 0:
            print("• " + str(_item.speed) + " speed")
        if _item.attack != 0:
            print("• + " + str(_item.attack) + " attack")
        if _item.defense != 0:
            print("• + " + str(_item.defense) + " defense")
        if _item.min_dmg != 0 and _item.max_dmg != 0:
            print("• " + str(item.min_dmg) + "-" + str(item.max_dmg) + " DMG")
        if _item.armor > 0:
            print("• + " + str(_item.armor) + " armor")
        elif _item.armor < 0:
            print("• " + str(_item.armor) + " armor")
    if type(_item) == key:
        print(_item.name + ":")
        print("Opens lock " + _item.lock)
    if type(_item) == scroll:
        print(_item.name + ":")
        print(_item.text)
def enemy_description(enemy):
    print(enemy.name + ":")
    if enemy.hp != 0:
        print("• " + str(enemy.hp) + " HP")
        print("• " + str(enemy.speed) + " speed")
        print("• " + str(enemy.attack) + " attack")
        print("• " + str(enemy.defense) + " defense")
        print("• " + str(enemy.armor) + " armor")
        print("• Wielding: " + enemy.inventory["Main Hand"].name + " (" + str(enemy.inventory["Main Hand"].min_dmg) + "-" + str(enemy.inventory["Main Hand"].max_dmg) + " dmg)")
    else:
        print("• 0 HP. 'E's dead, Milord!")
    if enemy.loot != []:
        print("The enemy is guarding ", end = "")
        list_len = len(enemy.loot)
        for i, x in enumerate(enemy.loot):
            if i < list_len - 1:
                print("a " + x.name.lower(), end = ", ")
            elif list_len - 1 == 0:
                print("a " + x.name.lower() + ".")
            else:
                print("and a " + x.name.lower() + ".")
def parse_text(prompt, mode): #mode: "in" for inventory, "ex" for exploration
    # Parsing rules:
    # - One/two words
    # - Separated by a single space
    # - Enter mode as argument? inventory/battle/navigation etc.
    global player_backpack
    global room_list
    global current_room
    global enemy_gobbo
    parse = True
    while parse == True:
        list = input(prompt).split(" ", 1)
        if list[0].lower() == "m":
            parse = False
            break
        if list[0].lower() == "help": #display help file
                with open("willcore_help.txt") as f:
                    print(f.read())
        if mode == "in": #---------------------------------------------------------------mode set to inventory
            found = False
            if valid_text(list[0], "in", "eq", "d", "help"):
                if list[0].lower() == "in": #inspect command in inventory
                    if len(list) > 1:
                        print("---------------")
                        for x in player_char.inventory:
                            if type(player_char.inventory[x]) == item:
                                if list[1].lower() == player_char.inventory[x].name.lower():
                                    item_description(player_char.inventory[x])
                                    found = True
                                    break
                        if found == False:
                            for i, x in enumerate(player_backpack):
                                if list[1].lower() == player_backpack[i].name.lower():
                                    item_description(player_backpack[i])
                                    found = True
                                    break
                        if found == False and list[1] != "self":
                            print("\"" + list[1] + "\"" + " not found.")
                            print("---------------")
                        if list[1].lower() == "self":
                            print("." * (len(player_char.name) + 1))
                            print(player_char.name + ":")
                            print("'" * (len(player_char.name) + 1))
                            print("HP      : " + str(player_char.hp))
                            print("Speed   : " + str(player_char.speed))
                            print("Attack  : " + str(player_char.attack))
                            print("Defense : " + str(player_char.defense))
                            print("Armor   : " + str(player_char.armor))
                            print("EXP     : " + str(player_char.exp))
                            print("Level   : " + str(player_char.level))
                            print("---------------")
                            found = True
                if list[0].lower() == "eq": #equip command in inventory
                    if len(list) > 1:
                        found = False
                        print("---------------")
                        for i, x in enumerate(player_backpack):
                            if list[1].lower() == player_backpack[i].name.lower() and type(player_backpack[i]) == item:
                                if player_char.inventory[player_backpack[i].slot] != item_dummy:
                                    old_item = player_char.inventory[player_backpack[i].slot]
                                    new_item = player_backpack[i]
                                    player_backpack.append(old_item)
                                    player_char.inventory[new_item.slot] = new_item
                                    player_backpack.remove(new_item)
                                    found = True
                                    print("Changed " + old_item.name + " for " + new_item.name)
                                    print("---------------")
                                else:
                                    new_item = player_backpack[i]
                                    player_char.inventory[new_item.slot] = new_item
                                    player_backpack.remove(new_item)
                                    found = True
                                    print("Equipped " + new_item.name)
                                    print("---------------")
                            if list[1].lower() == player_backpack[i].name.lower() and type(player_backpack[i]) != item:
                                print(player_backpack[i].name + " is not equippable.")
                                print("---------------")
                                found = True
                if list[0].lower() == "d": #drop command in inventory
                    if len(list) > 1:
                        found = False
                        print("---------------")
                        for i, x in enumerate(player_backpack):
                            if list[1].lower() == player_backpack[i].name.lower():
                                drop_item = player_backpack[i]
                                player_backpack.remove(drop_item)
                                current_room.items.append(drop_item)
                                found = True
                                print("Dropped the " + drop_item.name.lower())
                                print("---------------")
                                break
                        if found == False:
                            print("\"" + list[1] + "\"" + " not found.")
                            print("---------------")
                if found == False and len(list) > 1:
                    print(list[1].lower() + " not found")
                    break
                elif found == False and list[0] != "help":
                    print("Only one word found")
            else:
                print("Invalid command")
        if mode == "ex":#---------------------------------------------------------mode set to explore
            if valid_text(list[0], "in", "t", "help"):
                found = False
                if list[0].lower() == "in": # inspect command in exploration
                    if current_room.items != []:
                        for x in current_room.items:
                            if list[1].lower() == x.name.lower():
                                item_description(x)
                                found = True
                                parse = False
                    if list[1].lower() == current_room.enemy.name.lower():
                        enemy_description(current_room.enemy)
                        found = True
                        parse = False
                if list[0].lower() == "t": # take command in exploration
                    found = False
                    if current_room.items != []:
                        if list[1].lower() == "all":
                            found = True
                            for x in current_room.items:
                                player_backpack.append(x)
                                current_room.items.remove(x)
                            print("Took all items!")
                        for x in current_room.items:
                            if list[1].lower() == x.name.lower():
                                player_backpack.append(x)
                                print("Took " + x.name + " from the room.")
                                current_room.items.remove(x)
                                found = True
                if found == False and list[0].lower() != "help":
                    print("\"" + list[1] + "\"" + " not found.")
def spell_fanfare():
    i = 0
    for i in range(7):
        if i % 2 == 0:
            with open("willcore_spell.txt") as f:
                print(f.read())
            sleep(1)
        else:
            delete_rows(11)
            print("\n" * 10)
            sleep(1)
            delete_rows(11)
        i += 1
def spellcasting():
    global spell_hp_found
    global spell_speed_found
    global spell_armor_found
    spell_word = input("What is the magic spell?\n")
    if spell_word.lower() == spell_hp_keyword.lower():
        if spell_hp_found == False:
            spell_fanfare()
            player_char.hp += 5 #change to max HP
            spell_hp_found = True
            input("You cast the magic healing spell!\nMax HP increased by 5!")
        else:
            input("You cast the magic healing spell!\n... But you have already gained its power.")
    elif spell_word.lower() == spell_speed_keyword.lower():
        if spell_speed_found == False:
            spell_fanfare()
            player_char.speed += 2
            spell_speed_found = True
            input("You cast the magic speed spell!\nSpeed increased by 2!")
        else:
            input("You cast the magic speed spell!\n... But you have already gained its power.")
    elif spell_word.lower() == spell_armor_keyword.lower():
        if spell_armor_found == False:
            spell_fanfare()
            player_char.armor += 2
            spell_armor_found = True
            input("You cast the magic armor spell!\nArmor increased by 2!")
        else:
            input("You cast the magic armor spell!\n... But you have already gained its power.")
    else:
        input("No such spell - spell failed!")
def split_text(text):
    str1, str2 = text[:len(text)//2], text[len(text)//2:] 
    return [str1, str2]
def scroll_names(scrolls, adjectives):
    for x in scrolls:
        random = randint(0, len(adjectives) - 1)
        x.name = adjectives[random] + " Scroll"
        adjectives.remove(adjectives[random])
def valid_text(text, *key):
    for x in key:
        if text.lower() == x.lower():
            return True
    return False
def help():
    print("---------------")
    with open("willcore_help.txt") as f:
            print(f.read())
    print("---------------")
def player_setup():
    global player_char
    global player_backpack
    global player_xpos
    global player_ypos
    player_char = player(5, 3, 1, 1, 0, {
    "Helmet": item_dummy,
    "Armor": item_dummy,
    "Main Hand": item_shotgun,
    "Off Hand": item_dummy,
    "Necklace": item_dummy
    }, "Nobody", 0, 1)
    player_backpack = [item_short_sword, item_shield, item_key1]
    player_xpos = 0
    player_ypos = 0
def main_menu():
    menu_choice = menu("Navigate nav", "Explore ex", "Fight f", "Inventory i", "Help help", "Generate_loot_[TEST] gen", "Spellcasting spell")
    if menu_choice.lower() == "f":
        combat()
    if menu_choice.lower() == "i":
        inventory()
    if menu_choice.lower() == "nav":
        player_navigation()
    if menu_choice.lower() == "ex":
        explore()
    if menu_choice.lower() == "help":
        help()
    if menu_choice.lower() == "gen":
        generate_loot()
    if menu_choice.lower() == "spell":
        spellcasting()
    

#GAME SETUP
map_xsize = 0
map_ysize = 0
room_list = generate_world(5, 5)
player_setup()
current_room = room_list[0]
room_list[0].lock = ""
combat_threshold = 20
#Generate combat moves
#Use dict to make an actual dictionaries i.e. "leg:fruth, belly:ababan, groin:wherif" "in the:ger pa, the heck outta:ghitik bogu thram, etc"
#then generate sentence as keyword
relentless_attack_keyword = "ra"
disarm_keyword = "disarm"
turtle_keyword = "turtle"
ra_shortcut = "ra"
disarm_shortcut = "d"
turtle_shortcut = "t"

#Generate spells
spell_hp_keyword = generate_spell_name()
spell_hp_found = False
spell_speed_keyword = generate_spell_name()
spell_speed_found = False
spell_armor_keyword = generate_spell_name()
spell_armor_found = False

#Generate spell scrolls
hp_scroll1 = scroll("Scroll 1", "A torn scroll with the text:\n\"" + split_text(spell_hp_keyword)[0] + "-\"")
hp_scroll2 = scroll("Scroll 2", "A torn scroll with the text:\n\"-" + split_text(spell_hp_keyword)[1] + "\"")
speed_scroll1 = scroll("Scroll 3", "A torn scroll with the text:\n\"" + split_text(spell_speed_keyword)[0] + "-\"")
speed_scroll2 = scroll("Scroll 4", "A torn scroll with the text:\n\"-" + split_text(spell_speed_keyword)[1] + "\"")
armor_scroll1 = scroll("Scroll 5", "A torn scroll with the text:\n\"" + split_text(spell_armor_keyword)[0] + "-\"")
armor_scroll2 = scroll("Scroll 6", "A torn scroll with the text:\n\"-" + split_text(spell_armor_keyword)[1] + "\"")
print(spell_hp_keyword)
print(spell_speed_keyword)
print(spell_armor_keyword)
# print("Scroll 1 text: \n" + hp_scroll1.text)
# print("Scroll 2 text: \n" + hp_scroll2.text)

scroll_list = [hp_scroll1, hp_scroll2, speed_scroll1, speed_scroll2, armor_scroll1, armor_scroll2]
#Rename scrolls
scroll_adjectives = ["Dusty", "Crumpled", "Crinkled", "Weathered", "Folded", "Singed", "Old", "Torn", "Aged", "Burned", "Yellow", "Faded", "Simple"]
scroll_names(scroll_list, scroll_adjectives)
#Sprinkle scrolls into level
scroll_room_list = room_list
for x in scroll_list:
    scroll_room_list[0].items.append(x) #remove after testing
    # random_room = randint(0, len(scroll_room_list) - 1)
    # scroll_room_list[random_room].items.append(x)
    # print(x.name + " is in room " + str(room_list[random_room].xpos) + str(room_list[random_room].ypos))
    #scroll_room_list.remove(scroll_room_list[random_room]) #varför funkar inte det här? Verkar ta bort rum ur room_list?

#GAME START
with open("willcore_logo.txt") as f:
    print(f.read())
# start = ""
# while start.lower() != "start":
#     start = menu("Start start", "Story story", "Help h", "Exit x")
#     if start.lower() == "story":
#         with open("willcore_story.txt") as f:
#             print(f.read())
#     if start.lower() == "h":
#         with open("willcore_help.txt") as f:
#             print(f.read())
#     if start.lower() == "x":
#         exit()
  
# player_char.name = input("What is thy noble knight's name? ")
# if player_char.name == "":
#     player_char.name = "Nobody"
# print("Thy name is " + player_char.name)
# input("Enter to continue")
player_char.name = "Testimus"

while True:
    main_menu()