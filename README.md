# Hire ME ANGHAMI
- download anghami songs easily on a backend that's built to scale to the moon 🚀📈🌕
- Uses Elixir, RabbitMQ and Redis worker queues. Fully distributed out of the box! (why? I am gonna run this on a $5 VPS alsan lol)

![hiremeanghami_service_diag.svg](extras/hiremeanghami_service_diag.svg)

# Tech Stack
- [RabbitMQ](https://www.rabbitmq.com/)
- [Phoenix Live View](https://hexdocs.pm/phoenix_live_view/Phoenix.LiveView.html)
- [Redis RQ](https://github.com/rq/rq)
- [Elixir Redix](https://github.com/whatyouhide/redix)
- [Selenium](https://github.com/SeleniumHQ/selenium)
- [Docker](https://docker.com/)

# Services 

## Venator
Spawns and controls Selenium workers that download the songs.

#### API
- publish a message that looks like `{"song_url":"https://play.anghami.com/song/25770989"}` to queue `download_requests`
- consume  `downloaded_songs` and wait for a job completion message that should look like  `{"spng_state":"OK","song_id":"25770989","song_media_name":"Anghami_25770989.mp3"}` to be published
- the song should be located in the `SONG_DIR_PATH` under the name of the `song_media_name` param

## Omen
Frontend and basic Backend that talks to Venator and back. Keep the user happy while things are happening in the background.


# Deployment
- ```docker-compose up``` this will build and setup everything.
- open [localhost:4000](http://localhost:4000) in your browser.