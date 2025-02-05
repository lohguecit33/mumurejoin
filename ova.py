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
        with open (config_file ,'r')as OOOO0OO000O00O00O :#line:29
            OO0O000OOOO000000 =OOOO0OO000O00O00O .readlines ()#line:30
            if len (OO0O000OOOO000000 )>=2 :#line:31
                O00OO0O000OOOO0O0 =OO0O000OOOO000000 [1 ].strip ()#line:32
                return O00OO0O000OOOO0O0 #line:33
    return None ,None #line:34
def save_config (O00O00OO0O0O0OOOO ):#line:37
    with open (config_file ,'w')as O0O0OOO000OO0OO0O :#line:38
        O0O0OOO000OO0OO0O .write (f"{O00O00OO0O0O0OOOO}")#line:39
    print (colored (f"User ID dan Game ID telah disimpan di {config_file}",'green'))#line:40
def enable_adb_root_for_all (OO00O000OOOOOOOO0 ):#line:43
    for OOO0000O0O0OO0O00 in OO00O000OOOOOOOO0 :#line:44
        O00OO0O00O0O0OO0O =[ADB_PATH ,"-s",f"127.0.0.1:{OOO0000O0O0OO0O00}","root"]#line:45
        OO0OOO000O00000OO =subprocess .run (O00OO0O00O0O0OO0O ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE ,text =True )#line:46
        if OO0OOO000O00000OO .returncode !=0 :#line:47
            print (f"Error enabling adb root for emulator {OOO0000O0O0OO0O00}: {OO0OOO000O00000OO.stderr}")#line:48
def get_username_from_prefs (OOO0OOO0O000OOO0O ):#line:52
    OO0OO000OO0OOOOOO =[ADB_PATH ,"-s",f'127.0.0.1:{OOO0OOO0O000OOO0O}',"shell","cat","/data/data/com.roblox.client/shared_prefs/prefs.xml"]#line:54
    OO000OO00O00O0OOO =subprocess .run (OO0OO000OO0OOOOOO ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE ,text =True )#line:57
    if OO000OO00O00O0OOO .returncode !=0 :#line:58
        print (f"Error: {OO000OO00O00O0OOO.stderr}")#line:59
        return None #line:60
    OOO00OO000O00O0OO =OO000OO00O00O0OOO .stdout #line:63
    if OOO00OO000O00O0OO :#line:66
        OOOOO0O0OO0OOOOOO ='<string name="username">'#line:67
        O00OOOO000O0OO0O0 ='</string>'#line:68
        O00OOOO00O0O0O00O =OOO00OO000O00O0OO .find (OOOOO0O0OO0OOOOOO )#line:71
        if O00OOOO00O0O0O00O !=-1 :#line:72
            O00OOOO00O0O0O00O +=len (OOOOO0O0OO0OOOOOO )#line:73
            OO00O0O0OOOO0OO00 =OOO00OO000O00O0OO .find (O00OOOO000O0OO0O0 ,O00OOOO00O0O0O00O )#line:74
            if OO00O0O0OOOO0OO00 !=-1 :#line:75
                OO00OO0O000OOO0O0 =OOO00OO000O00O0OO [O00OOOO00O0O0O00O :OO00O0O0OOOO0OO00 ].strip ()#line:77
                return OO00OO0O000OOO0O0 #line:78
    print ("Username tidak ditemukan di prefs.xml.")#line:80
    return None #line:81
def load_ports ():#line:84
    if os .path .exists (port_file ):#line:85
        with open (port_file ,'r')as OO0O00O0OO0O0OO0O :#line:86
            O0O0O0O0000000OO0 =OO0O00O0OO0O0OO0O .readlines ()#line:87
            return [O00000000OOOOOO00 .strip ()for O00000000OOOOOO00 in O0O0O0O0000000OO0 ]#line:88
    return []#line:89
