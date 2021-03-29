# https://elixirforum.com/t/can-you-use-the-redix-pubsub-library-with-phoenix/15260/25

defmodule OmenWeb.RedisPubSubAdapter do
  """
  Basically subscribes to downloaded_songs and relays the confirmation + data to the LiveView process that's handling whatever client wants that song
  """
  use GenServer

  def start_link(opts) do
    GenServer.start_link(__MODULE__, :ok, opts)
  end

  def lookup(server, name) do
    GenServer.call(server, {:lookup, name})
  end

  def create(server, name) do
    GenServer.cast(server, {:create, name})
  end

  def init(:ok) do
      names = %{}
      refs = %{}

      {:ok, pubsub} = Redix.PubSub.start_link()
      Redix.PubSub.subscribe(pubsub, "downloaded_songs", self())

      {:ok, {names, refs}}
  end

  def handle_info(msg, state) do

      if Enum.member?(Tuple.to_list(msg),:message) do # ignore the subscription confirmation

        {:ok,message} = msg |> elem(4) |> Map.fetch(:payload) |> elem(1) |> Jason.decode()
        Map.fetch(message,"song_id") |> elem(1) |> OmenWeb.Endpoint.broadcast("download",%{done_state: "DONE"}) # Publish on the internal pub/sub system that the thing is done

        IO.inspect(message)
      else

        IO.puts("OMEN subscribed to downloaded_songs channel")

      end

      {:noreply, state}
  end
end
