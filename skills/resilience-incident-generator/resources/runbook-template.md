# Service Runbook Template

**Service Name:** [e.g., user-authentication-service]
**Team Owner:** [Team/Squad name]
**On-Call Rotation:** [PagerDuty schedule link]
**Last Updated:** [YYYY-MM-DD]

---

## Service Overview

**Description:** [Brief description of service purpose and functionality]

**Architecture:**
- Language/Framework: [e.g., Python/Flask, Go/gRPC, Node.js/Express]
- Database: [e.g., PostgreSQL, DynamoDB, MongoDB]
- Cache: [e.g., Redis, Memcached]
- Message Queue: [e.g., Kafka, RabbitMQ, SQS]
- External Dependencies: [list APIs, services, third-party integrations]

**Deployment:**
- Infrastructure: [AWS ECS, Kubernetes, Lambda]
- Regions: [us-east-1, eu-west-1]
- Replicas: [3 pods/containers per region]
- Auto-scaling: [Min: 3, Max: 20, Target CPU: 70%]

**SLOs:**
- Availability: 99.9% uptime (monthly)
- Latency: p95 < 200ms, p99 < 500ms
- Error Rate: < 0.5%

---

## Common Failure Scenarios

### Scenario 1: High Error Rate (>5%)

**Symptoms:**
- Monitoring alert: "Error rate > 5% for 5 minutes"
- Customers report: "Login failures", "500 Internal Server Error"
- Logs show: Database connection errors, timeout exceptions

**Diagnosis:**
```bash
# Check recent deployments
kubectl rollout history deployment/auth-service

# Check error rate by endpoint
curl -X GET "https://datadog.com/api/v1/query?query=sum:auth.errors{*}.as_rate()" \
  -H "DD-API-KEY: ${DD_API_KEY}"

# Check database connection pool
psql -h db.example.com -U readonly -c "SELECT count(*) FROM pg_stat_activity;"

# Check application logs
kubectl logs -l app=auth-service --tail=100 | grep ERROR
```

**Remediation:**
1. **Rollback recent deployment** (if deployment within last 30 minutes):
   ```bash
   kubectl rollout undo deployment/auth-service
   kubectl rollout status deployment/auth-service --watch
   ```

2. **Increase database connection pool** (if pool exhausted):
   ```bash
   # Update config map
   kubectl edit configmap auth-service-config
   # Set: DB_MAX_CONNECTIONS=200 (from 100)
   kubectl rollout restart deployment/auth-service
   ```

3. **Scale up replicas** (if traffic spike):
   ```bash
   kubectl scale deployment/auth-service --replicas=10
   ```

**Health Check:**
```bash
curl https://api.example.com/health
# Expected: {"status": "healthy", "db": "connected", "cache": "connected"}
```

---

### Scenario 2: High Latency (p95 > 1s)

**Symptoms:**
- Alert: "Auth service p95 latency > 1000ms"
- Customers report: "Slow login", "Page load delays"
- APM shows: Slow database queries, cache misses

**Diagnosis:**
```bash
# Check latency distribution
curl -X GET "https://datadog.com/api/v1/query?query=avg:auth.latency.p95{*}"

# Check slow queries
psql -h db.example.com -U readonly -c \
  "SELECT query, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"

# Check cache hit rate
redis-cli --cluster info redis.example.com:6379 | grep hit_rate
```

**Remediation:**
1. **Warm up cache** (if cache cold start):
   ```bash
   # Trigger cache pre-warming script
   kubectl exec -it deployment/auth-service -- /scripts/warm-cache.sh
   ```

2. **Add database indexes** (if slow query identified):
   ```sql
   -- Example: Add index on frequently queried column
   CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
   ```

3. **Enable query caching** (if repeated queries):
   ```bash
   # Update config to enable Redis query cache
   kubectl set env deployment/auth-service CACHE_QUERY_RESULTS=true
   ```

---

### Scenario 3: Service Unavailable (0% availability)

**Symptoms:**
- Alert: "Auth service returning 503 Service Unavailable"
- Health check endpoint returning 503
- All pods in CrashLoopBackOff state

**Diagnosis:**
```bash
# Check pod status
kubectl get pods -l app=auth-service

# Check pod logs
kubectl logs -l app=auth-service --previous --tail=50

# Check resource limits
kubectl describe pod -l app=auth-service | grep -A5 "Limits"

# Check dependency health
curl https://db.example.com/health  # Database health
curl https://redis.example.com/ping # Cache health
```

**Remediation:**
1. **Check dependencies** (database, cache, message queue):
   ```bash
   # If database is down, failover to read replica
   kubectl set env deployment/auth-service DB_HOST=replica.db.example.com
   ```

