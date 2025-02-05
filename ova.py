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
        with open (config_file ,'r')as OOOOOOOO0000O0OO0 :#line:29
            O0OO00000O000O0OO =OOOOOOOO0000O0OO0 .readlines ()#line:30
            if len (O0OO00000O000O0OO )>=2 :#line:31
                OO0OO000OOO0O0O0O =O0OO00000O000O0OO [1 ].strip ()#line:32
                return OO0OO000OOO0O0O0O #line:33
    return None ,None #line:34
def save_config (O00O0OO00O0OOOOOO ):#line:37
    with open (config_file ,'w')as OO00OOO00O0000OOO :#line:38
        OO00OOO00O0000OOO .write (f"{O00O0OO00O0OOOOOO}")#line:39
    print (colored (f"User ID dan Game ID telah disimpan di {config_file}",'green'))#line:40
def enable_adb_root_for_all (OOOOOOOO0OOO00000 ):#line:43
    for O0O0OO0000000000O in OOOOOOOO0OOO00000 :#line:44
        O0O00O0O0O00O0O0O =[ADB_PATH ,"-s",f"127.0.0.1:{O0O0OO0000000000O}","root"]#line:45
        OOO0OOO00OO0O0OOO =subprocess .run (O0O00O0O0O00O0O0O ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE ,text =True )#line:46
        if OOO0OOO00OO0O0OOO .returncode !=0 :#line:47
            print (f"Error enabling adb root for emulator {O0O0OO0000000000O}: {OOO0OOO00OO0O0OOO.stderr}")#line:48
def get_username_from_prefs (O0O00000000O000OO ):#line:52
    OOO0O000OOOOO0OO0 =[ADB_PATH ,"-s",f'127.0.0.1:{O0O00000000O000OO}',"shell","cat","/data/data/com.roblox.client/shared_prefs/prefs.xml"]#line:54
    OO000OO00OO00OOO0 =subprocess .run (OOO0O000OOOOO0OO0 ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE ,text =True )#line:57
    if OO000OO00OO00OOO0 .returncode !=0 :#line:58
        print (f"Error: {OO000OO00OO00OOO0.stderr}")#line:59
        return None #line:60
    OO0O0OO0OO0000O0O =OO000OO00OO00OOO0 .stdout #line:63
    if OO0O0OO0OO0000O0O :#line:66
        O0000O0O00O0O0000 ='<string name="username">'#line:67
        O00000OOOO00O000O ='</string>'#line:68
        OO00OOOO00000OO0O =OO0O0OO0OO0000O0O .find (O0000O0O00O0O0000 )#line:71
        if OO00OOOO00000OO0O !=-1 :#line:72
            OO00OOOO00000OO0O +=len (O0000O0O00O0O0000 )#line:73
            OOO0OOOOO000O000O =OO0O0OO0OO0000O0O .find (O00000OOOO00O000O ,OO00OOOO00000OO0O )#line:74
            if OOO0OOOOO000O000O !=-1 :#line:75
                O000O00OOOO000O0O =OO0O0OO0OO0000O0O [OO00OOOO00000OO0O :OOO0OOOOO000O000O ].strip ()#line:77
                return O000O00OOOO000O0O #line:78
    print ("Username tidak ditemukan di prefs.xml.")#line:80
    return None #line:81
def load_ports ():#line:84
    if os .path .exists (port_file ):#line:85
        with open (port_file ,'r')as O00O00OO0O0OOO0OO :#line:86
            O0O0O00O0OOO000OO =O00O00OO0O0OOO0OO .readlines ()#line:87
            return [O0OOO00O000OOOO00 .strip ()for O0OOO00O000OOOO00 in O0O0O00O0OOO000OO ]#line:88
    return []#line:89
def save_ports (O00O0OOO0OO00O0OO ):#line:92
    with open (port_file ,'w')as O00OO0000O00O0OOO :#line:94
        for OO0O0OOO00000000O in O00O0OOO0OO00O0OO :#line:95
            O00OO0000O00O0OOO .write (f"{OO0O0OOO00000000O}\n")#line:96
    print (colored (f"Port ADB telah disimpan di {port_file}",'green'))#line:97
def load_private_links ():#line:100
    try :#line:101
        if os .path .exists (PRIVATE_LINK_FILE ):#line:102
            with open (PRIVATE_LINK_FILE ,"r")as O000OO0O0O0O00O0O :#line:103
                return json .load (O000OO0O0O0O00O0O )#line:104
        else :#line:105
            return {}#line:106
    except Exception as OOO0OO0OOO0000OOO :#line:107
        print (colored (f"Error memuat private link: {OOO0OO0OOO0000OOO}","red"))#line:108
        return {}#line:109
