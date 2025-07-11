import vlc
import copy
import time
import random
import subprocess
import unicodedata

DIRECTORY_MUSIC="./musics"
MUSIC_FORMAT="*.mp3"
INFOS_FORMAT="infos.txt"

DIVISOR_VAR_NAME_CONTENT='='

GREEN_COLOR='\033[1;32m'
YELLOW_COLOR='\033[1;33m'
NO_COLOR='\033[0m'
FILL_SYMBOL_CENTER='-'

IGNORE_VARS_MUSIC=["path_audio","path_infos","score"]

class Music:
    def __init__(self,path_audio:str,path_infos:str)->None:
        self.path_audio=path_audio
        self.path_infos=path_infos
    def get_infos(self)->None:
        file=open(self.path_infos,'r')
        prev_name=''
        prev_cont=''
        #
        cont_file=file.read().split('\n')
        for i in cont_file:
            if not len(i):
                continue
            if not DIVISOR_VAR_NAME_CONTENT in i:
                setattr(self,prev_name,prev_cont+'\n'+i)
                prev_cont=self.__dict__[prev_name]
                continue
            name_content=i.split(DIVISOR_VAR_NAME_CONTENT)
            name_content[0]=name_content[0].upper()
            setattr(self,name_content[0],name_content[1])

            prev_name=name_content[0]
            prev_cont=name_content[1]

    def display_infos(self)->None:
        terminal_width=int(subprocess.run(["tput","cols"],text=True,capture_output=True).stdout)
        half_terminal=terminal_width//2
        name=self.__dict__['NAME'].upper()

        print(FILL_SYMBOL_CENTER*half_terminal)
        print(YELLOW_COLOR+name+NO_COLOR)
        print(FILL_SYMBOL_CENTER*half_terminal)
        #
        longest_str=0
        for i in self.__dict__.keys():
            if len(i)>longest_str:
                longest_str=len(i)
        for i in self.__dict__.keys():
            print(f"{i:<{longest_str}} : {self.__dict__[i]}")
class Player:
    def __init__(self)->None:
        self.media_path=None
        self.player=None
        self.player_duration=None
    def define_media(self,media_path:str)->None:
        self.media_path=media_path
        instance=vlc.Instance()
        #
        media=instance.media_new(self.media_path)
        media.parse_with_options(vlc.MediaParseFlag.local,timeout=5000)
        #
        time.sleep(1)
        self.player_duration=media.get_duration()
        #
        self.player=instance.media_player_new()
        self.player.set_media(media)

    def sound_play(self)->None:
        self.player.play()
    def sound_pause(self)->None:
        self.player.pause()
    def sound_stop(self)->None:
        self.player.stop()
        time.sleep(1)
        self.player.set_time(0)
    def sound_reset(self)->None:
        self.player=None
        self.define_media(self.media_path)
        time.sleep(2)

    def get_state(self)->object:
        return self.player.get_state()
    def get_time_pass(self)->int:
        return self.player.get_time()
###
def get_files(path_dir:str,pattern:str)->'list':
    cmd_find=subprocess.run(["find",path_dir,"-name",pattern],text=True,capture_output=True)
    files=cmd_find.stdout.split('\n')
    return files
def get_musics()->'list':
    musics=[]
    path_infos=get_files(DIRECTORY_MUSIC,INFOS_FORMAT)
    path_audios=get_files(DIRECTORY_MUSIC,MUSIC_FORMAT)
    #
    able_audios={}
    for i in path_audios:
        if not len(i):
            continue
        cmd_dirname=subprocess.run(["dirname",i],text=True,capture_output=True)
        parent_dir=cmd_dirname.stdout
        able_audios[parent_dir]=i
    
    for i in path_infos:
        if not len(i):
            continue
        cmd_dirname=subprocess.run(["dirname",i],text=True,capture_output=True)
        parent_dir=cmd_dirname.stdout
        if parent_dir in able_audios.keys():
            musics.append(Music(able_audios[parent_dir],i))

    return musics
