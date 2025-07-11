import subprocess
import random
import time
import copy

PREFIXES_WARSHIPS = [
    "USS",
    "HMS",
    "INS",
    "JS", 
    "KRI",
    "HMAS"
    "FS", 
    "BNS",
    "ARC",
    "BRP",
    "NRP",
    "HTMS"
    "ROKS"
    "TNS",
    "AOR",
]
SUFFIXES_WARSHIPS = [
    "Thunderbolt",
    "Vikrant",
    "Yamato",
    "Dreadnought",
    "Sachsen",
    "Arleigh Burke",
    "Charles de Gaulle",
    "Independence",
    "Zumwalt",
    "Triumph",
    "Varyag",
    "São Paulo",
    "Kaga",
    "Formidable",
    "Tarlac",
]
SYMBOLS_SMALL  = [chr(i+97) for i in range(26)] # a-z
SYMBOLS_MEDIUM = [chr(i+49) for i in range(9)] # A-Z
SYMBOLS_BIG    = [chr(i+33) for i in range(10) if chr(i+33) != '(' and chr(i+33) != ')' and chr(i+33) != '\'']

SMALL=3 # Small util N blocks...
MEDIUM=7

BLOCK_IGNORE='.'
SHOT_SYMBOL='^'
HIT_SHIP_SYMBOL='/'
DESTROY_SHIP_SYMBOL="&"

MSG_SHOT="shot missed"
MSG_HIT="hit ship"
MSG_DESTROY="destroy ship"

BASE_CHAR_CODE=65

DEFAULT_CAPTION={
        MSG_SHOT:SHOT_SYMBOL,
        MSG_HIT:HIT_SHIP_SYMBOL,
        MSG_DESTROY:DESTROY_SHIP_SYMBOL
     }

#
SCENARIOS_LITTLE=[[5,5],[3,8],[8,3],[1,25]]
SCENARIOS_NORMAL=[[10,10],[20,5],[5,20],[3,30]]
SCENARIOS_EXTEND=[[15,15],[5,45],[25,9],[20,25]]

SHIPS_LITTLE=[1,1,2,3]
SHIPS_NORMAL=[2,2,2,3,4,4,6,6,7,8]
SHIPS_EXTEND=[2,3,3,3,4,4,4,5,5,5,7,7,7,8,8,8,10]

###
def generate_warships_names(amount_ships:int,already_used_names:'list')->'list':
    warships_names=[]
    prefixe=PREFIXES_WARSHIPS[int(random.random()*len(PREFIXES_WARSHIPS))]
    for _ in range(amount_ships):
        suffixe=SUFFIXES_WARSHIPS[int(random.random()*len(SUFFIXES_WARSHIPS))]
        name=prefixe+' '+suffixe
        
        loops=0
        while True:
            temp=name+'-'+str(loops)
            if not temp in warships_names and not temp in already_used_names:
                name=temp
                break
            loops+=1
        warships_names.append(name)
    return warships_names
def generate_table(height:int,width:int)->'list':
    table=[[BLOCK_IGNORE for _ in range(width)] for _ in range(height)]
    return table
def display_table(table:'list',caption:'dict')->None:
    print('  ',end='')
    for i in range(len(table[0])):
        print(chr(i+BASE_CHAR_CODE),end=' ')
    print()
    print(' #',end='')
    for i in range(len(table[0])):
        print('-',end=' ')
    print()
    #
    for i in range(len(table)):
        print('{}|'.format(chr(i+BASE_CHAR_CODE)),end='')
        for j in table[i]:
            if not j in caption.keys():
                print(BLOCK_IGNORE,end=' ')
            else:
                print(caption[j],end=' ')
        print()
    # Numbers columns
    print(' #',end='')
    for i in range(len(table[0])):
        print('-',end=' ')
    print()
    print('  ',end='')
    for i in range(len(table[0])):
        print(chr(i+BASE_CHAR_CODE),end=' ')
    print()
    #