def save_private_link (O000O0OOO0OO00O0O ,O0OO0OO0OOOO0OOOO ):#line:112
    try :#line:113
        OO0O000O0OO0O0000 =load_private_links ()#line:114
        OO0O000O0OO0O0000 [O000O0OOO0OO00O0O ]=O0OO0OO0OOOO0OOOO #line:115
        with open (PRIVATE_LINK_FILE ,"w")as O0000OO00O000OO00 :#line:116
            json .dump (OO0O000O0OO0O0000 ,O0000OO00O000OO00 ,indent =4 )#line:117
        print (colored (f"Private link for emulator {O000O0OOO0OO00O0O} successfully saved: {O0OO0OO0OOOO0OOOO}","green"))#line:118
    except Exception as OOO00OOOO00O0000O :#line:119
        print (colored (f"Error saving private link: {OOO00OOOO00O0000O}","red"))#line:120
def auto_connect_adb (O0O000OOO00O0O0OO ):#line:123
    for OO0OO0O000O000OOO in O0O000OOO00O0O0OO :#line:124
        OOO0OOOO00OOOO000 =subprocess .run ([ADB_PATH ,'connect',f'127.0.0.1:{OO0OO0O000O000OOO}'],stdout =subprocess .DEVNULL ,stderr =subprocess .PIPE ,text =True )#line:125
        if OOO0OOOO00OOOO000 .returncode ==0 :#line:126
            enable_adb_root_for_all ([OO0OO0O000O000OOO ])#line:127
        else :#line:128
            print (f"Failed to connect to port {OO0OO0O000O000OOO}: {OOO0OOOO00OOOO000.stderr}")#line:129
def start_private_server (OO00000O0O0000O00 ,O0O0OO0OOOOOOOO0O ):#line:132
    try :#line:133
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OO00000O0O0000O00}','shell','am','start','-n','com.roblox.client/com.roblox.client.startup.ActivitySplash','-d',O0O0OO0OOOOOOOO0O ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:136
        time .sleep (10 )#line:137
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OO00000O0O0000O00}','shell','am','start','-n','com.roblox.client/com.roblox.client.ActivityProtocolLaunch','-d',O0O0OO0OOOOOOOO0O ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:140
        time .sleep (8 )#line:141
        print (colored (f"Private link dijalankan di emulator {OO00000O0O0000O00}.","green"))#line:142
    except Exception as O0OOOOOOOO0O00OOO :#line:143
        print (colored (f"Gagal menjalankan Private Server di emulator {OO00000O0O0000O00}: {O0OOOOOOOO0O00OOO}","red"))#line:144
def start_default_server (OO000000OOOO00OOO ,OOO0O0O0OOO00O00O ):#line:147
    try :#line:148
        O0O00000O00OOO0OO =f"roblox://placeID={OOO0O0O0OOO00O00O}"#line:149
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OO000000OOOO00OOO}','shell','am','start','-n','com.roblox.client/com.roblox.client.startup.ActivitySplash','-d',O0O00000O00OOO0OO ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:152
        time .sleep (10 )#line:153
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OO000000OOOO00OOO}','shell','am','start','-n','com.roblox.client/com.roblox.client.ActivityProtocolLaunch','-d',O0O00000O00OOO0OO ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:156
        time .sleep (10 )#line:157
        print (Fore .GREEN +f"Membuka game menggunakan server: {O0O00000O00OOO0OO}.")#line:158
    except Exception as O0O0O0O0O00O00O0O :#line:159
        print (colored (f"Failed to start Default Server: {O0O0O0O0O00O00O0O}",'red'))#line:160
def auto_join_game (OO0OO000O0O0OOO0O ,OOO0OOO0O0OO0O0OO ,OO0O00O0O000OO000 ,O0OO000OOOO0OO00O ):#line:163
    O0OO000OOOO0OO00O [OO0OO000O0O0OOO0O ]="Opening Roblox"#line:164
    update_table (O0OO000OOOO0OO00O )#line:165
    if OO0O00O0O000OO000 :#line:167
        start_private_server (OO0OO000O0O0OOO0O ,OO0O00O0O000OO000 )#line:168
    else :#line:169
        start_default_server (OO0OO000O0O0OOO0O ,OOO0OOO0O0OO0O0OO )#line:170
    O0OO000OOOO0OO00O [OO0OO000O0O0OOO0O ]="Opening the Game"#line:172
    update_table (O0OO000OOOO0OO00O )#line:173
    time .sleep (10 )#line:174
    O0OO000OOOO0OO00O [OO0OO000O0O0OOO0O ]="In Game"#line:176
    update_table (O0OO000OOOO0OO00O )#line:177
    time .sleep (1 )#line:178
