data "local_file" "ecr_password" {
    filename = "../ecr_password"
    #depends_on = [aws_ecr_repository.service_scriptbot_image]
}

data "aws_ecr_repository" "ictf_scriptbot" {
  name = "ictf_scriptbot"
}


resource "aws_instance" "scriptbot" {
    ami           = data.aws_ami.ictf_base.id
    instance_type = var.scriptbot_configuration[count.index].instance_type
    //instance_type = "scriptbot"
    count         = var.scriptbot_num

    key_name      = aws_key_pair.scriptbot-key.key_name

    subnet_id = aws_subnet.master_and_db_range_subnet.id
    vpc_security_group_ids = [aws_security_group.master_subnet_secgrp.id]

    #depends_on = [aws_ecr_repository.service_scriptbot_image,data.aws_ecr_repository.ictf_scriptbot]
    depends_on = [data.aws_ecr_repository.ictf_scriptbot]

    root_block_device {
        volume_size = var.scriptbot_configuration[count.index].volume_size
    }

    volume_tags = {
        Name = "scriptbot${var.scriptbot_configuration[count.index].id}-disk"
    }

    tags = {
        Name = "scriptbot${var.scriptbot_configuration[count.index].id}"
        Type = "Infrastructure"
    }

    connection {
        user = local.ictf_user
        private_key = file("../sshkeys/scriptbot-key.key")
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
        source = "../../../scriptbot/provisioning/ares_provisioning/"
        destination = "/home/ubuntu/ares_provisioning_second_stage"
    }
 
    provisioner "remote-exec" {
        inline = [
            local.scriptbot_common_provision_with_ansible,
            "ansible-playbook ~/ares_provisioning_second_stage/ansible-provisioning.yml --extra-vars SCRIPTBOT_ID=${count.index + 1} --extra-vars ALL_BOTS=${var.scriptbot_num} --extra-vars API_SECRET=${file("../../../secrets/database-api/secret")} --extra-vars REGISTRY_USERNAME=AWS --extra-vars REGISTRY_PASSWORD=${data.local_file.ecr_password.content} --extra-vars REGISTRY_ENDPOINT=${local.registry_id}.dkr.ecr.${var.region}.amazonaws.com --extra-vars USER=ubuntu --extra-vars DISPATCHER_IP=${aws_instance.dispatcher.private_ip}",
            local.start_service_container
        ]
    }
}
