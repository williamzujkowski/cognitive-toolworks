# Discovery & Baseline Workflow

## Purpose
Establish cost baseline and validate inputs before invoking cost-optimization-analyzer skill.

## Inputs Required
- `cloud_provider`: One or more of [aws, azure, gcp]
- `time_range`: Minimum 7d, recommend 30d for T2, 90d for commitments
- `optimization_targets`: Array of service categories or "all"
- `budget_constraints`: Optional monthly budget and alert thresholds

## Step-by-Step Process

### 1. Input Validation
```bash
# Validate cloud provider
if [[ ! "$cloud_provider" =~ ^(aws|azure|gcp|multi)$ ]]; then
  echo "ERROR: Invalid cloud provider. Must be aws, azure, gcp, or multi"
  exit 1
fi

# Validate time range
if [[ "$time_range" == "7d" || "$time_range" == "30d" || "$time_range" == "90d" ]]; then
  echo "Valid time range: $time_range"
else
  echo "WARNING: Custom time range. Ensure minimum 7d for analysis."
fi
```

### 2. Billing API Access Check
```bash
# AWS
aws ce get-cost-and-usage --time-period Start=2025-10-01,End=2025-10-02 --granularity DAILY --metrics BlendedCost

# Azure
az costmanagement query --type Usage --dataset-granularity Daily

# GCP
gcloud billing accounts list
```

### 3. Resource Discovery
- Fetch compute instances (EC2, VM, GCE)
- Fetch storage resources (S3, Blob, Cloud Storage)
- Fetch databases (RDS, SQL Database, Cloud SQL)
- Fetch networking (Load balancers, NAT gateways, VPN)

### 4. Baseline Metrics Calculation
```json
{
  "total_monthly_spend": 65000,
  "top_services": [
    {"service": "EC2", "spend": 28000},
    {"service": "RDS", "spend": 15000},
    {"service": "S3", "spend": 8000}
  ],
  "trend": "+15% month-over-month",
  "resource_count": 847
}
```

### 5. Tier Decision
- If spend <$10k/month → T1 quick check
- If spend ≥$10k/month → T2 comprehensive
- If commitments requested → Require 90d history

## Output
- Validated inputs ready for analysis step
- Baseline metrics for comparison
- Tier selection for cost-optimization-analyzer skill
