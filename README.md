# Hire ME ANGHAMI
- download anghami songs easily on a backend that's built to scale to the moon 🚀📈🌕
- Uses Elixir, RabbitMQ and Redis worker queues. Fully distributed out of the box! (why? I am gonna run this on a $5 VPS alsan lol)

# Tech Stack
- [RabbitMQ](https://www.rabbitmq.com/)
- [Phoenix Live View](https://hexdocs.pm/phoenix_live_view/Phoenix.LiveView.html)
- [Redis RQ](https://github.com/rq/rq)
- [Elixir Redix](https://github.com/whatyouhide/redix)
- [Selenium](https://github.com/SeleniumHQ/selenium)
- [Docker](https://docker.com/)

# Services 

## Venator
Spawns and controls RQ workers that download the songs.
The Service communicates with omen using a rabbit MQ message queue.Allowing us to potentially launch N-instances of venator and run RabbitMQ in a load balancer configuration across multiple compute nodes. 

#### API
- publish a message that looks like `{"song_url":"https://play.anghami.com/song/25770989"}` to queue `download_requests`
- consume  `downloaded_songs` and wait for a job completion message that should look like  `{"spng_state":"OK","song_id":"25770989","song_media_name":"Anghami_25770989.mp3"}` to be published
- the song should be located in the `SONG_DIR_PATH` under the name of the `song_media_name` param

## Omen
Frontend and basic Backend that talks to Venator and back, Keep the user happy while things are happening in the background.
This didn't need to be it's own service. But i wanted to learn Phoenix and yeah. worth it.

