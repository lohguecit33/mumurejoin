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
        with open (config_file ,'r')as O000OO00000OO0OO0 :#line:29
            OO00000OOOO0OOOO0 =O000OO00000OO0OO0 .readlines ()#line:30
            if len (OO00000OOOO0OOOO0 )>=2 :#line:31
                OO000O0OOO0O0O0O0 =OO00000OOOO0OOOO0 [1 ].strip ()#line:32
                return OO000O0OOO0O0O0O0 #line:33
    return None ,None #line:34
def save_config (OOOOO0000000OO0OO ):#line:37
    with open (config_file ,'w')as O0OO000OOOOO0OOO0 :#line:38
        O0OO000OOOOO0OOO0 .write (f"{OOOOO0000000OO0OO}")#line:39
    print (colored (f"User ID dan Game ID telah disimpan di {config_file}",'green'))#line:40
def enable_adb_root_for_all (OO0O00OOO0OOO0OO0 ):#line:43
    for OO0OOOOOOOO0OO0OO in OO0O00OOO0OOO0OO0 :#line:44
        O0OO000O0OO0OOOO0 =[ADB_PATH ,"-s",f"127.0.0.1:{OO0OOOOOOOO0OO0OO}","root"]#line:45
        OO000O0OOO00O0O00 =subprocess .run (O0OO000O0OO0OOOO0 ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE ,text =True )#line:46
        if OO000O0OOO00O0O00 .returncode !=0 :#line:47
            print (f"Error enabling adb root for emulator {OO0OOOOOOOO0OO0OO}: {OO000O0OOO00O0O00.stderr}")#line:48
def get_username_from_prefs (OOOO0O0OOO0O0O00O ):#line:52
    OO0O0OO0OOO0O00OO =[ADB_PATH ,"-s",f'127.0.0.1:{OOOO0O0OOO0O0O00O}',"shell","cat","/data/data/com.roblox.client/shared_prefs/prefs.xml"]#line:54
    O0000OOO0O00OO0O0 =subprocess .run (OO0O0OO0OOO0O00OO ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE ,text =True )#line:57
    if O0000OOO0O00OO0O0 .returncode !=0 :#line:58
        print (f"Error: {O0000OOO0O00OO0O0.stderr}")#line:59
        return None #line:60
    OO00OOO00O0OO0OO0 =O0000OOO0O00OO0O0 .stdout #line:63
    if OO00OOO00O0OO0OO0 :#line:66
        OOO00OO000OO0OO0O ='<string name="username">'#line:67
        OOOOO0000000O0O0O ='</string>'#line:68
        OO000OO0OO0OOO00O =OO00OOO00O0OO0OO0 .find (OOO00OO000OO0OO0O )#line:71
        if OO000OO0OO0OOO00O !=-1 :#line:72
            OO000OO0OO0OOO00O +=len (OOO00OO000OO0OO0O )#line:73
            OOOO000000O00OOO0 =OO00OOO00O0OO0OO0 .find (OOOOO0000000O0O0O ,OO000OO0OO0OOO00O )#line:74
            if OOOO000000O00OOO0 !=-1 :#line:75
                OOO00000OOO0O00O0 =OO00OOO00O0OO0OO0 [OO000OO0OO0OOO00O :OOOO000000O00OOO0 ].strip ()#line:77
                return OOO00000OOO0O00O0 #line:78
    print ("Username tidak ditemukan di prefs.xml.")#line:80
    return None #line:81
def load_ports ():#line:84
    if os .path .exists (port_file ):#line:85
        with open (port_file ,'r')as OOOO0O0OOOO0O0OO0 :#line:86
            O00O00000OOOO0O00 =OOOO0O0OOOO0O0OO0 .readlines ()#line:87
            return [OOO0OO0O0OOO0O0OO .strip ()for OOO0OO0O0OOO0O0OO in O00O00000OOOO0O00 ]#line:88
    return []#line:89
