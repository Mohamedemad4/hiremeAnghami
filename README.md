# Hire ME ANGHAMI
- download anghami songs easily on a backend that's built to scale to the moon 🚀📈🌕
- Uses Elixir, Redis Pub/sub and worker queues. Fully distributed out of the box! (why? I am gonna run this on a $5 VPS alsan lol)

# Tech Stack
- [Redis Pub/Sub](https://redis.io/topics/pubsub)
- [Redis RQ](https://github.com/rq/rq)
- [Phoenix Live View](https://hexdocs.pm/phoenix_live_view/Phoenix.LiveView.html)
- [Elixir Redix](https://github.com/whatyouhide/redix)
- [selenium](https://github.com/SeleniumHQ/selenium)
- [Docker](https://docker.com/)

# Services 

## Venator
Spawns and controls RQ workers that download the songs

#### API
- publish a message that looks like `{"song_url":"https://play.anghami.com/song/25770989"}` to channel `download_requests`
- subscribe to `downloaded_songs` and wait for a job completion message that should look like  `{"song_id":"25770989","song_media_name":"Anghami_25770989.mp3"}` to be published
- the song should be located in the `SONG_DIR_PATH` under the name of the `song_media_name` param

## Omen
Frontend and basic Backend that talks to Venator and back, Keep the user happy while things are happening in the background.
This didn't need to be it's own service. But i wanted to learn Phoenix and yeah. worth it.


# Future improvements
- use Message Queueing instead of redis Pub/Sub so we can launch N-instances of Venator