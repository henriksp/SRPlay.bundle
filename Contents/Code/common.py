# -*- coding: utf-8 -*

# Global constants
MUSIC_PREFIX = "/music/sverigesradioplay"

# URLs
BASE_URL      = "http://sverigesradio.se/api/v2/"
CATEGORY_URL  = BASE_URL + "programcategories?pagination=false"
CHANNEL_URL   = BASE_URL + "channels?pagination=false"
CHANNELTYPE_URL = CHANNEL_URL + "&filter=channel.channeltype&filtervalue="
RIGHTNOW_URL = BASE_URL + "scheduledepisodes/rightnow?channelid="
PROGRAMS_URL  = BASE_URL + "programs?pagination=false"
PROGRAMS_CATEGORY_URL = BASE_URL + "programs/index?pagination=false&programcategoryid="
PROGRAM_URL   = BASE_URL + "programs/"
POD_URL = BASE_URL + "podfiles?pagination=false&programid="
BROADCAST_URL = BASE_URL + "broadcasts?pagination=false&programid="

# Art & Icons
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
ICON_SR       = 'logo-sr.png'
ICON_EXTRA    = 'logo-sr-ext.png'

# http cache times
CACHE_TIME_LONG    = 60*60*24 # 1 day
CACHE_TIME_MEDIUM  = 60*60    # 1 hour
CACHE_TIME_SHORT   = 60*5     # 5 minutes

# Texts
TEXT_TITLE = u'Sveriges Radio Play'
TEXT_SUMMARY = u'The Swedish Radio website continually streams over 40 radio channels, including our four national FM stations and some ten web-only channels. All programmes are available archived and on demand 24 hours a day for 30 days following the original FM broadcast.'
TEXT_MAIN_TITLE = u'Sveriges Radio Play'
TEXT_LIVE_SHOWS = u'Livesändningar'
TEXT_LIVE_TAGLINE = u''
TEXT_LIVE_SUMMARY = u''
TEXT_PROGRAMS = u'Program'
TEXT_ALL_PROG_TITLE = u'Alla program A-Ö'
TEXT_ALL_PROG_TAGLINE = u''
TEXT_ALL_PROG_SUMMARY = u''
TEXT_NEXT_PROGRAM = u'Nästa'
TEXT_POD_TITLE = u'Poddarkiv'
TEXT_BROADCAST_TITLE = u'Sändningsarkiv'

# End of file
