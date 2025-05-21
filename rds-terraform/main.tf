resource "aws_db_instance" "splitclone_db" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "16.9"
  instance_class       = "db.t3.micro"
  identifier           = "splitclone-db"
  username             = var.username
  password             = var.password
  db_name              = var.db_name
  publicly_accessible  = true
  skip_final_snapshot  = true
  backup_retention_period = 0
}
