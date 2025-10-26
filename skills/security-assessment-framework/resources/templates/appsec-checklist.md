# Application Security (AppSec) Assessment Checklist

## OWASP Top 10 2021 Quick Reference

### A01:2021 - Broken Access Control
- [ ] Horizontal privilege escalation prevented
- [ ] Vertical privilege escalation prevented
- [ ] Direct object references protected (IDOR)
- [ ] Metadata manipulation blocked
- [ ] CORS properly configured

### A02:2021 - Cryptographic Failures
- [ ] Data classified (public, internal, sensitive, critical)
- [ ] Encryption at rest for sensitive data
- [ ] TLS for data in transit
- [ ] No weak algorithms (MD5, SHA1, DES)
- [ ] Proper key management

### A03:2021 - Injection
- [ ] Parameterized queries (SQL injection prevention)
- [ ] Input validation on all user inputs
- [ ] Output encoding (XSS prevention)
- [ ] Command injection protection
- [ ] LDAP/XML injection safeguards

### A04:2021 - Insecure Design
- [ ] Threat modeling conducted
- [ ] Security requirements defined
- [ ] Secure design patterns used
- [ ] Security controls at design phase

### A05:2021 - Security Misconfiguration
- [ ] Hardened default configurations
- [ ] Unnecessary features disabled
- [ ] Security headers configured (CSP, HSTS, X-Frame-Options)
- [ ] Error messages don't leak info
- [ ] Latest security patches applied

### A06:2021 - Vulnerable Components
- [ ] Component inventory maintained (SBOM)
- [ ] Regular vulnerability scanning
- [ ] Dependency updates monitored
- [ ] Components from trusted sources only

### A07:2021 - Identification & Authentication Failures
- [ ] Multi-factor authentication available
- [ ] Credential stuffing protection
- [ ] Session management secure
- [ ] Password policy enforced
- [ ] Account lockout mechanisms

### A08:2021 - Software/Data Integrity Failures
- [ ] Digital signatures verified
- [ ] CI/CD pipeline secured
- [ ] Auto-update security verified
- [ ] Serialization security

### A09:2021 - Logging & Monitoring Failures
- [ ] Security events logged
- [ ] Log integrity protected
- [ ] Alerting configured
- [ ] Incident response plan exists

### A10:2021 - Server-Side Request Forgery (SSRF)
- [ ] URL validation implemented
- [ ] Network segmentation used
- [ ] Deny-by-default firewall rules
