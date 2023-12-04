data "aws_s3_bucket" "database_bucket" {
  bucket = "ictf-database-bucket-${var.region}"
}

data "aws_ecr_repository" "ictf_database" {
  name = "ictf_database"
}

resource "aws_instance" "database" {
    ami = data.aws_ami.ictf_base.id
    instance_type = var.database_configuration.instance_type
    //instance_type = "database"
    subnet_id = aws_subnet.master_and_db_range_subnet.id
    vpc_security_group_ids = [aws_security_group.master_subnet_secgrp.id]
    key_name = aws_key_pair.database-key.key_name

    depends_on = [data.aws_ecr_repository.ictf_database]

    root_block_device {
        volume_size = var.database_configuration.volume_size
    }

    volume_tags = {
        Name = "database-disk"
    }

    tags = {
        Name = "database"
        Type = "Infrastructure"
    }

    connection {
        user = local.ictf_user
        private_key = file("../sshkeys/database-key.key")
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
        source = "../../../database/provisioning/ares_provisioning/docker-compose.yml"
        destination = "/home/ubuntu/docker-compose.yml"
    }

    provisioner "remote-exec" {
        inline = [
            local.database_provision_with_ansible,
            local.start_service_container
        ]
    }
}
