output "EC2_public_ip" {
  description = "Access EC2 instance"
  value       = aws_instance.app_server.public_ip
}

output "EC2_SSH" {
  value = "ssh -i dev-test-key.pem ubuntu@${aws_instance.app_server.public_ip}"
}

output "ECS_alb_dns_name" {
  description = "Access ECS - Application Load Balancer"
  value       = "http://${aws_lb.ecs_alb.dns_name}"
}

output "kubernetes_service_url" {
  description = "URL of the Kubernetes service"
  value       = "http://${try(data.kubernetes_service.app.status[0].load_balancer[0].ingress[0].hostname, "pending")}"
}

output "EKS_cluster_name" {
  description = "Kubernetes Cluster Name"
  value       = aws_eks_cluster.main.name
}

output "configure_kubectl" {
  description = "Configure kubectl command"
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${aws_eks_cluster.main.name}"
}

# output "cluster_id" {
#   description = "EKS cluster ID"
#   value       = aws_eks_cluster.main.id
# }

# output "cluster_endpoint" {
#   description = "Endpoint for EKS control plane"
#   value       = aws_eks_cluster.main.endpoint
# }

# output "cluster_certificate_authority_data" {
#   description = "Base64 encoded certificate data required to communicate with the cluster"
#   value       = aws_eks_cluster.main.certificate_authority[0].data
#   sensitive   = true
# }

# output "lightsail_public_ip" {
#   value = aws_lightsail_instance.dev_test_server.public_ip_address
# }

