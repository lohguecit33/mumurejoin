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
        with open (config_file ,'r')as OOO0OOO00OOOO0000 :#line:29
            OO00OO0000OOO0OOO =OOO0OOO00OOOO0000 .readlines ()#line:30
            if len (OO00OO0000OOO0OOO )>=2 :#line:31
                O0OOO0000000OOO00 =OO00OO0000OOO0OOO [1 ].strip ()#line:32
                return O0OOO0000000OOO00 #line:33
    return None ,None #line:34
def save_config (O000O0OOOO0000OOO ):#line:37
    with open (config_file ,'w')as OO00OOOOO00OO00O0 :#line:38
        OO00OOOOO00OO00O0 .write (f"{O000O0OOOO0000OOO}")#line:39
    print (colored (f"User ID dan Game ID telah disimpan di {config_file}",'green'))#line:40
def enable_adb_root_for_all (OO0OO0OOO0OO0O00O ):#line:43
    for O0OO0OO0OOO0OO0OO in OO0OO0OOO0OO0O00O :#line:44
        OOOO000000O0O000O =[ADB_PATH ,"-s",f"127.0.0.1:{O0OO0OO0OOO0OO0OO}","root"]#line:45
        O00OO00OOOOOOO0O0 =subprocess .run (OOOO000000O0O000O ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE ,text =True )#line:46
        if O00OO00OOOOOOO0O0 .returncode !=0 :#line:47
            print (f"Error enabling adb root for emulator {O0OO0OO0OOO0OO0OO}: {O00OO00OOOOOOO0O0.stderr}")#line:48
def get_username_from_prefs (O0O0O0O0OO0OO0O0O ):#line:52
    OOO000O0OOOOO0000 =[ADB_PATH ,"-s",f'127.0.0.1:{O0O0O0O0OO0OO0O0O}',"shell","cat","/data/data/com.roblox.client/shared_prefs/prefs.xml"]#line:54
    O0000OOO0000O0000 =subprocess .run (OOO000O0OOOOO0000 ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE ,text =True )#line:57
    if O0000OOO0000O0000 .returncode !=0 :#line:58
        print (f"Error: {O0000OOO0000O0000.stderr}")#line:59
        return None #line:60
    OOOOOOOO00000OOOO =O0000OOO0000O0000 .stdout #line:63
    if OOOOOOOO00000OOOO :#line:66
        OO0OOOO0OOOOO0000 ='<string name="username">'#line:67
        O0OOO0O0000O0OO00 ='</string>'#line:68
        O0OO0O0OO0O0OOOOO =OOOOOOOO00000OOOO .find (OO0OOOO0OOOOO0000 )#line:71
        if O0OO0O0OO0O0OOOOO !=-1 :#line:72
            O0OO0O0OO0O0OOOOO +=len (OO0OOOO0OOOOO0000 )#line:73
            OO0O0000OO0O000O0 =OOOOOOOO00000OOOO .find (O0OOO0O0000O0OO00 ,O0OO0O0OO0O0OOOOO )#line:74
            if OO0O0000OO0O000O0 !=-1 :#line:75
                OOO000OOOO00000O0 =OOOOOOOO00000OOOO [O0OO0O0OO0O0OOOOO :OO0O0000OO0O000O0 ].strip ()#line:77
                return OOO000OOOO00000O0 #line:78
    print ("Username tidak ditemukan di prefs.xml.")#line:80
    return None #line:81
def load_ports ():#line:84
    if os .path .exists (port_file ):#line:85
        with open (port_file ,'r')as OOO0O00O00O000OOO :#line:86
            OO000O000O0OOOOO0 =OOO0O00O00O000OOO .readlines ()#line:87
            return [O0OO0O0OOO00O00OO .strip ()for O0OO0O0OOO00O00OO in OO000O000O0OOOOO0 ]#line:88
    return []#line:89
