# Redis HA Sentinel Cluster Demo

This Python script simulates the concepts of Redis High Availability using Sentinel for failover and touches upon the principles of Redis Cluster for sharding and resilience. It demonstrates connecting to primary and replica instances and conceptually simulates a failover event.

## Language

`python`

## How to Run

1. Ensure you have Redis installed and running on localhost:6379 (primary) and localhost:6380 (replica, configured for replication).
2. Optionally, run a Sentinel instance on localhost:26379 for a more realistic failover simulation.
3. Run the script: python redis_ha_demo.py

## Original Article

This example accompanies the Turkish article: [Redis'te Kurumsal Seviyede Yüksek Erişilebilirlik: Sentinel ve Cluster ile WRedis](https://fatihsoysal.com/blog/rediste-kurumsal-seviyede-yuksek-erisilebilirlik-sentinel-ve-cluster-ile-wredis/).

## License

MIT — see [LICENSE](LICENSE).
