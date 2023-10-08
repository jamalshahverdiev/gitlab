#!/usr/bin/env sh

if [[ $# != 1 ]]; then echo "Usage: ./$(basename $0) .gitlab-ci-file.yml"; exit 1; fi

ms_pipeline_template='pipeline-template.yaml'
services_folder='microservices'
ci_yaml_name=$1
collected_names=$(ls | egrep "^ms*|^adp*|^bff*|^config*")
ms_ci_yaml_name='.gitlab-ci.yml'
shared_yaml_path='shared_yamls'
main_template_yaml='ci-main-template.yml'

apk add gettext

cat <<EOF > ${ci_yaml_name}
include:
  - local: ${shared_yaml_path}/${main_template_yaml}
EOF

for name in $collected_names; do
    if [[ ! -d ${services_folder} ]]; then mkdir ${services_folder}; fi
    export MS_NAME=${name} DOLLAR='$'
    cat ${ms_pipeline_template} | envsubst > ${services_folder}/${name}.yml
    echo "  - local: ${shared_yaml_path}/${services_folder}/${name}.yml" >> ${ci_yaml_name}
done