##
def init_game_quiz()->None:
    # Musics
    global musics
    # Order musics
    global order_musics
    # Game status
    global game_status
    # Questions
    global music_question
    global music_answer
    # Score
    global score_local
    global score_global

    global score_local_max
    global score_global_max

    global able_questions
    global able_verses

    global score_by_question
    global score_by_question_lyric

    global leading_zeros
    # Commands
    global commands
    # Sound manager
    global player
    ###
    # Musics
    musics=get_musics()
    # Order musics
    order_musics=list(random.sample(musics,len(musics)))
    order_musics[0].get_infos()
    # Game status
    game_status=1 # 1 ->playing 0 -> end
    # Question
    music_question=order_musics.pop(0)
    music_answer={}
    for i in music_question.__dict__.keys():
        music_answer[i]=""
        if i=="LYRIC":
            music_answer[i]={}
    # Score
    get_scores_question()
    leading_zeros=0
    for i in musics:
        object_copy=copy.copy(i)
        object_copy.get_infos()
        object_score=get_score(object_copy)
        #
        if object_score>leading_zeros:
            leading_zeros=object_score
    leading_zeros=len(str(leading_zeros))

    # print(score_by_question,score_local_max)
    # print(score_by_question_lyric,able_verses)
    # Commands
    commands=["reply","next","play","stop","pause","reset","finish","display"]
    # Sound manager
    player=Player()
    player.define_media(music_question.path_audio)
def move_game_quiz(cmd:str)->None:
    global commands
    global game_status

    cmd=cmd.split()
    if not len(cmd) or not cmd[0] in commands:
        print("Invalid command")
        return
    #
    if cmd[0]=="reply" and len(cmd)==1:
        print("The reply command needs, at least, one argument")
        return
    if cmd[0]=="reply" and not cmd[1].upper() in music_question.__dict__.keys():
        print("This attribute doesn't exist in this music")
        return
    if cmd[0]=="reply" and cmd[1].lower()!="lyric":
        check_answer(cmd[1],cmd[2].replace('_',' '))
        count_score()
        display_answer()
        return
    if cmd[0]=="reply" and cmd[1].lower()=="lyric":
        if __name__=='__main__':
            answer=get_answer_lyric_cli()
        #
        check_answer_lyric(answer)
        count_score()
        display_answer()
        return
    if cmd[0]=="next":
        get_next_question()
        display_answer()
        return
    if cmd[0]=="finish":
        game_status=0
        return

    if cmd[0]=="play" and not player.get_state() in [vlc.State.Playing]:
        play()
        return
    if cmd[0]=="play":
        print("The sound already playing")

    if cmd[0]=="pause":
        player.sound_pause()
    if cmd[0]=="stop":
        player.sound_stop()
    if cmd[0]=="reset":
        player.sound_stop()
        player.sound_play()

    if cmd[0]=="display":
        display_answer()
def end_game_quiz()->None:
    # Musics
    global musics
    # Order musics
    global order_musics
    # Game status
    global game_status
    # Questions
    global music_question
    global music_answer
    # Score
    global score_local
    global score_global

    global score_local_max
    global score_global_max

    global able_questions
    global able_verses

    global score_by_question
    global score_by_question_lyric

    global leading_zeros
    # Commands
    global commands
    # Sound manager
    global player
    ###
    # Musics
    del musics
    # Order musics
    del order_musics
    # Game status
    del game_status
    # Questions
    del music_question
    del music_answer
    # Score
    del score_local
    del score_global

    del score_local_max
    del score_global_max

    del able_questions
    del able_verses

    del score_by_question
    del score_by_question_lyric

    del leading_zeros
    # Commands
    del commands
    # Sound manager
    del player
##
def remove_marked_characters(text:str)->str:
    text_formated=unicodedata.normalize('NFD',text)
    text_nolatin=""
    for i in text_formated:
        if unicodedata.combining(i):
            continue
        text_nolatin+=i
    return text_nolatin
##
def get_answer_lyric_cli()->str:
    inp=""
    while True:
        try:
            inp+=input().lower()+'\n'
        except EOFError:
            break
    return inp
##
def get_next_question()->None:
    global music_question
    global music_answer

    global answer
    global order_musics
    #
    if not len(order_musics):
        print("There is no more able music!")
        return
    # print(order_musics)
    music_question=order_musics.pop(0)
    music_question.get_infos()
    music_answer={}
    for i in music_question.__dict__.keys():
        music_answer[i]=""
        if i=="LYRIC":
            music_answer[i]={}
    #
    get_scores_question()
    #
    player.sound_stop()
    player.define_media(music_question.path_audio)
    play()
