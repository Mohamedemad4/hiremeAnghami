# Hire ME ANGHAMI
- download anghami songs easily on a backend that's built to scale to the moon 🚀📈🌕
- Uses Elixir and Redis Worker Queues fully distributed out of the box. (why? I am gonna run this on a 5$ VPS alsan lol)

## Venator

#### Requirements:
- needs to share a `songs` DIR with Spectre service
- needs to have `geckodriver` configured to run headless

#### API
- publish a message that looks like `{"song_url":"https://play.anghami.com/song/25770989"}` to channel `download_requests`
- subscribe to `downloaded_songs` and wait for the `25770989` (songID) to be published
- the song should be located in the `SONG_DIR_PATH` like `Anghami_25770989.mp3`

## Omen (main backend service)
- get the song URL from the user
- put it in a work queue
- monitor the status of the job and when it finishes return (or emit lol) the download link
- store how much something gets downloaded in redis with it's songID
- if the songs/ dir gets too big delete the song with the least downloads (if multiple just pick randomly)
- and some funny things about HMU spotify and hey anghami call me

also put a rant there about how you would rather it worked by having omen enque jobs rather than publishing to redis

(does it actually make sense to download the songs and keep them?)