def save_ports (O0OOOO0OO000O0O00 ):#line:92
    with open (port_file ,'w')as OOOOOO0OOO0OO000O :#line:94
        for O0O0OO0O0O0O00O0O in O0OOOO0OO000O0O00 :#line:95
            OOOOOO0OOO0OO000O .write (f"{O0O0OO0O0O0O00O0O}\n")#line:96
    print (colored (f"Port ADB telah disimpan di {port_file}",'green'))#line:97
def load_private_links ():#line:100
    try :#line:101
        if os .path .exists (PRIVATE_LINK_FILE ):#line:102
            with open (PRIVATE_LINK_FILE ,"r")as O0O00OO00OOO0O000 :#line:103
                return json .load (O0O00OO00OOO0O000 )#line:104
        else :#line:105
            return {}#line:106
    except Exception as OOOO000O0OO0OOO0O :#line:107
        print (colored (f"Error memuat private link: {OOOO000O0OO0OOO0O}","red"))#line:108
        return {}#line:109
def save_private_link (O0OOO000O0O0O0O0O ,O0OOOO0000O00OOO0 ):#line:112
    try :#line:113
        O00000O0OOO000O00 =load_private_links ()#line:114
        O00000O0OOO000O00 [O0OOO000O0O0O0O0O ]=O0OOOO0000O00OOO0 #line:115
        with open (PRIVATE_LINK_FILE ,"w")as OO0O0OO0O0O000OOO :#line:116
            json .dump (O00000O0OOO000O00 ,OO0O0OO0O0O000OOO ,indent =4 )#line:117
        print (colored (f"Private link for emulator {O0OOO000O0O0O0O0O} successfully saved: {O0OOOO0000O00OOO0}","green"))#line:118
    except Exception as O000OOO00O0000OO0 :#line:119
        print (colored (f"Error saving private link: {O000OOO00O0000OO0}","red"))#line:120
def auto_connect_adb (OOO00O00000OOOOO0 ):#line:123
    for OOOOO0OOOO0O0OOOO in OOO00O00000OOOOO0 :#line:124
        OO0OO0O0OOO0OO0OO =subprocess .run ([ADB_PATH ,'connect',f'127.0.0.1:{OOOOO0OOOO0O0OOOO}'],stdout =subprocess .DEVNULL ,stderr =subprocess .PIPE ,text =True )#line:125
        if OO0OO0O0OOO0OO0OO .returncode ==0 :#line:126
            enable_adb_root_for_all ([OOOOO0OOOO0O0OOOO ])#line:127
        else :#line:128
            print (f"Failed to connect to port {OOOOO0OOOO0O0OOOO}: {OO0OO0O0OOO0OO0OO.stderr}")#line:129
def start_private_server (OO0OO000OO0OOO000 ,OO00000OOO0OOO0OO ):#line:132
    try :#line:133
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OO0OO000OO0OOO000}','shell','am','start','-n','com.roblox.client/com.roblox.client.startup.ActivitySplash','-d',OO00000OOO0OOO0OO ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:136
        time .sleep (10 )#line:137
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OO0OO000OO0OOO000}','shell','am','start','-n','com.roblox.client/com.roblox.client.ActivityProtocolLaunch','-d',OO00000OOO0OOO0OO ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:140
        time .sleep (8 )#line:141
        print (colored (f"Private link dijalankan di emulator {OO0OO000OO0OOO000}.","green"))#line:142
    except Exception as O0OOOO000O00OO0O0 :#line:143
        print (colored (f"Gagal menjalankan Private Server di emulator {OO0OO000OO0OOO000}: {O0OOOO000O00OO0O0}","red"))#line:144
