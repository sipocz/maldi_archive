# maldi_archive.py
import os
import shutil
import datetime as dt
import re

# ---------------------------
# Sipőcz László 2020. 01. 31.
# ---------------------------


# path definition

_logext = ".log"
_swname = "MALDI_ARCHIVE_"



_MaldiInput="C:\\Hungary\\dfsroot\\maldi_eredmenyek\\PRD\\"

_Logdirectory="\\log"
_Basedirectory="C:\\maldi_copy\\"
_UsedPlateFile="plates.dat"
_DebugToFile=True
_logprefix = _Basedirectory+_Logdirectory
_usedplatelist=_Basedirectory+_UsedPlateFile    # egy fájlra mutat ami csv-ként tartalmazza a plateID és fióktelep összerendeléseket


_DORNAME="DOROG"
_DEBNAME="DEBRECEN"
_BUDNAME="BUDAPEST"



_DOR_Source_Path="C:\\Hungary\\dfsroot\\maldi_eredmenyek\\Dorog_kezi\\"
_DEB_Source_Path="C:\\Hungary\\dfsroot\\maldi_eredmenyek\\Debrecen_kezi\\"
_BUD_Source_Path="C:\\Hungary\\dfsroot\\maldi_eredmenyek\\Budapest_kezi\\"

sites=(_DORNAME,_DEBNAME,_BUDNAME)
sites_place={_DORNAME:_DOR_Source_Path,_DEBNAME:_DEB_Source_Path,_BUDNAME:_BUD_Source_Path}

def createLogFile():
    '''
    meghatározza a msg fájl nevét
    :return: a Log file neve stringként
    '''
    import datetime as dt
    from os import path as ospath
    currentdate=dt.datetime.now()
    isostr=currentdate.isoformat()
    datestr="/"+_swname+str(isostr[0:4])+str(isostr[5:7])+str(isostr[8:10])
    fname=_logprefix+datestr+_logext
    #print(fname)
    if ospath.exists(fname):
       pass
    else:
        fileLog = open(fname, "x")
        fileLog.close()
        msg(tofile=_DebugToFile)
        msg("created",tofile=_DebugToFile)
    return (fname)


def timestamp(): 
    '''
    Az aktuális időpontot adja vissza string formában YYYY-MM-DD HH-MM-SS.xxxxxx
    '''
    n = dt.datetime.now()
    n.isoformat(" ", "seconds")
    # print(n)
    return (n)


def msg(msgstr="",tofile=True):
    '''
    :param msgstr: kiírandó szöveg
    :param tofile: alapértelmezett True esetén fájba ír, átírva standard kimenet
    :return:
    '''
    import sys
    caller=sys._getframe(1).f_code.co_name
    if msgstr=="":
        
        if tofile:

            filename=createLogFile()
            fname=open(filename, "a")
            print(timestamp(),file=fname)
            print("\tDEF: ",caller,file=fname)
            fname.close()
        else:
            print(timestamp())
            print("\tDEF: ", caller)
        #print("~"*(len(caller)+4))
    else:
        if tofile:
            filename = createLogFile()
            fname=open(filename, "a")
            print("\t\t"+caller+"-"+msgstr,file=fname)
            fname.close()
        else:
            print("\t\t" +caller+"-"+msgstr)



def listfiles(directory):
    '''
    directory könyvtár elemeit listázza
    :return: listába rendezett fálnevek
    '''
    msg(tofile=_DebugToFile)
    f = []
    for (_, _, filenames) in os.walk(directory):
        f.extend(filenames)
    msg("return: "+str(f), tofile=_DebugToFile)
    return(f)




def copyafile(sourcepath,fname,destpath,prefix):
    '''
    sourcepath könyvtárból fname file-t dest könyvtárba másolja prefix-et tesz a fname elejére 
    '''
    msg(tofile=_DebugToFile)
    sourcefname=sourcepath+fname
    destfname=destpath+prefix+fname
    # print(sourcefname,destfname)  # DEBUG print
    try:
        shutil.copyfile(sourcefname,destfname)
        msg("File copy: "+sourcefname+"-->"+destfname, tofile=_DebugToFile)    
    except: 
        print(destfname)  # DEBUG print
        msg("Exception return: "+" **** ERROR IN FILE COPY ****", tofile=_DebugToFile)        



def parseCSV(str):
    '''
    pontosvessző tagolt stringet elemei bont 
    :param str: a feldolgozandó string  
    :return:  list
    '''
    # print("parse:", str.strip())

    a = str.strip().split(";")
    return (a)

#e8 = u.encode('utf-8')        # encode without BOM
#e8s = u.encode('utf-8-sig')   # encode with BOM
#e16 = u.encode('utf-16')      # encode with BOM
#e16le = u.encode('utf-16le')  # encode without BOM
#e16be = u.encode('utf-16be')  # encode without BOM


def loadCSVfile(fname):
    '''
    csv fálj betöltése egy listába
    param fname: a fájl neve teljes elérési út
    :return: listában adja vissza a file tartalmát
    '''
    msg()
    msg("filename:"+fname)
    l1=[]
    csvfile = open(fname, "rt" , encoding='latin-1')
    for line in csvfile.readlines():
        l1.append(parseCSV(line))
    csvfile.close()
    return (l1)

def loadplates():
    f=loadCSVfile(_usedplatelist)
    f2=dict(f)
    return(f2) 



def checkfile(fname):
    '''
    fname ellenőrzése
        .csv?
        plateID létezik, és helyes?
    return: True, ha minden OK
    '''
    # print("*** file name:",fname)
    # .csv file érkezett?
    o=True
    if fname[-4:].upper() != ".CSV":
        return(False)
    
    # plate id korrekt?
    # megnézük hogy a file nevében szerepel-e a site és szerepel e a sitehoz rendelt plateid
    #
    foundamatch=False
    for key in plates :
        # print(fname, key,plates[key])   # DEBUG PRINT
        if (key in fname) and (plates[key] in fname ):
            foundamatch=True
            
    if not(foundamatch):
        return(False)
    
    # fenntartva egyéb pl. belső szintaktikai ellenőrzések számára
    # 
    if True:
        pass

    # ha nem léptünk ki hibával akkor kilépünk True-val
    return(True)

def ready_to_archive():
    '''
    A konfigurált könyvtárakban keresi a PLATE ID-t tartalmazó fájlokat 
    '''
    msg()
    for site in sites:
        msg("Telephely adatainak feldolgozása: "+site)
        print(site)
        print(sites_place[site])

# main


ready_to_archive()