def create_caption(size_each_name:'dict')->'dict':
    link_name_symbol=DEFAULT_CAPTION.copy()
    index_small=0
    index_medium=0
    index_big=0
    for i in size_each_name.keys():
        if size_each_name[i] <= SMALL:
            link_name_symbol[i]=SYMBOLS_SMALL[index_small]
            index_small+=1
        elif size_each_name[i] <= MEDIUM:
            link_name_symbol[i]=SYMBOLS_MEDIUM[index_medium]
            index_medium+=1
        else:
            link_name_symbol[i]=SYMBOLS_BIG[index_big]
            index_big+=1

        index_small%=len(SYMBOLS_SMALL)
        index_medium%=len(SYMBOLS_MEDIUM)
        index_big%=len(SYMBOLS_BIG)
    return link_name_symbol
def display_caption(caption:'dict')->None:
    longest_str=0
    for i in caption.keys():
        if len(i)>longest_str:
            longest_str=len(i)
    longest_str+=2
    print('Caption:')
    for i in caption.keys():
        print(f"{i:<{longest_str}} = {caption[i]}")
#
def check_able_lines(table:'matrix',ship_size:int)->'list':
    table_height=len(table)
    table_width=len(table[0])
    #
    able_columns=[[0 for i in range(table_width)] for j in range(table_height)]
    tag_columns=[[] for i in range(table_height)]
    for i in range(table_height):
        tag_columns[i].append(-1)
        for j in range(table_width):
            if table[i][j] != BLOCK_IGNORE:
                tag_columns[i].append(j)
        tag_columns[i].append(table_width)

    """
    for i in tag_columns:
        print(i)
    print()
    """

    for i in range(table_height):
        index=0
        index1_tag,index2_tag=0,1
        while index<table_width:
            if index==tag_columns[i][index2_tag]:
                index1_tag+=1
                index2_tag+=1
                index+=1
                continue
            #
            if tag_columns[i][index2_tag]-index>=ship_size: # forward
                able_columns[i][index]+=1
            if index-tag_columns[i][index1_tag]>=ship_size: # backward
                able_columns[i][index]+=2
            index+=1

    """
    for i in able_columns:
        print(i)
    """
    return able_columns
def check_able_columns(table:'matrix',ship_size:int)->'list':
    table_height=len(table)
    table_width=len(table[0])
    table_rev=[[] for i in range(table_width)]

    for i in range(table_width):
        for j in range(table_height):
            table_rev[i].append(table[j][i])

    """
    for i in table_rev:
        print(i)
    """
    return check_able_lines(table_rev,ship_size)
#
def put_randomly_ships_in_table(ships:'list',table:'matrix',ships_names:'liat')->'dict':
    if not len(table):
        print('Empty table')
        return
    table_height=len(table)
    table_width=len(table[0])

    ships_fit=[]
    ships_fit_name=[]
    for i in range(len(ships)):
        if ships[i]>table_width and ships[i]>table_height:
            continue
        ships_fit.append(ships[i])
        ships_fit_name.append(ships_names[i])
    #
    ships_fit.sort()
    used_names={}
    for index in range(len(ships_fit)):
        i=ships_fit[index]
        ship_name=ships_fit_name[index]
        #
        able_columns,able_lines=[],[]
        able_columns=check_able_columns(table,i)
        able_lines=check_able_lines(table,i)
        ##
        spots_ships_lines=[]
        spots_ships_columns=[]
        for j in range(table_height):
            for k in range(table_width):
                if able_lines[j][k]:
                    spots_ships_lines.append(j)
                    break
        for j in range(table_width):
            for k in range(table_height):
                if able_columns[j][k]:
                    spots_ships_columns.append(j)
                    break
        if not len(spots_ships_lines) and not len(spots_ships_columns):
            continue
        #
        vertical=int(random.random()*2)
        if vertical and not len(spots_ships_columns):
            vertical=0
        elif not vertical and not len(spots_ships_lines):
            vertical=1
        #
        list_spots=[]
        chosen_list_spots=0
        if vertical:
            chosen_list_spots=spots_ships_columns[int(random.random()*len(spots_ships_columns))]
            list_spots=able_columns[chosen_list_spots]
        else:
            chosen_list_spots=spots_ships_lines[int(random.random()*len(spots_ships_lines))]
            list_spots=able_lines[chosen_list_spots]

        # print(vertical,list_spots)
        index_spots=[]
        for j in range(len(list_spots)):
            if list_spots[j]!=0:
               index_spots.append(j)
        ##
        # print(list_spots,index_spots)
        line,column=None,None
        chosen_index=index_spots[int(random.random()*len(index_spots))]
        chosen=list_spots[chosen_index]
        # print(chosen_index,chosen)
        if vertical:
            column=chosen_list_spots
            line=chosen_index
        else:
            line=chosen_list_spots
            column=chosen_index
        #
        direction=0 # 1:forward 2:backward
        if chosen<3:
            direction=chosen
        else:
            direction=int(random.random()*2+1)
        #
        # print(vertical,direction)
        if vertical and direction==1:
            for j in range(i):
                table[line+j][column]=ship_name
        elif vertical and direction==2:
            for j in range(i):
                table[line-j][column]=ship_name

        if not vertical and direction==1:
            for j in range(i):
                table[line][column+j]=ship_name
        elif not vertical and direction==2:
            for j in range(i):
                table[line][column-j]=ship_name
        #
        # print("Ship {} size: {}, line:{}, column:{}, direction: {}".format(ship_name,i,line,column,direction))
        used_names[ship_name]=i
    return used_names
