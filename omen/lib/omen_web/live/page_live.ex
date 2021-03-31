defmodule OmenWeb.PageLive do
  use OmenWeb, :live_view

  @impl true
  def mount(_params, _session, socket) do
    {:ok, assign(socket, song_url: "",done_state: "Enter the song url")}
  end

  @impl true
  def handle_event("download", %{"song_url" => song_url}, socket) do
    # todo: validate the url

    OmenWeb.Redix.command(~w(PUBLISH download_requests {"song_url":"#{song_url}"}))

    IO.puts("LiveView Socket Subcribing to "<>getSongIDFromURL(song_url)) # subscribe to songID on the internal Pub/Sub system
    getSongIDFromURL(song_url) |> OmenWeb.Endpoint.subscribe()
    # when a message is recv. here handle_info is called to update the liveView (our Erlang process here is subscribed)

    {:noreply, assign(socket, song_url: song_url,done_state: "IN PROGRESS")}
  end


  @impl true
  def handle_info(payload,socket) do
    # the payload that handle_info recvs is the Internal Pub/subs message payload
    {:ok,done_state} = Map.fetch(payload.payload,:done_state)
    {:noreply,assign(socket,done_state: done_state)}
  end

  defp getSongIDFromURL(song_url) do
    String.split(song_url,"/") |> Enum.at(-1)
  end

end
