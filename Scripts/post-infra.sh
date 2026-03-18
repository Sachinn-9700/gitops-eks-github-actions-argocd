#!/bin/bash
set -euxo pipefail

AWS_REGION="us-east-1"
CLUSTER_NAME="auto-scaling-ecommerce-eks"

echo "Configuring kubeconfig..."
aws eks update-kubeconfig \
  --region "$AWS_REGION" \
  --name "$CLUSTER_NAME"

# Helm Installation
echo "Installing Helm..."
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

helm version

# ArgoCD Installation
echo "Installing ArgoCD..."
kubectl create namespace argocd || true

kubectl apply -n argocd \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

echo "Waiting for ArgoCD components..."
kubectl rollout status deployment/argocd-server -n argocd
kubectl rollout status deployment/argocd-repo-server -n argocd
kubectl rollout status deployment/argocd-application-controller -n argocd

echo "Fetching ArgoCD password..."
kubectl -n argocd get secret argocd-initial-admin-secret \
-o jsonpath="{.data.password}" | base64 -d
echo ""

echo "Access ArgoCD UI using:"
echo "kubectl port-forward svc/argocd-server -n argocd 8080:443"

# Monitoring Setup
echo "Setting up monitoring..."

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace

echo "Validating monitoring..."
kubectl get pods -n monitoring

echo "Post-infra setup completed!"