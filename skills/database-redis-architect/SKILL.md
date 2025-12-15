---
name: Redis Database Architect
slug: database-redis-architect
description: Design Redis architectures with caching patterns, data structures, eviction policies, persistence (RDB/AOF), and high availability (Sentinel/Cluster).
capabilities:
  - Caching strategy design (cache-aside, write-through, write-behind)
  - Data structure selection (strings, hashes, lists, sets, sorted sets, streams, probabilistic)
  - Eviction policy configuration (LRU, LFU, volatile, allkeys, noeviction)
  - Persistence configuration (RDB snapshots, AOF journaling, hybrid)
  - High availability architecture (Redis Sentinel, Redis Cluster)
  - Memory optimization (maxmemory tuning, hash compression, data structure efficiency)
  - Redis 8.0 specific features (I/O threading, vector sets, probabilistic structures)
  - Use case design (session storage, rate limiting, leaderboards, pub/sub, task queues)
inputs:
  - Use case (caching, session storage, real-time analytics, pub/sub, task queue)
  - Data access patterns (read/write ratio, TTL requirements, cache hit rate target)
  - Data volume and growth rate (keys, memory usage, throughput)
  - Availability requirements (SLA, RTO, RPO, failover tolerance)
  - Deployment environment (cloud provider, self-hosted, Redis Enterprise)
  - Redis version (default: 8.0)
outputs:
  - Caching strategy with cache consistency model
  - Data structure recommendations with memory efficiency estimates
  - Eviction policy configuration with maxmemory settings
  - Persistence configuration (RDB interval, AOF fsync policy)
  - High availability architecture (Sentinel/Cluster topology)
  - Performance tuning parameters (io-threads, maxclients, timeout)
  - Memory optimization recommendations with savings estimates
  - Migration plan if upgrading from older Redis versions
keywords:
  - redis
  - caching
  - in-memory
  - key-value
  - data-structures
  - eviction
  - persistence
  - high-availability
  - sentinel
  - cluster
  - redis-8
version: 1.0.0
owner: cognitive-toolworks
license: MIT
security: public
links:
  - title: "Redis 8.0 GA Release"
    url: "https://redis.io/blog/redis-8-ga/"
    accessed: "2025-10-26T18:28:30-0400"
  - title: "Redis Caching Patterns"
    url: "https://redis.io/solutions/caching/"
    accessed: "2025-10-26T18:28:30-0400"
  - title: "Redis Eviction Policies"
    url: "https://redis.io/docs/reference/eviction"
    accessed: "2025-10-26T18:28:30-0400"
  - title: "Redis Sentinel vs Cluster Comparison"
    url: "https://www.baeldung.com/redis-sentinel-vs-clustering"
    accessed: "2025-10-26T18:28:30-0400"
---

## Purpose & When-To-Use

Invoke this skill when designing, reviewing, or optimizing Redis database architectures for applications requiring sub-millisecond latency, high-throughput caching, session management, real-time analytics, or distributed data structures.

**Trigger Conditions:**
- "Design a Redis caching layer for [application]"
- "Which Redis data structure should I use for [use case]?"
- "Configure Redis for high availability with [SLA]"
- "Optimize Redis memory usage for [data volume]"
- "Design rate limiting with Redis"
- "Plan Redis Sentinel vs Cluster for [requirements]"
- "Migrate from Redis [old version] to 8.0"

**Out of Scope:**
- PostgreSQL/MongoDB database design (use database-postgres-architect or database-mongodb-architect)
- Message queue architecture (use integration-messagequeue-designer)
- General database migration (use database-migration-generator)

---

## Pre-Checks

1. **Time Normalization:** Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601).
2. **Input Validation:**
   - Use case specified (caching, session, analytics, pub/sub, queue)
   - Data access patterns described (read/write ratio, TTL, hit rate)
   - Data volume estimates available (keys, memory, throughput)
3. **Version Check:** Redis version specified (default to 8.0 if not provided).
4. **Deployment Context:** Cloud provider or self-hosted, resource constraints (RAM, CPU, network).
5. **Existing Setup:** If optimizing existing Redis, request current configuration and redis-cli INFO output.

**Abort Conditions:**
- No use case or access patterns provided → emit TODO list with required inputs.
- Memory requirements completely unknown → warn that sizing will be generic.

---

## Procedure

### T1: Quick Cache Strategy & Data Structure Selection (≤2k tokens)