def start_default_server (O0OO0O000OOO0O0OO ,OOOO00O0O000OO0OO ):#line:147
    try :#line:148
        O0OOO0OO0O000OOOO =f"roblox://placeID={OOOO00O0O000OO0OO}"#line:149
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{O0OO0O000OOO0O0OO}','shell','am','start','-n','com.roblox.client/com.roblox.client.startup.ActivitySplash','-d',O0OOO0OO0O000OOOO ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:152
        time .sleep (10 )#line:153
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{O0OO0O000OOO0O0OO}','shell','am','start','-n','com.roblox.client/com.roblox.client.ActivityProtocolLaunch','-d',O0OOO0OO0O000OOOO ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:156
        time .sleep (10 )#line:157
        print (Fore .GREEN +f"Membuka game menggunakan server: {O0OOO0OO0O000OOOO}.")#line:158
    except Exception as O0OOOO0O000000O0O :#line:159
        print (colored (f"Failed to start Default Server: {O0OOOO0O000000O0O}",'red'))#line:160
def auto_join_game (OOOO000O0OOOOOO0O ,OOOOOO0O0000OOOO0 ,O0OO0OO0O0000O0O0 ,OO0OOOO00O00OOO00 ):#line:163
    OO0OOOO00O00OOO00 [OOOO000O0OOOOOO0O ]="Opening Roblox"#line:164
    update_table (OO0OOOO00O00OOO00 )#line:165
    if O0OO0OO0O0000O0O0 :#line:167
        start_private_server (OOOO000O0OOOOOO0O ,O0OO0OO0O0000O0O0 )#line:168
    else :#line:169
        start_default_server (OOOO000O0OOOOOO0O ,OOOOOO0O0000OOOO0 )#line:170
    OO0OOOO00O00OOO00 [OOOO000O0OOOOOO0O ]="Opening the Game"#line:172
    update_table (OO0OOOO00O00OOO00 )#line:173
    time .sleep (10 )#line:174
    OO0OOOO00O00OOO00 [OOOO000O0OOOOOO0O ]="In Game"#line:176
    update_table (OO0OOOO00O00OOO00 )#line:177
    time .sleep (1 )#line:178
def ensure_roblox_running_with_interval (OOO00OO0OOO00O0O0 ,O0OO00000O00O0OOO ,O0O0000OO0O00O00O ,OOO0OO000OO00OO00 ):#line:181
    O0OO000O0OO0OOOOO ={O000OOOOO00OO000O :"waiting"for O000OOOOO00OO000O in OOO00OO0OOO00O0O0 }#line:182
    update_table (O0OO000O0OO0OOOOO )#line:183
    O00OOOO0OOOO000OO =OOO0OO000OO00OO00 *60 #line:185
    O0OO0OOO00000OO00 =time .time ()#line:186
    while True :#line:188
        OOOO0000O00O0O0OO =time .time ()-O0OO0OOO00000OO00 #line:189
        for OO0OOO0O0O0O0OOO0 in OOO00OO0OOO00O0O0 :#line:190
            OOOO0000O0O000OO0 =O0O0000OO0O00O00O .get (OO0OOO0O0O0O0OOO0 )#line:191
            if check_roblox_running (OO0OOO0O0O0O0OOO0 ):#line:192
                O0OO000O0OO0OOOOO [OO0OOO0O0O0O0OOO0 ]="In Game"#line:193
                update_table (O0OO000O0OO0OOOOO )#line:194
            else :#line:195
                O0OO000O0OO0OOOOO [OO0OOO0O0O0O0OOO0 ]="roblox offline"#line:196
                update_table (O0OO000O0OO0OOOOO )#line:197
                force_close_roblox (OO0OOO0O0O0O0OOO0 )#line:198
                auto_join_game (OO0OOO0O0O0O0OOO0 ,O0OO00000O00O0OOO ,OOOO0000O0O000OO0 ,O0OO000O0OO0OOOOO )#line:199
        if OOO0OO000OO00OO00 >0 and OOOO0000O00O0O0OO >=O00OOOO0OOOO000OO :#line:201
            for OO0OOO0O0O0O0OOO0 in OOO00OO0OOO00O0O0 :#line:202
                OOOO0000O0O000OO0 =O0O0000OO0O00O00O .get (OO0OOO0O0O0O0OOO0 )#line:203
                O0OO000O0OO0OOOOO [OO0OOO0O0O0O0OOO0 ]="roblox offline"#line:204
                update_table (O0OO000O0OO0OOOOO )#line:205
                force_close_roblox (OO0OOO0O0O0O0OOO0 )#line:206
                auto_join_game (OO0OOO0O0O0O0OOO0 ,O0OO00000O00O0OOO ,OOOO0000O0O000OO0 ,O0OO000O0OO0OOOOO )#line:207
            O0OO0OOO00000OO00 =time .time ()#line:208
        time .sleep (5 )#line:209
