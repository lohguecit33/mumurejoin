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
        with open (config_file ,'r')as O0O0OO0O0OOOOOO00 :#line:29
            O0O0OOO00OO0OO0OO =O0O0OO0O0OOOOOO00 .readlines ()#line:30
            if len (O0O0OOO00OO0OO0OO )>=2 :#line:31
                O000OO000OOO00OOO =O0O0OOO00OO0OO0OO [1 ].strip ()#line:32
                return O000OO000OOO00OOO #line:33
    return None ,None #line:34
def save_config (O0O00O00000O00OOO ):#line:37
    with open (config_file ,'w')as OOO00OO0OOOOOO00O :#line:38
        OOO00OO0OOOOOO00O .write (f"{O0O00O00000O00OOO}")#line:39
    print (colored (f"User ID dan Game ID telah disimpan di {config_file}",'green'))#line:40
def enable_adb_root_for_all (O0OO0O0OO00OO00O0 ):#line:43
    for O0O00O00OOO0O00O0 in O0OO0O0OO00OO00O0 :#line:44
        O0O0OO0O0OO00OOO0 =[ADB_PATH ,"-s",f"127.0.0.1:{O0O00O00OOO0O00O0}","root"]#line:45
        OOO0OO0O0O0O00000 =subprocess .run (O0O0OO0O0OO00OOO0 ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE ,text =True )#line:46
        if OOO0OO0O0O0O00000 .returncode !=0 :#line:47
            print (f"Error enabling adb root for emulator {O0O00O00OOO0O00O0}: {OOO0OO0O0O0O00000.stderr}")#line:48
def get_username_from_prefs (O0O000OOOOO0OOOOO ):#line:52
    O000OOO0O0000OOOO =[ADB_PATH ,"-s",f'127.0.0.1:{O0O000OOOOO0OOOOO}',"shell","cat","/data/data/com.roblox.client/shared_prefs/prefs.xml"]#line:54
    OO0O000O00O0OOO00 =subprocess .run (O000OOO0O0000OOOO ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE ,text =True )#line:57
    if OO0O000O00O0OOO00 .returncode !=0 :#line:58
        print (f"Error: {OO0O000O00O0OOO00.stderr}")#line:59
        return None #line:60
    OO00000OO000O00OO =OO0O000O00O0OOO00 .stdout #line:63
    if OO00000OO000O00OO :#line:66
        OO00O0OO0O0O00OO0 ='<string name="username">'#line:67
        OO0OO000O00OOO0OO ='</string>'#line:68
        O0O0O00O00O0OOOOO =OO00000OO000O00OO .find (OO00O0OO0O0O00OO0 )#line:71
        if O0O0O00O00O0OOOOO !=-1 :#line:72
            O0O0O00O00O0OOOOO +=len (OO00O0OO0O0O00OO0 )#line:73
            OOOOO0O0O00O0O00O =OO00000OO000O00OO .find (OO0OO000O00OOO0OO ,O0O0O00O00O0OOOOO )#line:74
            if OOOOO0O0O00O0O00O !=-1 :#line:75
                OO000O0O00OO0OOO0 =OO00000OO000O00OO [O0O0O00O00O0OOOOO :OOOOO0O0O00O0O00O ].strip ()#line:77
                return OO000O0O00OO0OOO0 #line:78
    print ("Username tidak ditemukan di prefs.xml.")#line:80
    return None #line:81
def load_ports ():#line:84
    if os .path .exists (port_file ):#line:85
        with open (port_file ,'r')as O00000O0O0O00O0OO :#line:86
            O00O000000OO00OOO =O00000O0O0O00O0OO .readlines ()#line:87
            return [O0000O000OO000OOO .strip ()for O0000O000OO000OOO in O00O000000OO00OOO ]#line:88
    return []#line:89
