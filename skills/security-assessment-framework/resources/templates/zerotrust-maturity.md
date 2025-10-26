# Zero Trust Maturity Assessment (CISA Model)

## Identity Pillar

### Traditional
- [ ] Basic username/password authentication
- [ ] Manual identity provisioning
- [ ] No centralized identity management

### Initial
- [ ] Centralized identity management system
- [ ] MFA for remote access
- [ ] Basic access control policies

### Advanced
- [ ] MFA enforced enterprise-wide
- [ ] Risk-based authentication
- [ ] Just-in-time access provisioning
- [ ] Continuous validation of identity

### Optimal
- [ ] Automated risk-based access decisions
- [ ] Behavioral analytics for anomaly detection
- [ ] Dynamic access policies based on context
- [ ] Zero standing privileges

## Device Pillar

### Traditional
- [ ] Unmanaged devices allowed
- [ ] No device inventory
- [ ] Basic antivirus only

### Initial
- [ ] Device inventory maintained
- [ ] MDM/MAM deployed
- [ ] Device compliance checks

### Advanced
- [ ] Device health attestation required
- [ ] Automated compliance enforcement
- [ ] Device risk scoring

### Optimal
- [ ] Continuous device trust assessment
- [ ] Automated remediation
- [ ] Integration with access policies

## Network Pillar

### Traditional
- [ ] Perimeter-based security (castle-and-moat)
- [ ] Implicit trust inside network
- [ ] Broad network segments

### Initial
- [ ] Basic network segmentation
- [ ] VPN for remote access
- [ ] Macro-segmentation by department

### Advanced
- [ ] Micro-segmentation implemented
- [ ] Application-level network policies
- [ ] Encrypted internal traffic
- [ ] Software-defined perimeter (SDP)

### Optimal
- [ ] Dynamic micro-segmentation
- [ ] Per-request authorization
- [ ] Zero implicit trust zones
- [ ] Service mesh security

## Application Pillar

### Traditional
- [ ] Network-based access control
- [ ] Static application security
- [ ] Infrequent updates

### Initial
- [ ] Application-layer authentication
- [ ] Basic authorization checks
- [ ] API security controls

### Advanced
- [ ] Fine-grained authorization (ABAC/RBAC)
- [ ] Application-aware security policies
- [ ] Runtime application protection

### Optimal
- [ ] Dynamic authorization per request
- [ ] Continuous security testing
- [ ] Zero-trust API gateway
- [ ] Context-aware access control

## Data Pillar

### Traditional
- [ ] Perimeter-based data protection
- [ ] Basic data classification
- [ ] Limited encryption

### Initial
- [ ] Data classification scheme
- [ ] Encryption at rest
- [ ] DLP policies defined

### Advanced
- [ ] Automated data classification
- [ ] Encryption in transit and at rest
- [ ] Context-aware DLP
- [ ] Data access governance

### Optimal
- [ ] Dynamic data protection
- [ ] Real-time data risk scoring
- [ ] Data-centric security
- [ ] Rights management integration

## Maturity Scoring
- Traditional: 0-20% controls implemented
- Initial: 21-50% controls implemented
- Advanced: 51-80% controls implemented
- Optimal: 81-100% controls implemented
