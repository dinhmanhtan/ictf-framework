resource "aws_key_pair" "database-key" { 
  key_name   = "database-key" 
  public_key = file("../sshkeys/database-key.pub") 
}
resource "aws_key_pair" "router-key" { 
  key_name   = "router-key" 
  public_key = file("../sshkeys/router-key.pub") 
}
resource "aws_key_pair" "gamebot-key" { 
  key_name   = "gamebot-key" 
  public_key = file("../sshkeys/gamebot-key.pub") 
}
resource "aws_key_pair" "scoreboard-key" { 
  key_name   = "scoreboard-key" 
  public_key = file("../sshkeys/scoreboard-key.pub") 
}
resource "aws_key_pair" "teaminterface-key" { 
  key_name   = "teaminterface-key" 
  public_key = file("../sshkeys/teaminterface-key.pub") 
}
resource "aws_key_pair" "scriptbot-key" { 
  key_name   = "scriptbot-key" 
  public_key = file("../sshkeys/scriptbot-key.pub") 
}
resource "aws_key_pair" "teamvmmaster-key" { 
  key_name   = "teamvmmaster-key" 
  public_key = file("../sshkeys/teamvmmaster-key.pub") 
}
resource "aws_key_pair" "dispatcher-key" { 
  key_name   = "dispatcher-key" 
  public_key = file("../sshkeys/dispatcher-key.pub") 
}
resource "aws_key_pair" "logger-key" { 
  key_name   = "logger-key" 
  public_key = file("../sshkeys/logger-key.pub") 
}
# resource "aws_key_pair" "team1-key" { 
#   key_name   = "team1-key" 
#   public_key = file("../sshkeys/team1-key.pub") 
# }
# resource "aws_key_pair" "team2-key" { 
#   key_name   = "team2-key" 
#   public_key = file("../sshkeys/team2-key.pub") 
# }
# resource "aws_key_pair" "team3-key" { 
#   key_name   = "team3-key" 
#   public_key = file("../sshkeys/team3-key.pub") 
# }
# resource "aws_key_pair" "team4-key" { 
#   key_name   = "team4-key" 
#   public_key = file("../sshkeys/team4-key.pub") 
# }
# resource "aws_key_pair" "team5-key" { 
#   key_name   = "team5-key" 
#   public_key = file("../sshkeys/team5-key.pub") 
# }
