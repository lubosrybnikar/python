#pri otvarani skriptu vybrat moznost Edit with IDLE (ArcGIS Pro)
import arcpy
arcpy.env.overwriteOutput = True
#import toolboxu s natrojom PripravaUdajovKN
arcpy.ImportToolbox(r"D:\rybnikar\PripravaUdajovKN.tbx", "kn")

#vytvorenie slovnika, ktory priraduje kod KU k nazvu KU 
zoznam_ku = {
  "871796": "ZahorskaBystrica",
  "870293": "Vrakuna",
  "853771": "Rusovce",
  "847755": "PodunajskeBiskupice",
  "822256": "Jarovce",
  "810649": "DevinskaNovaVes",
  "809985": "Cunovo",
  "806099": "Dubravka",
  "806005": "Lamac",
  "805866": "Raca",
  "805700": "Vajnory",
  "805556": "Ruzinov",
  "805343": "Trnavka",
  "805301": "Devin",
  "805211": "KarlovaVes",
  "804959": "Petrzalka",
  "804690": "NoveMesto",
  "804380": "Vinohrady",
  "804274": "Nivy",
  "804096": "StareMesto", 
}


#cyklus, ktory spusti nastoroj nad datami jednotlivych k. u.
for ku_kod, ku_naz in zoznam_ku.items():
    print(ku_naz)
    #vystupne GDB budu pomenovane podla nazvov jednotlivych k. u. 
    arcpy.management.CreateFileGDB(r'D:\rybnikar\2022_10\KU', ku_naz)
    print('Geodatabaza ' + ku_naz + ' vytvorena.')
    #premenna output_DB obsahuje cestu k vystupnej GDB vytvorenej v predoslom kroku
    output_DB = r'D:\\rybnikar\\2022_10\\KU\\' + ku_naz + r'.gdb'
    #premenna gdb obsahuje cestu k databazam v zlozke 1070000001 (mozu mat koncovku _1_1, 3_8_I alebo _2_1)
    gdb = r'D:\rybnikar\2022_10\C_gdb\KN' + ku_kod + r'_1_1.gdb'
    if not arcpy.Exists(gdb):
        gdb = r'D:\rybnikar\2022_10\C_gdb\KN' + ku_kod + r'_2_1.gdb'
        if not arcpy.Exists(r'D:\rybnikar\2022_10\C_gdb\KN' + ku_kod + r'_2_1.gdb'):
            gdb = r'D:\rybnikar\2022_10\C_gdb\KN' + ku_kod + r'_3_8_I.gdb'
    print(gdb)
    znacky = gdb + r'\znacky'
    hranice = gdb + r'\zappar_hrandruhpozemk'
    plocha_p_C = gdb + r'\kladpar_plochy'
    #premenna gdb2 obsahuje cestu k databazam v zlozke 2022_3_2_kon (mozu mat koncovku _3_8, _3_2  alebo _3_1)
    gdb2 = r'D:\rybnikar\2022_10\E_gdb\UO' + ku_kod + r'_3_8.gdb'
    if not arcpy.Exists(gdb2):
        gdb2 = r'D:\rybnikar\2022_10\E_gdb\UO' + ku_kod + r'_3_2.gdb'
        if not arcpy.Exists(r'D:\rybnikar\2022_10\E_gdb\UO' + ku_kod + r'_3_2.gdb'):
            gdb2 = r'D:\rybnikar\2022_10\E_gdb\UO' + ku_kod + r'_3_1.gdb'    
    print(gdb2)
    plocha_p_E = gdb2 + r'\uov_plochy'
    #premnne obsahuje cestu k databazam v zlozke 
    tabulka_CS = r'D:\rybnikar\2022_10\DATA_SPI\cs' + ku_kod + r'.dbf'
    tabulka_EP = r'D:\rybnikar\2022_10\DATA_SPI\ep' + ku_kod + r'.dbf'
    tabulka_PA = r'D:\rybnikar\2022_10\DATA_SPI\pa' + ku_kod + r'.dbf'
    #spustenie nastroja s parametrami definovanymi v premennych
    arcpy.PripravaUdajovKN_kn(output_DB, znacky, hranice, plocha_p_C, plocha_p_E, tabulka_CS, tabulka_EP, tabulka_PA)
    print ('operacia uspesne prebehla')

#spojenie vrstiev jednotlivych k. u. do jednej vrstvy pre Bratislavu
#ako workspace nastavi priecinok, v ktorom boli v predoslom kroku vytvorene GDB jednotlivych k. u. 
arcpy.env.workspace = r'D:\rybnikar\2022_10\KU'
#zoznam GDB jednotlivych k. u. 
ku_list = arcpy.ListWorkspaces()
#zoznam tried prvkov, ktore obsahuje kazda GDB
fc_list = ["kladpar_plochy", "uov_plochy", "zappar_hrandruhpozemk", "znacky"]

#vytvorenie vystupnej GDB
arcpy.management.CreateFileGDB(r'D:\rybnikar\2022_10', 'BA_2022_10')

#cyklus, ktory pomocou nastroja Merge spoji vrstvy v GDB jedotlivych k. u. do novych vrstiev v novej GDB pre Bratislavu
for fc in fc_list:
        print(fc + " - start")
        path_list = []
        for ku in ku_list:
                path_list.append(ku + r'\\' + fc)

        arcpy.management.Merge(path_list, r'D:\rybnikar\2022_10\BA_2022_10.gdb\\'+ fc +r'_merge')
        print ('Successfully merged ' + fc)

