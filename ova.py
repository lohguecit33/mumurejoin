import subprocess #line:1
import time #line:2
import os #line:3
import threading #line:4
import json #line:5
from tabulate import tabulate #line:6
from termcolor import colored #line:7
from colorama import init #line:8
init (autoreset =True )#line:11
if getattr (sys ,'frozen',False ):#line:14
    base_path =sys ._MEIPASS #line:15
else :#line:16
    base_path =os .path .dirname (os .path .abspath (__file__ ))#line:17
ADB_PATH =os .path .join (base_path ,'adb','adb.exe')#line:19
config_file ="roblox_config.txt"#line:22
port_file ="adb_ports.txt"#line:23
PRIVATE_LINK_FILE ="private_links.json"#line:24
def load_config ():#line:27
    if os .path .exists (config_file ):#line:28
        with open (config_file ,'r')as OOOO0O00OO000O0OO :#line:29
            OOO0O0OO0O0OOOO00 =OOOO0O00OO000O0OO .readlines ()#line:30
            if len (OOO0O0OO0O0OOOO00 )>=2 :#line:31
                O0OOO000O0OOOO0O0 =OOO0O0OO0O0OOOO00 [1 ].strip ()#line:32
                return O0OOO000O0OOOO0O0 #line:33
    return None ,None #line:34
def save_config (O0OOOOOOOOO0O0O0O ):#line:37
    with open (config_file ,'w')as O0000OO0O000O00O0 :#line:38
        O0000OO0O000O00O0 .write (f"{O0OOOOOOOOO0O0O0O}")#line:39
    print (colored (f"User ID dan Game ID telah disimpan di {config_file}",'green'))#line:40
def enable_adb_root_for_all (OO00O0O0O0O0O0000 ):#line:43
    for O0O0OO0O0OOO0O000 in OO00O0O0O0O0O0000 :#line:44
        OO0OOOO000O0O0OOO =[ADB_PATH ,"-s",f"127.0.0.1:{O0O0OO0O0OOO0O000}","root"]#line:45
        OOO0O00O00O00O0O0 =subprocess .run (OO0OOOO000O0O0OOO ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE ,text =True )#line:46
        if OOO0O00O00O00O0O0 .returncode !=0 :#line:47
            print (f"Error enabling adb root for emulator {O0O0OO0O0OOO0O000}: {OOO0O00O00O00O0O0.stderr}")#line:48
def get_username_from_prefs (O000OOOOO000O00O0 ):#line:52
    OOOO00OOOO0O0O0OO =[ADB_PATH ,"-s",f'127.0.0.1:{O000OOOOO000O00O0}',"shell","cat","/data/data/com.roblox.client/shared_prefs/prefs.xml"]#line:54
    OO0O0O0O00OO000O0 =subprocess .run (OOOO00OOOO0O0O0OO ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE ,text =True )#line:57
    if OO0O0O0O00OO000O0 .returncode !=0 :#line:58
        print (f"Error: {OO0O0O0O00OO000O0.stderr}")#line:59
        return None #line:60
    O0OO00OOO000O00O0 =OO0O0O0O00OO000O0 .stdout #line:63
    if O0OO00OOO000O00O0 :#line:66
        O00OO0000OOOO00O0 ='<string name="username">'#line:67
        OOO0O000OOOOO0O0O ='</string>'#line:68
        OOOOO00OO0O00OOOO =O0OO00OOO000O00O0 .find (O00OO0000OOOO00O0 )#line:71
        if OOOOO00OO0O00OOOO !=-1 :#line:72
            OOOOO00OO0O00OOOO +=len (O00OO0000OOOO00O0 )#line:73
            O0O00O00000000O00 =O0OO00OOO000O00O0 .find (OOO0O000OOOOO0O0O ,OOOOO00OO0O00OOOO )#line:74
            if O0O00O00000000O00 !=-1 :#line:75
                OO0OOO00O0O000OO0 =O0OO00OOO000O00O0 [OOOOO00OO0O00OOOO :O0O00O00000000O00 ].strip ()#line:77
                return OO0OOO00O0O000OO0 #line:78
    print ("Username tidak ditemukan di prefs.xml.")#line:80
    return None #line:81