def save_ports (O0OOOOOO0OOO0O0OO ):#line:92
    with open (port_file ,'w')as O0O0O00O0O0O0O00O :#line:94
        for OO0OO0O00OOO0OO0O in O0OOOOOO0OOO0O0OO :#line:95
            O0O0O00O0O0O0O00O .write (f"{OO0OO0O00OOO0OO0O}\n")#line:96
    print (colored (f"Port ADB telah disimpan di {port_file}",'green'))#line:97
def load_private_links ():#line:100
    try :#line:101
        if os .path .exists (PRIVATE_LINK_FILE ):#line:102
            with open (PRIVATE_LINK_FILE ,"r")as O0OOOOO0O0O0O000O :#line:103
                return json .load (O0OOOOO0O0O0O000O )#line:104
        else :#line:105
            return {}#line:106
    except Exception as OOOOOOO0OO0OOOO0O :#line:107
        print (colored (f"Error memuat private link: {OOOOOOO0OO0OOOO0O}","red"))#line:108
        return {}#line:109
def save_private_link (O000OOO000OO0O0O0 ,O000O00OO0OOOO00O ):#line:112
    try :#line:113
        O0OO0O00OOO0000O0 =load_private_links ()#line:114
        O0OO0O00OOO0000O0 [O000OOO000OO0O0O0 ]=O000O00OO0OOOO00O #line:115
        with open (PRIVATE_LINK_FILE ,"w")as OO0OOOOOOO00O0OOO :#line:116
            json .dump (O0OO0O00OOO0000O0 ,OO0OOOOOOO00O0OOO ,indent =4 )#line:117
        print (colored (f"Private link for emulator {O000OOO000OO0O0O0} successfully saved: {O000O00OO0OOOO00O}","green"))#line:118
    except Exception as O0OO00OO00O0O0O00 :#line:119
        print (colored (f"Error saving private link: {O0OO00OO00O0O0O00}","red"))#line:120
def auto_connect_adb (OO0O0O0OOOOO0OO0O ):#line:123
    for O0O0OO00OOO0O00O0 in OO0O0O0OOOOO0OO0O :#line:124
        O00OOO00OOO00OO00 =subprocess .run ([ADB_PATH ,'connect',f'127.0.0.1:{O0O0OO00OOO0O00O0}'],stdout =subprocess .DEVNULL ,stderr =subprocess .PIPE ,text =True )#line:125
        if O00OOO00OOO00OO00 .returncode ==0 :#line:126
            enable_adb_root_for_all ([O0O0OO00OOO0O00O0 ])#line:127
        else :#line:128
            print (f"Failed to connect to port {O0O0OO00OOO0O00O0}: {O00OOO00OOO00OO00.stderr}")#line:129
def start_private_server (OO00O00O00O000O0O ,O00OOO0OO0000OOO0 ):#line:132
    try :#line:133
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OO00O00O00O000O0O}','shell','am','start','-n','com.roblox.client/com.roblox.client.startup.ActivitySplash','-d',O00OOO0OO0000OOO0 ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:136
        time .sleep (10 )#line:137
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OO00O00O00O000O0O}','shell','am','start','-n','com.roblox.client/com.roblox.client.ActivityProtocolLaunch','-d',O00OOO0OO0000OOO0 ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:140
        time .sleep (8 )#line:141
        print (colored (f"Private link dijalankan di emulator {OO00O00O00O000O0O}.","green"))#line:142
    except Exception as OOO0OO00OOOOOOOOO :#line:143
        print (colored (f"Gagal menjalankan Private Server di emulator {OO00O00O00O000O0O}: {OOO0OO00OOOOOOOOO}","red"))#line:144
def start_default_server (OO000O000O0OOO0O0 ,O0OO0O00000O0O000 ):#line:147
    try :#line:148
        O000000O00OO00OOO =f"roblox://placeID={O0OO0O00000O0O000}"#line:149
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OO000O000O0OOO0O0}','shell','am','start','-n','com.roblox.client/com.roblox.client.startup.ActivitySplash','-d',O000000O00OO00OOO ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:152
        time .sleep (10 )#line:153
        subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OO000O000O0OOO0O0}','shell','am','start','-n','com.roblox.client/com.roblox.client.ActivityProtocolLaunch','-d',O000000O00OO00OOO ],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:156
        time .sleep (10 )#line:157
        print (Fore .GREEN +f"Membuka game menggunakan server: {O000000O00OO00OOO}.")#line:158
    except Exception as O0O000OOOOOOOO0OO :#line:159
        print (colored (f"Failed to start Default Server: {O0O000OOOOOOOO0OO}",'red'))#line:160
