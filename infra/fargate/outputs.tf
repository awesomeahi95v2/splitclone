output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = aws_ecs_cluster.this.name
}

output "service_name" {
  description = "ECS service name"
  value       = aws_ecs_service.app.name
}

output "load_balancer_dns" {
  description = "Public URL of the ALB"
  value       = aws_lb.this.dns_name
}