**Use Case:** Fast path for common scenarios (80% of requests).

**Steps:**
1. **Identify Use Case Category:**
   - **Caching:** Cache-aside (lazy loading) for read-heavy workloads.
   - **Session Storage:** Strings or Hashes with TTL for user sessions.
   - **Rate Limiting:** Sorted Sets or Strings with INCR + EXPIRE.
   - **Leaderboards:** Sorted Sets with ZADD + ZRANGE.
   - **Pub/Sub:** Redis Streams or Pub/Sub channels.
   - **Task Queue:** Lists with LPUSH + BRPOP or Redis Streams.

2. **Select Data Structure:**

| Use Case | Recommended Structure | Key Commands | Memory Efficiency |
|----------|----------------------|--------------|-------------------|
| Simple key-value cache | String | GET, SET, SETEX, TTL | Baseline |
| Structured objects (user profiles) | Hash | HGET, HSET, HGETALL | 50-70% savings vs strings |
| Recent items (activity feed) | List | LPUSH, LRANGE, LTRIM | Efficient for ordered data |
| Unique items (tags, followers) | Set | SADD, SMEMBERS, SINTER | Deduplication |
| Ranked items (leaderboards) | Sorted Set | ZADD, ZRANGE, ZRANK | Score-based sorting |
| Event streams (logs, messages) | Stream | XADD, XREAD, XGROUP | Append-only, consumer groups |
| Probabilistic (unique counts) | HyperLogLog | PFADD, PFCOUNT | 0.81% error, 12 KB max |
| Membership testing (spam filter) | Bloom Filter | BF.ADD, BF.EXISTS | Space-efficient (Redis 8.0) |

3. **Quick Wins:** Provide 1-3 immediate optimizations with estimated impact.
   - Example: "Use Hashes instead of JSON strings → 60% memory reduction"
   - Example: "Set maxmemory-policy allkeys-lru → prevent OOM errors"
   - Example: "Enable AOF with fsync everysec → 30% lower write latency"

**Output:** Use case mapping, data structure selection, top 3 quick wins.

---

### T2: Complete Architecture Design (≤6k tokens)

**Use Case:** Comprehensive architecture for production deployments.

**Steps:**

#### 1. Caching Strategy Selection

**Caching Patterns:**

| Pattern | Description | Pros | Cons | Best For |
|---------|-------------|------|------|----------|
| Cache-Aside (Lazy Loading) | App checks cache first, loads from DB on miss, populates cache | Flexible, cache only what's needed | First query slow (cache miss), stale data risk | Read-heavy apps, infrequent updates |
| Write-Through | App writes to cache, cache synchronously writes to DB | Strong consistency, simple invalidation | Slower writes (sync), cache all writes | Write-heavy, consistency critical |
| Write-Behind (Write-Back) | App writes to cache, cache asynchronously writes to DB | Fast writes (async), batch DB writes | Potential data loss on failure, eventual consistency | High write throughput, accept eventual consistency |

**Cache-Aside Example (Most Common):**
```python
def get_user(user_id):
    # 1. Check cache
    user = redis.get(f"user:{user_id}")
    if user:
        return json.loads(user)  # Cache hit

    # 2. Cache miss: load from database
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)

    # 3. Populate cache with TTL
    redis.setex(f"user:{user_id}", 3600, json.dumps(user))  # 1 hour TTL
    return user
```

**Write-Through Example:**
```python
def update_user(user_id, data):
    # 1. Write to cache
    redis.hset(f"user:{user_id}", mapping=data)

    # 2. Synchronously write to database
    db.execute("UPDATE users SET ... WHERE id = ?", user_id)

    # Cache and DB consistent
```

**Cache Consistency Models:**
- **Strong Consistency:** Write-through (cache + DB updated synchronously).
- **Eventual Consistency:** Write-behind (cache updated first, DB later).
- **TTL-based Expiry:** Cache-aside with Time-To-Live (auto-invalidation).

#### 2. Data Structure Optimization

**Memory Efficiency Techniques:**

1. **Use Hashes for Structured Data (50-70% savings):**
```redis
# Instead of multiple string keys (inefficient):
SET user:1000:name "Alice"
SET user:1000:email "alice@example.com"
SET user:1000:age "30"

# Use a single hash (efficient):
HSET user:1000 name "Alice" email "alice@example.com" age 30
HGETALL user:1000
```