def load_ports ():#line:84
    if os .path .exists (port_file ):#line:85
        with open (port_file ,'r')as OO0O0O00O00O0OOO0 :#line:86
            OO00O0OO0O0OOO0OO =OO0O0O00O00O0OOO0 .readlines ()#line:87
            return [OOO000O0OO0000OO0 .strip ()for OOO000O0OO0000OO0 in OO00O0OO0O0OOO0OO ]#line:88
    return []#line:89
def save_ports (O00OOOO00O00O0O00 ):#line:92
    with open (port_file ,'w')as OO0O0000O00O0O000 :#line:94
        for OO0000OO0OOOO0O00 in O00OOOO00O00O0O00 :#line:95
            OO0O0000O00O0O000 .write (f"{OO0000OO0OOOO0O00}\n")#line:96
    print (colored (f"Port ADB telah disimpan di {port_file}",'green'))#line:97
def load_private_links ():#line:100
    try :#line:101
        if os .path .exists (PRIVATE_LINK_FILE ):#line:102
            with open (PRIVATE_LINK_FILE ,"r")as O0000O00O00OO0O00 :#line:103
                return json .load (O0000O00O00OO0O00 )#line:104
        else :#line:105
            return {}#line:106
    except Exception as O0OOO0OOO0O0OO0O0 :#line:107
        print (colored (f"Error memuat private link: {O0OOO0OOO0O0OO0O0}","red"))#line:108
        return {}#line:109
def save_private_link (O0OOO0O00OOOO0O0O ,O000O00000OOOOOOO ):#line:112
    try :#line:113
        O0O000O0O00O0OO0O =load_private_links ()#line:114
        O0O000O0O00O0OO0O [O0OOO0O00OOOO0O0O ]=O000O00000OOOOOOO #line:115
        with open (PRIVATE_LINK_FILE ,"w")as OOO0OO00O0000O00O :#line:116
            json .dump (O0O000O0O00O0OO0O ,OOO0OO00O0000O00O ,indent =4 )#line:117
        print (colored (f"Private link for emulator {O0OOO0O00OOOO0O0O} successfully saved: {O000O00000OOOOOOO}","green"))#line:118
    except Exception as O00OOO0O0O00OO000 :#line:119
        print (colored (f"Error saving private link: {O00OOO0O0O00OO000}","red"))#line:120
def auto_connect_adb (OOOO0OO0000O0O00O ):#line:123
    for OO0OOOOOO0O00O0OO in OOOO0OO0000O0O00O :#line:124
        OOO000O000OOO00O0 =subprocess .run ([ADB_PATH ,'connect',f'127.0.0.1:{OO0OOOOOO0O00O0OO}'],stdout =subprocess .DEVNULL ,stderr =subprocess .PIPE ,text =True )#line:125
        if OOO000O000OOO00O0 .returncode ==0 :#line:126
            enable_adb_root_for_all ([OO0OOOOOO0O00O0OO ])#line:127
        else :#line:128
            print (f"Failed to connect to port {OO0OOOOOO0O00O0OO}: {OOO000O000OOO00O0.stderr}")#line:129
def start_private_server (O00OO00000OOOO00O ,O000O000OOOOO0O0O ):#line:132
    try :#line:133
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{O00OO00000OOOO00O}','shell','am','start','-n','com.roblox.client/com.roblox.client.startup.ActivitySplash','-d',O000O000OOOOO0O0O ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:136
        time .sleep (10 )#line:137
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{O00OO00000OOOO00O}','shell','am','start','-n','com.roblox.client/com.roblox.client.ActivityProtocolLaunch','-d',O000O000OOOOO0O0O ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:140
        time .sleep (8 )#line:141
        print (colored (f"Private link dijalankan di emulator {O00OO00000OOOO00O}.","green"))#line:142
    except Exception as O000OOOOO00O0OOO0 :#line:143
        print (colored (f"Gagal menjalankan Private Server di emulator {O00OO00000OOOO00O}: {O000OOOOO00O0OOO0}","red"))#line:144