def save_ports (O00OOOO0O00OOOOOO ):#line:92
    with open (port_file ,'w')as OOO0O00O0O00OOO00 :#line:94
        for OO00O0O00OO000000 in O00OOOO0O00OOOOOO :#line:95
            OOO0O00O0O00OOO00 .write (f"{OO00O0O00OO000000}\n")#line:96
    print (colored (f"Port ADB telah disimpan di {port_file}",'green'))#line:97
def load_private_links ():#line:100
    try :#line:101
        if os .path .exists (PRIVATE_LINK_FILE ):#line:102
            with open (PRIVATE_LINK_FILE ,"r")as O0OO000O0OOO0O000 :#line:103
                return json .load (O0OO000O0OOO0O000 )#line:104
        else :#line:105
            return {}#line:106
    except Exception as OO0O00OOOOO00O0O0 :#line:107
        print (colored (f"Error memuat private link: {OO0O00OOOOO00O0O0}","red"))#line:108
        return {}#line:109
def save_private_link (O0O00O0OOOOOO0O00 ,OO00OO0000O000O00 ):#line:112
    try :#line:113
        O00OOO0OO00O0O0OO =load_private_links ()#line:114
        O00OOO0OO00O0O0OO [O0O00O0OOOOOO0O00 ]=OO00OO0000O000O00 #line:115
        with open (PRIVATE_LINK_FILE ,"w")as O00OO0OO0OOOO0O0O :#line:116
            json .dump (O00OOO0OO00O0O0OO ,O00OO0OO0OOOO0O0O ,indent =4 )#line:117
        print (colored (f"Private link for emulator {O0O00O0OOOOOO0O00} successfully saved: {OO00OO0000O000O00}","green"))#line:118
    except Exception as O00OOO0O00OO000OO :#line:119
        print (colored (f"Error saving private link: {O00OOO0O00OO000OO}","red"))#line:120
def auto_connect_adb (O000000O0OO000OOO ):#line:123
    for O000OO0O0000OOOO0 in O000000O0OO000OOO :#line:124
        O000O0000OO00O00O =subprocess .run ([ADB_PATH ,'connect',f'127.0.0.1:{O000OO0O0000OOOO0}'],stdout =subprocess .DEVNULL ,stderr =subprocess .PIPE ,text =True )#line:125
        if O000O0000OO00O00O .returncode ==0 :#line:126
            enable_adb_root_for_all ([O000OO0O0000OOOO0 ])#line:127
        else :#line:128
            print (f"Failed to connect to port {O000OO0O0000OOOO0}: {O000O0000OO00O00O.stderr}")#line:129
def start_private_server (OO00000O0O000OO0O ,O00O0O00OO00OO000 ):#line:132
    try :#line:133
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OO00000O0O000OO0O}','shell','am','start','-n','com.roblox.client/com.roblox.client.startup.ActivitySplash','-d',O00O0O00OO00OO000 ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:136
        time .sleep (10 )#line:137
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OO00000O0O000OO0O}','shell','am','start','-n','com.roblox.client/com.roblox.client.ActivityProtocolLaunch','-d',O00O0O00OO00OO000 ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:140
        time .sleep (8 )#line:141
        print (colored (f"Private link dijalankan di emulator {OO00000O0O000OO0O}.","green"))#line:142
    except Exception as O0000OOOOO00O00OO :#line:143
        print (colored (f"Gagal menjalankan Private Server di emulator {OO00000O0O000OO0O}: {O0000OOOOO00O00OO}","red"))#line:144