def save_ports (O0OOOOOO0OOO0000O ):#line:92
    with open (port_file ,'w')as O0000000OOO0000OO :#line:94
        for OOO0O000O00OOO000 in O0OOOOOO0OOO0000O :#line:95
            O0000000OOO0000OO .write (f"{OOO0O000O00OOO000}\n")#line:96
    print (colored (f"Port ADB telah disimpan di {port_file}",'green'))#line:97
def load_private_links ():#line:100
    try :#line:101
        if os .path .exists (PRIVATE_LINK_FILE ):#line:102
            with open (PRIVATE_LINK_FILE ,"r")as OO0O0OOOO0OOOOO0O :#line:103
                return json .load (OO0O0OOOO0OOOOO0O )#line:104
        else :#line:105
            return {}#line:106
    except Exception as O000O0OOOOOOO00O0 :#line:107
        print (colored (f"Error memuat private link: {O000O0OOOOOOO00O0}","red"))#line:108
        return {}#line:109
def save_private_link (O0O0OO0OOOOOOOO00 ,O0O00O00000OOOOO0 ):#line:112
    try :#line:113
        O0OOO0OO00O0O0O0O =load_private_links ()#line:114
        O0OOO0OO00O0O0O0O [O0O0OO0OOOOOOOO00 ]=O0O00O00000OOOOO0 #line:115
        with open (PRIVATE_LINK_FILE ,"w")as O0OO0000OO000OOOO :#line:116
            json .dump (O0OOO0OO00O0O0O0O ,O0OO0000OO000OOOO ,indent =4 )#line:117
        print (colored (f"Private link for emulator {O0O0OO0OOOOOOOO00} successfully saved: {O0O00O00000OOOOO0}","green"))#line:118
    except Exception as OO000O0O000O0O00O :#line:119
        print (colored (f"Error saving private link: {OO000O0O000O0O00O}","red"))#line:120
def auto_connect_adb (O000OO0OO00000OOO ):#line:123
    for OO0O00OOOOO0000O0 in O000OO0OO00000OOO :#line:124
        OOOO0OOOO0OOO0OOO =subprocess .run ([ADB_PATH ,'connect',f'127.0.0.1:{OO0O00OOOOO0000O0}'],stdout =subprocess .DEVNULL ,stderr =subprocess .PIPE ,text =True )#line:125
        if OOOO0OOOO0OOO0OOO .returncode ==0 :#line:126
            enable_adb_root_for_all ([OO0O00OOOOO0000O0 ])#line:127
        else :#line:128
            print (f"Failed to connect to port {OO0O00OOOOO0000O0}: {OOOO0OOOO0OOO0OOO.stderr}")#line:129
def start_private_server (OOO00OOOOO0OO0O00 ,OO00OO0O00OOO0O0O ):#line:132
    try :#line:133
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OOO00OOOOO0OO0O00}','shell','am','start','-n','com.roblox.client/com.roblox.client.startup.ActivitySplash','-d',OO00OO0O00OOO0O0O ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:136
        time .sleep (10 )#line:137
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OOO00OOOOO0OO0O00}','shell','am','start','-n','com.roblox.client/com.roblox.client.ActivityProtocolLaunch','-d',OO00OO0O00OOO0O0O ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:140
        time .sleep (8 )#line:141
        print (colored (f"Private link dijalankan di emulator {OOO00OOOOO0OO0O00}.","green"))#line:142
    except Exception as OO0O0O00O00OOOOO0 :#line:143
        print (colored (f"Gagal menjalankan Private Server di emulator {OOO00OOOOO0OO0O00}: {OO0O0O00O00OOOOO0}","red"))#line:144