###
def get_ships_names(table:'matrix')->'list':
    ships_name=[]
    for i in table:
        for j in i:
            if not j in ships_name:
                ships_name.append(j)
    return ships_name
def get_ships_positions(table:'matrix')->'dict':
    ships_name=get_ships_names(table)
    position_by_name={}
    for i in ships_name:
        position_by_name[i]=[[],[]] # line,column
    #
    for i in range(len(table)):
        for j in range(len(table[i])):
            content=table[i][j]
            if not content in ships_name:
                continue
            position_by_name[content][0].append(i)
            position_by_name[content][1].append(j)
    return position_by_name
###
def init_game_battleship(table_height:int,table_width:int,ships_list:"list")->None:
    # Table with the ships 
    global table_ship_user
    global table_ship_bot
    # Table size
    global table_x # width
    global table_y # height
    # Ships size
    global ships
    # Ships blocks
    global ships_infos_user
    global ships_infos_bot
    # Ships posi
    global ships_posi_user
    global ships_posi_bot
    # Able commands
    global commands
    global commands_bot
    # Score
    global total_blocks_user
    global total_blocks_bot
    global score
    # Caption
    global caption_user
    global caption_bot
	# Bot QI
    global table_guess_bot
    global table_guess_user

    global caption_guess_bot
    global caption_guess_user

    global head_tail_bot
    global head_tail_user
    ###
    ## Init vars
    ships_name_user=generate_warships_names(len(ships_list),[])
    ships_name_bot=generate_warships_names(len(ships_list),ships_name_user)
    print(len(ships_list),len(ships_name_user))
    ## Tables with the ships
    table_ship_user=generate_table(table_height,table_width)
    table_ship_bot=generate_table(table_height,table_width)
    ## Table size
    table_x=table_width
    table_y=table_height
    ## Ships size
    ships=ships_list
    ## Ships blocks
    ships_infos_user=put_randomly_ships_in_table(ships,table_ship_user,ships_name_user)
    ships_infos_bot=put_randomly_ships_in_table(ships,table_ship_bot,ships_name_bot)
    ## Ships posi
    ships_posi_user=get_ships_positions(table_ship_user)
    ships_posi_bot=get_ships_positions(table_ship_bot)
    ## Able commands
    commands=["s","v","clear","caption","score"]
    commands_bot=["s"]
    ## Score
    total_blocks_user=0
    total_blocks_bot=0
    for i in ships_infos_user.values():
        total_blocks_user+=i
    for i in ships_infos_bot.values():
        total_blocks_bot+=i
    score=[0,0] # bot,user
    ## Caption
    caption_user=create_caption(ships_infos_user)
    caption_bot=create_caption(ships_infos_bot)
	## BOT QI
    table_guess_bot=generate_table(table_height,table_width)
    table_guess_user=generate_table(table_height,table_width)

    caption_guess_bot={}
    caption_guess_user={}

    head_tail_bot={}
    head_tail_user={}
    """
    print("TABLE_USER")
    display_table(table_ship_user,ships_infos_user)
    print("TABLE BOT")
    display_table(table_ship_bot,ships_infos_bot)
    """