2. **Increase resource limits** (if OOMKilled):
   ```bash
   kubectl set resources deployment/auth-service \
     --limits=cpu=2,memory=2Gi \
     --requests=cpu=500m,memory=512Mi
   ```

3. **Restart pods** (if stuck in bad state):
   ```bash
   kubectl rollout restart deployment/auth-service
   kubectl rollout status deployment/auth-service --watch
   ```

---

## Rollback Procedure

**Automated Rollback (CI/CD):**
```bash
# Trigger rollback via CI/CD pipeline
gh workflow run rollback.yml -f service=auth-service -f version=v1.2.3
```

**Manual Rollback (Kubernetes):**
```bash
# Rollback to previous deployment
kubectl rollout undo deployment/auth-service

# Rollback to specific revision
kubectl rollout history deployment/auth-service  # Find revision number
kubectl rollout undo deployment/auth-service --to-revision=5

# Verify rollback success
kubectl rollout status deployment/auth-service --watch
curl https://api.example.com/health
```

**Rollback Validation:**
1. [ ] Health check endpoint returns 200 OK
2. [ ] Error rate < 1%
3. [ ] Latency p95 < 200ms
4. [ ] No CrashLoopBackOff pods
5. [ ] Customer-facing functionality verified (manual smoke test)

---

## Health Checks

**Liveness Probe:**
```bash
curl https://api.example.com/health/live
# Expected: HTTP 200, {"alive": true}
```

**Readiness Probe:**
```bash
curl https://api.example.com/health/ready
# Expected: HTTP 200, {"ready": true, "dependencies": {"db": "ok", "cache": "ok"}}
```

**Deep Health Check:**
```bash
curl https://api.example.com/health/deep
# Expected: HTTP 200, {
#   "service": "auth-service",
#   "version": "v1.2.5",
#   "database": {"status": "connected", "latency_ms": 12},
#   "cache": {"status": "connected", "hit_rate": 0.95},
#   "queue": {"status": "connected", "pending_messages": 42}
# }
```

---

## Dependency Startup Order

**Cold Start Procedure (disaster recovery):**
1. Start infrastructure: VPC, subnets, security groups
2. Start data stores: PostgreSQL, Redis, Kafka
3. Wait for data stores healthy (5-10 minutes)
4. Start core services: auth-service, user-service
5. Start dependent services: api-gateway, web-app
6. Validate end-to-end flow: login → API call → logout

**Dependencies (auth-service requires):**
- PostgreSQL: `db.example.com:5432` (primary dependency)
- Redis: `redis.example.com:6379` (cache, soft dependency)
- Kafka: `kafka.example.com:9092` (async events, soft dependency)

**Dependents (require auth-service):**
- api-gateway (hard dependency)
- web-app (hard dependency)
- mobile-app (hard dependency)

---

## Monitoring Queries

**Error Rate (Datadog):**
```
sum:auth.requests{status:error}.as_rate() / sum:auth.requests{*}.as_rate() * 100
```

**Latency P95 (Datadog):**
```
p95:auth.request.duration{*}
```

**Database Connection Pool (Prometheus):**
```
pg_stat_database_numbackends{datname="auth_db"} / pg_settings_max_connections
```

**Cache Hit Rate (Redis):**
```
redis_keyspace_hits / (redis_keyspace_hits + redis_keyspace_misses)
```

**Pod CPU Usage (Kubernetes):**
```
rate(container_cpu_usage_seconds_total{pod=~"auth-service.*"}[5m])
```

---

## Configuration

**Environment Variables:**
```bash
# Database
DB_HOST=db.example.com
DB_PORT=5432
DB_NAME=auth_db
DB_MAX_CONNECTIONS=100

# Cache
REDIS_HOST=redis.example.com
REDIS_PORT=6379
CACHE_TTL_SECONDS=3600

# Security
JWT_SECRET_KEY=<from-secrets-manager>
SESSION_TIMEOUT_MINUTES=30

# Observability
DD_API_KEY=<from-secrets-manager>
LOG_LEVEL=INFO
TRACE_SAMPLE_RATE=0.1
```

**Secrets (AWS Secrets Manager):**
- `auth-service/db-password`
- `auth-service/jwt-secret`
- `auth-service/datadog-api-key`

---

## Contacts

**Primary On-Call:** [PagerDuty schedule: auth-team-oncall]
**Escalation:**
- Manager: alice@example.com
- Tech Lead: bob@example.com
- DBA: charlie@example.com (for database issues)
- Security: security-team@example.com (for security incidents)

**Slack Channels:**
- #team-auth (team channel)
- #incidents (incident coordination)
- #on-call (on-call questions)
