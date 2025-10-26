# Payment Platform DR Plan Example

**Service**: payment-processing-platform | **RTO**: 30min | **RPO**: 5min | **Pattern**: Warm Standby

## Architecture
- Primary: us-east-1 (active), DR: us-west-2 (warm standby 50%)
- Replication: Synchronous transaction-db, async logs
- Failover: Route53 health check → auto DNS cutover (TTL 60s)

## Backup Policy
- Frequency: Continuous WAL + hourly snapshots
- Retention: 30-day point-in-time recovery
- Encryption: AES-256 KMS | Cross-region: <5min to us-west-2

## Failover Procedure
1. Health check failure (3 consecutive, 15s interval)
2. Route53 DNS update to us-west-2 (60s)
3. Auto-scale to 100% capacity (5min)
4. Database promotion (automated)
5. Validation: smoke tests + transaction verification

## Rollback & Testing
- Rollback: DNS revert → DB demotion → weighted routing (10% increments)
- Quarterly: Tabletop | Semi-annual: Staging test
- Annual: Full drill (2am-6am ET) | Monthly: Chaos (1% blast radius)