def move_game_battleship(cmd:str,type_player:int)->None:
    cmd=cmd.split()
    # print(cmd)
    if not cmd[0] in commands:
        print("Invalid command")
        return type_player
    if cmd[0]=="s":
        position_shot=decode_position_table(cmd[1],cmd[2])
        res=shot(position_shot[0],position_shot[1],type_player)
        decision_guess_table(type_player)
        # print("type:",type_player)
        time.sleep(1)
        view_map((not type_player))
        time.sleep(2)
        return res
    #
    if cmd[0]=="score":
        print("Blocks ships remain to win: {}\nBlocks ships remain to defeat: {}".format(total_blocks_bot-score[1],total_blocks_user-score[0]))
        return type_player
    #
    if cmd[0]=="v" and cmd[1]=="user":
        view_map(1)
        return type_player
    elif cmd[0]=="v":
        view_map(0)
        return type_player
    #
    if cmd[0]=="clear":
        subprocess.run(["clear"])
        return type_player
    if cmd[0]=="caption":
        display_caption(caption_user)
        return type_player
def code_position_table(line:int,colm:int)->'list':
    line_code,colm_code=chr(line+BASE_CHAR_CODE),chr(colm+BASE_CHAR_CODE)
    return [line_code,colm_code] 
def decode_position_table(line:str,colm:str)->'list':
    line_dcode,colm_dcode=ord(line)-BASE_CHAR_CODE,ord(colm)-BASE_CHAR_CODE
    return [line_dcode,colm_dcode]
def end_game_battleship()->None:
    global table_ship_user
    global table_ship_bot
    # Table size
    global table_x # width
    global table_y # height
    # Ships size
    global ships
    # Ships blocks
    global ships_infos_user
    global ships_infos_bot
    # Ships posi
    global ships_posi_user
    global ships_posi_bot
    # Able commands
    global commands
    global commands_bot
    # Score
    global total_blocks_user
    global total_blocks_bot
    global score
    # Caption
    global caption_user
    global caption_bot
	# Bot QI
    global table_guess_bot
    global table_guess_user

    global caption_guess_bot
    global caption_guess_user

    global head_tail_bot
    global head_tail_user
    ###
    del table_ship_user
    del table_ship_bot
    # Table size
    del table_x # width
    del table_y # height
    # Ships size
    del ships
    # Ships blocks
    del ships_infos_user
    del ships_infos_bot
    # Ships posi
    del ships_posi_user
    del ships_posi_bot
    # Able commands
    del commands
    del commands_bot
    # Score
    del total_blocks_user
    del total_blocks_bot
    del score
    # Caption
    del caption_user
    del caption_bot
	# Bot QI
    del table_guess_bot
    del table_guess_user

    del caption_guess_bot
    del caption_guess_user

    del head_tail_bot
    del head_tail_user

###
def view_map(target:int)->None:
    if target:
        print("TABLE USER")
        display_table(table_ship_user,caption_user)
    else:
        print("TABLE BOT")
        display_table(table_ship_bot,DEFAULT_CAPTION)
        # display_table(table_ship_bot,caption_bot)
    return (not target)
def shot(line:int,column:int,type_player:int)->int: 
    table_ship=[]
    table_guess=[]

    caption_guess={}
    head_tail_guess={}

    ships_info=[]
    tot_blocks=score
    player_name=""
    #
    if type_player: #user
        table_ship=table_ship_bot
        table_guess=table_guess_user

        caption_guess=caption_guess_user
        head_tail_guess=head_tail_user
        
        ships_info=ships_infos_bot
        player_name="user"
    else: #bot
        table_ship=table_ship_user
        table_guess=table_guess_bot

        caption_guess=caption_guess_bot
        head_tail_guess=head_tail_bot

        ships_info=ships_infos_user
        player_name="bot"
    ###
    if line>=len(table_ship) or column>=len(table_ship[0]) or table_ship[line][column] in DEFAULT_CAPTION.keys():
        print("Invalid position. Try again")
        return type_player

    print("The {} will shot in line {} column {}!".format(player_name,chr(line+BASE_CHAR_CODE),chr(column+BASE_CHAR_CODE)))
    time.sleep(0.5)
    ##
    block_cont=table_ship[line][column]

    table_ship[line][column]=MSG_SHOT
    table_guess[line][column]=MSG_SHOT
    if block_cont != MSG_SHOT and block_cont!=MSG_HIT and block_cont!=BLOCK_IGNORE:
        print("The {} hit a ship! Shot again".format(player_name))
        # print(block_cont)
        # print(ships_info[block_cont])
        ships_info[block_cont]-=1
        table_ship[line][column]=MSG_HIT
        table_guess[line][column]=MSG_HIT
        guess_ships(table_guess,caption_guess,head_tail_guess)
        ##
        tot_blocks[type_player]+=1
        if not ships_info[block_cont] and type_player:
            destroy_ship(block_cont,type_player)
            print("You destroy the {} ship!".format(block_cont))
        elif not ships_info[block_cont] and not type_player:
            destroy_ship(block_cont,type_player)
            print("The enemy destroy the {} ship!".format(block_cont))
        return type_player
    print("The {} hit nothing".format(player_name))

    return (not type_player)
