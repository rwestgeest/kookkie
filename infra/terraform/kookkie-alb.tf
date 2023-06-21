resource "aws_lb" "kookkie_load_balancer" {
  name               = "kookkie-load-balancer"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [ aws_security_group.allow_http_s_from_the_world_2.id ]
  subnets            = [ aws_subnet.subnet_1a.id, aws_subnet.subnet_1b.id, aws_subnet.subnet_1c.id ]

  enable_deletion_protection = true

  tags = {
    Environment = "production"
    Infra = "kookkie"
  }
}

resource "aws_lb_target_group" "kookkie_server" {
  name     = "kookkie-server"
  port     = 9090
  protocol = "HTTP"
  vpc_id   = aws_vpc.kookkie_vpc.id
  health_check {
    interval = 30
    path = "/api/version"
    matcher = "200"
  }

  tags = {
    Infra = "kookkie"
  }
}

resource "aws_lb_target_group_attachment" "kookkie_server" {
  target_group_arn = aws_lb_target_group.kookkie_server.arn
  target_id        = aws_instance.kookkie-production-server.id
}

resource "aws_lb_listener" "front_end_https" {
  load_balancer_arn = aws_lb.kookkie_load_balancer.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = "arn:aws:acm:eu-central-1:525595969507:certificate/2a35a931-b1ac-45ac-90ce-3e5d3695362d"

  default_action {
    type = "fixed-response"

    fixed_response {
      content_type = "text/plain"
      message_body = "Not found"
      status_code  = "404"
    }  
  }
}

resource "aws_lb_listener_rule" "forward_https_to_backend" {
  listener_arn = aws_lb_listener.front_end_https.arn
  priority = 100
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.kookkie_server.arn
  }

  condition {
    path_pattern {
      values = [
        # back end urls:
        "/api/*"
      ]
    }
  }
}

resource "aws_lb_listener_rule" "forward_https_to_frontend_0" {
  listener_arn = aws_lb_listener.front_end_https.arn
  priority = 95
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.kookkie_server.arn
  }

  condition {
    path_pattern {
      values = [
        # front end assets etc
        "/", "/assets/*", "/js/*", "/css/*"
      ]
    }
  }
}

resource "aws_lb_listener_rule" "forward_https_to_frontend_1" {
  listener_arn = aws_lb_listener.front_end_https.arn
  priority = 90
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.kookkie_server.arn
  }

  condition {
    path_pattern {
      values = [
        # front end urls, keep this in sync with the front end routes!
        "/admin", "/insights", "/profile", "/error"
      ]
    }
  }
}

resource "aws_lb_listener_rule" "forward_https_to_frontend_2" {
  listener_arn = aws_lb_listener.front_end_https.arn
  priority = 80
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.kookkie_server.arn
  }

  condition {
    path_pattern {
      values = [
        # front end urls, keep this in sync with the front end routes!
        "/request-password-reset", "/reset-password/*", "/signin",
        "/join/*", "/survey/*"
      ]
    }
  }
}

resource "aws_lb_listener_rule" "forward_https_to_frontend_3" {
  listener_arn = aws_lb_listener.front_end_https.arn
  priority = 70
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.kookkie_server.arn
  }

  condition {
    path_pattern {
      values = [
        # front end urls, keep this in sync with the front end routes!
        "/dashboard", "/diagnostic-session/*", "/rollup/*", "/terms-of-service", "/doc/*"
      ]
    }
  }
}

resource "aws_lb_listener_certificate" "qwan_eu_certificate" {
  listener_arn      = aws_lb_listener.front_end_https.arn
  certificate_arn   = "arn:aws:acm:eu-central-1:525595969507:certificate/c3c014f0-3910-4076-ab1a-af9ef12d2bbf"
}

resource "aws_lb_listener" "front_end_http" {
  load_balancer_arn = aws_lb.kookkie_load_balancer.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}
