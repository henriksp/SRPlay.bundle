# -*- coding: utf-8 -*-
from common import *

##########################################################################################
def Start():
    ObjectContainer.title1 = TEXT_TITLE
    ObjectContainer.art = R(ART)
    
    DirectoryItem.thumb = R(ICON_SR)
    DirectoryItem.summary = TEXT_SUMMARY

##########################################################################################
@handler(PREFIX, TEXT_TITLE, thumb = ICON_SR, art = ART)
def MainMenu():
    oc = ObjectContainer()

    #  Add ListenLiveMenu
    oc.add(
        DirectoryObject(
            title = TEXT_LIVE_SHOWS,
            summary = TEXT_LIVE_SUMMARY,
            tagline = TEXT_LIVE_TAGLINE,
            key = Callback(ListenLiveMenu),
            thumb = R(ICON_DIREKT),
            art = R(ART)
        )
    )

    #  Add ProgramsMenu
    oc.add(
        DirectoryObject(
            title = TEXT_PROGRAMS,
            key = Callback(ProgramsMenu),
            thumb = R(ICON_ALLA),
            art = R(ART)
        )
    )

    return oc

##########################################################################################
@route(PREFIX + '/ListenLiveMenu')
def ListenLiveMenu():
    oc = ObjectContainer(
        title2 = TEXT_LIVE_SHOWS,
        art = R(ART_DIREKT)
    )

    data = JSON.ObjectFromURL(CHANNEL_URL, cacheTime = CACHE_TIME_LONG)
    
    channelTypes = []
    for channel in data['channels']:
        if channel['channeltype'] not in channelTypes:
            channelType = channel['channeltype']
            
            oc.add(
                DirectoryObject(
                    key = Callback(ListenLive, channelType = channelType),
                    title = channelType,
                    thumb = R(ICON_DIREKT)
                )
            )
            
            channelTypes.append(channelType)
    
    return oc
    
##########################################################################################
@route(PREFIX + '/ListenLive')
def ListenLive(channelType):
    oc = ObjectContainer(
        title2 = unicode(channelType),
        art = R(ART_DIREKT)
    )

    data = JSON.ObjectFromURL(CHANNEL_URL, cacheTime = CACHE_TIME_LONG)
    
    for channel in data['channels']:
        if channel['channeltype'] == channelType:
            url = channel['liveaudio']['url']
            title = unicode(channel['name'])
            thumb = channel['image']
    
            # No image provided for extra channels
            # Use own included
            if "SR Extra" in title:
                thumb = R(ICON_EXTRA)
            
            oc.add(
                CreateTrackObject(
                    url = url,
                    title = title,
                    thumb = thumb,
                    summary = '',
                    art = None
                    
                )
            )

    return oc

##########################################################################################
@route(PREFIX + '/ProgramsMenu')
def ProgramsMenu():
    oc = ObjectContainer(
        title2 = TEXT_PROGRAMS,
        art = R(ART_DIREKT)
    )

    oc.add(
        DirectoryObject(
            title = TEXT_ALL_PROG_TITLE,
            summary = TEXT_ALL_PROG_SUMMARY,
            tagline = TEXT_ALL_PROG_TAGLINE,
            key = 
                Callback(
                    CategoryMenu,
                    categoryid = 0,
                    categorytitle = TEXT_ALL_PROG_TITLE
                ),
            thumb = R(ICON_ALLA),
            art = R(ART)
        )
    )

    #  Add Categories
    data = JSON.ObjectFromURL(CATEGORY_URL, cacheTime = CACHE_TIME_LONG)

    for category in data['programcategories']:
        title = category['name']
        id = category['id']
        
        if "Barn" in title:
            thumb = R(ICON_BARN)
        elif "Dokument" in title:
            thumb = R(ICON_DOKU)
        elif "Kultur" in title:
            thumb = R(ICON_KULT)
        elif "Livsstil" in title:
            thumb = R(ICON_LIV1)
        elif "dning" in title:
            thumb = R(ICON_LIV2)
        elif "Musik" in title:
            thumb = R(ICON_MUSI)
        elif "Nyheter" in title:
            thumb = R(ICON_NYHE)
        elif "Sam" in title:
            thumb = R(ICON_SAMH)
        elif "Sport" in title:
            thumb = R(ICON_SPOR)
        elif "Spr" in title:
            thumb = R(ICON_SPRA)
        elif "Vetenskap" in title:
            thumb = R(ICON_VETE)
        else:
            thumb = R(ICON_SR)

        oc.add(
            DirectoryObject(
                title = unicode(title),
                key = 
                    Callback(
                        CategoryMenu,
                        categoryid = id,
                        categorytitle = title
                    ),
                thumb = thumb,
                art = R(ART)
            )
        )
    return oc

##########################################################################################
@route(PREFIX + '/CategoryMenu')
def CategoryMenu(categoryid, categorytitle):
    oc = ObjectContainer(
        title2 = unicode(categorytitle),
        art = R(ART)
    )

    if categoryid == 0:
        programURL = PROGRAMS_URL
    else:
        programURL = PROGRAMS_CATEGORY_URL + str(categoryid)

    data = JSON.ObjectFromURL(programURL, cacheTime = CACHE_TIME_SHORT)

    for program in data['programs']:
        title = program['name']
        programId = program['id']
        summary = program['description']
        broadcastInfo = program['broadcastinfo']
        
        if broadcastInfo:
            summary = summary + "\r\n\r\n" + broadcastInfo
        
        thumb = program['programimage']
        hasOndemand = program['hasondemand']
        hasPod = program['haspod']
        art = program['socialimage']

        try:
            tagline = unicode(program['payoff'])
        except:
            tagline = None

        #  Add ProgramMenu
        oc.add(
            DirectoryObject(
                title = unicode(title),
                key = 
                    Callback(
                        ProgramMenu,
                        progId = programId,
                        name = title,
                        description = summary,
                        programImage = thumb,
                        hasOndemand = hasOndemand,
                        hasPod = hasPod
                    ),
                tagline = tagline,
                summary = unicode(summary),
                thumb = thumb,
                art = art
            )
        )

    return oc