def start_default_server (OO00OOOO0OO00O0O0 ,OOO0OO00OOO0OOOO0 ):#line:147
    try :#line:148
        O0000OO00000OOO0O =f"roblox://placeID={OOO0OO00OOO0OOOO0}"#line:149
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OO00OOOO0OO00O0O0}','shell','am','start','-n','com.roblox.client/com.roblox.client.startup.ActivitySplash','-d',O0000OO00000OOO0O ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:152
        time .sleep (10 )#line:153
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OO00OOOO0OO00O0O0}','shell','am','start','-n','com.roblox.client/com.roblox.client.ActivityProtocolLaunch','-d',O0000OO00000OOO0O ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:156
        time .sleep (10 )#line:157
        print (Fore .GREEN +f"Membuka game menggunakan server: {O0000OO00000OOO0O}.")#line:158
    except Exception as O0O000OO000O0000O :#line:159
        print (colored (f"Failed to start Default Server: {O0O000OO000O0000O}",'red'))#line:160
def auto_join_game (O0O0O00O0O0O0OOO0 ,OO0OOO0OO0OO0O00O ,OOO0OO0O0O0O0000O ,O00O00OO00OOOO000 ):#line:163
    O00O00OO00OOOO000 [O0O0O00O0O0O0OOO0 ]="Opening Roblox"#line:164
    update_table (O00O00OO00OOOO000 )#line:165
    if OOO0OO0O0O0O0000O :#line:167
        start_private_server (O0O0O00O0O0O0OOO0 ,OOO0OO0O0O0O0000O )#line:168
    else :#line:169
        start_default_server (O0O0O00O0O0O0OOO0 ,OO0OOO0OO0OO0O00O )#line:170
    O00O00OO00OOOO000 [O0O0O00O0O0O0OOO0 ]="Opening the Game"#line:172
    update_table (O00O00OO00OOOO000 )#line:173
    time .sleep (10 )#line:174
    O00O00OO00OOOO000 [O0O0O00O0O0O0OOO0 ]="In Game"#line:176
    update_table (O00O00OO00OOOO000 )#line:177
    time .sleep (1 )#line:178
def ensure_roblox_running_with_interval (O0OOOO0O00OO0000O ,O0OO00000OO000O00 ,O0O000O000O00O0OO ,OO00O0O000O0OO00O ):#line:181
    OO00O000O00OO00O0 ={OOO0O0O00O0OOOO0O :"waiting"for OOO0O0O00O0OOOO0O in O0OOOO0O00OO0000O }#line:182
    update_table (OO00O000O00OO00O0 )#line:183
    OOOOO0O0OO0000OO0 =OO00O0O000O0OO00O *60 #line:185
    OOOO0000OO00O00O0 =time .time ()#line:186
    while True :#line:188
        O0000O00OO000OO0O =time .time ()-OOOO0000OO00O00O0 #line:189
        for OOO00OO00O00O0OOO in O0OOOO0O00OO0000O :#line:190
            O0O0000000000OO0O =O0O000O000O00O0OO .get (OOO00OO00O00O0OOO )#line:191
            if check_roblox_running (OOO00OO00O00O0OOO ):#line:192
                OO00O000O00OO00O0 [OOO00OO00O00O0OOO ]="In Game"#line:193
                update_table (OO00O000O00OO00O0 )#line:194
            else :#line:195
                OO00O000O00OO00O0 [OOO00OO00O00O0OOO ]="roblox offline"#line:196
                update_table (OO00O000O00OO00O0 )#line:197
                force_close_roblox (OOO00OO00O00O0OOO )#line:198
                auto_join_game (OOO00OO00O00O0OOO ,O0OO00000OO000O00 ,O0O0000000000OO0O ,OO00O000O00OO00O0 )#line:199
        if OO00O0O000O0OO00O >0 and O0000O00OO000OO0O >=OOOOO0O0OO0000OO0 :#line:201
            for OOO00OO00O00O0OOO in O0OOOO0O00OO0000O :#line:202
                O0O0000000000OO0O =O0O000O000O00O0OO .get (OOO00OO00O00O0OOO )#line:203
                OO00O000O00OO00O0 [OOO00OO00O00O0OOO ]="roblox offline"#line:204
                update_table (OO00O000O00OO00O0 )#line:205
                force_close_roblox (OOO00OO00O00O0OOO )#line:206
                auto_join_game (OOO00OO00O00O0OOO ,O0OO00000OO000O00 ,O0O0000000000OO0O ,OO00O000O00OO00O0 )#line:207
            OOOO0000OO00O00O0 =time .time ()#line:208
        time .sleep (5 )#line:209