def start_default_server (OOO000O0OO0OO00OO ,O0O0O0000OO00O00O ):#line:147
    try :#line:148
        OOOO000000OOO00OO =f"roblox://placeID={O0O0O0000OO00O00O}"#line:149
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OOO000O0OO0OO00OO}','shell','am','start','-n','com.roblox.client/com.roblox.client.startup.ActivitySplash','-d',OOOO000000OOO00OO ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:152
        time .sleep (10 )#line:153
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OOO000O0OO0OO00OO}','shell','am','start','-n','com.roblox.client/com.roblox.client.ActivityProtocolLaunch','-d',OOOO000000OOO00OO ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:156
        time .sleep (10 )#line:157
        print (Fore .GREEN +f"Membuka game menggunakan server: {OOOO000000OOO00OO}.")#line:158
    except Exception as OO00OOO00000O00OO :#line:159
        print (colored (f"Failed to start Default Server: {OO00OOO00000O00OO}",'red'))#line:160
def auto_join_game (OO00OO000O0OOOO0O ,OO00O000OO00O0O0O ,OOOOOO0O0O0O000OO ,O000OOOOO0OO00O00 ):#line:163
    O000OOOOO0OO00O00 [OO00OO000O0OOOO0O ]="Opening Roblox"#line:164
    update_table (O000OOOOO0OO00O00 )#line:165
    if OOOOOO0O0O0O000OO :#line:167
        start_private_server (OO00OO000O0OOOO0O ,OOOOOO0O0O0O000OO )#line:168
    else :#line:169
        start_default_server (OO00OO000O0OOOO0O ,OO00O000OO00O0O0O )#line:170
    O000OOOOO0OO00O00 [OO00OO000O0OOOO0O ]="Opening the Game"#line:172
    update_table (O000OOOOO0OO00O00 )#line:173
    time .sleep (10 )#line:174
    O000OOOOO0OO00O00 [OO00OO000O0OOOO0O ]="In Game"#line:176
    update_table (O000OOOOO0OO00O00 )#line:177
    time .sleep (1 )#line:178
def ensure_roblox_running_with_interval (O0000O0O000O0OOO0 ,O0O0O0OOO00OO000O ,OO000O0O0O000OO0O ,OOO0O000OO00O0O00 ):#line:181
    OO000OO000OO00OO0 ={O00O0O00OO0O0OO0O :"waiting"for O00O0O00OO0O0OO0O in O0000O0O000O0OOO0 }#line:182
    update_table (OO000OO000OO00OO0 )#line:183
    OO0O00O000000OO0O =OOO0O000OO00O0O00 *60 #line:185
    OOOOOOOO0OO00OOOO =time .time ()#line:186
    while True :#line:188
        O0O0000OOOO0OO0OO =time .time ()-OOOOOOOO0OO00OOOO #line:189
        for OOOO00OO00O00000O in O0000O0O000O0OOO0 :#line:190
            OOOO0000000OO00O0 =OO000O0O0O000OO0O .get (OOOO00OO00O00000O )#line:191
            if check_roblox_running (OOOO00OO00O00000O ):#line:192
                OO000OO000OO00OO0 [OOOO00OO00O00000O ]="In Game"#line:193
                update_table (OO000OO000OO00OO0 )#line:194
            else :#line:195
                OO000OO000OO00OO0 [OOOO00OO00O00000O ]="roblox offline"#line:196
                update_table (OO000OO000OO00OO0 )#line:197
                force_close_roblox (OOOO00OO00O00000O )#line:198
                auto_join_game (OOOO00OO00O00000O ,O0O0O0OOO00OO000O ,OOOO0000000OO00O0 ,OO000OO000OO00OO0 )#line:199
        if OOO0O000OO00O0O00 >0 and O0O0000OOOO0OO0OO >=OO0O00O000000OO0O :#line:201
            for OOOO00OO00O00000O in O0000O0O000O0OOO0 :#line:202
                OOOO0000000OO00O0 =OO000O0O0O000OO0O .get (OOOO00OO00O00000O )#line:203
                OO000OO000OO00OO0 [OOOO00OO00O00000O ]="roblox offline"#line:204
                update_table (OO000OO000OO00OO0 )#line:205
                force_close_roblox (OOOO00OO00O00000O )#line:206
                auto_join_game (OOOO00OO00O00000O ,O0O0O0OOO00OO000O ,OOOO0000000OO00O0 ,OO000OO000OO00OO0 )#line:207
            OOOOOOOO0OO00OOOO =time .time ()#line:208
        time .sleep (5 )#line:209
