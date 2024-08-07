provider "aws" {
  region = "us-east-1"
}

locals {
  public_key_path = "${path.module}/keys/${var.instance_name}-key.pub"
}

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