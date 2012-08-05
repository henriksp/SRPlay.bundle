# -*- coding: utf-8 -*-

from common import *

def Start():

	Plugin.AddPrefixHandler(MUSIC_PREFIX, MainMenu, TEXT_MAIN_TITLE, ICON, ART)

	Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
	Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

	MediaContainer.art = R(ART)
	MediaContainer.title1 = TEXT_TITLE
	DirectoryItem.thumb = R(ICON_SR)
	DirectoryItem.summary = TEXT_SUMMARY

def MainMenu():

	dir = ObjectContainer(view_group="List")
	dir.title1 = TEXT_TITLE
	dir.art = R(ART)

	#  Add ListenLiveMenu
	dir.add(
		DirectoryObject(
			title=TEXT_LIVE_SHOWS, 
			summary=TEXT_LIVE_SUMMARY, 
			tagline=TEXT_LIVE_TAGLINE, 
			key=Callback(ListenLiveMenu), 
			thumb=R(ICON_DIREKT), 
			art=R(ART)
		)
	)

	#  Add MainPodcastMenu
	dir.add(
		DirectoryObject(
			title=TEXT_POD_MAIN_TITLE, 
			summary=TEXT_POD_DESCRIPTION, 
			tagline=TEXT_POD_MAIN_TAGLINE, 
			key=Callback(MainPodcastMenu), 
			thumb=R(ICON_ARKIV), 
			art=R(ART)
		)
	)

	#  Add AllProgramsMenu
	dir.add(
		DirectoryObject(
			title=TEXT_ALL_PROG_TITLE, 
			summary=TEXT_ALL_PROG_SUMMARY, 
			tagline=TEXT_ALL_PROG_TAGLINE, 
			key=Callback(
				AllProgramsMenu, 
				categoryid=0, 
				categorytitle=TEXT_ALL_PROG_TITLE
			), 
			thumb=R(ICON_ALLA), 
			art=R(ART)
		)
	)

	#  Add Categories
	page = XML.ElementFromURL("http://api.sr.se/api/Poddradio/PoddCategories.aspx", 
		cacheTime=CACHE_TIME_LONG)

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
        
	dir.add(
		DirectoryObject(
			title=title, 
			key=Callback(
				AllProgramsMenu, 
				categoryid=int(item.findtext("id", default="0")), 
				categorytitle=title
			), 
			thumb=caticon,
			art=R(ART)
		)
	)        
    
	return dir

def ListenLiveMenu():

	dir = ObjectContainer(
		view_group = "List", 
		title1=TEXT_TITLE, 
		title2=TEXT_LIVE_SHOWS, 
		art = R(ART_DIREKT)
	)

	page = XML.ElementFromURL("http://api.sr.se/api/channels/channels.aspx", 
		cacheTime=CACHE_TIME_LONG)
	rightnow = XML.ElementFromURL("http://api.sr.se/api/rightnowinfo/rightnowinfo.aspx?filterinfo=all", 
		cacheTime=None)

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
				desc += TEXT_NEXT_PROGRAM + ":\n" + 
					str(info.findtext("NextSong")) + "\n\n"

		if info.findtext("NextProgramStartTime"):
			desc += "\n" + TEXT_NEXT_PROGRAM + ":\n"
		if info.findtext("NextProgramTitle"):
			desc += str(info.findtext("NextProgramTitle")) + 
				" (" + str(info.findtext("NextProgramStartTime")) + ")\n"
		if info.findtext("NextProgramDescription"):
			desc += str(info.findtext("NextProgramDescription")) + "\n"

		url = channel.findtext("streamingurl/url[@type='mp3']")
		Log.Info("live url %s", url)
		track = TrackObject(
			title = ch_name, 
			key =url, 
			rating_key = MUSIC_PREFIX + "/live/" + ch_name, 
			thumb = ch_thumb, 
			art = R(ART_DIREKT)
		)

		media = MediaObject(
			parts = [PartObject(key=Callback(PlayLiveAudio, url=url, ext='mp3'))],
			container = Container.MP3,
			audio_codec = AudioCodec.MP3
		)

		track.add(media)
		dir.add(track)

                #channel.findtext("streamingurl/url[@type='mp3']"),
                #ch_name,
                #subtitle=channel.findtext("tagline"),
                #summary=desc,
                #thumb=ch_thumb
	return dir

def PlayLiveAudio(url):
	return Redirect(url)

def AllProgramsMenu(sender, categoryid, categorytitle):

    dir = MediaContainer(viewGroup="InfoList")
    dir.title1 = TEXT_TITLE 
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
    dir.title1 = TEXT_TITLE 
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
                    TEXT_POD_ITEM_TITLE,
	            subtitle=TEXT_POD_ITEM_TAGLINE,
	            summary=TEXT_POD_DESCRIPTION,
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
    dir.title1 = TEXT_POD_TITLE
    dir.art = R(ART_POD)

    #  Add AllPodcastsMenu
    dir.Append(
        Function(
            DirectoryItem(
                AllPodcastsMenu,
                TEXT_ALL_PROG_TITLE,
                subtitle=TEXT_ALL_PROG_TAGLINE,
                summary=TEXT_ALL_PROG_SUMMARY,
                thumb=R(ICON_ALLA_POD),
                art=R(ART_POD)
            ),
            categoryid=0,
            categorytitle=TEXT_ALL_PROG_TITLE
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
    dir.title1 = TEXT_POD_TITLE 
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
    dir.title1 = TEXT_POD_TITLE 
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
