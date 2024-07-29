provider "aws" {
    region = var.AWS_REGION
    access_key = var.AWS_ACCESS_KEY
    secret_key = var.AWS_SECRET_KEY
}

resource "aws_instance" "c11-faris-kafka" {
  ami           = "ami-008ea0202116dbc56"
  instance_type = "t2.nano"           
  tags = {
    Name = "C11-Faris_Kafka"
  }
  key_name = "C11-FarisA-SigmaKey"
}

resource "aws_db_instance" "museum-db" {
    allocated_storage            = 10
    db_name                      = "museum"
    identifier                   = "c11-faris-museum-db"
    engine                       = "postgres"
    engine_version               = "16.1"
    instance_class               = "db.t3.micro"
    publicly_accessible          = true
    performance_insights_enabled = false
    skip_final_snapshot          = true
    db_subnet_group_name         = "public_subnet_group_11"
    vpc_security_group_ids       = [aws_security_group.db-security-group.id]
    username                     = var.DATABASE_USERNAME
    password                     = var.DATABASE_PASSWORD
}

resource "aws_security_group" "db-security-group" {
    name = "c11-faris-db-sg"
    vpc_id = data.aws_vpc.c11-vpc.id
    
    egress {
        from_port        = 0
        to_port          = 0
        protocol         = "-1"
        cidr_blocks      = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 5432
        to_port = 5432
        protocol = "tcp"
        cidr_blocks      = ["0.0.0.0/0"]
    }
}

data "aws_vpc" "c11-vpc" {
    id = "vpc-02112f9747d891585"
}