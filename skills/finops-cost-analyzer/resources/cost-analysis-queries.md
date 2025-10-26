# Cost Analysis Queries by Cloud Provider

## AWS Cost Explorer API Queries

### Get monthly cost by service (last 90 days)
```python
ce_client.get_cost_and_usage(
    TimePeriod={'Start': '2025-07-25', 'End': '2025-10-25'},
    Granularity='MONTHLY',
    Metrics=['UnblendedCost'],
    GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
)
```

### Identify unattached EBS volumes
```python
ec2_client.describe_volumes(
    Filters=[{'Name': 'status', 'Values': ['available']}]
)
# Cost calculation: volume_size_gb * $0.10/GB/month
```

### Get rightsizing recommendations
```python
ce_client.get_rightsizing_recommendation(
    Service='AmazonEC2',
    Configuration={'RecommendationTarget': 'SAME_INSTANCE_FAMILY'}
)
```

## Azure Cost Management API Queries

### Query cost by resource group
```http
POST https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.CostManagement/query?api-version=2023-11-01
{
  "type": "ActualCost",
  "timeframe": "MonthToDate",
  "dataset": {
    "granularity": "Daily",
    "aggregation": {"totalCost": {"name": "Cost", "function": "Sum"}},
    "grouping": [{"type": "Dimension", "name": "ResourceGroup"}]
  }
}
```

### Identify idle virtual machines (Azure Advisor)
```python
advisor_client.recommendations.list(
    filter="category eq 'Cost' and impactedField eq 'Microsoft.Compute/virtualMachines'"
)
```

## GCP Cloud Billing API Queries

### Export billing data to BigQuery
```sql
SELECT
  service.description AS service,
  SUM(cost) AS total_cost,
  SUM(usage.amount) AS usage_amount
FROM `project.billing_dataset.gcp_billing_export_v1_XXXXXX`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-07-25')
  AND _PARTITIONTIME < TIMESTAMP('2025-10-25')
GROUP BY service
ORDER BY total_cost DESC
```

### Identify idle persistent disks
```python
compute_client.disks().aggregatedList(
    project=project_id,
    filter='status=READY AND -users:*'
).execute()
```

## Cross-Cloud Waste Detection Patterns

### Unused Load Balancers (zero traffic >7 days)
- AWS: ELB/ALB/NLB with TargetHealthyHostCount=0
- Azure: Load Balancer with zero backend pool members
- GCP: Load Balancer with zero backend instances

### Orphaned Snapshots (>90 days old, source volume deleted)
- AWS: EC2 snapshots where OwnerAlias=self AND source volume not found
- Azure: Managed snapshots without corresponding disk
- GCP: Persistent disk snapshots with deleted source disk

### Over-provisioned Databases
- AWS RDS: CPUUtilization <20% AND DatabaseConnections <10% capacity
- Azure SQL: DTU utilization <15% for 30 days
- GCP Cloud SQL: CPU <20% AND active connections <10 for 30 days
