# pipeline-generator

#### As CI pipeline this repository will use `.gitlab-ci-scheduler.yml` file which will execute script `generator.sh` (for each of the microservice as the template yaml file which included will be used `pipeline-template.yaml` file) with argument `YAML_NAME` variable with value `.gitlab-ci-microservices.yml`. The file `.gitlab-ci-microservices.yml` will be used as main CI yaml file for the Monorepo where will be located all microservices. `.gitlab-ci-scheduler.yml` pipeline will be executed ecah 1 hour or could be executed with API. It means if developer will create new microservice in the microservices repository with naming convension `^ms*|^adp*|^bff*|^config*` then `generator.sh` script creates new pipeline for this microservice and include it to the `.gitlab-ci-microservices.yml` yaml file.