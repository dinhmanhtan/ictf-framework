
data "aws_ecr_repository" "ictf_gamebot" {
  name = "ictf_gamebot"
}


resource "aws_instance" "gamebot" {
    ami = data.aws_ami.ictf_base.id
    instance_type = var.gamebot_configuration.instance_type
    //instance_type = "gamebot"
    subnet_id = aws_subnet.master_and_db_range_subnet.id
    vpc_security_group_ids = [aws_security_group.master_subnet_secgrp.id]
    key_name = aws_key_pair.gamebot-key.key_name

    tags = {
        Name = "gamebot"
        Type = "Infrastructure"
    }

    root_block_device {
        volume_size = var.gamebot_configuration.volume_size
    }

    volume_tags = {
        Name = "gamebot-disk"
    }

    //depends_on = [data.aws_ecr_repository.ictf_gamebot]

    connection {
        user = local.ictf_user
        private_key = file("../sshkeys/gamebot-key.key")
        host = self.public_ip
        agent = false
        timeout = "10m"
    }


    provisioner "remote-exec" {
        inline = [
           "touch /tmp/test.txt"
        ]
    }

    # this folder has already been there in the base image
    provisioner "file" {
        source = "../../../gamebot/provisioning/ares_provisioning/"
        destination = "/home/ubuntu/ares_provisioning_second_stage"
    }

    provisioner "remote-exec" {
        inline = [
            local.gamebot_provision_with_ansible,
            "ansible-playbook ~/ares_provisioning_second_stage/ansible-provisioning.yml --extra-vars NUM_SCRIPTBOTS=${var.scriptbot_num} --extra-vars USER=ubuntu --extra-vars DISPATCHER_IP=${aws_instance.dispatcher.private_ip}",
            local.start_service_container
        ]
    }
}
