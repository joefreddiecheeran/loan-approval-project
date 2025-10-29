provider "aws" {
  region = "ap-south-1"
}

resource "aws_key_pair" "dev_key" {
  key_name   = "dev-key"
  public_key = file("C:/Users/joefr/.ssh/id_rsa.pub")
}

resource "aws_security_group" "flask_sg" {
  name_prefix = "flask-sg-"

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
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

resource "aws_instance" "flask_vm" {
  ami                    = "ami-087d1c9a513324697"
  instance_type          = "t3.micro"
  key_name               = aws_key_pair.dev_key.key_name
  vpc_security_group_ids = [aws_security_group.flask_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              sudo apt update -y
              sudo apt install python3-pip git -y
              pip install flask pandas scikit-learn joblib
              cd /home/ubuntu
              git clone https://github.com/joefreddiecheeran/loan-approval-project.git
              cd loan-approval-project/app
              python3 model.py
              nohup python3 app.py &
              EOF

  tags = {
    Name = "LoanApprovalApp"
  }
}