def destroy_ship(ship_name:str,type_player:int)->None:
    table_ship=[]
    table_guess=[]
    caption_guess=[]
    head_tail_guess=[]
    positions_line=[]
    positions_column=[]
    if not type_player: #bot
        table_ship=table_ship_user
        table_guess=table_guess_bot

        caption_guess=caption_guess_bot
        head_tail_guess=head_tail_bot

        positions_line=ships_posi_user[ship_name][0]
        positions_column=ships_posi_user[ship_name][1]
    else:
        table_ship=table_ship_bot
        table_guess=table_guess_user

        caption_guess=caption_guess_user
        head_tail_guess=head_tail_user

        positions_line=ships_posi_bot[ship_name][0]
        positions_column=ships_posi_bot[ship_name][1]

    ship_id_guess=[]
    for i in range(len(positions_line)):
        line=positions_line[i]
        column=positions_column[i]
        if not table_guess[line][column] in ship_id_guess:
            ship_id_guess.append(table_guess[line][column])
        table_ship[line][column]=MSG_DESTROY
        table_guess[line][column]=MSG_DESTROY

    curr_guess_ship=get_ships_names(table_guess)
    for i in ship_id_guess:
        if i in curr_guess_ship:
            continue
        # print('CLEAR {}'.format(i))
        if i in caption_guess:
            del caption_guess[i]
        if i in head_tail_guess :
            del head_tail_guess[i]
    decision_guess_table(type_player)
#
def update_head_tail(table_guess:'matrix',caption_guess:'dict',head_tail_guess:'dict')->None:
    guess_ships=get_ships_positions(table_guess)
    repeat=0
    for i in guess_ships.keys():
        if not i in caption_guess.keys():
            continue
        ship_posi=guess_ships[i]
        # print('2: {}'.format(ship_posi))

        line_head,colm_head=0,0
        line_tail,colm_tail=0,0
        if caption_guess[i]=='V':
            line_head,colm_head=ship_posi[0][0],ship_posi[1][0]
            line_tail,colm_tail=ship_posi[0][-1],ship_posi[1][-1]
        elif caption_guess[i]=='H':
            line_head,colm_head=ship_posi[0][-1],ship_posi[1][-1]
            line_tail,colm_tail=ship_posi[0][0],ship_posi[1][0]
        #
        if caption_guess[i]=='V' and line_tail<table_y-1 and table_guess[line_tail+1][colm_tail]==BLOCK_IGNORE:
            line_tail+=1
        if caption_guess[i]=='H' and colm_tail and table_guess[line_tail][colm_tail-1]==BLOCK_IGNORE:
            colm_tail-=1

        if caption_guess[i]=='V' and line_head and table_guess[line_head-1][colm_head]==BLOCK_IGNORE:
            line_head-=1
        if caption_guess[i]=='H' and colm_head<table_x-1 and table_guess[line_head][colm_head+1]==BLOCK_IGNORE:
            colm_head+=1
        #
        # print('6: {},{} {},{}'.format(line_head,colm_head,line_tail,colm_tail))
        if table_guess[line_head][colm_head] in [BLOCK_IGNORE,MSG_HIT] or table_guess[line_tail][colm_tail] in [BLOCK_IGNORE,MSG_HIT] :
            head_tail_guess[i]=[[line_head,colm_head],[line_tail,colm_tail]]
            continue

        ship_ID=max(list(caption_guess.keys()))
        direction='H' if caption_guess[i]=='V' else 'V'
        for j in range(len(ship_posi[0])):
            line,colm=ship_posi[0][j],ship_posi[1][j]
            table_guess[line][colm]=ship_ID
            caption_guess[ship_ID]=direction
            ship_ID+=1
            repeat=1
    if repeat:
        # print('REP!')
        update_head_tail(table_guess,caption_guess,head_tail_guess)
