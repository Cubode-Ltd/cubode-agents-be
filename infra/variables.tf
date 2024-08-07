variable "instance_name" {
  description = "Name of the EC2 instance"
  type        = string
  default     = "graph-cubode"
}

variable "instance_type" {
  description = "Type of EC2 instance"
  type        = string
  default     = "t2.medium"
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  type        = string
  default     = "ami-00874d747dde814fa"
}

variable "git_username" {
  description = "The Git username"
  type        = string
}

variable "git_email" {
  description = "The Git email address"
  type        = string
}