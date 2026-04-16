---
name: "domino-data-connectivity"
description: "Connect Domino workloads to external data sources — AWS S3 via Mountpoint CSI, AWS IRSA credential propagation, Azure Entra ID integration, and External Data Volumes."
version: "1.0.0"
author: "Domino Data Lab / Tolu"
tags: ["domino", "mlops", "data-connectivity", "aws", "s3", "irsa", "azure", "credentials", "cloud-storage"]
trigger_patterns:
  - "domino s3 access"
  - "domino data connectivity"
  - "domino aws irsa"
  - "domino azure credentials"
  - "domino s3 mountpoint"
  - "connect domino to s3"
  - "domino external data volume"
  - "domino credential propagation"
---

# Domino Data Connectivity Skill

Connect Domino workloads to external data sources including AWS S3 (via Mountpoint CSI driver), AWS IRSA credential propagation, Azure Entra ID, and External Data Volumes.

## Activation

Activate this skill when users want to:
- Connect Domino to external data sources (S3, Azure Storage, etc.)
- Configure S3 Mountpoint for file system access
- Set up AWS IRSA for credential propagation
- Configure Azure Entra ID integration
- Work with External Data Volumes (EDV)

---

## Data Access Options in Domino

| Option | Use Case |
|--------|----------|
| **Datasets** | Project-level data storage |
| **Data Sources** | External database connections |
| **External Data Volumes (EDV)** | Mount external storage as volumes |
| **S3 Mountpoint** | Direct S3 access as file system |
| **Credential Propagation** | Pass user identity to cloud services |

### Credential Propagation Methods

| Method | Cloud | Description |
|--------|-------|-------------|
| **IRSA** | AWS | IAM Role for Service Accounts via OIDC |
| **Azure Entra ID** | Azure | User-based credential propagation |

### When to Use Each Option

**Use S3 Mountpoint when:**
- Working with large datasets stored in S3
- Need file system interface to S3
- Want to avoid EFS costs for large data
- Require multi-region data access

**Use IRSA when:**
- Need AWS service access from Domino workloads
- Policy prohibits long-lived credentials
- Require user-level audit trails
- Need cross-account role assumption

**Use Azure Entra when:**
- Working with Azure data services
- Need OAuth-based authentication
- Require user-level access control
- Need centralized RBAC

---

## AWS S3 Mountpoint Integration

AWS Mountpoint for Amazon S3 CSI driver enables mounting S3 buckets as local file systems in Kubernetes pods, including Domino workspaces, jobs, and apps.

### Benefits
- **Cost-effective storage**: Direct S3 access without EFS overhead
- **Familiar interface**: File browsing just like local storage
- **Scalability**: Access massive datasets without copying
- **Security**: No privileged container access required

### Architecture

```
┌─────────────────────┐
│   Domino Workload   │
│   (Workspace/Job)   │
├─────────────────────┤
│  /mnt/s3-data/      │  ← Mounted S3 bucket
└──────────┬──────────┘
           │
    ┌──────▼──────┐
    │  CSI Driver  │
    │  (Node-level)│
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │  AWS S3      │
    │  Bucket      │
    └─────────────┘
```

**Ideal for:** Large datasets, read-heavy workloads, multi-region access, security-conscious environments.
**Not recommended for:** Write-heavy workloads, small frequently-accessed datasets, low-latency requirements.

### Setup

#### Step 1: IAM Configuration

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "MountpointFullBucketAccess",
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME"
    },
    {
      "Sid": "MountpointFullObjectAccess",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
    }
  ]
}
```

#### Step 2: Create Service Account

```bash
eksctl create iamserviceaccount \
  --name s3-csi-driver-sa \
  --namespace kube-system \
  --cluster YOUR-CLUSTER-NAME \
  --attach-policy-arn arn:aws:iam::ACCOUNT_ID:policy/S3CSIDriverPolicy \
  --approve \
  --override-existing-service-accounts
```

#### Step 3: Install CSI Driver

```bash
helm repo add aws-mountpoint-s3-csi-driver \
  https://awslabs.github.io/mountpoint-s3-csi-driver

helm install aws-mountpoint-s3-csi-driver \
  aws-mountpoint-s3-csi-driver/aws-mountpoint-s3-csi-driver \
  --namespace kube-system \
  --set controller.serviceAccount.annotations."eks\.amazonaws\.com/role-arn"=arn:aws:iam::ACCOUNT_ID:role/S3CSIDriverRole
```

#### Step 4: Create PersistentVolume

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: s3-pv
spec:
  capacity:
    storage: 1Ti
  accessModes:
    - ReadWriteMany
  mountOptions:
    - allow-delete
    - region us-east-1
    - uid=12574
    - gid=12574
  csi:
    driver: s3.csi.aws.com
    volumeHandle: s3-csi-driver-volume
    volumeAttributes:
      bucketName: YOUR-BUCKET-NAME
```

#### Step 5: Create PersistentVolumeClaim

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: s3-pvc
  namespace: domino-compute
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: ""
  resources:
    requests:
      storage: 1Ti
  volumeName: s3-pv