def ensure_roblox_running_with_interval (O0OO00O0OO000000O ,OO0O00O00O000O0O0 ,OOO00OOOO00000OOO ,O0O000O00O000OOO0 ):#line:181
    O0000O0OO0O00O000 ={O0O0OOOO0OOO00000 :"waiting"for O0O0OOOO0OOO00000 in O0OO00O0OO000000O }#line:182
    update_table (O0000O0OO0O00O000 )#line:183
    O000OO0000000O000 =O0O000O00O000OOO0 *60 #line:185
    OOOO0OOO000O000OO =time .time ()#line:186
    while True :#line:188
        O0OOOOOOO0OO00000 =time .time ()-OOOO0OOO000O000OO #line:189
        for O0000OOO00OO00000 in O0OO00O0OO000000O :#line:190
            OOOO0O0OO00000OO0 =OOO00OOOO00000OOO .get (O0000OOO00OO00000 )#line:191
            if check_roblox_running (O0000OOO00OO00000 ):#line:192
                O0000O0OO0O00O000 [O0000OOO00OO00000 ]="In Game"#line:193
                update_table (O0000O0OO0O00O000 )#line:194
            else :#line:195
                O0000O0OO0O00O000 [O0000OOO00OO00000 ]="roblox offline"#line:196
                update_table (O0000O0OO0O00O000 )#line:197
                force_close_roblox (O0000OOO00OO00000 )#line:198
                auto_join_game (O0000OOO00OO00000 ,OO0O00O00O000O0O0 ,OOOO0O0OO00000OO0 ,O0000O0OO0O00O000 )#line:199
        if O0O000O00O000OOO0 >0 and O0OOOOOOO0OO00000 >=O000OO0000000O000 :#line:201
            for O0000OOO00OO00000 in O0OO00O0OO000000O :#line:202
                OOOO0O0OO00000OO0 =OOO00OOOO00000OOO .get (O0000OOO00OO00000 )#line:203
                O0000O0OO0O00O000 [O0000OOO00OO00000 ]="roblox offline"#line:204
                update_table (O0000O0OO0O00O000 )#line:205
                force_close_roblox (O0000OOO00OO00000 )#line:206
                auto_join_game (O0000OOO00OO00000 ,OO0O00O00O000O0O0 ,OOOO0O0OO00000OO0 ,O0000O0OO0O00O000 )#line:207
            OOOO0OOO000O000OO =time .time ()#line:208
        time .sleep (5 )#line:209
def check_roblox_running (O0OO000O0O0O0000O ):#line:212
    try :#line:213
        O00000O00O0OO0OO0 =subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{O0OO000O0O0O0000O}','shell','pidof','com.roblox.client'],stdout =subprocess .PIPE ,stderr =subprocess .PIPE ,text =True )#line:217
        return bool (O00000O00O0OO0OO0 .stdout .strip ())#line:218
    except Exception as OO00OOO00OO0OO0O0 :#line:219
        print (colored (f"Error checking if Roblox is running on {O0OO000O0O0O0000O}: {OO00OOO00OO0OO0O0}",'red'))#line:220
        return False #line:221
def force_close_roblox (O0O00OOOOO0O00O0O ):#line:224
    subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{O0O00OOOOO0O00O0O}','shell','am','force-stop','com.roblox.client'],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:226
    time .sleep (8 )#line:227
def start_instance_in_thread (OO00OOOO000O0OOO0 ,OO000OO0O0O0OOOO0 ,OO0O000O00OO0OOOO ,O0OO000O0OOOOOOOO ):#line:230
    OOO0O0OO00OOO0000 =[]#line:231
    for O00OO0O00O0OO0O0O in OO00OOOO000O0OOO0 :#line:232
        O0O00000O0O00OOOO =threading .Thread (target =auto_join_game ,args =(O00OO0O00O0OO0O0O ,OO000OO0O0O0OOOO0 ,OO0O000O00OO0OOOO .get (O00OO0O00O0OO0O0O ),O0OO000O0OOOOOOOO ))#line:233
        O0O00000O0O00OOOO .start ()#line:234
        OOO0O0OO00OOO0000 .append (O0O00000O0O00OOOO )#line:235
    for O00OO0O00O0OO0O0O in OO00OOOO000O0OOO0 :#line:237
        O0O0000OOOOOOO00O =threading .Thread (target =ensure_roblox_running_with_interval ,args =([O00OO0O00O0OO0O0O ],OO000OO0O0O0OOOO0 ,OO0O000O00OO0OOOO ,1 ))#line:238
        O0O0000OOOOOOO00O .start ()#line:239
        OOO0O0OO00OOO0000 .append (O0O0000OOOOOOO00O )#line:240
    for O0O00000O0O00OOOO in OOO0O0OO00OOO0000 :#line:242
        O0O00000O0O00OOOO .join ()#line:243