def check_roblox_running (OOOO00OOOO0000000 ):#line:212
    try :#line:213
        O0O000O00O00O0OOO =subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OOOO00OOOO0000000}','shell','pidof','com.roblox.client'],stdout =subprocess .PIPE ,stderr =subprocess .PIPE ,text =True )#line:217
        return bool (O0O000O00O00O0OOO .stdout .strip ())#line:218
    except Exception as O000O00O0000OO0OO :#line:219
        print (colored (f"Error checking if Roblox is running on {OOOO00OOOO0000000}: {O000O00O0000OO0OO}",'red'))#line:220
        return False #line:221
def force_close_roblox (OOOOO0OO00O0OOO0O ):#line:224
    subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OOOOO0OO00O0OOO0O}','shell','am','force-stop','com.roblox.client'],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:226
    time .sleep (8 )#line:227
def start_instance_in_thread (OO0OOO00O0OO0O00O ,O0O0O0O00OO0000OO ,OO0000O0O00OO00O0 ,O0OO0000O0000OO0O ):#line:230
    O0O00OO0OOOO00OO0 =[]#line:231
    for OO000OOO0OO0000OO in OO0OOO00O0OO0O00O :#line:232
        O000O0O0O0OO0OO00 =threading .Thread (target =auto_join_game ,args =(OO000OOO0OO0000OO ,O0O0O0O00OO0000OO ,OO0000O0O00OO00O0 .get (OO000OOO0OO0000OO ),O0OO0000O0000OO0O ))#line:233
        O000O0O0O0OO0OO00 .start ()#line:234
        O0O00OO0OOOO00OO0 .append (O000O0O0O0OO0OO00 )#line:235
    for OO000OOO0OO0000OO in OO0OOO00O0OO0O00O :#line:237
        O0OO000O0OO0OO00O =threading .Thread (target =ensure_roblox_running_with_interval ,args =([OO000OOO0OO0000OO ],O0O0O0O00OO0000OO ,OO0000O0O00OO00O0 ,1 ))#line:238
        O0OO000O0OO0OO00O .start ()#line:239
        O0O00OO0OOOO00OO0 .append (O0OO000O0OO0OO00O )#line:240
    for O000O0O0O0OO0OO00 in O0O00OO0OOOO00OO0 :#line:242
        O000O0O0O0OO0OO00 .join ()#line:243
def update_table (OOO000O00O0000OOO ):#line:246
    os .system ('cls'if os .name =='nt'else 'clear')#line:247
    OOO00OOOO00OO00OO =[]#line:248
    for OOOO00OO000O00OO0 ,O00000000O0OO0000 in OOO000O00O0000OOO .items ():#line:249
        OO000O00OOOOOO00O =get_username_from_prefs (OOOO00OO000O00OO0 )#line:250
        if O00000000O0OO0000 =="In Game":#line:251
            OO00000OO0O0O00OO ='green'#line:252
        elif O00000000O0OO0000 =="Opening the Game":#line:253
            OO00000OO0O0O00OO ='cyan'#line:254
        elif O00000000O0OO0000 =="Opening Roblox":#line:255
            OO00000OO0O0O00OO ='yellow'#line:256
        elif O00000000O0OO0000 =="roblox offline":#line:257
            OO00000OO0O0O00OO ='red'#line:258
        else :#line:259
            OO00000OO0O0O00OO ='magenta'#line:260
        OOO00OOOO00OO00OO .append ({"NAME":f"emulator:{OOOO00OO000O00OO0}","Username":OO000O00OOOOOO00O or "Not Found","Proses":colored (O00000000O0OO0000 ,OO00000OO0O0O00OO )})#line:262
    print (tabulate (OOO00OOOO00OO00OO ,headers ="keys",tablefmt ="grid"))#line:264
    print (colored ("BANG OVA",'blue',attrs =['bold','underline']).center (50 ))#line:265
