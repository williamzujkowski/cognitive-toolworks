# Example: AWS Over-Budget Cost Optimization

## Scenario
AWS environment $15k over monthly budget ($65k actual vs $50k budget). Team needs rapid cost reduction.

## Input
```json
{
  "cloud_provider": "aws",
  "time_range": "90d",
  "current_spend": 65000,
  "budget": 50000,
  "optimization_targets": ["compute", "storage", "network"]
}
```

## Output Summary
- **Total savings**: $12,800/month ($153,600 annual)
- **Savings percentage**: 26.9% reduction
- **Quick wins**: $810/month (2 hours effort)
- **Implementation timeline**: 4 weeks to full savings

## Phased Rollout
1. Week 1: Quick wins + Storage = $2,010/month
2. Week 2-3: Network + Non-prod rightsizing = $2,990/month
3. Week 4: Production rightsizing = $2,400/month
4. Month 2: Commitment planning = $5,400/month

## Key Recommendations
- Delete 27 unused resources (volumes, IPs, load balancers)
- Rightsize 23 over-provisioned EC2/RDS instances
- Purchase 3-year Compute Savings Plan
- Enable S3 Intelligent-Tiering
- Deploy VPC endpoints to reduce NAT/egress costs
