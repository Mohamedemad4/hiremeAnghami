defmodule OmenWeb.MQConsumer do
  use GenServer

  @moduledoc """
  Basically subscribes to downloaded_songs and relays the confirmation + data to the LiveView process that's handling whatever client wants that song
  """

  def start_link(_opts) do
    GenServer.start_link(__MODULE__, :ok, name: :consumer)
  end


  def init(:ok) do
    channel_name = "downloaded_songs"
    {:ok, connection} = AMQP.Connection.open
    {:ok, channel} = AMQP.Channel.open(connection)
    AMQP.Queue.declare(channel, channel_name)
    AMQP.Basic.consume(channel, channel_name, nil, no_ack: true) # no need to ACK downloaded_songs
    _wait_for_messages()
  end


  defp _wait_for_messages do
    receive do
      {:basic_deliver, payload, _meta} ->
        relay_to_liveView(payload)
        _wait_for_messages()
    end
  end

  defp relay_to_liveView(payload) do
    {:ok,message} = payload |> Jason.decode()

    Map.fetch(message,"song_id")
    |> elem(1)
    |> OmenWeb.Endpoint.broadcast("download",%{data: message}) # Publish on the internal pub/sub system that the thing is done

    IO.inspect(message)

  end

  def terminate(_reason, state) do
    AMQP.Connection.close(state.connection)
  end

end