def auto_join_game (O0O00OO0OOO00OO00 ,OOO000O0OOOO0OO00 ,OO00O0O00000OOO0O ,O0OO00O0O00O00OO0 ):#line:163
    O0OO00O0O00O00OO0 [O0O00OO0OOO00OO00 ]="Opening Roblox"#line:164
    update_table (O0OO00O0O00O00OO0 )#line:165
    if OO00O0O00000OOO0O :#line:167
        start_private_server (O0O00OO0OOO00OO00 ,OO00O0O00000OOO0O )#line:168
    else :#line:169
        start_default_server (O0O00OO0OOO00OO00 ,OOO000O0OOOO0OO00 )#line:170
    O0OO00O0O00O00OO0 [O0O00OO0OOO00OO00 ]="Opening the Game"#line:172
    update_table (O0OO00O0O00O00OO0 )#line:173
    time .sleep (10 )#line:174
    O0OO00O0O00O00OO0 [O0O00OO0OOO00OO00 ]="In Game"#line:176
    update_table (O0OO00O0O00O00OO0 )#line:177
    time .sleep (1 )#line:178
def ensure_roblox_running_with_interval (O00OO000OO000000O ,O0OOO0OO00OO0O000 ,O0OOO0OOOOOOO0OO0 ,O0OOO00OOO00O000O ):#line:181
    O0000OOO0OO0OO00O ={OOO0OO000O000O0OO :"waiting"for OOO0OO000O000O0OO in O00OO000OO000000O }#line:182
    update_table (O0000OOO0OO0OO00O )#line:183
    O0O00000OOO0000O0 =O0OOO00OOO00O000O *60 #line:185
    OOO0OOOOOOO00000O =time .time ()#line:186
    while True :#line:188
        OO0OOO00O0O0OO0O0 =time .time ()-OOO0OOOOOOO00000O #line:189
        for O0O0O00OOO00OOO0O in O00OO000OO000000O :#line:190
            O0OOOOOOOOOOOOOOO =O0OOO0OOOOOOO0OO0 .get (O0O0O00OOO00OOO0O )#line:191
            if check_roblox_running (O0O0O00OOO00OOO0O ):#line:192
                O0000OOO0OO0OO00O [O0O0O00OOO00OOO0O ]="In Game"#line:193
                update_table (O0000OOO0OO0OO00O )#line:194
            else :#line:195
                O0000OOO0OO0OO00O [O0O0O00OOO00OOO0O ]="roblox offline"#line:196
                update_table (O0000OOO0OO0OO00O )#line:197
                force_close_roblox (O0O0O00OOO00OOO0O )#line:198
                auto_join_game (O0O0O00OOO00OOO0O ,O0OOO0OO00OO0O000 ,O0OOOOOOOOOOOOOOO ,O0000OOO0OO0OO00O )#line:199
        if O0OOO00OOO00O000O >0 and OO0OOO00O0O0OO0O0 >=O0O00000OOO0000O0 :#line:201
            for O0O0O00OOO00OOO0O in O00OO000OO000000O :#line:202
                O0OOOOOOOOOOOOOOO =O0OOO0OOOOOOO0OO0 .get (O0O0O00OOO00OOO0O )#line:203
                O0000OOO0OO0OO00O [O0O0O00OOO00OOO0O ]="roblox offline"#line:204
                update_table (O0000OOO0OO0OO00O )#line:205
                force_close_roblox (O0O0O00OOO00OOO0O )#line:206
                auto_join_game (O0O0O00OOO00OOO0O ,O0OOO0OO00OO0O000 ,O0OOOOOOOOOOOOOOO ,O0000OOO0OO0OO00O )#line:207
            OOO0OOOOOOO00000O =time .time ()#line:208
        time .sleep (5 )#line:209