def guess_ships(table_guess:'matrix',caption_guess:'dict',head_tail_guess:'dict')->None:
    ships_posi=get_ships_positions(table_guess)
    if not MSG_HIT in ships_posi.keys():
        return

    union_ships={}
    ships_ID=len(caption_guess.keys())
    if len(caption_guess.keys()):
        ships_ID=max(list(caption_guess.keys()))+1

    hit_ships=ships_posi[MSG_HIT]
    for i in range(len(hit_ships[0])):
        line,colm=hit_ships[0][i],hit_ships[1][i]
        able_ships=[]
        able_positions=[]
        
        cont_over=table_guess[line-1][colm] if line else None
        cont_down=table_guess[line+1][colm] if line<table_y-1 else None
        cont_left=table_guess[line][colm-1] if colm else None
        cont_right=table_guess[line][colm+1] if colm<table_x-1 else None

        vertical_able=0
        horizontal_able=0

        ##
        #
        if cont_over in caption_guess.keys() and caption_guess[cont_over]=='V':
            able_ships.append(cont_over)
            vertical_able+=1
        if cont_down in caption_guess.keys() and caption_guess[cont_down]=='V':
            able_ships.append(cont_down)
            vertical_able+=1
        if cont_left in caption_guess.keys() and caption_guess[cont_left]=='H':
            able_ships.append(cont_left)
            horizontal_able+=1
        if cont_right in caption_guess.keys() and caption_guess[cont_right]=='H':
            able_ships.append(cont_right)
            horizontal_able+=1
        #
        if cont_left==BLOCK_IGNORE:
            able_positions.append('H')
        if cont_over==BLOCK_IGNORE:
            able_positions.append('V')
        if cont_right==BLOCK_IGNORE:
            able_positions.append('H')
        if cont_down==BLOCK_IGNORE:
            able_positions.append('V')
        ##
        # print('1: {}'.format(able_positions))
        # print('5: {}'.format(able_ships))
        if not len(able_positions):
            able_positions=['V','H']
        if not len(able_ships):
            able_ships.append(ships_ID)
            index_random=int(random.random()*len(able_positions))
            # print(index_random)
            caption_guess[ships_ID]=able_positions[index_random]
            ships_ID+=1
        table_guess[line][colm]=able_ships[int(random.random()*len(able_ships))]
        #
        if caption_guess[table_guess[line][colm]]=='V' and vertical_able>1:
            union_ships[table_guess[line][colm]]=[cont_over,cont_down]
        if caption_guess[table_guess[line][colm]]=='H' and horizontal_able>1:
            union_ships[table_guess[line][colm]]=[cont_left,cont_right]

    for i in union_ships.keys():
        new_ship_id=i
        new_ship_direction=caption_guess[new_ship_id]
        ship_1=union_ships[new_ship_id][0]
        ship_2=union_ships[new_ship_id][1]

        del caption_guess[ship_1]
        del caption_guess[ship_2]
        if ship_1 in head_tail_guess:
            del head_tail_guess[ship_1]
        if ship_2 in head_tail_guess:
            del head_tail_guess[ship_2]
        caption_guess[new_ship_id]=new_ship_direction

        for j in range(len(ships_posi[ship_1][0])):
            line,colm=ships_posi[ship_1][0][j],ships_posi[ship_1][1][j]
            table_guess[line][colm]=new_ship_id
        for j in range(len(ships_posi[ship_2][1])):
            line,colm=ships_posi[ship_2][0][j],ships_posi[ship_2][1][j]
            table_guess[line][colm]=new_ship_id
def decision_guess_table(type_player:int)->None:
    table_guess=[]
    caption_guess=[]
    head_tail_guess=[]
    if type_player: # user
        table_guess=table_guess_user
        caption_guess=caption_guess_user
        head_tail_guess=head_tail_user
    else:
        table_guess=table_guess_bot
        caption_guess=caption_guess_bot
        head_tail_guess=head_tail_bot

    guess_ships(table_guess,caption_guess,head_tail_guess)
    update_head_tail(table_guess,caption_guess,head_tail_guess)
    # for i in table_guess:
    #    print(i)
    # print('3: {}'.format(caption_guess))
    # print('4: {}'.format(head_tail_guess))

