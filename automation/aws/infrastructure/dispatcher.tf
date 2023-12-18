data "aws_ecr_repository" "ictf_dispatcher" {
  name = "ictf_dispatcher"
}


resource "aws_instance" "dispatcher" {
    ami = data.aws_ami.ictf_base.id
    instance_type = var.dispatcher_configuration.instance_type
    //instance_type = "dispatcher"
    subnet_id = aws_subnet.master_and_db_range_subnet.id
    vpc_security_group_ids = [aws_security_group.master_subnet_secgrp.id]
    key_name = aws_key_pair.dispatcher-key.key_name

    tags = {
        Name = "dispatcher"
        Type = "Infrastructure"
    }

    root_block_device {
        volume_size = var.dispatcher_configuration.volume_size
    }

    volume_tags = {
        Name = "dispatcher-disk"
    }

    depends_on = [data.aws_ecr_repository.ictf_dispatcher]

    connection {
        user = local.ictf_user
        private_key = file("../sshkeys/dispatcher-key.key")
        host = self.public_ip
        agent = false
        timeout = "10m"
    }


    provisioner "remote-exec" {
        inline = [
            "touch /tmp/test.txt"
        ]
    }


    provisioner "file" {
        source = "../../../dispatcher/provisioning/ares_provisioning/docker-compose.yml"
        destination = "/home/ubuntu/docker-compose.yml"
    }

    provisioner "remote-exec" {
        inline = [
            local.dispatcher_provision_with_ansible,
            local.start_service_container
        ]
    }
}