2. **Sorted Sets for Ranked Data (Leaderboards):**
```redis
# Add players with scores
ZADD leaderboard 9500 "player1" 8200 "player2" 7800 "player3"

# Get top 10 players
ZRANGE leaderboard 0 9 WITHSCORES REV

# Get player rank
ZRANK leaderboard "player1"
```

3. **Streams for Event Processing (Redis 8.0 Enhanced):**
```redis
# Add event to stream
XADD events * type "login" user_id 1000 timestamp 1730000000

# Read events (consumer group)
XREADGROUP GROUP mygroup consumer1 COUNT 10 STREAMS events >
```

4. **HyperLogLog for Unique Counts (0.81% error, 12 KB max):**
```redis
# Count unique visitors
PFADD visitors:2025-10-26 "user1" "user2" "user1"  # Deduplication
PFCOUNT visitors:2025-10-26  # Returns ~2 (unique count)
```

5. **Bloom Filter for Membership Testing (Redis 8.0):**
```redis
# Create bloom filter with 10000 capacity, 1% error rate
BF.RESERVE spam_filter 0.01 10000

# Add emails
BF.ADD spam_filter "spam@example.com"

# Check membership (false positive possible, no false negative)
BF.EXISTS spam_filter "spam@example.com"  # Returns 1
BF.EXISTS spam_filter "real@example.com"  # Returns 0
```

#### 3. Eviction Policy Configuration

**8 Eviction Policies (Redis 8.0):**

| Policy | Target Keys | Algorithm | Best For |
|--------|-------------|-----------|----------|
| noeviction | N/A (errors on OOM) | N/A | Persistent data, cannot afford data loss |
| allkeys-lru | All keys | Least Recently Used | General cache, all keys eligible |
| volatile-lru | Keys with TTL | Least Recently Used | Mixed workload (cache + persistent) |
| allkeys-lfu | All keys | Least Frequently Used | Hotspot-heavy workloads (Redis 8.0: 16x faster) |
| volatile-lfu | Keys with TTL | Least Frequently Used | Mixed workload with frequency preference |
| allkeys-random | All keys | Random | Uniform access patterns |
| volatile-random | Keys with TTL | Random | Simple TTL-based expiry |
| volatile-ttl | Keys with TTL | Shortest TTL first | Expire soonest keys first |

**Configuration Example:**
```redis
# Set maximum memory to 4 GB (70-80% of 6 GB system RAM)
CONFIG SET maxmemory 4gb

# Set eviction policy to allkeys-lru
CONFIG SET maxmemory-policy allkeys-lru

# Verify
CONFIG GET maxmemory
CONFIG GET maxmemory-policy
```

**Redis 8.0 Eviction Improvements:**
- 16-slot eviction pool (improves key selection quality).
- allkeys-lfu: 16x faster query processing for frequency-based eviction.

#### 4. Persistence Configuration

**3 Persistence Options:**

| Option | Mechanism | Durability | Performance | Use Case |
|--------|-----------|------------|-------------|----------|
| RDB (Snapshots) | Point-in-time snapshots at intervals | Lose data since last snapshot | Fast (async), compact files | Backups, can tolerate data loss |
| AOF (Append-Only File) | Log every write operation | Lose ≤1 sec of data (fsync everysec) | Slower writes, larger files | Durability critical |
| Hybrid (RDB + AOF) | RDB snapshots + AOF log | Best of both | Balanced | Production (Redis 7.8.2+) |

**RDB Configuration:**
```redis
# Save snapshot every 900s if ≥1 key changed
# Save snapshot every 300s if ≥10 keys changed
# Save snapshot every 60s if ≥10000 keys changed
save 900 1
save 300 10
save 60 10000
```

**AOF Configuration (Recommended):**
```redis
# Enable AOF
appendonly yes

# fsync policy (choose one):
# - always: fsync every write (slowest, most durable)
# - everysec: fsync every second (30% lower latency, lose ≤1s data)
# - no: let OS decide (fastest, lose more data on crash)
appendfsync everysec

# AOF rewrite (compact log when 100% larger than last rewrite)
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

**Hybrid Persistence (Redis 7.8.2+, recommended for Redis 8.0):**
```redis
# Enable both RDB and AOF
save 900 1
appendonly yes
appendfsync everysec