def check_roblox_running (OOOO0O000O000OOOO ):#line:212
    try :#line:213
        OO0O0OO00OOO0000O =subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OOOO0O000O000OOOO}','shell','pidof','com.roblox.client'],stdout =subprocess .PIPE ,stderr =subprocess .PIPE ,text =True )#line:217
        return bool (OO0O0OO00OOO0000O .stdout .strip ())#line:218
    except Exception as OO000000OO00OO000 :#line:219
        print (colored (f"Error checking if Roblox is running on {OOOO0O000O000OOOO}: {OO000000OO00OO000}",'red'))#line:220
        return False #line:221
def force_close_roblox (OO0000O0OOOO00O0O ):#line:224
    subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OO0000O0OOOO00O0O}','shell','am','force-stop','com.roblox.client'],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:226
    time .sleep (8 )#line:227
def start_instance_in_thread (OOO00000O000OO00O ,OO0O00OO0O0OOOOO0 ,OO0OOOO00OOO000O0 ,OO0O0O00OO000OO0O ):#line:230
    O0O0000O00O00OO00 =[]#line:231
    for O0OO0O0O00O0OOO00 in OOO00000O000OO00O :#line:232
        O00OO0OO0O0000OO0 =threading .Thread (target =auto_join_game ,args =(O0OO0O0O00O0OOO00 ,OO0O00OO0O0OOOOO0 ,OO0OOOO00OOO000O0 .get (O0OO0O0O00O0OOO00 ),OO0O0O00OO000OO0O ))#line:233
        O00OO0OO0O0000OO0 .start ()#line:234
        O0O0000O00O00OO00 .append (O00OO0OO0O0000OO0 )#line:235
    for O0OO0O0O00O0OOO00 in OOO00000O000OO00O :#line:237
        OO0OOO0O00000OOOO =threading .Thread (target =ensure_roblox_running_with_interval ,args =([O0OO0O0O00O0OOO00 ],OO0O00OO0O0OOOOO0 ,OO0OOOO00OOO000O0 ,1 ))#line:238
        OO0OOO0O00000OOOO .start ()#line:239
        O0O0000O00O00OO00 .append (OO0OOO0O00000OOOO )#line:240
    for O00OO0OO0O0000OO0 in O0O0000O00O00OO00 :#line:242
        O00OO0OO0O0000OO0 .join ()#line:243
def update_table (O00O00O0O0OO0OOOO ):#line:246
    os .system ('cls'if os .name =='nt'else 'clear')#line:247
    OOO0000O00O0O00O0 =[]#line:248
    for OO00000O00000O00O ,O00O0O0OOOO0000OO in O00O00O0O0OO0OOOO .items ():#line:249
        O0OO00O0OOO0OO000 =get_username_from_prefs (OO00000O00000O00O )#line:250
        if O00O0O0OOOO0000OO =="In Game":#line:251
            OOOOO0OO000O0OO0O ='green'#line:252
        elif O00O0O0OOOO0000OO =="Opening the Game":#line:253
            OOOOO0OO000O0OO0O ='cyan'#line:254
        elif O00O0O0OOOO0000OO =="Opening Roblox":#line:255
            OOOOO0OO000O0OO0O ='yellow'#line:256
        elif O00O0O0OOOO0000OO =="roblox offline":#line:257
            OOOOO0OO000O0OO0O ='red'#line:258
        else :#line:259
            OOOOO0OO000O0OO0O ='magenta'#line:260
        OOO0000O00O0O00O0 .append ({"NAME":f"emulator:{OO00000O00000O00O}","Username":O0OO00O0OOO0OO000 or "Not Found","Proses":colored (O00O0O0OOOO0000OO ,OOOOO0OO000O0OO0O )})#line:262
    print (tabulate (OOO0000O00O0O00O0 ,headers ="keys",tablefmt ="grid"))#line:264
    print (colored ("BANG OVA",'blue',attrs =['bold','underline']).center (50 ))#line:265
