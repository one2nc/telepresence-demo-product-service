allow_k8s_contexts('arn:aws:eks:ap-south-1:987204596461:cluster/telepresence-demo')

load('ext://restart_process', 'docker_build_with_restart')

def deploy_helm():
    yaml = helm(
        "./k8s/helm/local",
        name="products-svc",
        values=["./k8s/helm/local.values.yaml"],
        namespace="api"
    )
    k8s_yaml(yaml)
    k8s_resource(workload="products-svc-local", port_forwards=["8080:8080"])

def deploy_k8s():
    k8s_yaml(yaml="k8s/local/deploy.yaml")
    k8s_resource(workload="product-svc", port_forwards=["8080:8080"])

def deploy():
    K8S_DEPLOY_MODE = os.getenv("K8S_DEPLOY_MODE", "helm")
    _modes = {
        "helm": deploy_helm, 
        "k8s": deploy_k8s
    }
    func = _modes[K8S_DEPLOY_MODE]
    func()

default_registry("ttl.sh")
docker_build_with_restart("ttl.sh/telepresence-demo-product-svc:2h", ".", entrypoint="uvicorn app:app --host 0.0.0.0 --port 8080", live_update=[sync("./src", "/app"), sync("./requirements.txt", "/app/requirements.txt")])
deploy()