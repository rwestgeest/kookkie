
resource "aws_vpc" "kookkie_vpc" {

  cidr_block       = "172.31.0.0/16"
  instance_tenancy = "default"

  tags = {
    Infra = "kookkie"
    Name = "kookkie-vpc"
  }
}


resource "aws_internet_gateway" "kookkie_internet_gateway" {
  vpc_id = aws_vpc.kookkie_vpc.id

  tags = {
    Infra = "kookkie"
    Name = "kookkie-internet-gateway"
  }
}

resource "aws_route_table" "kookkie_route_table" {
  vpc_id = aws_vpc.kookkie_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.kookkie_internet_gateway.id
  }

  tags = {
    Infra = "kookkie"
    Name = "kookkie-route-table"
  }
}

resource "aws_main_route_table_association" "kookkie_route_table_association" {
  vpc_id         = aws_vpc.kookkie_vpc.id
  route_table_id = aws_route_table.kookkie_route_table.id
}

resource "aws_subnet" "subnet_1a" {
  vpc_id     = aws_vpc.kookkie_vpc.id
  cidr_block = "172.31.16.0/20"
  availability_zone = "eu-central-1a"

  tags = {
    Infra = "kookkie"
  }
}

resource "aws_subnet" "subnet_1b" {
  vpc_id     = aws_vpc.kookkie_vpc.id
  cidr_block = "172.31.32.0/20"
  availability_zone = "eu-central-1b"

  tags = {
    Infra = "kookkie"
  }
}

resource "aws_subnet" "subnet_1c" {
  vpc_id     = aws_vpc.kookkie_vpc.id
  cidr_block = "172.31.0.0/20"
  availability_zone = "eu-central-1c"

  tags = {
    Infra = "kookkie"
  }
}



resource "aws_security_group" "allow_http_s_from_the_world_2" {
  name        = "kookkie-allow-http-s-from-the-world"
  description = "Allow ingress port 443 & 80, egress port 9090"
  vpc_id      = aws_vpc.kookkie_vpc.id

  tags = {
    Infra = "kookkie"
  }
}

resource "aws_security_group_rule" "allow_http_s_from_the_world_in_443" {
  type = "ingress"
  from_port   = 443
  to_port     = 443
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
  security_group_id = aws_security_group.allow_http_s_from_the_world_2.id
}

resource "aws_security_group_rule" "allow_http_s_from_the_world_in_80" {

  type = "ingress"
  from_port   = 80
  to_port     = 80
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
  security_group_id = aws_security_group.allow_http_s_from_the_world_2.id
}

resource "aws_security_group_rule" "allow_http_s_from_the_world_egress" {
  type = "egress"
  from_port       = 9090
  to_port         = 9090
  protocol        = "tcp"
  security_group_id = aws_security_group.allow_http_s_from_the_world_2.id
  source_security_group_id = aws_security_group.allow_kookkie_incoming_traffic_2.id
}


resource "aws_security_group" "allow_kookkie_incoming_traffic_2" {
  name        = "kookkie-allow-server-traffic"
  description = "Allow ingress port 9090 from alb, ssh from world, egress anything"
  vpc_id      = aws_vpc.kookkie_vpc.id

  tags = {
    Infra = "kookkie"
  }
}

resource "aws_security_group_rule" "allow_kookkie_incoming_traffic_in_alb" {
  type = "ingress"
  from_port   = 9090
  to_port     = 9090
  protocol    = "tcp"
  security_group_id = aws_security_group.allow_kookkie_incoming_traffic_2.id
  source_security_group_id = aws_security_group.allow_http_s_from_the_world_2.id
}

resource "aws_security_group_rule" "allow_kookkie_incoming_traffic_in_ssh" {
  type = "ingress"
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
  security_group_id = aws_security_group.allow_kookkie_incoming_traffic_2.id
}

resource "aws_security_group_rule" "allow_kookkie_incoming_traffic_egress" {
  type = "egress"
  from_port       = 0
  to_port         = 0
  protocol        = "-1"
  cidr_blocks     = ["0.0.0.0/0"]
  security_group_id = aws_security_group.allow_kookkie_incoming_traffic_2.id
}
