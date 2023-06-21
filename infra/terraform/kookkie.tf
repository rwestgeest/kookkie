resource "aws_key_pair" "kookkie-machine" {
  key_name = "kookkie-machine"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDBAe9Ebm3UDaSWmoT2yYBMdP8oU46TwLK2//ynZzO10PkgSaYPE0XkB6bbN7xLIH+rw0KfbPua1c3pwwArr9lnmpG9H0iiK5txs1pRCEMZb+LZfvd5A/Civub9q1QBrJeRJufKq78qFzqnFFt1Sv3faP2OZxwYC7I92nW3w8dgYgHPDUa1EGe8FFD7YCkxWQjWZhfB2bhLYuhjXmNTQWfXq2H5in1VX4xK/ZKtNuGayAvEeOXlFtcS1AUTO6pfMmC1arIDX5RHHsWtKiil1Fsj2Bk1jTeIzvslwApyIqVbxrZevVdbzEJULfPVBr1hE6Y7Td+A/Po673c6TJFRfwPstpwYW+4c5ni9ivm7wwT0N14gLP4onUe5igL05IxQdyl3Lmi+3s7ZeTFApUNPP6ZsFODhzRMiBNmjLt7zRQOncwphKG+3Njcvy3Q3vfD201kW9jZ7qkd03elS6jRosqDEAcuIhqZ9BD2fr7dWdooPKNuiRBexx8dpVlDWRtv2a58= rob@blixa"
}

resource "aws_instance" "kookkie-production-server" {
  ami = "ami-04e601abe3e1a910f" # ubuntu 22.04
  associate_public_ip_address = true
  disable_api_termination = false
  ebs_optimized = false
  instance_type = "t3a.micro"
  key_name = "kookkie-machine"
  monitoring = false
  root_block_device {
    delete_on_termination = true
    volume_size = "50"
    volume_type = "gp2"
    encrypted = true
    tags = {
      Infra = "kookkie"
    }
  }
  subnet_id = aws_subnet.subnet_1a.id
  vpc_security_group_ids = [aws_security_group.allow_kookkie_incoming_traffic_2.id]
  source_dest_check = true
  tenancy = "default"
  iam_instance_profile = aws_iam_instance_profile.KookkieECRAccessForEC2.name

  connection {
    type        = "ssh"
    host        = self.public_ip
    user        = "ubuntu"
    private_key = file("~/.ssh/id_rsa_kookkie")
  }

  # provisioner "remote-exec" {
  #   scripts = [
  #     "install-docker.sh"
  #   ]
  # }
  tags = {
    Name = "kookkie-prd"
    Infra = "kookkie"
  }
}