# Redis performs RDB snapshots + AOF log for best durability
```

#### 5. High Availability Architecture

**Redis Sentinel (Failover & Monitoring):**

**Use Case:** High availability for single master, automatic failover, service discovery.

**Architecture:**
- **Minimum:** 3 Sentinel nodes (majority voting for failover).
- **Topology:** 1 master + 2 replicas + 3 Sentinel processes (can co-locate).
- **Failover Time:** Typically 10-30 seconds (configurable).

**Configuration:**
```redis
# sentinel.conf
sentinel monitor mymaster 192.168.1.100 6379 2  # 2 = quorum (majority of 3 sentinels)
sentinel down-after-milliseconds mymaster 5000   # Declare master down after 5s
sentinel parallel-syncs mymaster 1               # Sync 1 replica at a time during failover
sentinel failover-timeout mymaster 10000         # Failover timeout 10s
```

**Pros:**
- Simple setup (3 nodes minimum).
- Automatic failover with master election.
- Service discovery (clients query Sentinel for current master).

**Cons:**
- No horizontal scaling (single master).
- All data must fit on one node.

**Redis Cluster (Sharding & Scaling):**

**Use Case:** Horizontal scaling, data partitioning across nodes, built-in HA.

**Architecture:**
- **Minimum:** 6 nodes (3 masters + 3 replicas).
- **Sharding:** 16384 hash slots distributed across masters.
- **Topology:** Each master has ≥1 replica, automatic failover per shard.

**Configuration:**
```bash
# Create cluster with 3 masters + 3 replicas
redis-cli --cluster create \
  192.168.1.101:6379 192.168.1.102:6379 192.168.1.103:6379 \
  192.168.1.104:6379 192.168.1.105:6379 192.168.1.106:6379 \
  --cluster-replicas 1
```

**Hash Slot Distribution:**
- Total slots: 16384
- Example: Master1 (slots 0-5460), Master2 (5461-10922), Master3 (10923-16383)
- Key hashing: `CRC16(key) mod 16384` determines slot.

**Pros:**
- Horizontal scaling (1000 nodes max).
- Automatic sharding and rebalancing.
- Built-in HA (no external Sentinel).

**Cons:**
- More complex (6 nodes minimum).
- Multi-key operations limited (keys must be on same slot or use hash tags).
- No support for SELECT database command (only DB 0).

**Sentinel vs Cluster Decision Matrix:**

| Requirement | Redis Sentinel | Redis Cluster |
|-------------|----------------|---------------|
| Data size fits on single node | ✅ Yes | Not needed |
| Need horizontal scaling | ❌ No | ✅ Yes |
| Simple failover only | ✅ Yes | Overkill |
| High availability + sharding | ❌ No | ✅ Yes |
| Minimum nodes | 3 | 6 |

#### 6. Performance Tuning (Redis 8.0)

**Redis 8.0 Performance Improvements:**
- **87% faster latency** (p50 latency reduction).
- **2x more operations per second** (throughput).
- **16x faster query processing** (allkeys-lfu eviction).
- **112% throughput improvement** with I/O threading on multi-core CPUs.

**Configuration Parameters:**

```redis
# I/O Threading (Redis 8.0 - up to 112% improvement on multi-core)
io-threads 4  # Set to number of CPU cores (max 8)
io-threads-do-reads yes  # Enable threaded reads (Redis 8.0+)

# Max clients (default 10000)
maxclients 50000

# Timeout for idle clients (default 0 = never)
timeout 300  # Close idle clients after 5 minutes

# TCP backlog (default 511, increase for high concurrency)
tcp-backlog 65535

# Disable slow commands in production (optional)
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command CONFIG ""

# Lazy freeing (async deletion of large keys)
lazyfree-lazy-eviction yes
lazyfree-lazy-expire yes
lazyfree-lazy-server-del yes
```

**Memory Configuration:**
```redis
# Set maxmemory to 70-80% of system RAM (allows OS cache)
maxmemory 6gb  # For 8 GB RAM server

# Eviction policy
maxmemory-policy allkeys-lru

# Memory sampling for eviction (default 5, higher = better accuracy, slower)
maxmemory-samples 10
```

**Output:** Complete architecture with caching strategy, data structures, eviction policy, persistence, HA topology, performance tuning.

---

### T3: Enterprise Features & Use Case Patterns (≤12k tokens)

**Use Case:** Advanced patterns, multi-region, specific use cases, version migrations.

**Steps:**

#### 1. Advanced Use Case Patterns

**Rate Limiting (Fixed Window):**
```python
def is_rate_limited(user_id, limit=100, window=60):
    key = f"rate_limit:{user_id}"
    current = redis.incr(key)

    if current == 1:
        redis.expire(key, window)  # Set TTL on first request

    return current > limit  # True if over limit
