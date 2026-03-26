provider "aws" {
  region = "us-east-1"
}

resource "aws_security_group" "bad_sg" {
  name        = "allow_all_ssh"
  description = "Allow SSH from anywhere"

  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
