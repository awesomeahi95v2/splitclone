resource "aws_db_instance" "splitclone_db" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "16.9"
  instance_class       = "db.t3.micro"
  identifier           = "splitclone-db"
  username             = var.username
  password             = var.password
  db_name              = var.db_name
  db_subnet_group_name = aws_db_subnet_group.splitclone.name
  publicly_accessible  = true
  skip_final_snapshot  = true
  backup_retention_period = 0
}
resource "aws_db_subnet_group" "splitclone" {
  name       = "splitclone-subnet-group"
  subnet_ids = var.subnet_ids

  tags = {
    Name = "splitclone-subnet-group"
  }
}