def check_answer(var_name:str,answer:str)->None:
    # print(music_question.__dict__)
    var_name=var_name.upper()
    if not var_name in  music_question.__dict__.keys():
        print("This attribute aren't in music infos")
        return
    if var_name in music_answer.keys() and music_answer[var_name]==music_question.__dict__[var_name]:
        print("This question already completed")
        return
    answer=answer.lower()
    answer_formated=remove_marked_characters(answer)
    # print(answer)
    #
    if answer_formated==remove_marked_characters(music_question.__dict__[var_name].lower()):
        music_answer[var_name]=music_question.__dict__[var_name]
        print("Correct answer!")
    else:
        print("Incorrect answer")
def check_answer_lyric(answer_lyric:str)->None:
    if not "LYRIC" in music_question.__dict__.keys():
        print("This song doesn't have lyrics")
        return
    lyric_user=answer_lyric.split('\n')
    #
    lyric_correct=music_question.__dict__["LYRIC"].split('\n')
    answer_user={}
    #
    # print(lyric_user)
    for i in lyric_user:
        splited_answer=i.split()
        possible_phrases=[]
        for j in lyric_correct:
            if len(splited_answer)==len(j.split()) and not j in possible_phrases:
                possible_phrases.append(j)
        #
        # print('U: '+i)
        correct_words_cont=[0 for j in range(len(possible_phrases))]
        for j in range(len(possible_phrases)):
            splited_phrase=possible_phrases[j].split()
            for k in range(len(splited_phrase)):
                # print(remove_marked_characters(splited_answer[k]),remove_marked_characters(splited_phrase[k].lower()))
                if remove_marked_characters(splited_answer[k])!=remove_marked_characters(splited_phrase[k].lower()):
                    continue
                correct_words_cont[j]+=1
        print(correct_words_cont,possible_phrases)
        phrases=[]
        phrase_points=0
        for j in range(len(correct_words_cont)):
            if phrase_points<correct_words_cont[j]:
                phrase_points=correct_words_cont[j]

                phrases.clear()
                phrases.append(possible_phrases[j])
            elif phrase_points==correct_words_cont[j]:
                phrases.append(possible_phrases[j])
        for  j in phrases:
            splited_phrase=j.split()
            answer=""
            for k in range(len(splited_phrase)):
                if remove_marked_characters(splited_phrase[k].lower())!=remove_marked_characters(splited_answer[k].lower()):
                    answer+=('-'*len(splited_phrase[k]))+' '
                    continue
                answer+=splited_phrase[k]+' '
            #
            if j in answer_user.keys() and answer_user[j][0]<phrase_points:
                answer_user[j]=[phrase_points,answer.strip()]
                continue
            elif j in answer_user.keys():
                continue
            answer_user[j]=[phrase_points,answer.strip()] # weight of the phrases and the phrases
    #
    """
    for i in answer_user.keys():
        print(i,answer_user[i])
    """
    #
    answer_user_prev={}
    if "LYRIC" in music_answer.keys():
        answer_user_prev=music_answer["LYRIC"]
    
    for i in answer_user_prev.keys():
        key_value_prev=answer_user_prev[i]
        key_value_curr=answer_user[i] if i in answer_user.keys() else None
        # print(i,key_value_prev,key_value_curr)
        if not key_value_curr:
            answer_user[i]=key_value_prev
            continue
        if key_value_prev[0]>key_value_curr[0]:
            answer_user[i]=key_value_prev
    """
    print('====')
    for i in answer_user.keys():
        print(i,answer_user[i])
    """
    music_answer["LYRIC"]=answer_user

def get_score(music)->int:
    if not "SCORE" in music.__dict__.keys():
        return 100
    return int(music.__dict__["SCORE"])
def get_scores_question()->None:
    global music_question

    global score_local
    global score_global

    global score_local_max
    global score_global_max

    global able_questions
    global able_verses

    global score_by_question
    global score_by_question_lyric

    #
    score_local=0
    if not "score_global" in globals():
        score_global=0

    score_local_max=get_score(music_question)
    score_global_max=0
    for i in musics:
        copy_object=copy.copy(i)
        copy_object.get_infos()
        score_global_max+=get_score(copy_object)

    able_questions=len(music_question.__dict__.keys())-len(IGNORE_VARS_MUSIC)
    if not "SCORE" in music_question.__dict__.keys():
        able_questions+=1
    able_verses=len(music_question.__dict__["LYRIC"].split('\n'))-1 if "LYRIC" in music_question.__dict__.keys() else 0

    score_by_question=score_local_max/able_questions
    score_by_question_lyric=score_by_question/able_verses if able_verses else 0
