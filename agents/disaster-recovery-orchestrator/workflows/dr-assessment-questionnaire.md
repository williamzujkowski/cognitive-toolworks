# Disaster Recovery Assessment Questionnaire

**Purpose**: Gather business and technical requirements for DR planning.

## Business Impact Analysis

### Service Criticality
1. What is the maximum acceptable downtime for this service?
   - [ ] <15 minutes (critical, revenue-impacting)
   - [ ] <1 hour (high priority, customer-facing)
   - [ ] <4 hours (medium priority, internal systems)
   - [ ] <24 hours (low priority, batch processing)

2. What is the maximum acceptable data loss?
   - [ ] Zero data loss (synchronous replication required)
   - [ ] <5 minutes (near-real-time replication)
   - [ ] <1 hour (hourly backups acceptable)
   - [ ] <24 hours (daily backups acceptable)

3. What is the estimated business impact of downtime?
   - Revenue loss per hour: $__________
   - Regulatory penalties: Yes / No (specify: ____________)
   - Reputation damage: Critical / High / Medium / Low

### Compliance Requirements
4. Which regulatory frameworks apply?
   - [ ] PCI-DSS (payment card data)
   - [ ] HIPAA (healthcare data)
   - [ ] SOC2 (customer data security)
   - [ ] GDPR (EU customer data)
   - [ ] FedRAMP (federal systems)

5. Data residency restrictions?
   - [ ] Must remain in specific region/country: __________
   - [ ] No cross-border data transfer allowed
   - [ ] Encryption required for data at rest and in transit

## Technical Architecture

### Current State
6. What backup mechanisms currently exist?
   - Backup frequency: __________
   - Backup retention period: __________
   - Cross-region replication: Yes / No
   - Last tested restore date: __________

7. Service dependencies (list critical dependencies):
   - Databases: __________
   - External APIs: __________
   - Cloud services: __________
   - On-premises systems: __________

8. Single points of failure identified?
   - [ ] Single database instance (no replicas)
   - [ ] Single region deployment
   - [ ] No load balancer redundancy
   - [ ] Shared storage without replication

### DR Readiness
9. Have disaster recovery procedures been tested?
   - [ ] Never tested
   - [ ] Tested >12 months ago
   - [ ] Tested within last 6 months
   - [ ] Quarterly DR drills conducted

10. Existing DR documentation?
    - [ ] No documentation exists
    - [ ] High-level plan only
    - [ ] Detailed runbooks with step-by-step procedures
    - [ ] Automated failover with validated procedures

## Budget and Constraints

11. Budget allocated for disaster recovery?
    - [ ] No dedicated budget
    - [ ] <$5k/month (backup/restore pattern)
    - [ ] $5k-$20k/month (pilot light or warm standby)
    - [ ] >$20k/month (multi-site active-active)

12. Acceptable complexity for operations team?
    - [ ] Minimal (automated failover preferred)
    - [ ] Moderate (manual procedures acceptable with training)
    - [ ] High (dedicated SRE team available)

## Prioritization

13. Rank these disaster scenarios by concern level (1=highest, 5=lowest):
    - [ ] Regional cloud provider outage
    - [ ] Ransomware/malware attack
    - [ ] Accidental data deletion
    - [ ] Database corruption
    - [ ] Natural disaster impacting data center

---

**Completed by**: __________
**Date**: __________
**Reviewed by**: __________
