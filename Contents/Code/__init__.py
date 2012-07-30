# PMS plugin framework
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

####################################################################################################

MUSIC_PREFIX = "/music/sverigesradioplay"

ART           = 'art-default.jpg'
ART_DIREKT    = 'art-direkt.jpg'
ART_POD       = 'art-pod.jpg'
ICON          = 'icon-default.png'
ICON_DIREKT   = 'c-direkt.png'
ICON_ARKIV    = 'c-arkiv.png'
ICON_ALLA     = 'c-alla.png'
ICON_BARN     = 'c-barn.png'
ICON_DOKU     = 'c-doku.png'
ICON_KULT     = 'c-kult.png'
ICON_LIV1     = 'c-liv1.png'
ICON_LIV2     = 'c-liv2.png'
ICON_MUSI     = 'c-musi.png'
ICON_NYHE     = 'c-nyhe.png'
ICON_SAMH     = 'c-samh.png'
ICON_SPOR     = 'c-spor.png'
ICON_SPRA     = 'c-spra.png'
ICON_VETE     = 'c-vete.png'
ICON_P1       = 'logo-p1.png'
ICON_P2       = 'logo-p2.png'
ICON_P3       = 'logo-p3.png'
ICON_P4       = 'logo-p4.png'
ICON_SR       = 'logo-sr.png'
ICON_EXTRA    = 'logo-sr-ext.png'
ICON_ALLA_POD = 'c-alla-pod.png'
ICON_BARN_POD = 'c-barn-pod.png'
ICON_DOKU_POD = 'c-doku-pod.png'
ICON_KULT_POD = 'c-kult-pod.png'
ICON_LIV1_POD = 'c-liv1-pod.png'
ICON_LIV2_POD = 'c-liv2-pod.png'
ICON_MUSI_POD = 'c-musi-pod.png'
ICON_NYHE_POD = 'c-nyhe-pod.png'
ICON_SAMH_POD = 'c-samh-pod.png'
ICON_SPOR_POD = 'c-spor-pod.png'
ICON_SPRA_POD = 'c-spra-pod.png'
ICON_VETE_POD = 'c-vete-pod.png'
ICON_SR_POD   = 'logo-sr-pod.png'

ITUNES_NAMESPACE                      = {'itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd'}

CACHE_TIME_LONG    = 60*60*24 # 1 day
CACHE_TIME_MEDIUM  = 60*60    # 1 hour
CACHE_TIME_SHORT   = 60*5     # 5 minutes

####################################################################################################

