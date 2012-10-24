# -*- coding: utf-8 -*-

from common import *
from sets import Set
import httplib
import urlparse

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

	#  Add ProgramsMenu
	dir.add(
		DirectoryObject(
			title=TEXT_PROGRAMS,
			key=Callback(
				ProgramsMenu
			),
			thumb=R(ICON_ALLA),
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

	page = XML.ElementFromURL(CHANNEL_URL, cacheTime=CACHE_TIME_LONG)
	channeltypes = page.xpath("//channeltype/text()")
	typeSet = Set()
	for i in range(len(channeltypes)):
		if channeltypes[i] not in typeSet:
			dir.add (
				DirectoryObject (
					title=channeltypes[i],
					key=Callback(
						ListenLiveChannelType,
						channelType = channeltypes[i]
					),
					thumb=R(ICON_DIREKT)
				)
			)
			typeSet.add(channeltypes[i])

	return dir

def ListenLiveChannelType(channelType):

	dir = ObjectContainer(
		view_group = "List",
		title1=TEXT_TITLE,
		title2=channelType,
		art = R(ART_DIREKT)
	)
	pageurl = CHANNELTYPE_URL + channelType
	pageurl = pageurl.replace(" ", "+")
	page = XML.ElementFromURL(pageurl, cacheTime=CACHE_TIME_LONG)

	for channel in page.getiterator('channel'):

		channelName = channel.attrib.get("name")
		channelId = channel.attrib.get("id")
		image = channel.findtext("image")
		tagline = channel.findtext("tagline")
		if tagline:
			fullName = channelName + " - " + tagline
		else:
			fullName = channelName

		url = channel.xpath("liveaudio/url/text()")[0]

		# SR uses redirect so lets get the actual url
		parsedUrl = urlparse.urlparse(url)
		httpCon = httplib.HTTPConnection(parsedUrl.netloc)
		httpCon.request('HEAD', parsedUrl.path)
		httpRes = httpCon.getresponse()
		url = httpRes.getheader("location")

		# No image provided for extra channels
		# Use own included
		if "SR Extra" in channelName:
			image = R(ICON_EXTRA)

		# disable rightnow info right now since plex
		# will not present this information
#		rightnow = XML.ElementFromURL(RIGHTNOW_URL + channelId, cacheTime=None)

		description = ""
#		currentProgram = rightnow.xpath("/sr/channel/currentscheduledepisode/title/text()")
#		nextProgram = rightnow.xpath("/sr/channel/nextscheduledepisode/title/text()")
#		if  currentProgram:
#			description = currentProgram[0] + "\n"
#		if nextProgram:
#			description += TEXT_NEXT_PROGRAM+ ": " + nextProgram[0]

		track = TrackObject(
			title = fullName,
			summary = description,
			key =url,
			rating_key = MUSIC_PREFIX + "/live/" + channelName,
			thumb = image,
			art = R(ART_DIREKT)
		)

		media = MediaObject(
			parts = [PartObject(key=Callback(PlayLiveAudio, url=url, ext='mp3'))],
			container = Container.MP3,
			audio_codec = AudioCodec.MP3
		)

		track.add(media)
		dir.add(track)

	return dir

def PlayLiveAudio(url):
	return Redirect(url)

def ProgramsMenu():
	dir = ObjectContainer(
		view_group = "List",
		title1=TEXT_TITLE,
		title2=TEXT_PROGRAMS,
		art = R(ART_DIREKT)
	)

	dir.add(
		DirectoryObject(
			title=TEXT_ALL_PROG_TITLE,
			summary=TEXT_ALL_PROG_SUMMARY,
			tagline=TEXT_ALL_PROG_TAGLINE,
			key=Callback(
				CategoryMenu,
				categoryid=0,
				categorytitle=TEXT_ALL_PROG_TITLE
			),
			thumb=R(ICON_ALLA),
			art=R(ART)
		)
	)

	#  Add Categories
	page = XML.ElementFromURL(CATEGORY_URL,
		cacheTime=CACHE_TIME_LONG)

	for item in page.getiterator('programcategory'):

		name = item.attrib.get("name")
		caticon = R(ICON_SR)
		if "Barn" in name:
			caticon = R(ICON_BARN)
		elif "Dokument" in name:
			caticon = R(ICON_DOKU)
		elif "Kultur" in name:
			caticon = R(ICON_KULT)
		elif "Livsstil" in name:
			caticon = R(ICON_LIV1)
		elif "dning" in name:
			caticon = R(ICON_LIV2)
		elif "Musik" in name:
			caticon = R(ICON_MUSI)
		elif "Nyheter" in name:
			caticon = R(ICON_NYHE)
		elif "Sam" in name:
			caticon = R(ICON_SAMH)
		elif "Sport" in name:
			caticon = R(ICON_SPOR)
		elif "Spr" in name:
			caticon = R(ICON_SPRA)
		elif "Vetenskap" in name:
			caticon = R(ICON_VETE)
		else:
			caticon = R(ICON_SR)

		dir.add(
			DirectoryObject(
				title=name,
				key=Callback(
					CategoryMenu,
					categoryid=int(item.attrib.get("id", default="0")),
					categorytitle=name
				),
				thumb=caticon,
				art=R(ART)
			)
		)
	return dir


def CategoryMenu(categoryid, categorytitle):

	dir = ObjectContainer(
		view_group = "List",
		title1 = TEXT_TITLE,
		title2 = categorytitle,
		art = R(ART)
	)

	if categoryid == 0:
		programUrl = PROGRAMS_URL
	else:
		programUrl = PROGRAMS_CATEGORY_URL + str(categoryid)

	page = XML.ElementFromURL(programUrl, cacheTime=CACHE_TIME_SHORT)

	for program in page.getiterator('program'):

		name = program.attrib.get("name")
		programId = program.attrib.get("id")
		description = program.findtext("description")
		broadcastInfo = program.findtext("broadcastinfo")
		if broadcastInfo:
			description += "\n\n" + broadcastInfo
		programImage = program.findtext("programimage")
		hasOndemand = program.findtext("hasondemand")
		hasPod = program.findtext("haspod")


		#  Add ProgramMenu
		dir.add(
			DirectoryObject(
				title = name,
				key = Callback(
					ProgramMenu,
					progId = programId,
					name = name,
					description = description,
					programImage = programImage,
					hasOndemand = hasOndemand,
					hasPod = hasPod
				),
#				tagline = program.findtext("payoff"),
				summary = description,
		#		thumb = programImage,
				art = programImage
			)
		)

	return dir

def ProgramMenu(progId, name, description, programImage, hasOndemand, hasPod):

	dir = ObjectContainer(
		view_group="InfoList",
		title1 = TEXT_TITLE,
		title2 = name,
		art = programImage
	)

	if hasOndemand == "true":
		dir.add (
			DirectoryObject (
				title = TEXT_BROADCAST_TITLE,
				key = Callback (
					ProgramBroadcast,
					progId = progId,
					progName = name,
					progImage = programImage
				),
				summary = description,
				thumb = R(ICON_SR)
			)
		)

	if hasPod == "true":
		dir.add (
			DirectoryObject (
				title = TEXT_POD_TITLE,
				key = Callback (
					ProgramPods,
					progId = progId,
					progName = name,
					progImage = programImage
				),
				summary = description,
				thumb = R(ICON_ARKIV)
			)
		)

	return dir

def ProgramPods(progId, progName, progImage):

	dir = ObjectContainer (
		view_group="InfoList",
		title1 = TEXT_TITLE,
		title2 = progName,
		art = progImage
	)

	files = XML.ElementFromURL(POD_URL + progId, cacheTime=CACHE_TIME_SHORT)

	for progFile in files.getiterator("podfile"):
		title = progFile.findtext("title")
		duration = int(progFile.findtext("duration"))
		filesize = int(progFile.findtext("filesizeinbytes"))

		# SR API Bug
		# Some podcasts have incorrect duration
		# Use filesize to calculate duration
		# All Podscasts are encoded in 96 kbits/s
		# Expect that a pod cast that is longer than
		# 10 hours are incorrect
		if duration > 36000:
			duration = filesize / 12000

		duration = duration * 1000
		description = progFile.findtext("description")
		key = progFile.findtext("statkey")
		url = progFile.findtext("url")

		track = TrackObject (
			title = title,
			key = key,
			summary = description,
			rating_key = MUSIC_PREFIX + key,
			thumb = progImage,
			duration = duration
		)

		media = MediaObject (
			audio_codec = AudioCodec.MP3,
			duration = duration
		)

		media.add(PartObject(key = url, duration = duration))
		track.add(media)
		dir.add(track)

	return dir

def ProgramBroadcast(progId, progName, progImage):

	dir = ObjectContainer (
		view_group="InfoList",
		title1 = TEXT_TITLE,
		title2 = progName,
		art = progImage
	)

	files = XML.ElementFromURL(BROADCAST_URL + progId, cacheTime=CACHE_TIME_SHORT)

	for progFile in files.getiterator("broadcast"):
		title = progFile.findtext("title")
		duration = int(int(progFile.findtext("totalduration")) * 1000)
		description = progFile.findtext("description")

		track = TrackObject (
			title = title,
			key = BROADCAST_URL + progId,
			summary = description,
			rating_key =MUSIC_PREFIX + BROADCAST_URL + progId,
			thumb = progImage,
			duration = duration
		)

		media = MediaObject (
			audio_codec = AudioCodec.AAC,
			duration = duration
		)

		for brfile in progFile.getiterator("broadcastfile"):
			brDuration = brfile.findtext("duration")
			brUrl = brfile.findtext("url")
			media.add(PartObject(key=brUrl, duration=brDuration))

		track.add(media)
		dir.add(track)

	return dir

# End of file
