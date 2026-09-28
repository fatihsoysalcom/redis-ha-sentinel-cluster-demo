import redis
import time
import random

# This example simulates a basic Redis HA setup using Sentinel and Cluster concepts.
# In a real-world scenario, you would have separate Sentinel processes monitoring Redis instances
# and a Redis Cluster for sharding and failover.

# --- Configuration ---
PRIMARY_REDIS_HOST = 'localhost'
PRIMARY_REDIS_PORT = 6379
REPLICA_REDIS_HOST = 'localhost'
REPLICA_REDIS_PORT = 6380

# Sentinel simulation (simplified: we'll manually trigger a failover)
SENTINEL_PORT = 26379

# --- Helper Functions ---
def get_redis_client(host, port):
    try:
        r = redis.StrictRedis(host=host, port=port, db=0, decode_responses=True)
        r.ping()
        print(f"Successfully connected to Redis at {host}:{port}")
        return r
    except redis.exceptions.ConnectionError as e:
        print(f"Failed to connect to Redis at {host}:{port}: {e}")
        return None

def simulate_primary_failure(primary_client):
    print("\n--- Simulating Primary Redis Failure ---")
    # In a real Sentinel setup, Sentinel would detect this and promote a replica.
    # Here, we'll just stop the primary process (conceptually).
    print("Primary Redis instance is now unavailable.")
    # We can't actually stop a process here, so we'll just mark it as down.

def simulate_sentinel_failover(sentinel_client, old_master_host, old_master_port, new_master_host, new_master_port):
    print("\n--- Sentinel Initiating Failover ---")
    # This is a highly simplified simulation. Real Sentinel commands are more complex.
    # Sentinel would monitor, detect failure, and reconfigure replicas.
    print(f"Sentinel detected failure of {old_master_host}:{old_master_port}.")
    print(f"Promoting {new_master_host}:{new_master_port} as the new master.")
    # In a real scenario, Sentinel would send commands to replicas to switch master.
    # For this demo, we assume the replica is now the master.
    return get_redis_client(new_master_host, new_master_port)

def simulate_cluster_reconfiguration(cluster_nodes):
    # This is a conceptual placeholder. Redis Cluster handles sharding and failover automatically.
    # In a real cluster, nodes communicate to rebalance data and elect new masters.
    print("\n--- Redis Cluster Reconfiguration (Conceptual) ---")
    print("Cluster nodes are communicating to rebalance data and ensure availability.")
    pass

# --- Main Simulation ---
def main():
    print("Starting Redis HA Demo (Sentinel & Cluster Concepts)")

    # 1. Connect to the primary Redis instance
    primary_client = get_redis_client(PRIMARY_REDIS_HOST, PRIMARY_REDIS_PORT)
    if not primary_client:
        print("Cannot proceed without a primary Redis instance. Please start Redis on port 6379.")
        return

    # 2. Connect to a replica Redis instance (configured for replication)
    # In a real setup, this replica would be configured to follow the primary.
    # For this demo, we assume it's ready to be promoted.
    replica_client = get_redis_client(REPLICA_REDIS_HOST, REPLICA_REDIS_PORT)
    if not replica_client:
        print("Cannot proceed without a replica Redis instance. Please start Redis on port 6380.")
        return

    # 3. Connect to a Sentinel instance (for monitoring and failover coordination)
    sentinel_client = get_redis_client('localhost', SENTINEL_PORT)
    if not sentinel_client:
        print("Sentinel is not running on port 26379. Failover simulation will be manual.")

    # --- Initial Operations ---
    print("\n--- Performing initial operations on primary ---")
    key = "mykey"
    value = "myvalue"
    primary_client.set(key, value)
    print(f"Set '{key}' to '{value}' on primary.")
    retrieved_value = primary_client.get(key)
    print(f"Retrieved '{key}': '{retrieved_value}' from primary.")

    # --- Simulate Failure and Failover ---
    simulate_primary_failure(primary_client)

    # Manually simulate Sentinel's role if Sentinel client is not available
    new_master_client = None
    if sentinel_client:
        # In a real scenario, Sentinel would handle this. We are simulating its outcome.
        # This is a placeholder for Sentinel's internal logic.
        print("\n(Sentinel would now be coordinating failover...)")
        # Assume Sentinel successfully promoted the replica
        new_master_client = simulate_sentinel_failover(sentinel_client, PRIMARY_REDIS_HOST, PRIMARY_REDIS_PORT, REPLICA_REDIS_HOST, REPLICA_REDIS_PORT)
    else:
        print("\n--- Manual Failover Simulation ---")
        print("Assuming replica is now the master.")
        new_master_client = replica_client # Treat replica as the new master

    if not new_master_client:
        print("Failover failed or new master could not be established.")
        return

    # --- Operations on the new master ---
    print("\n--- Performing operations on the new master ---")
    new_key = "newkey"
    new_value = "newvalue"
    try:
        new_master_client.set(new_key, new_value)
        print(f"Set '{new_key}' to '{new_value}' on new master.")
        retrieved_new_value = new_master_client.get(new_key)
        print(f"Retrieved '{new_key}': '{retrieved_new_value}' from new master.")
    except redis.exceptions.ConnectionError as e:
        print(f"Could not perform operations on the new master: {e}")

    # --- Conceptual Cluster Aspect ---
    # Redis Cluster provides sharding and automatic failover across multiple nodes.
    # This demo doesn't set up a full cluster but illustrates the HA goal.
    # If this were a cluster, data would be sharded, and failover would be handled by cluster nodes.
    cluster_nodes = [primary_client, replica_client] # Conceptual list of nodes
    simulate_cluster_reconfiguration(cluster_nodes)

    print("\nDemo finished.")

if __name__ == "__main__":
    main()
