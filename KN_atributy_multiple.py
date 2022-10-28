#pri otvarani skriptu vybrat moznost Edit with IDLE (ArcGIS Pro)
import arcpy
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r'D:\rybnikar\2022_09\BA_2022_09.gdb'

#vytvorenie zoznamu polygonovych vrstiev
list_fc = arcpy.ListFeatureClasses(feature_type='Polygon')

#ulozenie vrstvy komunikacii a tabulky s nazvami k. u. do premennej
komunikacie = r'D:\rybnikar\BA_OSM\komunikacie_vybrane_BA.shp'
ku_table = r'D:\rybnikar\Kataster_07_2022\UTJ_mc_okresy.xls\Hárok1$'

#cyklus, ktory zopakuje operacie pre vsetky vrstvy zo zoznamu
for fc in list_fc:
    #pridanie pola s nazvom k. u.
    arcpy.management.JoinField(fc, 'CKU', ku_table, 'UTJ_E', 'KU')
    print ('Successfully joined ' + fc)

    #pridanie poli Najdi parcelu, Google Street View a pomocnych poli pre suradnice v spravnom formate
    arcpy.management.AddField(fc, 'find_pc', 'TEXT', '', '', '', 'Nájdi parcelu')
    arcpy.management.AddField(fc, 'sview', 'TEXT','', '', '1000', 'Google Street View')
    #arcpy.management.AddField(fc, 'x_sur_bodka', 'TEXT')
    #arcpy.management.AddField(fc, 'y_sur_bodka', 'TEXT')
    print ('Successfully added fields in ' + fc)

    #aktualizacia pola Najdi parcelu
    arcpy.management.CalculateField(fc, 'find_pc', "$feature.ku + ': ' + $feature.cpa_text", 'ARCADE')
    print ('Successfully calculated field in ' + fc)

    #vyber parcel nachadzajucich sa v blizkosti 10 m od cesty - pre ne sa bude vytvarat odkaz na Google Street View
    parcely_fc_select = arcpy.management.SelectLayerByLocation(fc, 'INTERSECT', komunikacie, '10 Meters')
    print ('Successfully selected features in ' + fc)

    #vypocet suradnic parcel
    arcpy.management.CalculateGeometryAttributes(parcely_fc_select, [['x_sur', 'CENTROID_X'],['y_sur', 'CENTROID_Y']], '', '', '4326', 'SAME_AS_INPUT')
    print ('Successfully calculated coordinates in ' + fc)

    #nahradenie desatinnej ciarky bodkou, vyplnenie pola Street View
    arcpy.management.CalculateField(parcely_fc_select, 'x_sur_bodka', "Replace($feature.x_sur, ',', '.')", 'ARCADE')
    arcpy.management.CalculateField(parcely_fc_select, 'y_sur_bodka', "Replace($feature.y_sur, ',', '.')", 'ARCADE')
    arcpy.management.CalculateField(parcely_fc_select, 'sview', "'https://www.google.com/maps?cbll=' + $feature.y_sur_bodka + ',' + $feature.x_sur_bodka + '&cbp=11,90,0,0,5&layer=c'"
                                , 'ARCADE')
    print ('Successfully calculated fields in ' + fc)