def check_victory()->int: # 1:user victory 2:bot victory 0:nothing
    if score[1]==total_blocks_bot: # user
        return 1
    if score[0]==total_blocks_user: # bot
        return 2
    return 0
###
def generate_command()->str:
    return commands_bot[int(random.random()*len(commands_bot))]
def generate_options(cmd:str)->str:
    if cmd=="s":
        return generate_options_shot()
def generate_options_shot()->str:
    if not len(caption_guess_bot):
        white_spaces=get_ships_positions(table_guess_bot)
        white_spaces=white_spaces[BLOCK_IGNORE]
        index_xy=int(random.random()*len(white_spaces[0]))
        position_shot=code_position_table(white_spaces[0][index_xy],white_spaces[1][index_xy])
        
        return 's '+position_shot[0]+' '+position_shot[1]
    ship_guess_id=list(head_tail_bot.keys())[int(random.random()*len(list(head_tail_bot.keys())))]
    ship_head_tail=head_tail_bot[ship_guess_id]
    line_head,colm_head=ship_head_tail[0][0],ship_head_tail[0][1]
    line_tail,colm_tail=ship_head_tail[1][0],ship_head_tail[1][1]

    able_posi=[]
    if table_guess_bot[line_head][colm_head]==BLOCK_IGNORE:
        able_posi.append([line_head,colm_head])
    if table_guess_bot[line_tail][colm_tail]==BLOCK_IGNORE:
        able_posi.append([line_tail,colm_tail])
    index_random=int(random.random()*len(able_posi))
    line_shot,colm_shot=able_posi[index_random][0],able_posi[index_random][1]

    position_shot=code_position_table(line_shot,colm_shot)
    return 's '+position_shot[0]+' '+position_shot[1]
#
def wait_key(key:str)->None: # Needs the root permision to run in linux :/
    while True:
        if keyboard.is_pressed(key):
            break
###
""" Commands
s [line] [column]   -> shot in line x and column y
v [table_name]      -> view a selected table, user or bot table
caption             -> display the user ships caption
score               -> display the current score, i.e, how many ships you have destroy to win and how many the enemy have destroy to win
clear               -> clear the console output
"""

if __name__=='__main__':
    while True:
        size_game=int(random.random()*3)
        ships=[]
        scenario=[]
        scenario_type=0
        if not size_game:
            ships=SHIPS_LITTLE
            scenario=SCENARIOS_LITTLE
            scenario_type=int(random.random()*len(SCENARIOS_LITTLE))
        elif size_game==1:
            ships=SHIPS_NORMAL
            scenario=SCENARIOS_NORMAL
            scenario_type=int(random.random()*len(SCENARIOS_NORMAL))
        elif size_game==2:
            ships=SHIPS_EXTEND
            scenario=SCENARIOS_EXTEND
            scenario_type=int(random.random()*len(SCENARIOS_EXTEND))
        #
        init_game_battleship(scenario[scenario_type][0],scenario[scenario_type][1],ships)
        user=(not int(random.random()*2))
        ##
        view_map(1)
        print("="*int((subprocess.run(["tput","cols"],text=True,capture_output=True)).stdout))
        view_map(0)
        print("="*int((subprocess.run(["tput","cols"],text=True,capture_output=True)).stdout))
        time.sleep(2)
        prev_user_value=-1
        ##
        while not (victory:=check_victory()):
            if prev_user_value!=user and user:
                print("\033[92mUSER ROUND")
                prev_user_value=user
            elif prev_user_value!=user and not user:
                print("\033[94mBOT ROUND")
                prev_user_value=user
            #print(user)
            if user:
                inp=input('*: ')
                print("\033[1A",end='')
                user=move_game_battleship(inp,user)
                continue
            #
            time.sleep(0.5)
            bot_command=generate_command()
            bot_command=generate_options(bot_command)
            print(bot_command)
            user=move_game_battleship(bot_command,user)
        if victory==1:
            print("\033[1;92mYou win!\033[0m")
        else:
            print("\033[1;91mThe enemy win :(\033[0m")
        end_game_battleship()
        time.sleep(1)
