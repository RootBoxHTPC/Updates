import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os

import json


ADDON = xbmcaddon.Addon(id='plugin.video.uktvplay')

img=os.path.join(ADDON.getAddonInfo('path'),'resources','img')

#http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId=2134509084001

def CATEGORIES():
    addDir('Dave','dave',1,img+'/dave.jpg','')
    addDir('Really','really',1,img+'/really.jpg','')
    addDir('Yesterday','yesterday',1,img+'/yesterday.png','')
    addDir('Drama','drama',1,img+'/drama.jpg','')
       
                                                                      
def GetContent(url):
    CHANNEL = url       
    xunity='http://vschedules.uktv.co.uk/mapi/browse/?format=json'
    
    response=OPEN_URL(xunity)
    
    link=json.loads(response)

    data=link['brands']

    for field in data:
        name= field['name'].encode("utf-8")
        iconimage= field['image'].encode("utf-8")
        channel=field['channel'].encode("utf-8")
        try:desc=field['description'].encode("utf-8")
        except:desc=''
        brand_id=field['id']
        if CHANNEL in channel:
            
            addDir(name.strip(),str(brand_id),2,iconimage,desc)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)            
    setView('movies', 'default')

    
    
def GetEpisodes(url):
        
    xunity='http://vschedules.uktv.co.uk/mapi/branddata/?format=json&brand_id='+url
    
    response=OPEN_URL(xunity)
    
    link=json.loads(response)

    data=link['videos']

    for field in data:
        name= 'S'+field['series_txt']+'E'+field['episode_txt']+' - '+field['brand_name'].encode("utf-8")
        iconimage= field['episode_img_cached'].encode("utf-8")
        channel=field['channel'].encode("utf-8")
        desc=field['teaser_text'].encode("utf-8")
        brightcove=field['brightcove_video_id']            
        addDir(name,str(brightcove),200,iconimage,desc)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)            
    setView('movies', 'default') 
                   
 
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
    
    
def PLAY_STREAM(name,url,iconimage):
    url='http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId='+url    
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

    
    
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def addDir(name,url,mode,iconimage,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        if mode ==200:
            liz.setProperty("IsPlayable","true")
            
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
        
 
        
def setView(content, viewType):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass

   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        GetContent(url)

elif mode==2:
        print ""+url
        GetEpisodes(url)        
        
elif mode==200:

        PLAY_STREAM(name,url,iconimage)
    
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
