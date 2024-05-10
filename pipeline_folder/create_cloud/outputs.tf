output "instance_public_ip" {
  description = "Public IP address of the RDS instance"
  value       = aws_db_instance.museum-db.address
}
