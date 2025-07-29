DIR_NAME?=FMJDGR
game:
	curl -L https://github.com/CommandBeat/Fruit-Merge-Juicy-Drop-Game-REMAKE/archive/refs/heads/main.zip -o repo.zip
	unzip repo.zip -d $(DIR_NAME)
