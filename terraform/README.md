# Infrastructure as Code

Instead of clicking around in the cloud in a non-repeatable and (sometimes) confusing way, store your cloud configuration as code.

This brings all the benefits of code (versioning, sharing, updating) to the cloud.

## Credentials

If you want to work with AWS resources through code, you need [credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/security-creds.html) with that power.

## Terraform

Terraform is **declarative**.

- Describe exactly what cloud resources you want
- Build them automatically
- Destroy them automatically
- Share your configuration easily with other people

This is a configuration tool, not a language.

## Documentation

- [Terraform docs](https://developer.hashicorp.com/terraform/docs)
- [Terraform AWS resources docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

### Setup

- Create a `main.tf` file
- Add a `provider` block with AWS config details
- Run `terraform init` to get the folder set up for terraforming
- Run `terraform plan` to see what your config would build
- Run `terraform apply` to actually build your infrastructure
- Run `terraform destroy` to shut down and clean up all resources

## Basic database config

```s
resource "aws_db_instance" "museum-db" {
    allocated_storage            = 10
    db_name                      = ""
    identifier                   = ""
    engine                       = "postgres"
    engine_version               = "16.1"
    instance_class               = "db.t3.micro"
    publicly_accessible          = true
    performance_insights_enabled = false
    skip_final_snapshot          = true
    db_subnet_group_name         = ""
    vpc_security_group_ids       = []
    username                     = ""
    password                     = ""
}
```

## Configuration

Create a `Terraform.tfvars` file and populate it with the following:

```bash
DATABASE_USERNAME=your_username
DATABASE_PASSWORD=your_password
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
```