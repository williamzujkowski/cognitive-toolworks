# Error Budget Calculations

## Error Budget Formula

For a given SLO target over a time window:

```
Error Budget = (1 - SLO) × Time Window
```

### Examples

**99.9% SLO over 30 days:**
- Error Budget = (1 - 0.999) × 30 days = 0.001 × 30 days
- = 0.001 × 43,200 minutes = 43.2 minutes downtime allowed

**99.95% SLO over 30 days:**
- Error Budget = (1 - 0.9995) × 30 days = 0.0005 × 30 days
- = 0.0005 × 43,200 minutes = 21.6 minutes downtime allowed

**99.99% SLO over 30 days:**
- Error Budget = (1 - 0.9999) × 30 days = 0.0001 × 30 days
- = 0.0001 × 43,200 minutes = 4.32 minutes downtime allowed

## Burn Rate Thresholds

Burn rate is the speed at which error budget is consumed. A burn rate of 1x means consuming budget at exactly the rate allowed by SLO.

### Multi-Window Multi-Burn-Rate (MWMBR) Alerting

Based on Google SRE Workbook Chapter 5 (Alerting on SLOs):

| Window | Burn Rate | % Budget Consumed | Action | Severity |
|--------|-----------|-------------------|--------|----------|
| 1 hour | 14.4x | 2% in 1 hour | Page on-call immediately | Critical |
| 6 hours | 6x | 5% in 6 hours | Alert on-call engineer | Warning |
| 3 days | 1x | 10% in 3 days | Create ticket for review | Info |

### Burn Rate Calculation

For a 99.9% SLO (0.1% error budget):

**Critical threshold (1-hour window):**
```
Burn rate = (2% of budget) / (1 hour / 30 days)
          = 0.02 / (1/720)
          = 14.4x
Alert when: error_rate_1h > 14.4 × 0.001 = 0.0144 (1.44%)
```

**Warning threshold (6-hour window):**
```
Burn rate = (5% of budget) / (6 hours / 30 days)
          = 0.05 / (6/720)
          = 6x
Alert when: error_rate_6h > 6 × 0.001 = 0.006 (0.6%)
```

**Info threshold (3-day window):**
```
Burn rate = (10% of budget) / (3 days / 30 days)
          = 0.1 / 0.1
          = 1x
Alert when: error_rate_3d > 1 × 0.001 = 0.001 (0.1%)
```

## Error Budget Policy

### When Error Budget is Exhausted

1. **Immediate Actions:**
   - Halt all non-critical deployments
   - Defer feature work; focus on reliability improvements
   - Conduct incident review for root cause analysis

2. **Escalation Path:**
   - 90% budget consumed → SRE team notified
   - 100% budget consumed → Engineering manager escalation
   - SLO missed for 2 consecutive windows → VP Engineering escalation

3. **Recovery:**
   - Implement fixes for top reliability issues
   - Increase test coverage for failure modes
   - Review and tighten change management
   - Budget replenishes at start of new time window

### Error Budget-Based Release Decisions

| Budget Remaining | Release Policy |
|------------------|----------------|
| > 50% | Normal release velocity |
| 25-50% | Increase testing rigor; defer risky changes |
| 10-25% | Only critical bug fixes; defer features |
| < 10% | Feature freeze; reliability work only |

## Time to Budget Exhaustion

Calculate how long until error budget runs out at current burn rate:

```
Time to exhaustion = (Remaining budget) / (Current burn rate × Budget per day)
```

**Example:**
- SLO: 99.9% (43.2 min/30 days = 1.44 min/day)
- Remaining budget: 30 minutes
- Current error rate: 0.5% (5x burn rate)
- Time to exhaustion = 30 / (5 × 1.44) = 4.17 days

## Common SLO Targets

| SLO | Downtime/Year | Downtime/Month | Downtime/Week |
|-----|---------------|----------------|---------------|
| 90% | 36.5 days | 3 days | 16.8 hours |
| 95% | 18.25 days | 1.5 days | 8.4 hours |
| 99% | 3.65 days | 7.2 hours | 1.68 hours |
| 99.5% | 1.83 days | 3.6 hours | 50.4 minutes |
| 99.9% | 8.76 hours | 43.2 minutes | 10.1 minutes |
| 99.95% | 4.38 hours | 21.6 minutes | 5.04 minutes |
| 99.99% | 52.6 minutes | 4.32 minutes | 1.01 minutes |
| 99.999% | 5.26 minutes | 25.9 seconds | 6.05 seconds |