def check_roblox_running (O0O000O00O0O000OO ):#line:212
    try :#line:213
        OO000000O0OOO000O =subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{O0O000O00O0O000OO}','shell','pidof','com.roblox.client'],stdout =subprocess .PIPE ,stderr =subprocess .PIPE ,text =True )#line:217
        return bool (OO000000O0OOO000O .stdout .strip ())#line:218
    except Exception as O00O0OO0000O00OOO :#line:219
        print (colored (f"Error checking if Roblox is running on {O0O000O00O0O000OO}: {O00O0OO0000O00OOO}",'red'))#line:220
        return False #line:221
def force_close_roblox (OOO0000O0O0000OO0 ):#line:224
    subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OOO0000O0O0000OO0}','shell','am','force-stop','com.roblox.client'],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:226
    time .sleep (8 )#line:227
def start_instance_in_thread (OOO0O0OOO00O000OO ,OOOOO0000OOOOO0OO ,O0OOO00O0O00O00OO ,O00O0O0O0O0O00OO0 ):#line:230
    OO00O0O0O000OO000 =[]#line:231
    for O00000OO0OO00O0O0 in OOO0O0OOO00O000OO :#line:232
        O000O000OO00O0000 =threading .Thread (target =auto_join_game ,args =(O00000OO0OO00O0O0 ,OOOOO0000OOOOO0OO ,O0OOO00O0O00O00OO .get (O00000OO0OO00O0O0 ),O00O0O0O0O0O00OO0 ))#line:233
        O000O000OO00O0000 .start ()#line:234
        OO00O0O0O000OO000 .append (O000O000OO00O0000 )#line:235
    for O00000OO0OO00O0O0 in OOO0O0OOO00O000OO :#line:237
        O00O0O0O0OOOOOOOO =threading .Thread (target =ensure_roblox_running_with_interval ,args =([O00000OO0OO00O0O0 ],OOOOO0000OOOOO0OO ,O0OOO00O0O00O00OO ,1 ))#line:238
        O00O0O0O0OOOOOOOO .start ()#line:239
        OO00O0O0O000OO000 .append (O00O0O0O0OOOOOOOO )#line:240
    for O000O000OO00O0000 in OO00O0O0O000OO000 :#line:242
        O000O000OO00O0000 .join ()#line:243
def update_table (OO00OO0OO00OO000O ):#line:246
    os .system ('cls'if os .name =='nt'else 'clear')#line:247
    O00OO0OO0OOOOO0OO =[]#line:248
    for O0O0OO00OOO00O000 ,OOO000O0O0OOOO0OO in OO00OO0OO00OO000O .items ():#line:249
        O00OOOO000O00000O =get_username_from_prefs (O0O0OO00OOO00O000 )#line:250
        if OOO000O0O0OOOO0OO =="In Game":#line:251
            OO0000O000O000OOO ='green'#line:252
        elif OOO000O0O0OOOO0OO =="Opening the Game":#line:253
            OO0000O000O000OOO ='cyan'#line:254
        elif OOO000O0O0OOOO0OO =="Opening Roblox":#line:255
            OO0000O000O000OOO ='yellow'#line:256
        elif OOO000O0O0OOOO0OO =="roblox offline":#line:257
            OO0000O000O000OOO ='red'#line:258
        else :#line:259
            OO0000O000O000OOO ='magenta'#line:260
        O00OO0OO0OOOOO0OO .append ({"NAME":f"emulator:{O0O0OO00OOO00O000}","Username":O00OOOO000O00000O or "Not Found","Proses":colored (OOO000O0O0OOOO0OO ,OO0000O000O000OOO )})#line:262
    print (tabulate (O00OO0OO0OOOOO0OO ,headers ="keys",tablefmt ="grid"))#line:264
    print (colored ("BANG OVA",'blue',attrs =['bold','underline']).center (50 ))#line:265
