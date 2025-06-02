# Splitclone

Splitclone is a full-stack expense-splitting platform that helps users track group expenses and automatically calculate fair repayments using a custom settle-up algorithm.

## Features
- Group-based expense tracking with dynamic member selection
- Settle-up algorithm to minimize repayments across groups
- Backend built with Flask + PostgreSQL (AWS RDS)
- Frontend built with React, hosted via S3 and CloudFront
- Infrastructure managed using Terraform
- Containerized deployment on AWS ECS Fargate with ALB
- CI/CD pipelines using GitHub Actions
- Custom domain via Route 53 with SSL (in progress)
- Observability via Prometheus + Grafana (WIP)
- Authentication and test coverage (WIP)

## Tech Stack
- **Languages:** Python, SQL, JavaScript, Bash  
- **Backend:** Flask, SQLAlchemy, PostgreSQL  
- **Frontend:** React  
- **Infra/DevOps:** Docker, Terraform, ECS Fargate, ECR, ALB, RDS, VPC, S3, CloudFront, Route 53, IAM, ACM  
- **Monitoring:** Prometheus, Grafana, CloudWatch  
- **CI/CD:** GitHub Actions  

## Architecture Overview

### Frontend
- Built with React (hooks + functional components)
- Hosted on AWS S3, delivered globally via CloudFront
- HTTPS and domain configured through Route 53 and ACM

### Backend
- Flask API containerized with Docker
- Connects to RDS PostgreSQL database
- Deployed to ECS Fargate behind an ALB
- Scales across multiple Availability Zones

### Infrastructure
- Managed entirely with Terraform
- Modular structure for VPC, ECS, RDS, ALB, IAM, and more
- Parameterized for staging vs production flexibility

### CI/CD
- GitHub Actions pipeline builds and pushes images to ECR
- Deploys new tasks to ECS Fargate
- Syncs frontend to S3 and auto-invalidates CloudFront cache

### Observability
- Prometheus exposes backend metrics
- Grafana dashboards and alerts (WIP)
- CloudWatch handles logs and alarms

## Design Choices & Best Practices

- **Managed AWS Services:** Used RDS, ECS Fargate, and CloudFront to reduce operational overhead.
- **Security:** ALB access controlled via Security Groups; RDS is isolated in private subnets with restricted IP access.
- **Secrets Handling:** Environment variables used locally; production secrets stored in AWS Secrets Manager and ECS task definitions.
- **Terraform Structure:** Code split into logical modules with clean separation of concerns. Remote state (S3 + DynamoDB) can be added for production use.
- **CI/CD Reliability:** ECS circuit breakers and ALB health checks prevent faulty deployments from replacing healthy tasks.
- **Frontend Delivery:** CloudFront cache invalidation ensures users always see the latest build.
- **Cost Optimization:** Low-tier RDS instance, minimal logging, no autoscaling, and efficient use of subnets and ENIs.

---

This project demonstrates real-world infrastructure, observability, automation, and security practices using a modern AWS stack and is actively maintained.