def check_roblox_running (OO0O00OO0000O00O0 ):#line:212
    try :#line:213
        OO0OO00000O00O000 =subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OO0O00OO0000O00O0}','shell','pidof','com.roblox.client'],stdout =subprocess .PIPE ,stderr =subprocess .PIPE ,text =True )#line:217
        return bool (OO0OO00000O00O000 .stdout .strip ())#line:218
    except Exception as O000OOO0000000OO0 :#line:219
        print (colored (f"Error checking if Roblox is running on {OO0O00OO0000O00O0}: {O000OOO0000000OO0}",'red'))#line:220
        return False #line:221
def force_close_roblox (OOOO000000O0OO0OO ):#line:224
    subprocess .run ([ADB_PATH ,'-s',f'127.0.0.1:{OOOO000000O0OO0OO}','shell','am','force-stop','com.roblox.client'],stdout =subprocess .DEVNULL ,stderr =subprocess .DEVNULL )#line:226
    time .sleep (8 )#line:227
def start_instance_in_thread (OO0O00000O0000OOO ,OOOO00O000OO0OOOO ,O00000O000OOO0OOO ,OO000OO0OO0O0000O ):#line:230
    OOO00OO0O000OOOOO =[]#line:231
    for OO00O00O0OO0O0000 in OO0O00000O0000OOO :#line:232
        O0O0OOO0OO00OOO00 =threading .Thread (target =auto_join_game ,args =(OO00O00O0OO0O0000 ,OOOO00O000OO0OOOO ,O00000O000OOO0OOO .get (OO00O00O0OO0O0000 ),OO000OO0OO0O0000O ))#line:233
        O0O0OOO0OO00OOO00 .start ()#line:234
        OOO00OO0O000OOOOO .append (O0O0OOO0OO00OOO00 )#line:235
    for OO00O00O0OO0O0000 in OO0O00000O0000OOO :#line:237
        OOOOOO000O0OOOO00 =threading .Thread (target =ensure_roblox_running_with_interval ,args =([OO00O00O0OO0O0000 ],OOOO00O000OO0OOOO ,O00000O000OOO0OOO ,1 ))#line:238
        OOOOOO000O0OOOO00 .start ()#line:239
        OOO00OO0O000OOOOO .append (OOOOOO000O0OOOO00 )#line:240
    for O0O0OOO0OO00OOO00 in OOO00OO0O000OOOOO :#line:242
        O0O0OOO0OO00OOO00 .join ()#line:243
def update_table (O0OOO0OOOO00000O0 ):#line:246
    os .system ('cls'if os .name =='nt'else 'clear')#line:247
    OO0OOOO00OOO00O0O =[]#line:248
    for OOOO00O00O0OO0O00 ,OO00OOO00O0OO00O0 in O0OOO0OOOO00000O0 .items ():#line:249
        OOOO000O00OOO0O0O =get_username_from_prefs (OOOO00O00O0OO0O00 )#line:250
        if OO00OOO00O0OO00O0 =="In Game":#line:251
            OOO0OOO00OOO0OO00 ='green'#line:252
        elif OO00OOO00O0OO00O0 =="Opening the Game":#line:253
            OOO0OOO00OOO0OO00 ='cyan'#line:254
        elif OO00OOO00O0OO00O0 =="Opening Roblox":#line:255
            OOO0OOO00OOO0OO00 ='yellow'#line:256
        elif OO00OOO00O0OO00O0 =="roblox offline":#line:257
            OOO0OOO00OOO0OO00 ='red'#line:258
        else :#line:259
            OOO0OOO00OOO0OO00 ='magenta'#line:260
        OO0OOOO00OOO00O0O .append ({"NAME":f"emulator:{OOOO00O00O0OO0O00}","Username":OOOO000O00OOO0O0O or "Not Found","Proses":colored (OO00OOO00O0OO00O0 ,OOO0OOO00OOO0OO00 )})#line:262
    print (tabulate (OO0OOOO00OOO00O0O ,headers ="keys",tablefmt ="grid"))#line:264
    print (colored ("BANG OVA",'blue',attrs =['bold','underline']).center (50 ))#line:265
