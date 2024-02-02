
# Ray Service

## Table of Contents
* [Background](#background)
* [High level features of RayService](#high-level-features-of-rayservice)



## Background

KubeRay is a robust open-source Kubernetes operator designed to facilitate the deployment and management of Ray applications on Kubernetes clusters. It seamlessly combines the user-friendly and Pythonic experience of Ray with the scalability and reliability of Kubernetes.

Within KubeRay, a Ray cluster is composed of a head node pod and a set of worker node pods. The operator offers optional autoscaling capabilities, enabling dynamic adjustment of Ray cluster sizes based on workload requirements. KubeRay supports heterogeneous compute nodes, including GPUs, and allows the concurrent execution of multiple Ray clusters with varying Ray versions within the same Kubernetes cluster.

The core of KubeRay consists of three Kubernetes Custom Resource Definitions (CRDs):

1. **RayCluster**:This CRD enables KubeRay to fully manage the lifecycle of a RayCluster. It automates tasks such as cluster creation, deletion, autoscaling, and ensures fault tolerance.

2. **RayJob**: KubeRay streamlines job submission by automatically creating a RayCluster when needed. Users can configure RayJob to initiate job deletion once the task is completed, enhancing operational efficiency.

3. **RayService**: Comprising of a RayCluster and Ray Serve deployment graphs, RayService facilitates zero-downtime upgrades for RayCluster and ensures high availability.


## High level features of RayService

1. RayService is responsible for:

   * RayCluster- takes charge of efficiently managing resources within a Kubernetes cluster.
   * Ray Serve Applications- responsible for managing users' applications deployed on Ray Serve.

2. Kubernetes-native Support - RayService leverages Kubernetes as its native environment, aligning with Kubernetes principles and conventions. Following configuration setup, users can utilize the familiar `kubectl` command-line tool to create and manage both Ray clusters and Ray Serve applications on the Kubernetes cluster.
3. In-Place Updates for Ray Serve Applications - Users can effortlessly update Ray Serve configurations within the RayService CR config. Leveraging `kubectl apply`, users can easily apply these changes, ensuring updates to Ray Serve applications.
4. Zero Downtime Upgrades for Ray Clusters - Users can update Ray cluster configurations within the RayService CR config. Utilizing `kubectl apply`, users trigger the update process, prompting RayService to create a pending cluster.Once the new cluster is ready, RayService intelligently redirects traffic to the updated cluster, seamlessly transitioning without downtime.

Refer the [Ray Service](https://docs.ray.io/en/latest/cluster/kubernetes/getting-started/rayservice-quick-start.html) documentation for more information.
