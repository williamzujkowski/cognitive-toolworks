# Model Card: [Model Name]

**Version:** [e.g., 2.1.0]
**Date:** [YYYY-MM-DD]
**Model Type:** [Classification, Regression, Clustering, etc.]
**Framework:** [XGBoost, TensorFlow, PyTorch, scikit-learn, etc.]

## Model Details

**Developed by:** [Team/Organization]
**Model date:** [Training completion date]
**Model version:** [Semantic version]
**Model type:** [Architecture details]
**License:** [MIT, Apache 2.0, Proprietary, etc.]
**Contact:** [email@example.com]

### Intended Use

**Primary intended uses:** [e.g., Fraud detection for online transactions]
**Primary intended users:** [e.g., Risk operations team, automated decisioning system]
**Out-of-scope uses:** [e.g., Not for credit scoring or loan decisions]

## Training Data

**Dataset:** [Name and version]
**Size:** [Number of samples, features, classes]
**Time period:** [Data collection period]
**Geographic scope:** [If applicable]
**Source:** [Internal, public dataset, vendor]

**Preprocessing:**
- Feature engineering: [List key transformations]
- Normalization: [StandardScaler, MinMaxScaler, etc.]
- Missing value handling: [Imputation strategy]
- Class balancing: [SMOTE, undersampling, class weights]

**Data splits:**
- Training: [70%, N samples]
- Validation: [15%, N samples]
- Test: [15%, N samples]

**Label distribution:**
- Class 0 (negative): [Percentage]
- Class 1 (positive): [Percentage]

## Performance Metrics

### Overall Performance (Test Set)

| Metric         | Value  | Confidence Interval |
|----------------|--------|---------------------|
| Accuracy       | 0.943  | [0.938, 0.948]      |
| Precision      | 0.89   | [0.86, 0.92]        |
| Recall         | 0.87   | [0.84, 0.90]        |
| F1 Score       | 0.88   | [0.85, 0.91]        |
| AUC-ROC        | 0.956  | [0.951, 0.961]      |

### Performance by Subgroup

Evaluate fairness and bias across demographic/geographic groups:

| Subgroup       | Precision | Recall | F1    | Sample Size |
|----------------|-----------|--------|-------|-------------|
| Overall        | 0.89      | 0.87   | 0.88  | 10,000      |
| Region A       | 0.91      | 0.85   | 0.88  | 4,000       |
| Region B       | 0.87      | 0.89   | 0.88  | 6,000       |
| Transaction <$100 | 0.92   | 0.83   | 0.87  | 7,000       |
| Transaction ≥$100 | 0.84   | 0.93   | 0.88  | 3,000       |

**Disparate impact analysis:** [Description of fairness assessment]

## Model Architecture

**Algorithm:** [e.g., Gradient Boosted Trees (XGBoost)]
**Hyperparameters:**
```yaml
max_depth: 6
learning_rate: 0.1
n_estimators: 100
min_child_weight: 1
subsample: 0.8
colsample_bytree: 0.8
```

**Feature importance (Top 10):**
1. transaction_amount: 0.24
2. time_since_last_transaction: 0.18
3. account_age_days: 0.15
4. [Continue...]

**Input schema:**
```json
{
  "transaction_amount": "float",
  "merchant_category": "categorical",
  "transaction_hour": "int",
  "...": "..."
}
```

**Output schema:**
```json
{
  "fraud_probability": "float [0, 1]",
  "prediction": "binary {0, 1}",
  "decision_threshold": "float (default: 0.5)"
}
```

## Ethical Considerations

**Potential biases:**
- [e.g., Underrepresented in rural transactions]
- [e.g., Higher false positive rate for international transactions]

**Mitigation strategies:**
- [e.g., Balanced sampling during training]
- [e.g., Regularization to prevent overfitting on majority class]
- [e.g., Human review for high-value transactions]

**Privacy considerations:**
- PII handling: [Anonymized, encrypted, aggregated]
- Data retention: [30 days for predictions, 1 year for retraining]
- GDPR compliance: [Right to explanation via SHAP values]

**Limitations:**
- Not suitable for unseen transaction types
- Performance degrades after 90 days without retraining
- Requires minimum 50 features for accurate predictions

## Caveats and Recommendations

**Known failure modes:**
- Novel fraud patterns (zero-day attacks) have lower detection rate
- High-velocity attacks may bypass rate limiting
- Adversarial manipulation of feature values

**Recommendations:**
- Use as decision support, not sole arbiter
- Implement human review for edge cases (probability 0.4-0.6)
- Monitor for data drift and concept drift monthly
- Retrain model quarterly or when PSI > 0.25
- Combine with rule-based systems for comprehensive coverage

**Decision threshold guidance:**
- Default: 0.5 (balanced precision/recall)
- High precision: 0.7 (fewer false positives, more manual reviews)
- High recall: 0.3 (catch more fraud, higher false positive rate)

## Quantitative Analysis

**Confusion matrix (Test Set, threshold=0.5):**
```
                Predicted Negative    Predicted Positive
Actual Negative      8,500                   200
Actual Positive       200                   1,100
```

**Precision-Recall trade-off:**
- At precision=0.95: recall=0.72, F1=0.82
- At recall=0.95: precision=0.75, F1=0.84

**Latency benchmarks:**
- p50: 12ms
- p95: 45ms
- p99: 98ms
- Hardware: 2 CPU cores, 4GB RAM

## Monitoring and Maintenance

**Monitoring metrics:**
- Prediction distribution (fraud rate should be 1-2%)
- Feature drift (PSI per feature, threshold=0.2)
- Model accuracy on labeled subset (weekly)
- Latency and throughput

**Retraining triggers:**
- Scheduled: Quarterly
- Performance: F1 score drops below 0.85
- Drift: PSI > 0.25 on key features
- Business rule: Major regulatory change

**Versioning:**
- Current version: 2.1.0
- Previous version: 2.0.3 (archived)
- Training code: git@github.com/org/fraud-model.git, commit a3f4d9e

**Approval and deployment:**
- Trained by: [data-scientist@example.com]
- Reviewed by: [ml-lead@example.com]
- Approved by: [risk-manager@example.com]
- Deployed: [2025-10-20T14:32:18Z]
- Deployment environment: [Production, Kubernetes cluster us-west-2]

## References

- Training code repository: [GitHub URL]
- Experiment tracking: [MLflow run ID]
- Dataset documentation: [Wiki/Confluence link]
- Related models: [Predecessor model card]
- Standards: [ISO/IEC TR 24028:2020 AI trustworthiness]