def menu ():#line:268
    O0OOO0OOOOO0O00O0 =load_config ()#line:269
    O000OOOO00O0O0OO0 =load_ports ()#line:270
    O0OO0O0O0OO0OOO0O =load_private_links ()#line:271
    if O000OOOO00O0O0OO0 :#line:273
        auto_connect_adb (O000OOOO00O0O0OO0 )#line:274
    else :#line:275
        print (colored ("ADB port not found. Please set it first..",'yellow'))#line:276
    if O0OOO0OOOOO0O00O0 :#line:278
        print (colored (f"Game ID: {O0OOO0OOOOO0O00O0} has been loaded from configuration.",'green'))#line:279
    else :#line:280
        print (colored ("User ID dan Game ID not set yet. Please set it first.",'yellow'))#line:281
    while True :#line:283
        print ("\nMenu:")#line:284
        print ("1. Auto join")#line:285
        print ("2. Set User ID dan Game ID")#line:286
        print ("3. Set Port ADB")#line:287
        print ("4. Set private code for all instances")#line:288
        print ("5. Set private code for 1 instance")#line:289
        print ("6. Exit")#line:290
        O0O0OOOOOO00O000O =input ("Select number (1/2/3/4/5/6): ")#line:292
        if O0O0OOOOOO00O000O =='1':#line:294
            if not O0OOO0OOOOO0O00O0 :#line:295
                print (colored ("User ID or Game ID has not been set. Please set it first.",'red'))#line:296
                continue #line:297
            OOO000000OOOOO00O =int (input ("Enter the time interval (in minutes, enter 0 for no interval).: "))#line:298
            ensure_roblox_running_with_interval (O000OOOO00O0O0OO0 ,O0OOO0OOOOO0O00O0 ,O0OO0O0O0OO0OOO0O ,OOO000000OOOOO00O )#line:299
        elif O0O0OOOOOO00O000O =='2':#line:300
            O0OOO0OOOOO0O00O0 =input ("Enter Game ID: ")#line:301
            save_config (O0OOO0OOOOO0O00O0 )#line:302
        elif O0O0OOOOOO00O000O =='3':#line:303
            O000O00O0O0O0OO0O =input ("Enter the ADB port (separate with commas if more than one).: ").split (',')#line:304
            save_ports ([O0O000OOO00000000 .strip ()for O0O000OOO00000000 in O000O00O0O0O0OO0O ])#line:305
            O000OOOO00O0O0OO0 =O000O00O0O0O0OO0O #line:306
            auto_connect_adb (O000OOOO00O0O0OO0 )#line:307
        elif O0O0OOOOOO00O000O =='4':#line:308
            OO0OO00O00O00OO00 =input ("Enter private code for all instances.(only support link like this https://www.roblox.com/games/2753915549/DRAGON-Blox-Fruits?privateServerLinkCode=313232213213123123131): ").strip ()#line:309
            for O00O000OO0000OOOO in O000OOOO00O0O0OO0 :#line:310
                save_private_link (O00O000OO0000OOOO ,OO0OO00O00O00OO00 )#line:311
                O0OO0O0O0OO0OOO0O =load_private_links ()#line:312
        elif O0O0OOOOOO00O000O =='5':#line:313
            OO00OOO00000O0000 =input ("Enter the instance port: ").strip ()#line:314
            OO0OO00O00O00OO00 =input ("Enter the private code for this instance.(only support link like this https://www.roblox.com/games/2753915549/DRAGON-Blox-Fruits?privateServerLinkCode=313232213213123123131): ").strip ()#line:315
            save_private_link (OO00OOO00000O0000 ,OO0OO00O00O00OO00 )#line:316
            O0OO0O0O0OO0OOO0O =load_private_links ()#line:317
        elif O0O0OOOOOO00O000O =='6':#line:318
            print ("Exit the program...")#line:319
            break #line:320
        else :#line:321
            print ("Invalid selection!")#line:322
menu ()
