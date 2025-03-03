alias d := deploy

# List Available Commands
default:
  just --list

# Start Development Server
develop:
    docker compose -f ./develop.yaml build 
    docker compose -f ./develop.yaml up --watch --env DOMAIN=rovermfg.localhost 
    
# Automatic Deployment
deploy:
    @notify-send -a Deployment " Deployment" "Started Automated Deployment for AI Tutor"
    @echo '{{BOLD + GREEN}}Starting Automated Deployment{{NORMAL}}'
    @bash ./send_files.sh
    @echo '{{BOLD + BLUE}} - Files Sync Success!{{NORMAL}}'
    @ssh aitutor 'cd aitutor; docker compose -f deploy.yaml build'
    @echo '{{BOLD + BLUE}} - Build Success!{{NORMAL}}'
    @ssh aitutor 'cd aitutor; docker compose -f deploy.yaml down'
    @ssh aitutor 'cd aitutor; docker compose -f deploy.yaml up -d'
    @echo '{{BOLD + GREEN}}Finished Automated Deployment{{NORMAL}}'
    @notify-send -a Deployment " Deployment" "Successfully Finished Automated Deployment for AI Tutor"
