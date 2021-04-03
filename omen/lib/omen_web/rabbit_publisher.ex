defmodule OmenWeb.MQPublisher do
  use GenServer

  ## Client API

  def start_link(_opts) do
    GenServer.start_link(__MODULE__, :ok, name: :publisher)
  end

  def publish(message) do
    GenServer.cast(:publisher, {:publish, message})
  end

  ## Server Callbacks
  @impl true
  def init(:ok) do
    {:ok, connection} = AMQP.Connection.open
    {:ok, channel} = AMQP.Channel.open(connection)
    AMQP.Queue.declare(channel, "download_requests")
    {:ok, %{channel: channel, connection: connection} }
  end

  @impl true
  def handle_cast({:publish, message}, state) do
    AMQP.Basic.publish(state.channel, "", "download_requests", message)
    {:noreply, state}
  end

  @impl true
  def terminate(_reason, state) do
    AMQP.Connection.close(state.connection)
  end
end