def start_default_server (O0OOO00OOO0O000O0 ,OOO0O0OOOO00OO0O0 ):#line:147
    try :#line:148
        OOOO0OOO00OOOOO0O =f"roblox://placeID={OOO0O0OOOO00OO0O0}"#line:149
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{O0OOO00OOO0O000O0}','shell','am','start','-n','com.roblox.client/com.roblox.client.startup.ActivitySplash','-d',OOOO0OOO00OOOOO0O ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:152
        time .sleep (10 )#line:153
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{O0OOO00OOO0O000O0}','shell','am','start','-n','com.roblox.client/com.roblox.client.ActivityProtocolLaunch','-d',OOOO0OOO00OOOOO0O ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:156
        time .sleep (10 )#line:157
        print (Fore .GREEN +f"Membuka game menggunakan server: {OOOO0OOO00OOOOO0O}.")#line:158
    except Exception as OOO0OOOOO00OO00O0 :#line:159
        print (colored (f"Failed to start Default Server: {OOO0OOOOO00OO00O0}",'red'))#line:160
def auto_join_game (OO000OO0O00O0OO0O ,OOOOOO0OO0OO0OO00 ,OO000O0000OOO0OO0 ,O00O0O0OOOOO0O0OO ):#line:163
    O00O0O0OOOOO0O0OO [OO000OO0O00O0OO0O ]="Opening Roblox"#line:164
    update_table (O00O0O0OOOOO0O0OO )#line:165
    if OO000O0000OOO0OO0 :#line:167
        start_private_server (OO000OO0O00O0OO0O ,OO000O0000OOO0OO0 )#line:168
    else :#line:169
        start_default_server (OO000OO0O00O0OO0O ,OOOOOO0OO0OO0OO00 )#line:170
    O00O0O0OOOOO0O0OO [OO000OO0O00O0OO0O ]="Opening the Game"#line:172
    update_table (O00O0O0OOOOO0O0OO )#line:173
    time .sleep (10 )#line:174
    O00O0O0OOOOO0O0OO [OO000OO0O00O0OO0O ]="In Game"#line:176
    update_table (O00O0O0OOOOO0O0OO )#line:177
    time .sleep (1 )#line:178
def ensure_roblox_running_with_interval (OO0OOOO0O00O0OO00 ,OO0OO00O0OO00OO0O ,O0O000O00O00O00O0 ,OOOOOOO0OO00OOOO0 ):#line:181
    O0OO00O000OO00O00 ={O00O0OOOO0OOO0O00 :"waiting"for O00O0OOOO0OOO0O00 in OO0OOOO0O00O0OO00 }#line:182
    update_table (O0OO00O000OO00O00 )#line:183
    OO0OOOO0O00OOOO00 =OOOOOOO0OO00OOOO0 *60 #line:185
    OO000OO0OO000OOO0 =time .time ()#line:186
    while True :#line:188
        O0OO0O0O0000O000O =time .time ()-OO000OO0OO000OOO0 #line:189
        for O0OOO0O0O0OO0O0O0 in OO0OOOO0O00O0OO00 :#line:190
            OO000O0000OOO00OO =O0O000O00O00O00O0 .get (O0OOO0O0O0OO0O0O0 )#line:191
            if check_roblox_running (O0OOO0O0O0OO0O0O0 ):#line:192
                O0OO00O000OO00O00 [O0OOO0O0O0OO0O0O0 ]="In Game"#line:193
                update_table (O0OO00O000OO00O00 )#line:194
            else :#line:195
                O0OO00O000OO00O00 [O0OOO0O0O0OO0O0O0 ]="roblox offline"#line:196
                update_table (O0OO00O000OO00O00 )#line:197
                force_close_roblox (O0OOO0O0O0OO0O0O0 )#line:198
                auto_join_game (O0OOO0O0O0OO0O0O0 ,OO0OO00O0OO00OO0O ,OO000O0000OOO00OO ,O0OO00O000OO00O00 )#line:199
        if OOOOOOO0OO00OOOO0 >0 and O0OO0O0O0000O000O >=OO0OOOO0O00OOOO00 :#line:201
            for O0OOO0O0O0OO0O0O0 in OO0OOOO0O00O0OO00 :#line:202
                OO000O0000OOO00OO =O0O000O00O00O00O0 .get (O0OOO0O0O0OO0O0O0 )#line:203
                O0OO00O000OO00O00 [O0OOO0O0O0OO0O0O0 ]="roblox offline"#line:204
                update_table (O0OO00O000OO00O00 )#line:205
                force_close_roblox (O0OOO0O0O0OO0O0O0 )#line:206
                auto_join_game (O0OOO0O0O0OO0O0O0 ,OO0OO00O0OO00OO0O ,OO000O0000OOO00OO ,O0OO00O000OO00O00 )#line:207
            OO000OO0OO000OOO0 =time .time ()#line:208
        time .sleep (5 )#line:209
