data "aws_ami" "ictf_base" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ictf_base_20.04"]
  }

  owners = ["self"]
}