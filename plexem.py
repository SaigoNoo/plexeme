import os
from os.path import exists
from plexapi.server import PlexServer

### PLEX Configuration ###
https = True
server = "myplex.doussis.be"
port = "443"
token = "uzPJzTCb-SZw1kTohgV3"

# Connexion à l'instance Plex
fullurl = print(f"{'https' if https else 'http'}://{server}:{port}")
plex = PlexServer(fullurl, token)

### Library Names ###
library = plex.library.sections()

# Fonctions
def lib_items(library):
	medias = plex.library.section(f"{library}")
	for index, media in enumerate(medias.all(),1):
		print(f"\033[33m{str(index).zfill(2)}\033[0m) {media.title}")

def fetch_id(library,index):
	medias = plex.library.section(f"{library}").all()
	return medias[int(index)].ratingKey

def return_path(id):
	return plex.fetchItem(id).locations[0]

def fetch_name(id):
	return plex.fetchItem(id).title

def fetchItems(lib):
	return len(plex.library.section(lib))

# Programme
# Variable pour indiquer si ajout = 0
add = False
## Parcourir toutes les librairies
for lib in library:
	## Si les librairies sont de type show, les traiter, sinon ignorer
	if lib.type == "show":
		## Stocker un array de tout les médias de la librairie
		subLib = plex.library.section(str(lib.title)).all()
		## Parcourir les épisodes des séries
		for medias in subLib:
			title = medias.title
			index = subLib.index(medias)
			ratingKey = fetch_id(lib.title,index)
			path = return_path(ratingKey)
			theme = exists(f"{path}/theme.mp3")
			if not theme:
				add = True
				os.system(f"yt-dlp -q \"ytsearch:{title} Opening Saion 01\" -x --audio-format mp3 --output \"{path}\"/theme.mp3")
if not add:
	print("\033[32mTout vos médias possèdent un thème MP3\033[0m")