```

**Rate Limiting (Sliding Window with Sorted Set):**
```python
def is_rate_limited_sliding(user_id, limit=100, window=60):
    now = time.time()
    key = f"rate_limit:{user_id}"

    # Remove old entries outside window
    redis.zremrangebyscore(key, 0, now - window)

    # Count requests in window
    count = redis.zcard(key)

    if count < limit:
        redis.zadd(key, {str(uuid.uuid4()): now})  # Add new request
        redis.expire(key, window)
        return False  # Not limited

    return True  # Limited
```

**Session Storage:**
```python
def create_session(user_id, session_data, ttl=3600):
    session_id = str(uuid.uuid4())
    key = f"session:{session_id}"

    # Store session as hash
    redis.hset(key, mapping={
        "user_id": user_id,
        **session_data
    })
    redis.expire(key, ttl)  # Auto-expire after 1 hour

    return session_id
```

**Real-Time Leaderboard:**
```python
def update_leaderboard(player_id, score):
    redis.zadd("leaderboard", {player_id: score})

def get_leaderboard(top_n=10):
    # Get top N players with scores
    return redis.zrange("leaderboard", 0, top_n - 1, withscores=True, desc=True)

def get_player_rank(player_id):
    rank = redis.zrevrank("leaderboard", player_id)  # 0-indexed
    return rank + 1 if rank is not None else None
```

**Pub/Sub (Real-Time Notifications):**
```python
# Publisher
def publish_notification(channel, message):
    redis.publish(channel, json.dumps(message))

# Subscriber
def subscribe_notifications(channel):
    pubsub = redis.pubsub()
    pubsub.subscribe(channel)

    for message in pubsub.listen():
        if message['type'] == 'message':
            data = json.loads(message['data'])
            handle_notification(data)
```

**Task Queue (Simple FIFO):**
```python
# Producer
def enqueue_task(queue_name, task_data):
    redis.lpush(queue_name, json.dumps(task_data))

# Consumer (blocking pop)
def process_tasks(queue_name):
    while True:
        # BRPOP blocks until item available (timeout 0 = infinite)
        _, task_json = redis.brpop(queue_name, timeout=0)
        task = json.loads(task_json)
        process_task(task)
```

#### 2. Multi-Region Deployment (Redis Enterprise)

**Active-Active Geo-Replication:**
- Redis Enterprise feature (not OSS).
- Conflict-free replicated data types (CRDTs).
- Bidirectional replication across regions.
- Automatic conflict resolution.

**Architecture:**
- Region 1: Redis cluster (3 masters + 3 replicas).
- Region 2: Redis cluster (3 masters + 3 replicas).
- Active-active replication between regions.
- Local reads/writes in each region (low latency).

**Use Case:** Global applications with local write requirements.

#### 3. Migration from Redis 7.x to 8.0

**Benefits of Redis 8.0:**
- 87% faster latency, 2x ops/sec (accessed 2025-10-26T18:28:30-0400, [Redis Blog](https://redis.io/blog/redis-8-ga/)).
- New I/O threading: 112% throughput improvement.
- Vector sets (beta), enhanced JSON, time series.
- 5 probabilistic structures: Bloom, Cuckoo, Count-min sketch, Top-k, t-digest.

**Migration Strategy (Zero-Downtime):**

1. **Set up Redis 8.0 replica** (add as slave to existing Redis 7.x master).
2. **Replicate data** (wait for replication lag to stabilize).
3. **Test queries on Redis 8.0 replica** (validate compatibility, performance).
4. **Promote Redis 8.0 replica to master** (use SLAVEOF NO ONE or Sentinel failover).
5. **Upgrade remaining replicas** (one at a time).
6. **Enable Redis 8.0 features** (io-threads, new data structures).
7. **Monitor for 24h** (rollback if issues detected).

**Risks:**
- Client library compatibility (ensure drivers support Redis 8.0).
- Deprecated features removed (check release notes).
- I/O threading requires tuning (set io-threads = CPU cores).

#### 4. Monitoring & Observability

**Key Metrics:**

```redis
# Server stats
INFO stats
# - total_commands_processed: Total commands executed
# - instantaneous_ops_per_sec: Current ops/sec
# - total_net_input_bytes, total_net_output_bytes: Network I/O
# - evicted_keys: Keys evicted due to maxmemory
# - expired_keys: Keys expired by TTL