```

#### Step 6: Configure Domino EDV

1. Go to **Admin** → **External Data Volumes**
2. Click **New External Data Volume**
3. Configure:
   - **Name**: s3-data
   - **Mount Path**: /mnt/s3-data
   - **PVC Name**: s3-pvc
   - **Namespace**: domino-compute

### Using S3 Mountpoint in Workloads

```python
import pandas as pd

# Read data
	df = pd.read_csv("/mnt/s3-data/datasets/sales.csv")
df = pd.read_parquet("/mnt/s3-data/datasets/large_dataset.parquet")

# Write results
df.to_parquet("/mnt/s3-data/outputs/results.parquet")

# List files
import os
files = os.listdir("/mnt/s3-data/datasets/")
```

### With Spark

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
df = spark.read.parquet("/mnt/s3-data/datasets/")
df_processed = df.filter(...)
df_processed.write.parquet("/mnt/s3-data/outputs/")
```

### Mount Options

| Option | Description |
|--------|-------------|
| `region` | AWS region of the bucket |
| `uid` / `gid` | User/group ID for file ownership |
| `allow-delete` | Enable file deletion |
| `allow-other` | Allow access by other users |
| `prefix` | Mount only a specific prefix |

### Performance Tips

1. Use Parquet or other columnar formats
2. Partition large datasets
3. Avoid many small files
4. Use appropriate file sizes (100MB-1GB)
5. First access may have higher latency; subsequent reads benefit from caching
6. Writes are uploaded on close; large files uploaded in parts

### S3 Mountpoint Troubleshooting

**Mount Failures:**
```bash
kubectl get pods -n kube-system | grep mountpoint
kubectl logs -n kube-system -l app=aws-mountpoint-s3-csi-driver
```

**Permission Errors (Access Denied):**
1. Verify IAM policy is correct
2. Check service account annotation
3. Verify bucket name is correct
4. Check uid/gid mount options

**Slow Performance:**
1. Check network connectivity to S3
2. Verify bucket is in same region
3. Consider S3 Transfer Acceleration
4. Use larger files to reduce overhead

---

## AWS IRSA (IAM Role for Service Accounts)

IRSA enables Kubernetes workloads to assume AWS IAM roles securely using OpenID Connect (OIDC) authentication, eliminating the need for long-lived credentials.

### Benefits
- **No hardcoded credentials**: Eliminates static access keys
- **Short-lived tokens**: Automatic token rotation
- **Least privilege**: Fine-grained IAM policies
- **Audit trails**: Full CloudTrail logging
- **Cross-account access**: Support for multi-account architectures

### How IRSA Works

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Domino         │────▶│  Kubernetes      │────▶│  AWS STS        │
│  Workload       │     │  Service Account │     │  AssumeRole     │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                        ┌──────────────────┐              │
                        │  OIDC Provider   │◀─────────────┘
                        │  (EKS/Kubernetes)│   Validates JWT
                        └──────────────────┘
```

### Setup

#### Step 1: Enable OIDC Provider

```bash
aws eks describe-cluster \
  --name YOUR-CLUSTER-NAME \
  --query "cluster.identity.oidc.issuer" \
  --output text

eksctl utils associate-iam-oidc-provider \
  --cluster YOUR-CLUSTER-NAME \
  --approve
```

#### Step 2: Create IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:ListBucket"],
      "Resource": ["arn:aws:s3:::your-bucket", "arn:aws:s3:::your-bucket/*"]
    },
    {
      "Effect": "Allow",
      "Action": ["sagemaker:CreateEndpoint", "sagemaker:InvokeEndpoint"],
      "Resource": "*"
    }
  ]
}
```

#### Step 3: Create IAM Role with Trust Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::ACCOUNT_ID:oidc-provider/oidc.eks.REGION.amazonaws.com/id/OIDC_ID"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.REGION.amazonaws.com/id/OIDC_ID:sub": "system:serviceaccount:domino-compute:SERVICEACCOUNT_NAME"
        }
      }
    }
  ]
}
```

#### Step 4: Create Kubernetes Service Account

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: domino-irsa-sa
  namespace: domino-compute
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::ACCOUNT_ID:role/DominoWorkloadRole
```

#### Step 5: Configure Domino Workloads

Domino uses a mutating webhook (Domsed) to inject IRSA configuration. Configure mutations based on user identity, project, hardware tier, or custom labels.

### Using IRSA in Workloads

```python
import boto3

# No explicit credentials needed - IRSA provides them automatically
s3 = boto3.client('s3')
response = s3.list_objects_v2(Bucket='my-bucket')

# Access other AWS services
sagemaker = boto3.client('sagemaker')
dynamodb = boto3.resource('dynamodb')
secretsmanager = boto3.client('secretsmanager')
```

### Verify Credentials

```python
import boto3
sts = boto3.client('sts')
identity = sts.get_caller_identity()
print(f"Account: {identity['Account']}")
print(f"ARN: {identity['Arn']}