def count_score()->None:
    global music_answer
    global music_question

    global score_local
    global score_global

    global score_by_question
    global score_by_question_lyric
    #
    answer_user=music_answer
    answer_correct=music_question.__dict__

    score_global-=score_local
    score_local=0
    for i in answer_user.keys():
        if answer_user[i]==answer_correct[i]:
            score_local+=score_by_question

    lyric_user=music_answer["LYRIC"] if "LYRIC" in music_answer.keys() else None
    lyric_correct=music_question.__dict__["LYRIC"] if lyric_user else None
    score_global+=score_local
    if not lyric_user:
        return
    score_lyric=0
    for i in lyric_correct.split('\n'):
        if not len(i):
            continue
        if not i in lyric_user.keys():
            continue
        print(len(i.lower()),len(lyric_user[i][1].lower()))
        if i.lower()!=lyric_user[i][1].lower():
            continue
        score_lyric+=score_by_question_lyric
    score_local+=score_lyric
    score_global+=score_lyric
##
def display_answer()->None:
    global music_answer
    global leading_zeros

    global score_local
    global score_local_max
    #
    name=music_answer["NAME"]
    name="No reply yet" if not len(name) else name
    name=name.upper()
    
    score_formated_local=str(round(score_local)).zfill(leading_zeros)
    score_formated_local_max=str(score_local_max).zfill(leading_zeros)
    #
    terminal_width=int(subprocess.run(["tput","cols"],text=True,capture_output=True).stdout)
    half_terminal_width=terminal_width//2
    print(FILL_SYMBOL_CENTER*half_terminal_width)
    print(GREEN_COLOR+name+NO_COLOR)
    print(f"SCORE {score_formated_local}/{score_formated_local_max} ")
    print(FILL_SYMBOL_CENTER*half_terminal_width)
    #
    longest_str=0
    for i in music_answer.keys():
        if i in IGNORE_VARS_MUSIC:
            continue
        if len(i)>longest_str:
            longest_str=len(i)

    for i in music_answer.keys():
        if i.lower() in IGNORE_VARS_MUSIC:
            continue
        i[0].upper()
        if i=="LYRIC":
            print(f"{i:<{longest_str}} = ")
            display_answer_lyric()
            continue
        print(f"{i:<{longest_str}} = {music_answer[i]}")
def display_answer_lyric()->None:
    global music_answer
    global music_question
    #
    if not "LYRIC" in music_question.__dict__.keys():
        print("This song doesn't have lyric")
        return
    lyric_correct=music_question.__dict__["LYRIC"] # string
    lyric_user=music_answer["LYRIC"] # dict

    for i in lyric_correct.split('\n'):
        if not i in lyric_user.keys():
            for j in i.split():
                print('-'*len(j),end=' ')
            print()
            continue
        print(lyric_user[i][1])
##
def play()->None:
    global player
    #
    if player.get_state()==vlc.State.Ended:
        player.sound_reset()
    #
    if player.get_state() in [vlc.State.Paused]:
        print("Resume...")
        player.sound_play()
        return

    for i in range(3):
        print("The sound will begin in {}\r".format(3-i),end='')
        time.sleep(1)
    for i in range(int(subprocess.run(["tput","cols"],text=True,capture_output=True).stdout)):
        print(' ',end='')
    print('\r',end='')
    print("GO!")
    player.sound_play()
###

"""
player=Player()
for i in get_musics():
    i.get_infos()
    i.display_infos()
    #
    player.define_media(i.path_audio)
    player.sound_play()
    print(player.player_duration)
    while player.get_state() != vlc.State.Ended:
        print(player.get_time_pass())
        time.sleep(1)
"""
if __name__=="__main__":
    init_game_quiz()
    display_answer()
    move_game_quiz("play")
    while game_status:
        inp=input('*: ')
        move_game_quiz(inp)
    print("Your final score is {}".format(score_global))
    end_game_quiz()
    print("END!")
