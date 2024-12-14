# AI-Powered Fantasy Premier League Optimization Platform

## Overview

This platform is a solution designed to empower Fantasy Premier League (FPL) players with data-driven insights and intelligent team management strategies. By leveraging machine learning and advanced analytics, the platform helps managers make optimal decisions to maximize their team's performance.

## Project Description

In the world of Fantasy Premier League, managers face complex challenges:
- Limited budget for player acquisition
- Restrictions on team composition
- Weekly transfer constraints
- Performance variability of players

Our platform addresses these challenges by:
- Predicting the best lineup using advanced machine learning algorithms
- Analyzing key performance indicators
- Providing strategic transfer recommendations
- Ensuring a responsive and scalable user experience

### Key Features

- **Intelligent Lineup Optimization**: Predict the most effective team of the gameweek based on:
  - Player form
  - Match difficulty
  - Performance metrics
- **Smart Transfer Recommendations**: 
  - Input current team
  - Receive optimal transfer suggestions
  - Maximize potential points for upcoming gameweek
- **Scalable Microservices Architecture**: 
  - Robust infrastructure
  - High availability
  - Responsive under varying user loads

## Prerequisites

### System Requirements
- Docker Desktop
- Kubernetes support
- Google Cloud Platform account

### Installation

1. **Create GCP account and connect to it**

2. **Create a GKE cluster in GCP**
     Make sure that Workload Identity is enabled when creating the cluster.

3. **Create a Google and Kubernete Service Accounts**
     ```bash
     # Create K8 service account
     kubectl create serviceaccount my-app-service-account
     # Create google service account
     gcloud iam service-accounts create my-app-service-account \
    --display-name "Service account for GKE"
     # Grant permissions
     gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member "serviceAccount:my-app-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role "roles/storage.objectViewer"
     # Link K8 service account with google service account
     kubectl annotate serviceaccount my-app-service-account \
    iam.gke.io/gcp-service-account=my-app-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com
      
     ```
   
4. **Clone this repo**\
   
5. **Replace the service account with your own**
     Replace the service account name given in cronjob/pushpreds-cronjob.yaml with your own.

6. **Deploy Application**
   ```bash
   # Use deployment script
   ./deploy.sh
   ```

7. **Get external IP of frontend-service**
     ```bash
     # Use deployment script
     kubectl get svc
     ```
     Copy and paste the external IP in your browser to open the web-app

8. **Connect to the web-app**
   ```bash
   # Get frontend External IP
   kubectl get svc
   ```
   Copy and paste the external IP of frontend-service to the browser to connect to the app.

## Technology Stack

### Backend
- **Framework**: Flask (RPC/API interfaces)
- **Databases**: PostgreSQL
- **Caching**: Redis

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Kubernetes (Google Kubernetes Engine)
- **Scheduled Jobs**: Kubernetes CronJob
- **Storage**: Google Cloud Storage

## Usage

1. Initialize the platform
2. Input your current FPL team
3. Receive data-driven recommendations
4. Implement suggested transfers
5. Track performance improvements

## Author

**Mukund Mahesan**

## Disclaimer

This platform provides recommendations based on data analysis and machine learning predictions. While striving for accuracy, actual performance may vary. Always use your judgment when making final decisions.
