from gino import Gino
from sshtunnel import SSHTunnelForwarder

db = Gino()


# Create an SSH tunnel
tunnel = SSHTunnelForwarder(
    ("localhost", 3333),
    ssh_username="user",
    ssh_private_key="/home/oleg/.ssh/id_rsa",
    remote_bind_address=("localhost", 5432),
    local_bind_address=("localhost", 6543),  # could be any available port
)
