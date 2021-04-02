defmodule OmenWeb.PageLive do
  use OmenWeb, :live_view

  @impl true
  def mount(_params, _session, socket) do
    {:ok, assign(socket, song_url: "",song_media_name: "",done_state: "ENTER_STH")}
  end

  @impl true
  def handle_event("download", %{"song_url" => song_url}, socket) do
    if validate_song_url(song_url) do
      OmenWeb.Redix.command(~w(PUBLISH download_requests {"song_url":"#{song_url}"}))

      IO.puts("LiveView Socket Subcribing to "<>get_songID_from_URL(song_url)) # subscribe to songID on the internal Pub/Sub system
      get_songID_from_URL(song_url) |> OmenWeb.Endpoint.subscribe()
      # when a message is recv. here handle_info is called to update the liveView (our Erlang process here is subscribed)

      {:noreply, assign(socket, song_url: song_url,done_state: "IN_PROGRESS")}
    else
      {:noreply, assign(socket, song_url: song_url,done_state: "ERROR")}
    end
  end


  @impl true
  def handle_info(payload,socket) do
    # the payload that handle_info recvs is the Internal Pub/subs message payload
    {:ok,msg_data} = Map.fetch(payload.payload,:data)
    {:ok,song_state} = Map.fetch(msg_data,"song_state")

    if song_state=="OK" do
      {:ok,song_media_name} = Map.fetch(msg_data,"song_media_name")
      {:noreply,assign(socket,done_state: "DONE",song_media_name: song_media_name)}
    else
      {:noreply,assign(socket,done_state: "ERROR",song_media_name: "")}
    end

  end

  defp get_songID_from_URL(song_url) do
      String.split(song_url,"/") |> Enum.at(4)
  end

  defp validate_song_url(song_url) do
    # song_url looks like: https://play.anghami.com/song/25770989
    String.contains?(song_url,"play.anghami.com") and String.contains?(song_url,"song/") and String.contains?(song_url,"https://")
  end

end
