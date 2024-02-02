# Ray Serve Documentation

## Table of Contents

* [What is Ray?](#what-is-ray)
* [High level overview](#high-level-overview)
* [Ray Serve Introduction](#ray-serve-introduction)
*  [Configuring Ray Serve Deployments](#configuring-ray-serve-deployments)

## What is Ray?

Ray is an open source framework that comprises libraries to handle common machine learning tasks such as distributed training and hyperparameter tuning, distributed computing components for data intensive applications and integration with cloud platforms and cluster managers(YARN,k8s) for deployment.


## High level overview

Ray framework is made up of:


* **Ray AI libraries** - These libraries are useful to scale individual tasks and entire ML applications.They are made up of five subcategories: Data,Train,Tune,Serve and RLib.
* **Ray Core** - These offer a simple way to build scalable distributed systems.This library helps in the development of RAY AI libraries and third-party integrations within the RAY ecosystem.
* **Ray Clusters** - These are used to deploy workloads on AWS,GCP,Azure. It boasts a rich ecosystem of integrations with an array of tools, including Dask, HuggingFace, ScikitLearn, and beyond.

Now we will learn more in depth about Ray Serve.


## Ray Serve Introduction


1. Deployment - A deployment contains business logic or an ML model to handle incoming requests and can be scaled up to run across a Ray cluster. At runtime, a deployment consists of a number of _replicas. _
2. Application - made of 1 or more deployments.
3. DeploymentHandle - Ray Serve enables flexible model composition and scaling by allowing multiple independent deployments to call into each other. When binding a deployment, you can include references to _other bound deployments_. Then, at runtime each of these arguments is converted to a DeploymentHandle.
4. IngressDeployment - Serves as entrypoint for all traffic to application. It is passed into `serve.run` to deploy the application. It defines the HTTP handling logic for the application.

##  Configuring Ray Serve Deployments

Deploying a serve application using kuberay requires the below serve config to be created.

```yaml
proxy_location: ...

http_options:
    host: ...
    port: ...
    request_timeout_s: ...
    keep_alive_timeout_s: ...

grpc_options:
    port: ...
    grpc_servicer_functions: ...

logging_config:
    log_level: ...
    logs_dir: ...
    encoding: ...
    enable_access_log: ...

applications:
    - name: ...
    route_prefix: ...
    import_path: ...
    runtime_env: ...
    deployments:
    - name: ...
        num_replicas: ...
        ...
    - name:
        ...

```

* `name` - Name to uniquely identify deployment
* `num_replicas` - Number of replicas to run that handle requests to this deployment. Defaults to 1.
* `ray_actor_options` - Options to pass to Ray Actor decorator such as `accelerator_type`,`memory`,`num_cpus`,`num_gpus`
* `max_concurrent_queries` - Maximum number of queries that are sent to replica deployment without receiving response.Default value is 100.
* `autoscaling_config` - If set,you cannot set num_replicas. Deployment can be configured to autoscale based on incoming traffic. This is more complex than manually increasing replicas which is done by setting `num_replicas`.
* `user_config` - Supply structured configuration for deployment by passing JSON serializable objects to YAML config.Serve applies it to all replicas.You can now dynamically adjust model weights, versions without restarting the cluster.
* `health_check_period_s` - Duration between health check calls for the replica. Defaults to 10s.
* `health-check_timeout_s - Duration in seconds, that replicas wait for a health check method to return before considering it as failed. Defaults to 30s.
* `graceful_shutdown_wait_loop_s` - Duration that replicas wait until there is no more work to be done before shutting down. Defaults to 2s.
* `graceful_shutdown_timeout_s`- Duration to wait for a replica to gracefully shut down before being forcefully killed. Defaults to 20s.
* `logging_config` - Logging config for deployment

For more details on configuring ray serve application refer [Ray Serve Config File](https://docs.ray.io/en/latest/serve/production-guide/config.html)
