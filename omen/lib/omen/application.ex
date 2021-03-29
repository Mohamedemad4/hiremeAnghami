defmodule Omen.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  def start(_type, _args) do
    children = [
      # Start the Telemetry supervisor
      OmenWeb.Telemetry,
      # Start the PubSub system
      {Phoenix.PubSub, [name: Omen.PubSub, adapter: Phoenix.PubSub.PG2]},
      # Start the Endpoint (http/https)
      OmenWeb.Endpoint,
      OmenWeb.Redix,
      OmenWeb.RedisPubSubAdapter
      # Start a worker by calling: Omen.Worker.start_link(arg)
      # {Omen.Worker, arg}
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: Omen.Supervisor]
    Supervisor.start_link(children, opts)
  end

  # Tell Phoenix to update the endpoint configuration
  # whenever the application is updated.
  def config_change(changed, _new, removed) do
    OmenWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end
