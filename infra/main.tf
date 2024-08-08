provider "aws" {
  region = "us-east-1"
}

# --- 0. Steps 
# 1. Create the S3 Bucket and Permissions
# 2. Create the Policy, Group and User for S3 / EC2
# 3. Create the EC2 with Security Group 80, 443 and 22
# 4. Create the CloudFront and link to S3.



# --- 1. Create S3 Bucket
resource "aws_s3_bucket" "graph_cubode_static_bucket" {
  bucket = "${var.instance_name}-static-bucket"
  tags = {
    Name        = "${var.instance_name}-static-bucket"
    Environment = "production"
  }
}

resource "aws_s3_bucket_versioning" "graph_cubode_static_bucket_versioning" {
  bucket = aws_s3_bucket.graph_cubode_static_bucket.bucket

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_cors_configuration" "graph_cubode_static_bucket_cors" {
  bucket = aws_s3_bucket.graph_cubode_static_bucket.bucket

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = ["*"]
    max_age_seconds = 3000
  }
}


# --- 2.- Policy, Group and User
resource "aws_iam_policy" "s3_ec2_access_policy" {
  name        = "s3-ec2-access-policy"
  description = "Policy granting access to S3 and EC2"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:ListBucket",
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ],
        Resource = [
          "arn:aws:s3:::${var.instance_name}-static-bucket",
          "arn:aws:s3:::${var.instance_name}-static-bucket/*"
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "ec2:DescribeInstances",
          "ec2:StartInstances",
          "ec2:StopInstances"
        ],
        Resource = "*"
      }
    ]
  })
}

# Create an IAM group and attach the policy
resource "aws_iam_group" "s3_ec2_access_group" {
  name = "s3-ec2-access-group"
}

resource "aws_iam_group_policy_attachment" "s3_ec2_policy_attachment" {
  group      = aws_iam_group.s3_ec2_access_group.name
  policy_arn = aws_iam_policy.s3_ec2_access_policy.arn
}

# Create an IAM user and attach the user to the group
resource "aws_iam_user" "s3_ec2_user" {
  name = "s3-ec2-user"
}

resource "aws_iam_user_group_membership" "s3_ec2_user_membership" {
  user = aws_iam_user.s3_ec2_user.name
  groups = [aws_iam_group.s3_ec2_access_group.name]
}

# Create an IAM role that EC2 instances can assume
resource "aws_iam_role" "graph_cubode_s3_access_role" {
  name = "${var.instance_name}_s3_access_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# Attach the S3 and EC2 access policy to the IAM role
resource "aws_iam_role_policy_attachment" "s3_ec2_role_policy_attachment" {
  role       = aws_iam_role.graph_cubode_s3_access_role.name
  policy_arn = aws_iam_policy.s3_ec2_access_policy.arn
}

# Create an instance profile to link the IAM role to the EC2 instance
resource "aws_iam_instance_profile" "graph_cubode_s3_access_profile" {
  name = "${var.instance_name}_s3_access_profile"
  role = aws_iam_role.graph_cubode_s3_access_role.name
}

# --- 3.- EC2
resource "aws_key_pair" "graph_cubode_key" {
  key_name   = "${var.instance_name}-key"
  public_key = file("${path.module}/keys/${var.instance_name}-key.pub")
}

resource "aws_instance" "graph-cubode" {
  ami           = "ami-00874d747dde814fa"
  instance_type = "t2.medium"

  # EC2 key pair for SSH access - same name as defined above.
  key_name = aws_key_pair.graph_cubode_key.key_name

  # Security group with SSH access
  vpc_security_group_ids = [aws_security_group.allow_ssh_and_web.id]

  iam_instance_profile = aws_iam_instance_profile.graph_cubode_s3_access_profile.name

  # User data script for installing Docker, Git, and configuring the environment
  user_data = <<-EOF
    #!/bin/bash
    # Export Git credentials as environment variables # Defined both in variables.tf
    export GIT_USERNAME="${var.git_username}"
    export GIT_EMAIL="${var.git_email}"

    # Docker installation
    sudo apt-get update
    sudo apt-get -y install ca-certificates curl gnupg lsb-release
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get -y update
    sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin docker-compose
    sudo groupadd -f docker
    sudo usermod -aG docker $USER
    newgrp docker

    # Git installation and configuration
    sudo apt-get -y install git
    git config --global user.name "$GIT_USERNAME"
    git config --global user.email "$GIT_EMAIL"
  EOF

  tags = {
    Name = var.instance_name
  }
}

resource "aws_security_group" "allow_ssh_and_web" {
  name        = "allow_ssh_and_web"
  description = "Allow SSH, HTTP, and HTTPS inbound traffic"
  
  # Allow SSH
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow HTTP
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow HTTPS
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# --- 4. - CloudFront and S3 Policy change
resource "aws_cloudfront_origin_access_identity" "graph_cubode_oai" {
  comment = "${var.instance_name} OAI for S3 bucket"
}

resource "aws_cloudfront_distribution" "graph_cubode_distribution" {
  origin {
    domain_name = aws_s3_bucket.graph_cubode_static_bucket.bucket_regional_domain_name
    origin_id   = "${var.instance_name}-s3-origin"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.graph_cubode_oai.cloudfront_access_identity_path
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "CloudFront distribution for ${var.instance_name} static content"
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "${var.instance_name}-s3-origin"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 86400
    max_ttl                = 31536000
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  tags = {
    Name = "${var.instance_name}-cloudfront-distribution"
  }
}

# Update S3 Bucket Policy to Allow CloudFront OAI Access
resource "aws_s3_bucket_policy" "graph_cubode_bucket_policy" {
  bucket = aws_s3_bucket.graph_cubode_static_bucket.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          AWS = aws_cloudfront_origin_access_identity.graph_cubode_oai.iam_arn
        },
        Action   = "s3:GetObject",
        Resource = "${aws_s3_bucket.graph_cubode_static_bucket.arn}/*"
      }
    ]
  })
}

# --- 5. Outputs
# S3 Bucket Name
output "s3_bucket_name" {
  value = aws_s3_bucket.graph_cubode_static_bucket.bucket
}

# CloudFront Domain Name
output "cloudfront_domain_name" {
  value = aws_cloudfront_distribution.graph_cubode_distribution.domain_name
}

# IAM Instance Profile Name (if needed)
output "iam_instance_profile_name" {
  value = aws_iam_instance_profile.graph_cubode_s3_access_profile.name
}

# CloudFront Origin Access Identity
output "cloudfront_oai" {
  value = aws_cloudfront_origin_access_identity.graph_cubode_oai.cloudfront_access_identity_path
}

# CloudFront Origin Access Identity ARN (if needed)
output "cloudfront_oai_arn" {
  value = aws_cloudfront_origin_access_identity.graph_cubode_oai.iam_arn
}