def menu ():#line:268
    OO000OOO0000O000O =load_config ()#line:269
    O0OO0O000000OO0OO =load_ports ()#line:270
    OOO0O0OO0O0O0OOO0 =load_private_links ()#line:271
    if O0OO0O000000OO0OO :#line:273
        auto_connect_adb (O0OO0O000000OO0OO )#line:274
    else :#line:275
        print (colored ("ADB port not found. Please set it first..",'yellow'))#line:276
    if OO000OOO0000O000O :#line:278
        print (colored (f"Game ID: {OO000OOO0000O000O} has been loaded from configuration.",'green'))#line:279
    else :#line:280
        print (colored ("Game ID not set yet. Please set it first.",'yellow'))#line:281
    while True :#line:283
        print ("\nMenu:")#line:284
        print ("1. Auto join")#line:285
        print ("2. Game ID")#line:286
        print ("3. Set Port ADB")#line:287
        print ("4. Set private code for all instances")#line:288
        print ("5. Set private code for 1 instance")#line:289
        print ("6. Exit")#line:290
        OOOO00OO00O00O00O =input ("Select number (1/2/3/4/5/6): ")#line:292
        if OOOO00OO00O00O00O =='1':#line:294
            if not OO000OOO0000O000O :#line:295
                print (colored ("Game ID has not been set. Please set it first.",'red'))#line:296
                continue #line:297
            OO0OO00O00OO00OO0 =int (input ("Enter the time interval (in minutes, enter 0 for no interval).: "))#line:298
            ensure_roblox_running_with_interval (O0OO0O000000OO0OO ,OO000OOO0000O000O ,OOO0O0OO0O0O0OOO0 ,OO0OO00O00OO00OO0 )#line:299
        elif OOOO00OO00O00O00O =='2':#line:300
            OO000OOO0000O000O =input ("Enter Game ID: ")#line:301
            save_config (OO000OOO0000O000O )#line:302
        elif OOOO00OO00O00O00O =='3':#line:303
            O0O00O0O0O0OO000O =input ("Enter the ADB port (separate with commas if more than one).: ").split (',')#line:304
            save_ports ([O0OOO00OOOO0O0O00 .strip ()for O0OOO00OOOO0O0O00 in O0O00O0O0O0OO000O ])#line:305
            O0OO0O000000OO0OO =O0O00O0O0O0OO000O #line:306
            auto_connect_adb (O0OO0O000000OO0OO )#line:307
        elif OOOO00OO00O00O00O =='4':#line:308
            OOO0000OO0OO0O0OO =input ("Enter private code for all instances.(only support link like this https://www.roblox.com/games/2753915549/DRAGON-Blox-Fruits?privateServerLinkCode=313232213213123123131): ").strip ()#line:309
            for OOOO0OO000O00000O in O0OO0O000000OO0OO :#line:310
                save_private_link (OOOO0OO000O00000O ,OOO0000OO0OO0O0OO )#line:311
                OOO0O0OO0O0O0OOO0 =load_private_links ()#line:312
        elif OOOO00OO00O00O00O =='5':#line:313
            OO0O000O00OOO000O =input ("Enter the instance port: ").strip ()#line:314
            OOO0000OO0OO0O0OO =input ("Enter the private code for this instance.(only support link like this https://www.roblox.com/games/2753915549/DRAGON-Blox-Fruits?privateServerLinkCode=313232213213123123131): ").strip ()#line:315
            save_private_link (OO0O000O00OOO000O ,OOO0000OO0OO0O0OO )#line:316
            OOO0O0OO0O0O0OOO0 =load_private_links ()#line:317
        elif OOOO00OO00O00O00O =='6':#line:318
            print ("Exit the program...")#line:319
            break #line:320
        else :#line:321
            print ("Invalid selection!")#line:322
menu ()
