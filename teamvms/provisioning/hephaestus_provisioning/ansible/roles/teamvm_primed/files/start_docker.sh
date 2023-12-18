sudo chmod 766 /opt/ictf/services/prosopagnosia/deploy/init.sql
cd /opt/ictf/services/prosopagnosia/deploy && docker-compose up -d
cd /opt/ictf/services/museumorphosis && docker-compose up -d
sudo chmod +x /opt/ictf/services/mailbox/scripts/*
cd /opt/ictf/services/mailbox/ && docker-compose up -d
cd /opt/ictf/services/yellow_submarine/ && docker-compose up -d
cd /opt/ictf/services/st_2_hide/ && docker-compose up -d
cd /opt/ictf/services/sky_with_diamonds/ && docker-compose up -d
cd /opt/ictf/services/strawberry_forever/ && docker-compose up -d