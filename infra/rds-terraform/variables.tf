variable "db_name" {
  default = "splitclone"
}

variable "username" {
  default = "splitcloneuser"
}

variable "password" {
  default = "your-secure-password"
}

variable "subnet_ids" {
  description = "Subnets to use for RDS DB subnet group"
  type        = list(string)
}