def update_table (O0OO00O00OOOO00OO ):#line:246
    os .system ('cls'if os .name =='nt'else 'clear')#line:247
    OO0O0OOOO00O00OOO =[]#line:248
    for OO00OO00OOO00O000 ,O0OO000O0OO0O0O0O in O0OO00O00OOOO00OO .items ():#line:249
        OO0O00O0O000O0OO0 =get_username_from_prefs (OO00OO00OOO00O000 )#line:250
        if O0OO000O0OO0O0O0O =="In Game":#line:251
            OO000O00OOOO0OOOO ='green'#line:252
        elif O0OO000O0OO0O0O0O =="Opening the Game":#line:253
            OO000O00OOOO0OOOO ='cyan'#line:254
        elif O0OO000O0OO0O0O0O =="Opening Roblox":#line:255
            OO000O00OOOO0OOOO ='yellow'#line:256
        elif O0OO000O0OO0O0O0O =="roblox offline":#line:257
            OO000O00OOOO0OOOO ='red'#line:258
        else :#line:259
            OO000O00OOOO0OOOO ='magenta'#line:260
        OO0O0OOOO00O00OOO .append ({"NAME":f"emulator:{OO00OO00OOO00O000}","Username":OO0O00O0O000O0OO0 or "Not Found","Proses":colored (O0OO000O0OO0O0O0O ,OO000O00OOOO0OOOO )})#line:262
    print (tabulate (OO0O0OOOO00O00OOO ,headers ="keys",tablefmt ="grid"))#line:264
    print (colored ("BANG OVA",'blue',attrs =['bold','underline']).center (50 ))#line:265
def menu ():#line:268
    O0OOOO00O00OOO000 =load_config ()#line:269
    O00O000OO0000O0OO =load_ports ()#line:270
    OO0O00O0000OO0OOO =load_private_links ()#line:271
    if O00O000OO0000O0OO :#line:273
        auto_connect_adb (O00O000OO0000O0OO )#line:274
    else :#line:275
        print (colored ("ADB port not found. Please set it first..",'yellow'))#line:276
    if O0OOOO00O00OOO000 :#line:278
        print (colored (f"Game ID: {O0OOOO00O00OOO000} has been loaded from configuration.",'green'))#line:279
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
        OOO00O000OO0OOOO0 =input ("Select number (1/2/3/4/5/6): ")#line:292
        if OOO00O000OO0OOOO0 =='1':#line:294
            if not O0OOOO00O00OOO000 :#line:295
                print (colored ("Game ID has not been set. Please set it first.",'red'))#line:296
                continue #line:297
            OO000OO000O00O00O =int (input ("Enter the time interval (in minutes, enter 0 for no interval).: "))#line:298
            ensure_roblox_running_with_interval (O00O000OO0000O0OO ,O0OOOO00O00OOO000 ,OO0O00O0000OO0OOO ,OO000OO000O00O00O )#line:299
        elif OOO00O000OO0OOOO0 =='2':#line:300
            O0OOOO00O00OOO000 =input ("Enter Game ID: ")#line:301
            save_config (O0OOOO00O00OOO000 )#line:302
        elif OOO00O000OO0OOOO0 =='3':#line:303
            OOOO0OOO00OO0OO00 =input ("Enter the ADB port (separate with commas if more than one).: ").split (',')#line:304
            save_ports ([O0OOOOO0O0O00OOO0 .strip ()for O0OOOOO0O0O00OOO0 in OOOO0OOO00OO0OO00 ])#line:305
            O00O000OO0000O0OO =OOOO0OOO00OO0OO00 #line:306
            auto_connect_adb (O00O000OO0000O0OO )#line:307
        elif OOO00O000OO0OOOO0 =='4':#line:308
            OOO0O0OOO00O0000O =input ("Enter private code for all instances.(only support link like this https://www.roblox.com/games/2753915549/DRAGON-Blox-Fruits?privateServerLinkCode=313232213213123123131): ").strip ()#line:309
            for OO000OO00000OOO0O in O00O000OO0000O0OO :#line:310
                save_private_link (OO000OO00000OOO0O ,OOO0O0OOO00O0000O )#line:311
                OO0O00O0000OO0OOO =load_private_links ()#line:312
        elif OOO00O000OO0OOOO0 =='5':#line:313
            OOO00O00OO0000OOO =input ("Enter the instance port: ").strip ()#line:314
            OOO0O0OOO00O0000O =input ("Enter the private code for this instance.(only support link like this https://www.roblox.com/games/2753915549/DRAGON-Blox-Fruits?privateServerLinkCode=313232213213123123131): ").strip ()#line:315
            save_private_link (OOO00O00OO0000OOO ,OOO0O0OOO00O0000O )#line:316
            OO0O00O0000OO0OOO =load_private_links ()#line:317
        elif OOO00O000OO0OOOO0 =='6':#line:318
            print ("Exit the program...")#line:319
            break #line:320
        else :#line:321
            print ("Invalid selection!")#line:322
menu ()
