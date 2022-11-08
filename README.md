# gc-flipr-calculator

### BlockFrost gc flipr calculator

this small project based on csv and pandas search for minimalization of blockfrost requests

> build project: ```docker build .```
>
>run locally: ```docker run -e BF_API_KEY=****** --network host -it $(docker build -q .)```
>
>run on k8s: ```kubectl apply -f k8s/deployment.yaml``` example for DigitalOcean (requires: cert-manager/nginx-ingress)
>