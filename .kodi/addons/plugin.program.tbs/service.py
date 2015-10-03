import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, os, sys, time, xbmcvfs
import shutil
import time
from addon.common.addon import Addon

#################################################
AddonID        = 'plugin.program.tbs'
#################################################
dialog         =  xbmcgui.Dialog()
dp             =  xbmcgui.DialogProgress()
ADDON          =  xbmcaddon.Addon(id=AddonID)
ADDONDATA      =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data',''))
TBSXML         =  xbmc.translatePath(os.path.join('special://home/addons/plugin.program.tbs/addon.xml'))
firstrun       =  xbmc.translatePath('special://home/userdata/firstrun/')
sellername     =  ADDON.getSetting('resellername')
internetcheck  =  ADDON.getSetting('internetcheck')
cbnotifycheck  =  ADDON.getSetting('cbnotifycheck')
trcheck        =  ADDON.getSetting('trcheck')
idfile         =  xbmc.translatePath(os.path.join(ADDONDATA,AddonID,'id.xml'))
TBSDATA        =  xbmc.translatePath(os.path.join(ADDONDATA,AddonID,''))
newguifile     =  xbmc.translatePath(os.path.join('special://home','newbuild'))

if os.path.exists(newguifile):
    time.sleep(10)
    dialog.ok('New Keyword Detected','An install or update of a keyword has recently taken place, please be patient while the keyword content updates. Your skin may momentarily flicker or go black for a minute or two - do not worry this is perfectly normal.')
    shutil.rmtree(newguifile)
#    xbmc.executebuiltin('ActivateWindow(10040,"addons://outdated/",return)')

if AddonID=='plugin.program.tbs' and trcheck=='true':
    localfile2      = open(TBSXML, mode='r')
    content2        = file.read(localfile2)
    file.close(localfile2)
    
    localnamematch  = re.compile('tbs" name="(.+?)"').findall(content2)
    localnamecheck  = localnamematch[0] if (len(localnamematch) > 0) else 'TBS'
    print'###### '+localnamecheck+' Update Service ######'

else:
    print"##### TotalRevolution Update Service #####"

if not os.path.exists(TBSDATA):
    os.makedirs(TBSDATA)

xbmc.executebuiltin('XBMC.RunScript(special://home/addons/'+AddonID+'/notify.py)')
if not os.path.exists(firstrun) and sellername != '' and trcheck=='true':
        xbmc.sleep(2000)
        
        if not os.path.exists(firstrun):
            choice = dialog.yesno("Install Packs Available",'[COLOR=yellow]Would you like to view the packs available on this device?[/COLOR]','[COLOR=lime]IMPORTANT:[/COLOR] Packs may contain add-ons offering access to','content deemed unlawful in your country. Please check your local laws before installing.')
            
            if choice ==1:
                os.makedirs(firstrun)
                xbmc.executebuiltin('ActivateWindow(10001,"plugin://plugin.program.tbs?mode=community&name=Community%20Builds&url=reseller",return)')
            
            if choice ==0:
                dialog.ok('Vanilla Setup','You now have a vanilla Kodi setup, a complete blank','canvas to create to your own taste. If you wish to install','any content you can still find it in the '+localnamecheck+' add-on.')
                os.makedirs(firstrun)

if internetcheck == 'true':
    xbmc.executebuiltin('XBMC.AlarmClock(internetloop,XBMC.RunScript(special://home/addons/'+AddonID+'/connectivity.py,silent=true),00:00:30,silent,loop)')

if sellername != '' or cbnotifycheck=='true':
    xbmc.executebuiltin('XBMC.AlarmClock(Notifyloop,XBMC.RunScript(special://home/addons/'+AddonID+'/notify.py,silent=true),00:30:00,silent,loop)')
