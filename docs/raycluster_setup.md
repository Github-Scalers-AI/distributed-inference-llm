# KubeRay Installation and Ray Cluster Configuration

**Estimated Time: 40 mins ⏱️**


In this section, we will be streamlining the integration of KubeRay and will configure our Ray Clusters for inferencing.

## Table of Contents

* [KubeRay Installation](#kuberay-installation)
* [Creating Kubernetes Secrets](#creating-image-pull-secret-for-kubernetes)
* [Our Test Cluster for Llama 2 70B Inferencing](#our-test-cluster-for-llama-2-70b-inferencing)


## KubeRay Installation

Follow the below steps to deploy the [KubeRay Operator v1.0.0](https://docs.ray.io/en/latest/cluster/kubernetes/index.html) on your k3s cluster.

1. Add the kuberay repo to helm.

    ```sh
    helm repo add kuberay https://ray-project.github.io/kuberay-helm/
    helm repo update
    ```
2. Install both CRDs and KubeRay operator v1.0.0.

    ```sh
    helm install kuberay-operator kuberay/kuberay-operator --version 1.0.0
    ```
3. Verify the kuberay operator pod deployment.

    ```sh
    kubectl get pods
    ```

    You should see an output similar to this.

    ```sh
    NAME                                READY   STATUS    RESTARTS   AGE
    kuberay-operator-7fbdbf8c89-pt8bk   1/1     Running   0          27s
    ```


## Creating Image Pull Secret for Kubernetes

> *Note: This step may vary based on different container registries.*

The Image Pull Secret should be created for the cluster to pull images from the Azure container registry.

1. Collect the below details from your container registry

    | Name | Details | Example |
    | --- | --- | --- |
    | `CR Server` | Container registry server URI. | `infer.cr.io` |
    | `CR User Name` | Container registry user name | `user` |
    | `CR Password` | Container registry password | `password123` |

2. Create the secret on your k3s cluster.

    ```sh
    kubectl create secret docker-registry cr-login --docker-server=<CR Server> --docker-username=<CR User Name> --docker-password=<CR Password>
    ```

## Our Test Cluster for Llama 2 70B Inferencing

Below are the details of the cluster we configured for inferencing the Llama 2 70B LLM model.

| Server Name | CPU | RAM | Disk | GPUs |
| -- | -- | -- | -- | -- |
| [Dell PowerEdge XE9680](https://www.dell.com/en-in/work/shop/ipovw/poweredge-xe9680) | Intel(R) Xeon(R) Platinum 8480+ <br> 56 Cores <br> 2 Sockets | 2 TB | 3 TB | 8x[NVIDIA A100 80 GB SXM](https://www.nvidia.com/en-in/data-center/a100/) GPUs |
| [Dell PowerEdge XE8545](https://www.dell.com/en-us/shop/ipovw/poweredge-xe8545) | AMD EPYC 7763 64-Core Processor <br> 64 Cores <br> 2 Sockets | 1 TB | 2 TB | 4x[NVIDIA A100 80 GB SXM](https://www.nvidia.com/en-in/data-center/a100/) GPUs |
| [Dell PowerEdge R760xa](https://www.dell.com/en-us/shop/dell-poweredge-servers/poweredge-r760xa-rack-server/spd/poweredge-r760xa/pe_r760xa_16902_vi_vp) | Intel(R) Xeon(R) Platinum 8480+ <br> 56 Cores <br> 2 Sockets | 1 TB | 1 TB | 4x[NVIDIA H100 80 GB PCIe](https://www.nvidia.com/en-in/data-center/h100/) GPUs |

Each server is networked to an Dell PowerSwitch Z9664F-ON through Broadcom BCM57508 NICs with 100 Gb/s bandwidth.

[Back to Detailed setup guide](../README.md#detailed-set-up-guide)