def menu ():#line:268
    OOOO00O000O00000O =load_config ()#line:269
    O00OOOOOO000000O0 =load_ports ()#line:270
    O0O0O0OOO000OOOO0 =load_private_links ()#line:271
    if O00OOOOOO000000O0 :#line:273
        auto_connect_adb (O00OOOOOO000000O0 )#line:274
    else :#line:275
        print (colored ("ADB port not found. Please set it first..",'yellow'))#line:276
    if OOOO00O000O00000O :#line:278
        print (colored (f"Game ID: {OOOO00O000O00000O} has been loaded from configuration.",'green'))#line:279
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
        O00O000O00O00OOO0 =input ("Select number (1/2/3/4/5/6): ")#line:292
        if O00O000O00O00OOO0 =='1':#line:294
            if not OOOO00O000O00000O :#line:295
                print (colored ("Game ID has not been set. Please set it first.",'red'))#line:296
                continue #line:297
            OOOOOO0OOO0OO0O00 =int (input ("Enter the time interval (in minutes, enter 0 for no interval).: "))#line:298
            ensure_roblox_running_with_interval (O00OOOOOO000000O0 ,OOOO00O000O00000O ,O0O0O0OOO000OOOO0 ,OOOOOO0OOO0OO0O00 )#line:299
        elif O00O000O00O00OOO0 =='2':#line:300
            OOOO00O000O00000O =input ("Enter Game ID: ")#line:301
            save_config (OOOO00O000O00000O )#line:302
        elif O00O000O00O00OOO0 =='3':#line:303
            O0OO00O00000OO000 =input ("Enter the ADB port (separate with commas if more than one).: ").split (',')#line:304
            save_ports ([O0O0O000O000O000O .strip ()for O0O0O000O000O000O in O0OO00O00000OO000 ])#line:305
            O00OOOOOO000000O0 =O0OO00O00000OO000 #line:306
            auto_connect_adb (O00OOOOOO000000O0 )#line:307
        elif O00O000O00O00OOO0 =='4':#line:308
            O00OOOO00O0O0000O =input ("Enter private code for all instances.(only support link like this https://www.roblox.com/games/2753915549/DRAGON-Blox-Fruits?privateServerLinkCode=313232213213123123131): ").strip ()#line:309
            for O000O00O00O00O0O0 in O00OOOOOO000000O0 :#line:310
                save_private_link (O000O00O00O00O0O0 ,O00OOOO00O0O0000O )#line:311
                O0O0O0OOO000OOOO0 =load_private_links ()#line:312
        elif O00O000O00O00OOO0 =='5':#line:313
            OO0OO0OO0OO0OOO00 =input ("Enter the instance port: ").strip ()#line:314
            O00OOOO00O0O0000O =input ("Enter the private code for this instance.(only support link like this https://www.roblox.com/games/2753915549/DRAGON-Blox-Fruits?privateServerLinkCode=313232213213123123131): ").strip ()#line:315
            save_private_link (OO0OO0OO0OO0OOO00 ,O00OOOO00O0O0000O )#line:316
            O0O0O0OOO000OOOO0 =load_private_links ()#line:317
        elif O00O000O00O00OOO0 =='6':#line:318
            print ("Exit the program...")#line:319
            break #line:320
        else :#line:321
            print ("Invalid selection!")#line:322
menu ()