def check_roblox_running (OOOO0O0OOO0000000 ):#line:212
    try :#line:213
        O00O0O0OO000OO00O =subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OOOO0O0OOO0000000}','shell','pidof','com.roblox.client'],stdout =subprocess .PIPE ,stderr =subprocess .PIPE ,text =True )#line:217
        return bool (O00O0O0OO000OO00O .stdout .strip ())#line:218
    except Exception as O00O00O00O000O00O :#line:219
        print (colored (f"Error checking if Roblox is running on {OOOO0O0OOO0000000}: {O00O00O00O000O00O}",'red'))#line:220
        return False #line:221
def force_close_roblox (OOO0OOOOO000OO00O ):#line:224
    subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OOO0OOOOO000OO00O}','shell','am','force-stop','com.roblox.client'],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:226
    time .sleep (8 )#line:227
def start_instance_in_thread (OO0OOOO0OO0O0OOOO ,OOO00OOO00OOOOO00 ,OOOO0000O000OO0O0 ,O00OOOOO00000OO00 ):#line:230
    O00000000OO0OOOOO =[]#line:231
    for O0O000000OOOO0O0O in OO0OOOO0OO0O0OOOO :#line:232
        O000O00O0OOOOOO0O =threading .Thread (target =auto_join_game ,args =(O0O000000OOOO0O0O ,OOO00OOO00OOOOO00 ,OOOO0000O000OO0O0 .get (O0O000000OOOO0O0O ),O00OOOOO00000OO00 ))#line:233
        O000O00O0OOOOOO0O .start ()#line:234
        O00000000OO0OOOOO .append (O000O00O0OOOOOO0O )#line:235
    for O0O000000OOOO0O0O in OO0OOOO0OO0O0OOOO :#line:237
        OO00O0OO0O0OOO00O =threading .Thread (target =ensure_roblox_running_with_interval ,args =([O0O000000OOOO0O0O ],OOO00OOO00OOOOO00 ,OOOO0000O000OO0O0 ,1 ))#line:238
        OO00O0OO0O0OOO00O .start ()#line:239
        O00000000OO0OOOOO .append (OO00O0OO0O0OOO00O )#line:240
    for O000O00O0OOOOOO0O in O00000000OO0OOOOO :#line:242
        O000O00O0OOOOOO0O .join ()#line:243
def update_table (O0OO00O00OO0OO00O ):#line:246
    os .system ('cls'if os .name =='nt'else 'clear')#line:247
    O0O00O000OO000O0O =[]#line:248
    for O0OOOOO0OOOO00000 ,OO0O00OOO0O00O000 in O0OO00O00OO0OO00O .items ():#line:249
        O0OO0O00000O00O0O =get_username_from_prefs (O0OOOOO0OOOO00000 )#line:250
        if OO0O00OOO0O00O000 =="In Game":#line:251
            O00000O00OOOOO00O ='green'#line:252
        elif OO0O00OOO0O00O000 =="Opening the Game":#line:253
            O00000O00OOOOO00O ='cyan'#line:254
        elif OO0O00OOO0O00O000 =="Opening Roblox":#line:255
            O00000O00OOOOO00O ='yellow'#line:256
        elif OO0O00OOO0O00O000 =="roblox offline":#line:257
            O00000O00OOOOO00O ='red'#line:258
        else :#line:259
            O00000O00OOOOO00O ='magenta'#line:260
        O0O00O000OO000O0O .append ({"NAME":f"emulator:{O0OOOOO0OOOO00000}","Username":O0OO0O00000O00O0O or "Not Found","Proses":colored (OO0O00OOO0O00O000 ,O00000O00OOOOO00O )})#line:262
    print (tabulate (O0O00O000OO000O0O ,headers ="keys",tablefmt ="grid"))#line:264
    print (colored ("BANG OVA",'blue',attrs =['bold','underline']).center (50 ))#line:265
