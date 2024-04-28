container_name="vehicletracker"
container_tag="latest"
registry_name="befriendsvehicletracker"
registry_url="${registry_name}.azurecr.io/${container_name}:${container_tag}"
containerapp_name="vehicle-tracker"
resource_group_name="Be-Friends-Prototype"

echo "Start Deployment script. Check that azure cli is installed and docker daemon is running."
echo "check azure user login"
az account show > /dev/null
if [ $? -eq 0 ]; then
    echo "azure user already logged in."
else
     echo "start azure login"
     az login > /dev/null
        if [ $? -eq 0 ]; then
            echo "azure login successful."
        else
            echo "azure login failed."
            exit 1
        fi
fi
echo "start docker registry login."
az acr login --name "${registry_name}" > /dev/null
if [ $? -eq 0 ]; then
    echo "docker login successful."
else
    echo "docker login failed."
    exit 1
fi
echo "build docker image"
#!/bin/bash
# Abrufen der Maschinenarchitektur
arch=$(uname -m)

case "$arch" in
    x86_64)
        docker build -t "${registry_url}" . > /dev/null
        ;;
    arm* | aarch64 | *)
        docker build -t "${registry_url}" --platform "linux/amd64" . > /dev/null
        ;;
esac
if [ $? -eq 0 ]; then
    echo "docker build sucessful"
else
    echo "docker build failed"
    exit 1
fi
echo "Push image into docker registry"

docker push "${registry_url}"
echo "Create new Revision"
az containerapp update  -g "${resource_group_name}" -n "${containerapp_name}" --container-name "${container_name}" -i "${registry_url}" >/dev/null
if [ $? -eq 0 ]; then
    echo "Revision updated. Deployment successful triggered."
    while true; do
        # Abfrage des aktuellen Status der ContainerApp
        status=$(az containerapp show -g "${resource_group_name}" -n "${containerapp_name}" --query properties.runningStatus -o tsv)

        # Überprüfung, ob der Status 'Running' ist
        if [[ "$status" == "Running" ]]; then
            echo "Deployment is up. exit"
            exit 0
        else
            echo "Deployment in progress. Current state: $status..."
        fi
        sleep 1
    done
else
    echo "Deployment failed"
    exit 1
fi