def Start():

    ## make this plugin show up in the 'Music' section
    ## in Plex. The L() function pulls the string out of the strings
    ## file in the Contents/Strings/ folder in the bundle
    Plugin.AddPrefixHandler(MUSIC_PREFIX, MainMenu, L('MainTitle'), ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

    ## set some defaults so that you don't have to
    ## pass these parameters to these object types
    ## every single time
    MediaContainer.art = R(ART)
    MediaContainer.title1 = L("Title")
    DirectoryItem.thumb = R(ICON_SR)
    DirectoryItem.summary = L("Summary")


#### the rest of these are user created functions and
#### are not reserved by the plugin framework.

#
# Main menu referenced in the Start() method
# for the 'Music' prefix handler
#

def MainMenu():

    dir = MediaContainer(viewGroup="List")
    dir.title1 = L("Title")
    dir.art = R(ART)

    #  Add ListenLiveMenu
    dir.Append(
        Function(
            DirectoryItem(
                ListenLiveMenu,
                L("ListenLiveTitle"),
                subtitle=L("ListenLiveSubtitle"),
                summary=L("ListenLiveSummary"),
                thumb=R(ICON_DIREKT),
                art=R(ART)
            )
        )
    )

    #  Add MainPodcastMenu
    dir.Append(
        Function(
            DirectoryItem(
                MainPodcastMenu,
                L("PodMainTitle"),
                subtitle=L("PodMainSubtitle"),
                summary=L("PodDescription"),
                thumb=R(ICON_ARKIV),
                art=R(ART)
            )
        )
    )

    #  Add AllProgramsMenu
    dir.Append(
        Function(
            DirectoryItem(
                AllProgramsMenu,
                L("AllProgramsTitle"),
                subtitle=L("AllProgramsSubtitle"),
                summary=L("AllProgramsSummary"),
                thumb=R(ICON_ALLA),
                art=R(ART)
            ),
            categoryid=0,
            categorytitle=L("AllProgramsTitle")
        )
    )

    #  Add Categories
    page = XML.ElementFromURL("http://api.sr.se/api/Poddradio/PoddCategories.aspx", cacheTime=CACHE_TIME_LONG)

    for item in page.getiterator('item'):
   
        title = item.findtext("title")
        caticon = R(ICON_SR)
        if "Barn" in title:
            caticon = R(ICON_BARN)
        elif "Dokument" in title:
            caticon = R(ICON_DOKU)
        elif "Kultur" in title:
            caticon = R(ICON_KULT)
        elif "Livsstil" in title:
            caticon = R(ICON_LIV1)
        elif "dning" in title:
            caticon = R(ICON_LIV2)
        elif "Musik" in title:
            caticon = R(ICON_MUSI)
        elif "Nyheter" in title:
            caticon = R(ICON_NYHE)
        elif "Sam" in title:
            caticon = R(ICON_SAMH)
        elif "Sport" in title:
            caticon = R(ICON_SPOR)
        elif "Spr" in title:
            caticon = R(ICON_SPRA)
        elif "Vetenskap" in title:
            caticon = R(ICON_VETE)
        else:
            caticon = R(ICON_SR)
        
        dir.Append(
            Function(
                DirectoryItem(
                    AllProgramsMenu,
                    title,
                    subtitle="",
                    summary="",
                    thumb=caticon,
                    art=R(ART)
                ),
                categoryid=int(item.findtext("id", default="0")),
                categorytitle=title
            )
        )


    # ... and then return the container
    return dir

def ListenLiveMenu(sender):

    dir = MediaContainer(viewGroup="InfoList")
    dir.title1 = L("Title")
    dir.title2 = L("ListenLiveTitle")
    dir.art = R(ART_DIREKT)

    page = XML.ElementFromURL("http://api.sr.se/api/channels/channels.aspx", cacheTime=CACHE_TIME_LONG)
    rightnow = XML.ElementFromURL("http://api.sr.se/api/rightnowinfo/rightnowinfo.aspx?filterinfo=all", cacheTime=None)

    for channel in page.getiterator('channel'):

        info = rightnow.find("Channel[@Id='" + channel.attrib.get("id") + "']")
        desc = ""
        ch_name = channel.attrib.get("name")

        ch_thumb = R(ICON_DIREKT)
        if "P1" in ch_name:
            ch_thumb = R(ICON_P1)
        elif "P2" in ch_name:
            ch_thumb = R(ICON_P2)
        elif "P3" in ch_name:
            ch_thumb = R(ICON_P3)
        elif "P4" in ch_name:
            ch_thumb = R(ICON_P4)
        elif "SR Extra" in ch_name:
            ch_thumb = R(ICON_EXTRA)
        else:
            ch_thumb = R(ICON_SR)

        if info:

            if info.findtext("ProgramTitle"):
                desc += str(info.findtext("ProgramTitle")) + "\n"
                if info.findtext("ProgramInfo"):
                    desc += str(info.findtext("ProgramInfo")) + "\n\n"
                else:
                    desc += "\n"
            else:
                if info.findtext("Song"):
                    desc += str(info.findtext("Song")) + "\n\n"
                if info.findtext("NextSong"):
                    desc += L("NextProgram") + ":\n" + str(info.findtext("NextSong")) + "\n\n"

            if info.findtext("NextProgramStartTime"):
                desc += "\n" + L("NextProgram") + ":\n"
                if info.findtext("NextProgramTitle"):
                    desc += str(info.findtext("NextProgramTitle")) + " (" + str(info.findtext("NextProgramStartTime")) + ")\n"
                    if info.findtext("NextProgramDescription"):
                        desc += str(info.findtext("NextProgramDescription")) + "\n"

        dir.Append(
            TrackItem(
                channel.findtext("streamingurl/url[@type='mp3']"),
                ch_name,
                subtitle=channel.findtext("tagline"),
                summary=desc,
                thumb=ch_thumb
            )
        )


    # ... and then return the container
    return dir
  
def AllProgramsMenu(sender, categoryid, categorytitle):

    dir = MediaContainer(viewGroup="InfoList")
    dir.title1 = L("Title")
    dir.title2 = categorytitle
    dir.art = R(ART)

    feedurl = "http://api.sr.se/api/program/programfeed.aspx"

    if categoryid == 0:
        feedurl = "http://api.sr.se/api/program/programfeed.aspx"
    else:
        feedurl = "http://api.sr.se/api/program/programfeed.aspx?CategoryId=" + str(categoryid)

    page = XML.ElementFromURL(feedurl, cacheTime=CACHE_TIME_MEDIUM)

    for item in page.getiterator('item'):

        hasOndemand = item.find("ondemand").attrib.get("hasOndemand")
        if hasOndemand == "1":
        
            description = str(item.findtext("description"))
            if item.findtext("broadcastinfo"):
                description += "\n\n" + str(item.findtext("broadcastinfo"))

            unitid = item.findtext("unitid")
            poddid = "0"
            podd = item.find("poddunits/podd")
            if podd is not None:
                poddid = podd.attrib.get("poddid")

            #  Add ProgramMenu
            dir.Append(
                Function(
                    DirectoryItem(
                        ProgramMenu,
                        item.findtext("title"),
                        subtitle=item.findtext("payoff"),
                        summary=description,
                        thumb=R(ICON_SR),
                        art=R(ART)
                    ),
                    poddid=poddid,
                    unitid=unitid
                )
            )

    # ... and then return the container
    return dir


def ProgramMenu(sender, poddid, unitid):

    feedurl = "http://api.sr.se/api/program/broadcastfeed.aspx?unitid=" + unitid

    page = XML.ElementFromURL(feedurl, cacheTime=CACHE_TIME_SHORT)

    dir = MediaContainer(viewGroup="InfoList")
    dir.title1 = L("Title")
    dir.title2 = page.findtext("title")
    dir.art = R(ART)

    channellogo = R(ICON_SR)
    baseurl = page.xpath("//urlset/url[@type='m4a' and @protocol='http' and @quality='normal' and @name='LatestBroadcast']/text()")[0]

    for item in page.getiterator('item'):

        broadcastid = item.find("ondemand").attrib.get("mainbroadcastid")
        itemlink = baseurl.replace("[broadcastid]", broadcastid)
        itemtitle = item.find("ondemand").attrib.get("mainbroadcasttitle")
        itemsubtitle = item.find("ondemand").attrib.get("mainbroadcastdate")
        itemsummary = item.find("ondemand").attrib.get("mainbroadcastdescription")

        dir.Append(
            TrackItem(
                itemlink,
                itemtitle,
                subtitle=itemsubtitle,
                summary=itemsummary,
                thumb=channellogo
            )
        )

    #  Append PodcastMenu if one exists
    if poddid != "0":
        dir.Append(
            Function(
                DirectoryItem(
                    PodcastMenu,
                    L("PodItemTitle"),
	            subtitle=L("PodItemSubtitle"),
	            summary=L("PodDescription"),
	            thumb=R(ICON_ARKIV),
	            art=R(ART)
	        ),
	        poddid=poddid,
	        unitid=unitid
            )
        )

    # ... and then return the container
    return dir

def MainPodcastMenu(sender):

    dir = MediaContainer(viewGroup="List")
    dir.title1 = L("PodTitle")
    dir.art = R(ART_POD)

    #  Add AllPodcastsMenu
    dir.Append(
        Function(
            DirectoryItem(
                AllPodcastsMenu,
                L("AllProgramsTitle"),
                subtitle=L("AllProgramsSubtitle"),
                summary=L("AllProgramsSummary"),
                thumb=R(ICON_ALLA_POD),
                art=R(ART_POD)
            ),
            categoryid=0,
            categorytitle=L("AllProgramsTitle")
        )
    )

    #  Add Podcast Categories
    page = XML.ElementFromURL("http://api.sr.se/api/Poddradio/PoddCategories.aspx", cacheTime=CACHE_TIME_LONG)

    for item in page.getiterator('item'):
   
        title = item.findtext("title")
        caticon = R(ICON_SR_POD)
        if "Barn" in title:
            caticon = R(ICON_BARN_POD)
        elif "Dokument" in title:
            caticon = R(ICON_DOKU_POD)
        elif "Kultur" in title:
            caticon = R(ICON_KULT_POD)
        elif "Livsstil" in title:
            caticon = R(ICON_LIV1_POD)
        elif "dning" in title:
            caticon = R(ICON_LIV2_POD)
        elif "Musik" in title:
            caticon = R(ICON_MUSI_POD)
        elif "Nyheter" in title:
            caticon = R(ICON_NYHE_POD)
        elif "Sam" in title:
            caticon = R(ICON_SAMH_POD)
        elif "Sport" in title:
            caticon = R(ICON_SPOR_POD)
        elif "Spr" in title:
            caticon = R(ICON_SPRA_POD)
        elif "Vetenskap" in title:
            caticon = R(ICON_VETE_POD)
        else:
            caticon = R(ICON_SR_POD)
        
        dir.Append(
            Function(
                DirectoryItem(
                    AllPodcastsMenu,
                    title,
                    subtitle="",
                    summary="",
                    thumb=caticon,
                    art=R(ART_POD)
                ),
                categoryid=int(item.findtext("id", default="0")),
                categorytitle=title
            )
        )


    # ... and then return the container
    return dir

def AllPodcastsMenu(sender, categoryid, categorytitle):

    dir = MediaContainer(viewGroup="InfoList")
    dir.title1 = L("PodTitle")
    dir.title2 = categorytitle
    dir.art = R(ART_POD)

    feedurl = "http://api.sr.se/api/Poddradio/PoddFeed.aspx"

    if categoryid == 0:
        feedurl = "http://api.sr.se/api/Poddradio/PoddFeed.aspx"
    else:
        feedurl = "http://api.sr.se/api/Poddradio/PoddFeed.aspx?CategoryId=" + str(categoryid) 

    page = XML.ElementFromURL(feedurl, cacheTime=CACHE_TIME_MEDIUM)

    for item in page.getiterator('item'):

        #  Add PodcastMenu
        dir.Append(
            Function(
                DirectoryItem(
                    PodcastMenu,
                    item.findtext("title"),
                    subtitle=item.findtext("unit"),
                    summary=item.findtext("description"),
                    thumb=R(ICON_SR_POD),
                    art=R(ART_POD)
                ),
                poddid=item.findtext("poddid"),
                unitid=item.findtext("unitid")
            )
        )

    # ... and then return the container
    return dir

def PodcastMenu(sender, poddid, unitid):

    poddurl = "http://api.sr.se/api/rssfeed/rssfeed.aspx?Poddfeed=" + poddid

    page = XML.ElementFromURL(poddurl, cacheTime=CACHE_TIME_SHORT)

    dir = MediaContainer(viewGroup="InfoList")
    dir.title1 = L("PodTitle")
    dir.title2 = page.findtext("channel/title")
    dir.art = R(ART_POD)

    channellogo = page.xpath('//itunes:image', namespaces=ITUNES_NAMESPACE)[0].get('href')

    for item in page.getiterator('item'):

        dir.Append(
            TrackItem(
                item.findtext("link"),
                item.findtext("title"),
                subtitle=item.findtext("pubDate"),
                summary=item.findtext("description"),
                duration=int(item.find("enclosure").attrib.get("length")) * 8 / 128,
                thumb=channellogo
            )
        )

    # ... and then return the container
    return dir