# Memory stats
INFO memory
# - used_memory_human: Total memory used
# - used_memory_rss_human: OS-reported RSS
# - mem_fragmentation_ratio: RSS / used_memory (>1.5 = fragmentation issue)
# - maxmemory_human: Configured maxmemory limit

# Replication stats
INFO replication
# - role: master or slave
# - connected_slaves: Number of replicas
# - master_repl_offset: Replication offset (lag indicator)

# Slow log (queries >threshold)
SLOWLOG GET 10  # Last 10 slow queries
CONFIG SET slowlog-log-slower-than 10000  # Log queries >10ms
```

**Prometheus Exporter:**
- Use `redis_exporter` for Prometheus integration.
- Metrics: `redis_uptime_in_seconds`, `redis_connected_clients`, `redis_used_memory_bytes`, `redis_evicted_keys_total`.

**Output:** Advanced use case patterns, multi-region architecture, migration plan, monitoring dashboards.

---

## Decision Rules

1. **Caching Strategy:**
   - If read-heavy (80%+ reads) → **Cache-aside** (lazy loading).
   - If write-heavy + strong consistency → **Write-through**.
   - If write-heavy + eventual consistency OK → **Write-behind**.

2. **Data Structure:**
   - Simple key-value → **String**.
   - Structured object (user profile) → **Hash** (50-70% memory savings).
   - Ordered list (activity feed) → **List**.
   - Unique items (tags, followers) → **Set**.
   - Ranked items (leaderboard) → **Sorted Set**.
   - Event stream → **Stream** (consumer groups).
   - Unique count approximation → **HyperLogLog**.
   - Membership testing → **Bloom Filter** (Redis 8.0).

3. **Eviction Policy:**
   - General cache (all keys cache) → **allkeys-lru**.
   - Mixed workload (cache + persistent) → **volatile-lru**.
   - Hotspot-heavy → **allkeys-lfu** (Redis 8.0: 16x faster).
   - Cannot lose data → **noeviction** + monitor memory.

4. **Persistence:**
   - Can tolerate data loss (cache) → **RDB** only (fast).
   - Durability critical → **AOF** (appendfsync everysec).
   - Production → **Hybrid** (RDB + AOF) (Redis 7.8.2+).

5. **High Availability:**
   - Data fits on one node + need failover → **Redis Sentinel** (3 nodes).
   - Need horizontal scaling (>100 GB) → **Redis Cluster** (6+ nodes).
   - Global low-latency writes → **Redis Enterprise Active-Active** (multi-region).

6. **Memory Sizing:**
   - Set maxmemory to **70-80% of system RAM** (leave room for OS, fragmentation).
   - If mem_fragmentation_ratio >1.5 → restart Redis or use `CONFIG SET activedefrag yes`.

**Uncertainty Thresholds:**
- If access patterns unclear → request cache hit rate target and read/write ratio.
- If memory highly uncertain → provide scalable architecture with Cluster plan.
- If existing Redis has issues → request `INFO` output and slow log analysis.

---

## Output Contract

**Required Fields:**

```yaml
caching_strategy:
  - pattern: "cache-aside" | "write-through" | "write-behind"
    consistency_model: "strong" | "eventual" | "ttl-based"
    cache_invalidation: string (how to invalidate stale data)

data_structures:
  - use_case: string
    structure: "string" | "hash" | "list" | "set" | "sorted_set" | "stream" | "hyperloglog" | "bloom_filter"
    key_pattern: string (e.g., "user:{user_id}")
    commands: array (Redis commands used)
    memory_efficiency: string (e.g., "50% savings vs strings")

eviction_policy:
  - maxmemory: string (e.g., "4gb")
    policy: "allkeys-lru" | "volatile-lru" | "allkeys-lfu" | "noeviction" | ...
    justification: string

persistence:
  - type: "rdb" | "aof" | "hybrid"
    rdb_config: object (save intervals) if applicable
    aof_config: object (fsync policy) if applicable
    data_loss_tolerance: string (e.g., "≤1 second")

high_availability:
  - architecture: "standalone" | "sentinel" | "cluster"
    topology: string (e.g., "1 master + 2 replicas + 3 sentinels")
    failover_time: string (e.g., "10-30 seconds")
    scaling_plan: string (if cluster)