##########################################################################################
@route(PREFIX + '/ProgramMenu', hasOndemand = bool, hasPod = bool)
def ProgramMenu(progId, name, description, programImage, hasOndemand, hasPod):
    oc = ObjectContainer(
        title2 = unicode(name),
        art = programImage
    )

    if hasOndemand:
        oc.add(
            DirectoryObject (
                title = TEXT_BROADCAST_TITLE,
                key = 
                    Callback (
                        ProgramBroadcast,
                        progId = progId,
                        progName = name,
                        progImage = programImage
                    ),
                summary = unicode(description),
                thumb = R(ICON_SR)
            )
        )

    if hasPod:
        oc.add(
            DirectoryObject (
                title = TEXT_POD_TITLE,
                key = 
                    Callback (
                        ProgramPods,
                        progId = progId,
                        progName = name,
                        progImage = programImage
                    ),
                summary = unicode(description),
                thumb = R(ICON_ARKIV)
            )
        )

    return oc

##########################################################################################
@route(PREFIX + '/ProgramPods')
def ProgramPods(progId, progName, progImage):
    oc = ObjectContainer(
        title2 = unicode(progName),
        art = progImage
    )

    data = JSON.ObjectFromURL(POD_URL + progId, cacheTime = CACHE_TIME_SHORT)

    for progFile in data['podfiles']:
        title = progFile['title']
        duration = progFile['duration']
        filesize = progFile['filesizeinbytes']

        # SR API Bug
        # Some podcasts have incorrect duration
        # Use filesize to calculate duration
        # All Podscasts are encoded in 96 kbits/s
        # Expect that a pod cast that is longer than
        # 10 hours are incorrect
        if duration > 36000:
            duration = filesize / 12000

        duration = duration * 1000
        description = progFile['description']
        url = progFile['url']
        
        oc.add(
            CreateTrackObject(
                url = url,
                title = title,
                thumb = progImage,
                summary = description,
                art = progImage,
                duration = duration
            )
        )

    return oc

##########################################################################################
@route(PREFIX + '/ProgramBroadcast')
def ProgramBroadcast(progId, progName, progImage):
    oc = ObjectContainer(
        title2 = unicode(progName),
        art = progImage
    )

    data = JSON.ObjectFromURL(BROADCAST_URL + progId, cacheTime = CACHE_TIME_SHORT)

    for broadcast in data['broadcasts']:
        title = broadcast['title']
        duration = broadcast['totalduration'] * 1000
        summary = broadcast['description']
        
        if len(broadcast['broadcastfiles']) > 1:
            part = 1
            for file in broadcast['broadcastfiles']:
                title = broadcast['title'] + ' - Del ' + str(part)
                url = file['url']
                duration = file['duration']
                
                oc.add(
                    CreateTrackObject(
                        url = url,
                        title = title,
                        thumb = progImage,
                        summary = summary,
                        art = progImage,
                        duration = duration
                    )
                )     
        else:
            url = broadcast['broadcastfiles'][0]['url']
            oc.add(
                CreateTrackObject(
                    url = url,
                    title = title,
                    thumb = progImage,
                    summary = summary,
                    art = progImage,
                    duration = duration
                )
            )

    return oc

####################################################################################################
@route(PREFIX + '/CreateTrackObject', include_container = bool) 
def CreateTrackObject(url, title, thumb, summary, art, duration = None, include_container = False):
    items = []

    if '.mp3' in url:
        codec = AudioCodec.MP3
        container = Container.MP3
        key = Callback(PlayMP3, url = url)
        
    elif '.m4a' in url:
        codec = AudioCodec.AAC
        container = Container.MP4
        key = Callback(PlayM4A, url = url)
        
    else:
        codec = None
        container = None
        key = Callback(PlayAudio, url = url)

    streams = [
        AudioStreamObject(
            codec = codec,
            duration = duration,
            channels = 2
        )
    ]

    items.append(
        MediaObject(
            container = container,
            audio_codec = codec,
            audio_channels = 2,
            duration = duration,
            parts = [
                PartObject(
                    key = key,
                    streams = streams
                )
            ]
        )
    )
        
    to = TrackObject(
            key = 
                Callback(
                    CreateTrackObject,
                    url = url,
                    title = title,
                    thumb = thumb,
                    summary = summary,
                    art = art,
                    duration = duration,
                    include_container = True
                ),
            rating_key = title,
            title = unicode(title),
            thumb = thumb,
            summary = unicode(summary),
            items = items,
            art = art
    )
   
    if include_container:
        return ObjectContainer(objects = [to])
    else:
        return to

#################################################################################################### 
@route(PREFIX + '/PlayMP3.mp3')
def PlayMP3(url):
    return Redirect(url)
    
#################################################################################################### 
@route(PREFIX + '/PlayM4A.m4a')
def PlayM4A(url):
    return Redirect(url)

#################################################################################################### 
@route(PREFIX + '/PlayAudio')
def PlayAudio(url):
    return Redirect(url)

# End of file
