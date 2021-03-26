# Hire ME ANGHAMI
- download ANGHAMI songs easily

## Venator (core selenuim download songs and stuff)

#### Requirements:
- needs to share a `songs` DIR with Spectre service
- needs to have `geckodriver` configured to run headless

#### Procedures 
- look inside the creds/*_user.pkl and pick one for cookies every 60s
- get the download link
- download it and save it to a folder 
- send the download link to the Main Backend Service

## Spectre (main backend service)
- get the song URL from the user
- put it in a work queue
- monitor the status of the job and when it finishes return (or emit lol) the download link
- store how much something gets downloaded in redis with it's songID
- if the songs/ dir gets too big delete the song with the least downloads (if multiple just pick randomly)

## Omen (the frontend):
- just a single page with an enter song URL box
- with app instructions t7t
- and some funny things about HMU spotify and hey anghami call me


## References/Tech to look at 
Elixr Redis Jobs: https://github.com/akira/exq
Selenuim driver for elxir: https://hexdocs.pm/hound/readme.html


## MSC
- redis (for worker queues) and Key Value storage (needs to be persistent with a `data/` dir)
- contact this guy: https://github.com/Almo7aya