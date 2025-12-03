provider "kubernetes" {
  host                   = aws_eks_cluster.main.endpoint
  cluster_ca_certificate = base64decode(aws_eks_cluster.main.certificate_authority[0].data)
  
  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    args = [
      "eks",
      "get-token",
      "--cluster-name",
      aws_eks_cluster.main.name,
      "--region",
      var.aws_region
    ]
  }
}

# Kubernetes Deployment
resource "kubernetes_deployment" "app" {
  depends_on = [aws_eks_node_group.main]

  metadata {
    name = "portcicd-deployment"
    labels = {
      app = "portcicd"
    }
  }

  spec {
    replicas = 3

    selector {
      match_labels = {
        app = "portcicd"
      }
    }

    template {
      metadata {
        labels = {
          app = "portcicd"
        }
      }

      spec {
        container {
          name  = "portcicd"
          image = "public.ecr.aws/m1y0v6d8/portcicd"

          port {
            container_port = 80
          }

          resources {
            requests = {
              cpu    = "100m"
              memory = "128Mi"
            }
            limits = {
              cpu    = "250m"
              memory = "256Mi"
            }
          }

          liveness_probe {
            http_get {
              path = "/"
              port = 80
            }
            initial_delay_seconds = 30
            period_seconds        = 10
          }

          readiness_probe {
            http_get {
              path = "/"
              port = 80
            }
            initial_delay_seconds = 5
            period_seconds        = 5
          }
        }
      }
    }
  }
}

# Kubernetes Service (LoadBalancer)
resource "kubernetes_service" "app" {
  depends_on = [kubernetes_deployment.app]

  metadata {
    name = "portcicd-service"
  }

  spec {
    selector = {
      app = "portcicd"
    }

    port {
      port        = 80
      target_port = 80
      protocol    = "TCP"
    }

    type = "LoadBalancer"
  }
}

# Data source to get the LoadBalancer URL
data "kubernetes_service" "app" {
  depends_on = [kubernetes_service.app]

  metadata {
    name = kubernetes_service.app.metadata[0].name
  }
}