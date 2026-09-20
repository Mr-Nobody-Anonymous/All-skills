# 🐳 Docker & Kubernetes Cheatsheet

```bash
# Docker Operations
docker build -t my-app:latest .             # Build image from Dockerfile
docker run -d -p 8080:80 --name web my-app  # Run detached container
docker exec -it web /bin/sh                 # Open interactive shell in container
docker logs -f --tail 100 web               # Follow last 100 log lines
docker system prune -af --volumes           # Remove all unused containers/images

# Kubernetes (kubectl)
kubectl get pods -A -o wide                 # List all pods in all namespaces
kubectl describe pod <pod-name>             # Inspect events and status of pod
kubectl logs -f <pod-name> -c <container>   # Stream container logs
kubectl exec -it <pod-name> -- /bin/bash    # Exec into running pod
kubectl apply -f deployment.yaml            # Apply declarative manifest
kubectl rollout restart deployment/<name>   # Gracefully restart deployment pods
```
