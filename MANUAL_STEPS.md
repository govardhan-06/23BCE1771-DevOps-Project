# Manual Steps You Must Perform

The project files, configurations, dashboard, and report template are already prepared. The following actions need access to your own GitHub account, Docker Desktop, Jenkins UI, and local Kubernetes, so you must perform them and capture screenshots.

## 1. Create and push the GitHub repository

```bash
cd 23BCE1771_DevOps_Project
git init
git add .
git commit -m "Complete DevOps Assignment 2 portfolio project"
git branch -M main
git remote add origin https://github.com/govardhan-06/23BCE1771-DevOps-Project.git
git push -u origin main
```

Create the empty repository named **23BCE1771-DevOps-Project** on GitHub before the last two commands.

Capture:
- Repository home page showing the files.
- Commit history page.

## 2. Run the Maven build and local Docker application

```bash
mvn clean package
docker build -t 23bce1771-devops-project:1.0 .
docker run -d --name portfolio-local -p 8080:80 23bce1771-devops-project:1.0
```

Open `http://localhost:8080` and capture:
- Successful Maven terminal output.
- Docker image list: `docker images`.
- Running container: `docker ps`.
- Website in the browser.

## 3. Configure Jenkins

Start the prepared Jenkins container:

```bash
docker compose -f jenkins/docker-compose.yml up --build -d
docker exec devops-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Open `http://localhost:8085`.

In the Jenkins setup wizard:
1. Enter the initial password.
2. Install Suggested Plugins.
3. Create an admin user.
4. Install **Pipeline** and **Git** plugins if not already installed.
5. Select **New Item** -> **Pipeline**.
6. Name: `23BCE1771-DevOps-Portfolio`.
7. Under Pipeline, choose **Pipeline script from SCM**.
8. SCM: Git.
9. Repository URL: `https://github.com/govardhan-06/23BCE1771-DevOps-Project.git`.
10. Branch: `*/main`.
11. Script Path: `Jenkinsfile`.
12. Save and click **Build Now**.

The pipeline deploys its own container at `http://localhost:8090` to avoid conflicting with the monitoring stack.

Capture:
- Jenkins dashboard.
- Job configuration showing Git and Jenkinsfile.
- Stage view / successful green build.
- Console output containing Maven Build, Docker Build, Automated Docker Deployment, and Health Check.

## 4. Deploy to Kubernetes

Enable Kubernetes in Docker Desktop, or start Minikube.

```bash
./scripts/deploy-kubernetes.sh
kubectl get deployments
kubectl get pods -o wide
kubectl get services
```

For Docker Desktop, open `http://localhost:30080`.
For Minikube, run:

```bash
minikube service portfolio-service --url
```

Capture:
- `kubectl get deployments`.
- Two Pods in Running state.
- NodePort Service.
- Browser output through the Kubernetes URL.

## 5. Start Graphite, Grafana, Nagios, and the metrics agent

If a separate container is already using port 8080, remove it first:

```bash
docker rm -f portfolio-local 2>/dev/null || true
./scripts/start-monitoring.sh
```

On Apple Silicon Macs, the Graphite and Nagios images may run through Docker emulation, so the first startup can take a few minutes.

Wait 1-3 minutes, then open:
- Portfolio: `http://localhost:8080`
- Graphite: `http://localhost:8081`
- Grafana: `http://localhost:3000` (`admin` / `admin`)
- Nagios: `http://localhost:8082/nagios/` (`nagiosadmin` / `nagios`)

Grafana is pre-provisioned. Open:
**Dashboards -> DevOps Assignment 2 -> Online Portfolio - System Health**

Capture:
- Graphite tree/graph showing `portfolio.*` metrics.
- Grafana dashboard showing CPU, memory, disk, network, HTTP availability, response time, and uptime.
- Nagios Hosts page showing `portfolio-app` as UP.
- Nagios Services page showing `HTTP Service` as OK.

Useful checks:

```bash
docker compose -f monitoring/docker-compose.yml ps
docker logs devops-metrics-agent --tail 20
```

## 6. Complete the report

Open `23BCE1771_Govardhan_AR_DevOps_Report.docx` and replace each grey screenshot box with the corresponding screenshot. Update the first-page links if your final URLs differ. Export it as:

`23BCE1771_Govardhan_AR_DevOps_Report.pdf`

## 7. Final submission files

- `23BCE1771_Govardhan_AR_DevOps_Project.zip`
- `23BCE1771_Govardhan_AR_DevOps_Report.pdf`
- GitHub repository link
- All screenshots included inside the report
