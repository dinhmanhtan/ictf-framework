data "aws_ami" "teamvm" {
  most_recent = true

  filter {
    name   = "name"
    values = ["teamvm_primer"]
  }

  owners = ["self"]
}

locals {
  teams_list = jsondecode(file(var.game_config_file)).teams
  teams_organizer_hosted_map = { for team in local.teams_list: team.id => team if team.organizer_hosted }
}


resource "aws_instance" "teamvm" {
    # for_each = local.teams_organizer_hosted_map
    ami = data.aws_ami.teamvm.id
    instance_type = var.teamvm_configuration[count.index].instance_type
    //instance_type = "teamvm"
    subnet_id = aws_subnet.war_range_subnet.id
    vpc_security_group_ids = [aws_security_group.teams_secgrp.id]
    count = length(var.teamvm_configuration)

    private_ip = "172.31.${129 + floor((var.teamvm_configuration[count.index].id - 1) / 254)}.${(var.teamvm_configuration[count.index].id) % 254}"
    key_name = aws_key_pair.teamvmmaster-key.key_name

    tags = {
        Name = "teamvm${var.teamvm_configuration[count.index].id}"
        TeamIdx = var.teamvm_configuration[count.index].id
        Type = "Teams"
    }

    root_block_device {
        volume_size = var.teamvm_configuration[count.index].volume_size
    }

    volume_tags = {
        Name = "teamvm${var.teamvm_configuration[count.index].id}-disk"
    }

    connection {
        user = local.ictf_user
        private_key = file("../sshkeys/teamvmmaster-key.key")
        host = self.public_ip
        agent = false
        timeout = "10m"
    }

   # provisioner "local-exec" {
   #     command ="cat ../sshkeys/team${var.teamvm_configuration[count.index].id}-key.pub >> ../sshkeys/authorized_keys_team${var.teamvm_configuration[count.index].id}"
   # }


    provisioner "remote-exec" {
        inline = [
            "touch /tmp/test.txt"
        ]
    }

    provisioner "file" {
        source = "../sshkeys/authorized_keys_team${var.teamvm_configuration[count.index].id}"
        destination = "/home/ubuntu/authorized_keys"
    }

    provisioner "file" {
        source = "../vpnkeys/team${var.teamvm_configuration[count.index].id}.ovpn"
        destination = "/home/ubuntu/openvpn.conf.j2"
    }

    # provisioner "local-exec" {
    #     command = "rm ../sshkeys/authorized_keys_team${var.teamvm_configuration[count.index].id}"
    # }

    provisioner "file" {
        source = "../../../teamvms/provisioning/ares_provisioning/ansible-provisioning.yml"
        destination = "/home/ubuntu/terraform_provisioning.yml"
    }

    provisioner "remote-exec" {
        inline = [
            "ansible-playbook ~/terraform_provisioning.yml --extra-vars ROUTER_PRIVATE_IP=172.31.172.1 --extra-vars TEAM_ID=${var.teamvm_configuration[count.index].id}" ,
            "sudo service ssh restart"
        ]
    }
}