performance_tuning:
  - io_threads: integer (Redis 8.0)
    maxclients: integer
    timeout: integer (seconds)
    lazy_freeing: boolean
    estimated_improvement: string (e.g., "87% faster latency")

memory_optimization:
  - techniques: array (hash optimization, data structure selection, etc.)
    estimated_savings: string (e.g., "60% memory reduction")

migration_plan:  # If upgrading versions
  - current_version: string
    target_version: string
    strategy: "replica promotion" | "blue-green" | "rolling upgrade"
    steps: array (migration steps)
    risks: array (potential issues)
```

**Token Tier Minimums:**
- T1: caching_strategy, data_structures (top 3), eviction_policy, quick wins.
- T2: All of T1 + persistence, high_availability, performance_tuning, memory_optimization.
- T3: All of T2 + use_case_patterns, multi-region, migration_plan, monitoring.

---

## Examples

**Cache-Aside Pattern with Hash:**

```python
# User profile caching (60% memory savings vs JSON string)
def get_user_profile(user_id):
    key = f"user:{user_id}"

    # Check cache (hash structure)
    if redis.exists(key):
        return redis.hgetall(key)  # Cache hit

    # Cache miss: load from database
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)

    # Populate cache with TTL
    redis.hset(key, mapping=user)
    redis.expire(key, 3600)  # 1 hour

    return user
```

See `examples/session-storage-redis-architecture.txt` for a complete session management architecture.

---

## Quality Gates

1. **Token Budgets:**
   - T1 response ≤2k tokens (fast path, common scenarios).
   - T2 response ≤6k tokens (complete architecture).
   - T3 response ≤12k tokens (enterprise features, migrations).

2. **Safety Checks:**
   - No credentials or connection strings with passwords in output.
   - Eviction policy configured to prevent OOM errors.
   - Persistence enabled for durability-critical use cases.

3. **Auditability:**
   - All data structure selections include memory efficiency justification.
   - All HA architectures include failover time and scaling plan.
   - All performance claims cite Redis 8.0 benchmarks with access dates.

4. **Determinism:**
   - Same input (use case, access patterns, data volume) → same architecture recommendations.
   - Data structure selection deterministic (use case mapping table).

5. **Citations:**
   - Redis 8.0 performance: 87% faster latency, 2x ops/sec, 16x query processing (accessed 2025-10-26T18:28:30-0400, [Redis Blog](https://redis.io/blog/redis-8-ga/)).
   - Hash memory savings: 50-70% vs separate strings (accessed 2025-10-26T18:28:30-0400, [Redis Memory Optimization](https://medium.com/platform-engineer/redis-memory-optimization-techniques-best-practices-3cad22a5a986)).
   - Caching patterns: Cache-aside, write-through, write-behind (accessed 2025-10-26T18:28:30-0400, [Redis Caching](https://redis.io/solutions/caching/)).

---

## Resources

**Official Redis Documentation:**
- [Redis 8.0 Release Notes](https://redis.io/blog/redis-8-ga/) (accessed 2025-10-26T18:28:30-0400)
- [Redis Data Types Introduction](https://redis.io/docs/data-types/)
- [Redis Persistence](https://redis.io/docs/management/persistence/)
- [Redis Sentinel](https://redis.io/docs/management/sentinel/)
- [Redis Cluster](https://redis.io/docs/management/scaling/)

**Performance & Best Practices:**
- [Redis Caching Patterns](https://redis.io/solutions/caching/) (accessed 2025-10-26T18:28:30-0400)
- [Redis Eviction Policies](https://redis.io/docs/reference/eviction) (accessed 2025-10-26T18:28:30-0400)
- [Redis Memory Optimization](https://medium.com/platform-engineer/redis-memory-optimization-techniques-best-practices-3cad22a5a986) (accessed 2025-10-26T18:28:30-0400)
- [Sentinel vs Cluster Comparison](https://www.baeldung.com/redis-sentinel-vs-clustering) (accessed 2025-10-26T18:28:30-0400)

**Tools:**
- [RedisInsight](https://redis.io/insight/) (GUI for Redis with profiling)
- [redis-cli](https://redis.io/docs/ui/cli/) (command-line interface)
- [redis_exporter](https://github.com/oliver006/redis_exporter) (Prometheus exporter)
