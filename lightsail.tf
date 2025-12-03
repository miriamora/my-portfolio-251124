

# resource "aws_lightsail_instance" "dev_test_server" {
#   name              = "dev_test_server"
#   availability_zone = "us-east-1a"
#   blueprint_id      = "ubuntu_22_04"
#   bundle_id         = "nano_2_0"
#   key_pair_name     = "awskeypair"
#   user_data  = file("docker.sh")


#   tags = {
#     Name        = "dev_test_server_portcicd"
#     env         = "dev"
#     team        = "dev_team"
#     application = "portcicd"
#   }
# }
# resource "aws_lightsail_instance_public_ports" "dev_test_ports" {
#   instance_name = aws_lightsail_instance.dev_test_server.name

#   # SSH (port 22)
#   port_info {
#     from_port = 22
#     to_port   = 22
#     protocol  = "tcp"
#   }

#   # HTTP (port 80)
#   port_info {
#     from_port = 80
#     to_port   = 80
#     protocol  = "tcp"
#   }

#   # App range (ports 800–8100)
#   port_info {
#     from_port = 8000
#     to_port   = 8100
#     protocol  = "tcp"
#   }
# }



