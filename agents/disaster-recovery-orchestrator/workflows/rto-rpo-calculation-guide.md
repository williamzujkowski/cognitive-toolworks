# RTO/RPO Calculation Guide

**Purpose**: Methodology for determining Recovery Time Objective (RTO) and Recovery Point Objective (RPO) targets based on business requirements.

## Definitions

**RTO (Recovery Time Objective)**: Maximum acceptable duration of downtime after a disaster before business impact becomes unacceptable.

**RPO (Recovery Point Objective)**: Maximum acceptable amount of data loss measured in time (e.g., 5 minutes of transactions).

## Calculation Methodology

### Step 1: Determine Business Impact

Calculate the cost of downtime per hour:
```
Downtime_Cost = Revenue_Loss + Regulatory_Penalties + Operational_Cost + Reputation_Damage
```

Example (e-commerce platform):
- Revenue loss: $50,000/hour (average transaction volume)
- Operational cost: $5,000/hour (support team escalations)
- Reputation damage: High (customer trust impact)
- **Total**: ~$55,000/hour + reputational risk

### Step 2: Map Impact to RTO Tiers

| Business Impact | RTO Target | DR Pattern | Est. Cost |
|----------------|------------|------------|-----------|
| Critical (>$50k/hr) | <30 min | Multi-site active-active or warm standby | $20k-$50k/month |
| High ($10k-$50k/hr) | <1 hour | Warm standby or pilot light | $10k-$20k/month |
| Medium ($1k-$10k/hr) | <4 hours | Pilot light or backup/restore | $2k-$10k/month |
| Low (<$1k/hr) | <24 hours | Backup/restore | <$2k/month |

### Step 3: Determine Data Loss Tolerance (RPO)

Consider:
- **Transaction systems**: RPO typically <5 minutes (risk of lost orders, payments)
- **Analytics/reporting**: RPO can be hours or days (historical data, less time-sensitive)
- **Compliance requirements**: GDPR, HIPAA may mandate specific RPO targets

RPO formula:
```
Acceptable_Data_Loss = (Avg_Transactions_Per_Minute) × (RPO_Minutes) × (Avg_Transaction_Value)
```

Example:
- 100 transactions/minute × 5 minutes RPO × $50/transaction = $25,000 potential loss
- If acceptable, RPO = 5 minutes; if not, reduce to 1 minute or implement synchronous replication (RPO=0)

### Step 4: Align with SLO Error Budgets

If service has defined SLO (e.g., 99.9% availability):
```
Monthly_Error_Budget = (1 - SLO) × 30_days × 24_hours × 60_minutes
99.9% SLO = 43.2 minutes/month allowed downtime
```

RTO must be significantly less than error budget to allow for multiple incidents:
```
RTO_Target ≤ Error_Budget / Expected_Incidents_Per_Month
```

Example: 43.2 min/month ÷ 2 incidents = 21.6 min RTO target

### Step 5: Validate Technical Feasibility

Check if RTO/RPO targets are achievable:

| RTO Target | Technical Requirements | Complexity |
|------------|----------------------|------------|
| <5 min | Automated failover, multi-region active-active, <30s DNS TTL | Very High |
| <30 min | Warm standby, health check automation, pre-scaled capacity | High |
| <1 hour | Pilot light, auto-scaling, tested runbooks | Medium |
| <4 hours | Backup/restore with automation, documented procedures | Low |

| RPO Target | Replication Strategy | Cost Impact |
|------------|---------------------|-------------|
| 0 (zero data loss) | Synchronous replication, quorum writes | High (2-3x storage) |
| <5 min | Asynchronous replication, WAL shipping | Medium (2x storage) |
| <1 hour | Hourly snapshots, incremental backups | Low (1.5x storage) |
| <24 hours | Daily backups, full snapshots | Minimal (1.2x storage) |

## Example Calculation Worksheet

**Service**: Payment Processing API

1. **Business Impact**:
   - Revenue: $100k/hour downtime
   - Compliance: PCI-DSS (no specific RTO mandate)
   - Reputation: Critical (customer payment failures)

2. **RTO Determination**:
   - Impact tier: Critical (>$50k/hr)
   - Recommended RTO: <30 minutes
   - Selected DR pattern: Warm standby (us-east-1 primary, us-west-2 standby)

3. **RPO Determination**:
   - Avg transactions: 200/min
   - Avg value: $75/transaction
   - 5-min RPO loss: 200 × 5 × $75 = $75,000
   - Decision: Unacceptable → reduce to 1-min RPO (asynchronous replication)
   - 1-min RPO loss: 200 × 1 × $75 = $15,000 (acceptable threshold)

4. **SLO Alignment**:
   - SLO: 99.95% (21.6 min/month error budget)
   - Expected incidents: 2/month
   - RTO target: 21.6 ÷ 2 = ~10 minutes (target under 30-min requirement)

5. **Final Targets**:
   - **RTO**: 30 minutes (with 10-min aspirational goal)
   - **RPO**: 1 minute
   - **Pattern**: Warm standby with asynchronous replication
   - **Cost**: ~$18k/month (standby infrastructure + cross-region bandwidth)

---

**Template Usage**: Copy this worksheet, fill in service-specific values, and use results to inform DR strategy selection.