def menu ():#line:268
    O0O0O00OOOO0OO0O0 =load_config ()#line:269
    O0O0O0O00OOOOO00O =load_ports ()#line:270
    OO0O0O0OO00O0000O =load_private_links ()#line:271
    if O0O0O0O00OOOOO00O :#line:273
        auto_connect_adb (O0O0O0O00OOOOO00O )#line:274
    else :#line:275
        print (colored ("ADB port not found. Please set it first..",'yellow'))#line:276
    if O0O0O00OOOO0OO0O0 :#line:278
        print (colored (f"Game ID: {O0O0O00OOOO0OO0O0} has been loaded from configuration.",'green'))#line:279
    else :#line:280
        print (colored ("User ID dan Game ID not set yet. Please set it first.",'yellow'))#line:281
    while True :#line:283
        print ("\nMenu:")#line:284
        print ("1. Auto join")#line:285
        print ("2. Set Game ID")#line:286
        print ("3. Set Port ADB")#line:287
        print ("4. Set private code for all instances")#line:288
        print ("5. Set private code for 1 instance")#line:289
        print ("6. Exit")#line:290
        O0O000O000O0OOO00 =input ("Select number (1/2/3/4/5/6): ")#line:292
        if O0O000O000O0OOO00 =='1':#line:294
            if not O0O0O00OOOO0OO0O0 :#line:295
                print (colored ("Game ID has not been set. Please set it first.",'red'))#line:296
                continue #line:297
            OO0000000O0O0O00O =int (input ("Enter the time interval (in minutes, enter 0 for no interval).: "))#line:298
            ensure_roblox_running_with_interval (O0O0O0O00OOOOO00O ,O0O0O00OOOO0OO0O0 ,OO0O0O0OO00O0000O ,OO0000000O0O0O00O )#line:299
        elif O0O000O000O0OOO00 =='2':#line:300
            O0O0O00OOOO0OO0O0 =input ("Enter Game ID: ")#line:301
            save_config (O0O0O00OOOO0OO0O0 )#line:302
        elif O0O000O000O0OOO00 =='3':#line:303
            O0OOOO0O0OOOOOO00 =input ("Enter the ADB port (separate with commas if more than one).: ").split (',')#line:304
            save_ports ([O00OO0O00OO0O000O .strip ()for O00OO0O00OO0O000O in O0OOOO0O0OOOOOO00 ])#line:305
            O0O0O0O00OOOOO00O =O0OOOO0O0OOOOOO00 #line:306
            auto_connect_adb (O0O0O0O00OOOOO00O )#line:307
        elif O0O000O000O0OOO00 =='4':#line:308
            OO0O0OO0O00OO00O0 =input ("Enter private code for all instances.(only support link like this https://www.roblox.com/games/2753915549/DRAGON-Blox-Fruits?privateServerLinkCode=313232213213123123131): ").strip ()#line:309
            for OO0OO00O0OO000OO0 in O0O0O0O00OOOOO00O :#line:310
                save_private_link (OO0OO00O0OO000OO0 ,OO0O0OO0O00OO00O0 )#line:311
                OO0O0O0OO00O0000O =load_private_links ()#line:312
        elif O0O000O000O0OOO00 =='5':#line:313
            OOOOOO0O0OOO0OOOO =input ("Enter the instance port: ").strip ()#line:314
            OO0O0OO0O00OO00O0 =input ("Enter the private code for this instance.(only support link like this https://www.roblox.com/games/2753915549/DRAGON-Blox-Fruits?privateServerLinkCode=313232213213123123131): ").strip ()#line:315
            save_private_link (OOOOOO0O0OOO0OOOO ,OO0O0OO0O00OO00O0 )#line:316
            OO0O0O0OO00O0000O =load_private_links ()#line:317
        elif O0O000O000O0OOO00 =='6':#line:318
            print ("Exit the program...")#line:319
            break #line:320
        else :#line:321
            print ("Invalid selection!")#line:322
menu ()
