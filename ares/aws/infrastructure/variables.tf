variable "region" {
    description = "AWS region where spawn the game"
    type = string
}

variable "vpc_cdir_block" {
    default = "172.31.0.0/16"
    description = "Ip addresses range for the VPC"
    type = string
}

variable "war_zone_subnet_cidr" {
    default = "172.31.128.0/17"
    description = "Ip addresses range for the warzone subnet"
    type = string
}

variable "master_and_db_zone_subnet_cidr" {
    default = "172.31.64.0/20"
    description = "Ip addresses range for the database and the game-master subnet"
    type = string
}

variable "router_cidr" {
    default = "172.31.172.0/24"
    description = "Router cidr block"
    type = string
}

variable "access_key"  {
    description = "AWS access key"
    type = string
}

variable "secret_key"  {
    description = "AWS secret key"
    type = string
}

variable "scriptbot_num"  {
    description = "Number of scriptbots to spawn for the game"
    type = number
}

variable "teams_num" {
    description = "Number of team to spawn for the game"
    type = number
}

variable "services_path" {
    description = "Path to the deployed services"
    type = string
}

variable "game_config_file" {
    description = "Path to the game cofiguration file"
    type = string
    
}

variable "database_registry_repository_url" {
    description = "Registry repository url pointing to the database docker image"
    type = string
    default = "503448012112.dkr.ecr.ap-southeast-1.amazonaws.com/ictf_database"
}

variable "gamebot_registry_repository_url" {
    description = "Registry repository url pointing to the gamebot docker image"
    type = string
    default = "503448012112.dkr.ecr.ap-southeast-1.amazonaws.com/ictf_gamebot"
}

variable "scoreboard_registry_repository_url" {
    description = "Registry repository url pointing to the scoreboard docker image"
    type = string
    default = "503448012112.dkr.ecr.ap-southeast-1.amazonaws.com/ictf_scoreboard"
}

variable "teaminterface_registry_repository_url" {
    description = "Registry repository url pointing to the teaminterface docker image"
    type = string
    default = "503448012112.dkr.ecr.ap-southeast-1.amazonaws.com/ictf_teaminterface"
}

variable "scriptbot_registry_repository_url" {
    description = "Registry repository url pointing to the scriptbot docker image"
    type = string
    default = "503448012112.dkr.ecr.ap-southeast-1.amazonaws.com/ictf_scriptbot"
}

variable "logger_registry_repository_url" {
    description = "Registry repository url pointing to the logger docker image"
    type = string
    default = "503448012112.dkr.ecr.ap-southeast-1.amazonaws.com/ictf_logger"
}

variable "router_registry_repository_url" {
    description = "Registry repository url pointing to the router docker image"
    type = string
    default = "503448012112.dkr.ecr.ap-southeast-1.amazonaws.com/ictf_router"
}

variable "dispatcher_registry_repository_url" {
    description = "Registry repository url pointing to the dispatcher docker image"
    type = string
    default = "503448012112.dkr.ecr.ap-southeast-1.amazonaws.com/ictf_dispatcher"
}





variable "database_configuration" {
    type = object({
        instance_type    = string
        volume_size = string
    })
    default = {
        instance_type = "t2.small"
        volume_size = 15
    }
}
variable "teamvm_configuration" {
    type = list(object({
        id = string
        instance_type    = string
        volume_size = string
    }))
    default =[
        {
        id = 1
        instance_type = "t2.small"
        volume_size = 15
        },
        {
        id = 2
        instance_type = "t2.small"
        volume_size = 15
        }
    ]
}

variable "logger_configuration" {
    type = object({
        instance_type    = string
        volume_size = string
    })
    default = {
        instance_type = "t2.large"
        volume_size = 40
    }
}

variable "router_configuration" {
    type = object({
        instance_type    = string
        volume_size = string
    })
    default = {
        instance_type = "t2.small"
        volume_size = 15
    }
}

variable "scriptbot_configuration" {
    type = list(object({
        id = string
        instance_type    = string
        volume_size = string
    }))
    default = [{
        id = 1
        instance_type = "t2.small"
        volume_size = 15
    }]
}
variable "gamebot_configuration" {
    type = object({
        instance_type    = string
        volume_size = string
    })
    default = {
        instance_type = "t2.small"
        volume_size = 15
    }
}

variable "scoreboard_configuration" {
    type = object({
        instance_type    = string
        volume_size = string
    })
    default = {
        instance_type = "t2.small"
        volume_size = 15
    }
}

variable "dispatcher_configuration" {
    type = object({
        instance_type    = string
        volume_size = string
    })
    default = {
        instance_type = "t2.small"
        volume_size = 10
    }
}

variable "teaminterface_configuration" {
    type = object({
        instance_type    = string
        volume_size = string
    })
    default = {
        instance_type = "t2.small"
        volume_size = 15
    }
}
