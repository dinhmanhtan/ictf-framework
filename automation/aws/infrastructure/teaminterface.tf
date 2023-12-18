data "aws_eip" "teaminterface_ip" {
  tags = {
    Name = "ictf-teaminterface-ip"
  }
}

resource "aws_eip_association" "teaminterface_ip" {
    instance_id = aws_instance.teaminterface.id
    allocation_id = data.aws_eip.teaminterface_ip.id
}


data "aws_ecr_repository" "ictf_teaminterface" {
  name = "ictf_teaminterface"
}


resource "aws_instance" "teaminterface" {
    ami = data.aws_ami.ictf_base.id
    instance_type = var.teaminterface_configuration.instance_type
    //instance_type = "teaminterface"
    subnet_id = aws_subnet.master_and_db_range_subnet.id
    vpc_security_group_ids = [aws_security_group.master_subnet_secgrp.id]
    key_name = aws_key_pair.teaminterface-key.key_name

    depends_on = [data.aws_ecr_repository.ictf_teaminterface]

    tags = {
        Name = "teaminterface"
        Type = "Infrastructure"
    }

    root_block_device {
        volume_size = var.teaminterface_configuration.volume_size
    }

    volume_tags = {
        Name = "teaminterface-disk"
    }

    connection {
        user = local.ictf_user
        private_key = file("../sshkeys/teaminterface-key.key")
        host = self.public_ip
        agent = false
    }
    
    provisioner "remote-exec" {
        inline = [
            "touch /tmp/test.txt"
        ]
    }

    provisioner "file" {
        source = "../../../teaminterface/provisioning/ares_provisioning/docker-compose.yml"
        destination = "/home/ubuntu/docker-compose.yml"
    }

    provisioner "remote-exec" {
        inline = [
            local.teaminterface_provision_with_ansible,
            local.start_service_container
        ]
    }
}