def menu ():#line:268
    O00O000O000O00O0O =load_config ()#line:269
    OOOOOO00O0OO000O0 =load_ports ()#line:270
    O0O0OOO0O00O00O00 =load_private_links ()#line:271
    if OOOOOO00O0OO000O0 :#line:273
        auto_connect_adb (OOOOOO00O0OO000O0 )#line:274
    else :#line:275
        print (colored ("ADB port not found. Please set it first..",'yellow'))#line:276
    if O00O000O000O00O0O :#line:278
        print (colored (f"Game ID: {O00O000O000O00O0O} has been loaded from configuration.",'green'))#line:279
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
        O0O0OOOO0O0OO00O0 =input ("Select number (1/2/3/4/5/6): ")#line:292
        if O0O0OOOO0O0OO00O0 =='1':#line:294
            if not O00O000O000O00O0O :#line:295
                print (colored ("Game ID has not been set. Please set it first.",'red'))#line:296
                continue #line:297
            OOO0OO00O0O0OO0O0 =int (input ("Enter the time interval (in minutes, enter 0 for no interval).: "))#line:298
            ensure_roblox_running_with_interval (OOOOOO00O0OO000O0 ,O00O000O000O00O0O ,O0O0OOO0O00O00O00 ,OOO0OO00O0O0OO0O0 )#line:299
        elif O0O0OOOO0O0OO00O0 =='2':#line:300
            O00O000O000O00O0O =input ("Enter Game ID: ")#line:301
            save_config (O00O000O000O00O0O )#line:302
        elif O0O0OOOO0O0OO00O0 =='3':#line:303
            OO0O0OOO0O0O0O00O =input ("Enter the ADB port (separate with commas if more than one).: ").split (',')#line:304
            save_ports ([OOOOO0O000000OOOO .strip ()for OOOOO0O000000OOOO in OO0O0OOO0O0O0O00O ])#line:305
            OOOOOO00O0OO000O0 =OO0O0OOO0O0O0O00O #line:306
            auto_connect_adb (OOOOOO00O0OO000O0 )#line:307
        elif O0O0OOOO0O0OO00O0 =='4':#line:308
            O0OO00O0OO00O0O00 =input ("Enter private code for all instances.(only support link like this https://www.roblox.com/games/2753915549/DRAGON-Blox-Fruits?privateServerLinkCode=313232213213123123131): ").strip ()#line:309
            for O0OOOOO0O00OOOOO0 in OOOOOO00O0OO000O0 :#line:310
                save_private_link (O0OOOOO0O00OOOOO0 ,O0OO00O0OO00O0O00 )#line:311
                O0O0OOO0O00O00O00 =load_private_links ()#line:312
        elif O0O0OOOO0O0OO00O0 =='5':#line:313
            OOO000OO00O000O0O =input ("Enter the instance port: ").strip ()#line:314
            O0OO00O0OO00O0O00 =input ("Enter the private code for this instance.(only support link like this https://www.roblox.com/games/2753915549/DRAGON-Blox-Fruits?privateServerLinkCode=313232213213123123131): ").strip ()#line:315
            save_private_link (OOO000OO00O000O0O ,O0OO00O0OO00O0O00 )#line:316
            O0O0OOO0O00O00O00 =load_private_links ()#line:317
        elif O0O0OOOO0O0OO00O0 =='6':#line:318
            print ("Exit the program...")#line:319
            break #line:320
        else :#line:321
            print ("Invalid selection!")#line:322
menu ()
