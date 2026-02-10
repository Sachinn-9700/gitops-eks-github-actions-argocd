# 🚀 GitOps-Based Deployment on AWS EKS

**Auto-Scaling E-Commerce Application**

---

## 📌 Project Introduction

This project demonstrates a **practical DevOps workflow** for deploying and operating a small e-commerce application on **AWS EKS** using **GitOps principles**.

The focus of this project is not feature-rich application logic, but **infrastructure automation, deployment strategies, and Kubernetes operations**, implemented in a way that reflects real-world DevOps responsibilities.

---

## 🧰 Technologies Used

* **AWS** – EKS, networking components
* **Terraform** – Infrastructure provisioning
* **Docker** – Containerization
* **Kubernetes** – Application orchestration
* **GitHub Actions** – CI pipeline
* **Argo CD** – GitOps-based continuous delivery
* **Prometheus Client** – Metrics exposure

---

## ✨ Features Implemented

* Containerized frontend and backend services
* AWS EKS cluster provisioned using Terraform
* GitHub Actions CI triggered on code changes
* GitOps-based deployment using Argo CD
* Blue/Green deployment structure for frontend and backend
* CPU-based Horizontal Pod Autoscaler (HPA)
* Application health, versioning, and metrics endpoints
* Prometheus-compatible metrics exposure

---

## 🔁 The Process (How It Works)

1. **Infrastructure Provisioning**

   * Terraform is used to create AWS networking and EKS resources.
   * Cluster and node groups are created declaratively.

2. **Application Build**

   * Backend and frontend are containerized using Docker.
   * Backend runs Flask with Gunicorn for production readiness.

3. **Continuous Integration (CI)**

   * Code changes trigger GitHub Actions.
   * Images are built and prepared for deployment.

4. **GitOps Deployment (CD)**

   * Kubernetes manifests are stored in Git.
   * Argo CD monitors the repository and syncs changes to EKS.

5. **Deployment Strategy**

   * Blue and Green deployments exist side-by-side.
   * Traffic can be shifted without application downtime.

6. **Scaling & Observability**

   * CPU load is intentionally generated for HPA demonstration.
   * Prometheus metrics are exposed via `/metrics`.

---

## 📈 Overall Growth

This project helped me transition from **operational support thinking** to **deployment and platform thinking**, strengthening my understanding of how DevOps decisions impact reliability, scalability, and delivery speed.

---

