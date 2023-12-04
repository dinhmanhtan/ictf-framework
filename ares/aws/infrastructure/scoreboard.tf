# data "aws_eip" "scoreboard_ip" {
#   tags = {
#     Name = "ictf-scoreboard-ip"
#   }
# }

# resource "aws_eip_association" "scoreboard_ip" {
#     instance_id = aws_instance.scoreboard.id
#     allocation_id = data.aws_eip.scoreboard_ip.id
# }

data "aws_ecr_repository" "ictf_scoreboard" {
  name = "ictf_scoreboard"
}

resource "aws_instance" "scoreboard" {
    ami = data.aws_ami.ictf_base.id
    instance_type = var.scoreboard_configuration.instance_type
    //instance_type = "scoreboard"
    subnet_id = aws_subnet.master_and_db_range_subnet.id
    vpc_security_group_ids = [aws_security_group.master_subnet_secgrp.id]
    key_name = aws_key_pair.scoreboard-key.key_name

    tags = {
        Name = "scoreboard"
        Type = "Infrastructure"
    }

    root_block_device {
        volume_size = var.scoreboard_configuration.volume_size
    }

    volume_tags = {
        Name = "scoreboard-disk"
    }

    depends_on = [data.aws_ecr_repository.ictf_scoreboard]

    connection {
        user = local.ictf_user
        private_key = file("../sshkeys/scoreboard-key.key")
        host = self.public_ip
        agent = false
    }

    provisioner "remote-exec" {
        inline = [
            "touch /tmp/test.txt"
        ]
    }

    provisioner "file" {
        source = "../../../scoreboard/provisioning/ares_provisioning/docker-compose.yml"
        destination = "/home/ubuntu/docker-compose.yml"
    }

    provisioner "remote-exec" {
        inline = [
            local.scoreboard_provision_with_ansible,
            local.start_service_container
        ]
    }
}
