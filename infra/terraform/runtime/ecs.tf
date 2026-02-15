resource "aws_ecs_cluster" "this" {
    name = "${local.name_prefix}-cluster"
}

resource "aws_ecs_task_definition" "app" {
    family                   = "${local.name_prefix}-task"
    network_mode             = "awsvpc"
    requires_compatibilities = ["FARGATE"]
    cpu                      = var.task_cpu
    memory                   = var.task_memory
    execution_role_arn       = aws_iam_role.task_execution.arn

    container_definitions = jsonencode([
        {
            name      = "app"
            image     = var.container_image
            essential = true

            portMappings = [
              { containerPort = var.container_port, hostPort = var.container_port, protocol = "tcp" }
            ]
            logConfiguration = {
                logDriver = "awslogs"
                options   = {
                    "awslogs-group"         = aws_cloudwatch_log_group.app.name
                    "awslogs-region"        = var.aws_region
                    "awslogs-stream-prefix"= "app"
                }
            }
        }
    ])
}

resource "aws_ecs_service" "app" {
  name            = "${local.name_prefix}-service"
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [for s in aws_subnet.public : s.id]
    security_groups  = [aws_security_group.services.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "app"
    container_port   = var.container_port
  }

  depends_on = [aws_lb_listener.http]
}