# Architecture - So how does everything work?
# NOTE: I barely know anything about System Design. So I'll resort to using unga-bunga methods!
# Each instance is represented by a port number.
# Numbering starts from INSTANCE_PORT_NUMBER_BEGIN and each new port is incremented by 1, till MAX_INSTANCES
# port_to_container is a Dictionary in which the port number is the key, and the values are Container objects



# TODO: Make building the image from repo dynamic.
# NOTE: But don't always build when user tries to launch the container,
# because that could be heavily abused. Maybe some sort of admin panel,
# which can issue rebuild commands? idk lol

import docker
import docker.errors
import os
import shutil

IMAGE_NAME = "omen/runenv"
READY = False
INSTANCE_PORT_NUMBER_BEGIN = 18200
MAX_INSTANCES = 10
port_to_container = {}
available_ports = [x for x in range(INSTANCE_PORT_NUMBER_BEGIN, INSTANCE_PORT_NUMBER_BEGIN + MAX_INSTANCES)]


def docker_image_exists(client):
    try:
        _ = client.images.get(IMAGE_NAME)
        return True
    except docker.errors.ImageNotFound:
        print("Image does not exist")
        global READY
        READY = False
        return False


def init_launcher():

    current_directory = os.path.join(os.getcwd(), "app")
    source_img = os.path.join(current_directory, "img", "omen.img")
    for port in available_ports:
        dest_img = os.path.join(current_directory, "img", f"{port}.img")
        
        if not os.path.isfile(dest_img):
            print(f"Creating image for port {port}...")
            shutil.copyfile(source_img, dest_img)
        else:
            print(f"Image for port {port} already exists. Skipping.")

    client = docker.from_env()

    try:
        if docker_image_exists(client):
            print("Docker Image already exists")
        else:
            print("Creating Docker Image")
            _ = client.images.build(tag=IMAGE_NAME, path=os.getcwd() + "/app/", dockerfile="Dockerfile.runenv")
        global READY
        READY = True

    except docker.errors.APIError:
        print("Error with Docker API when trying to create image")
    except docker.errors.BuildError:
        print("Error when building the image")


# TODO: fix the directory path of cleanup (careful! don't delete your entire SSD)
def cleanup_launcher():
    print("Removing all copied Omen images...")
    current_directory = os.getcwd() + "/app/img"
    for filename in os.listdir(current_directory):
        if not filename == "omen.img":
            f = os.path.join(current_directory, filename)
            if(os.path.isfile(f)):
                print("Deleting: " + f)
                os.remove(f)


def create_instance():
    if READY:
        # Check whether we are able to launch a new instance
        if not available_ports:
            return -1

        new_instance_port = available_ports.pop()
        client = docker.from_env()
        container = client.containers.run(detach=True, auto_remove=True, devices=["/dev/kvm"], cap_add=["NET_ADMIN"], volumes=[os.getcwd() + "/app/img/" + str(new_instance_port) + ".img" + ":/boot.img:rw"], environment=["BOOT_MODE=uefi", "ARGUMENTS=-cpu qemu64 -d cpu_reset -no-reboot -no-shutdown -machine q35 -m 4G"], ports={8006:new_instance_port}, image="omen/runenv")
        port_to_container[new_instance_port] = container
        return new_instance_port
    else:
        print("Cannot create containers because image does not exist")
        return -1 


def delete_instance(port):
    container = port_to_container[port]
    container.kill()
    available_ports.append(port)

