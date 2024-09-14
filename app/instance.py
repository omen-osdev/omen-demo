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

def cleanup_launcher():
    print("Removing all copied Omen images...")
    
    # Construct the path to the directory
    current_directory = os.path.join(os.getcwd(), "app", "img")
    
    # Check if the directory exists
    if not os.path.isdir(current_directory):
        print(f"Directory does not exist: {current_directory}")
        return
    
    # Iterate through all files in the directory
    for filename in os.listdir(current_directory):
        file_path = os.path.join(current_directory, filename)
        
        # Skip if the file is named 'omen.img'
        if filename == "omen.img":
            continue
        
        # Check if it's a file and then delete it
        if os.path.isfile(file_path):
            print(f"Deleting: {file_path}")
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
        
        # Even if folder, try to remove it
        elif os.path.isdir(file_path):
            print(f"Deleting directory: {file_path}")
            try:
                shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error deleting directory {file_path}: {e}")
    
    print("Cleanup complete.")

def init_launcher():
    current_directory = os.path.join(os.getcwd(), "app")
    source_img = os.path.join(current_directory, "img", "omen.img")
    
    # Check if the source image exists
    if not os.path.isfile(source_img):
        print(f"Source image does not exist: {source_img}")
        return
    
    # Create images for each port (example: 8080.img, 8081.img, etc.)
    for port in range(8080, 8085):  # Example ports
        dest_img = os.path.join(current_directory, "img", f"{port}.img")
        
        if not os.path.isfile(dest_img):
            print(f"Creating image for port {port}...")
            try:
                shutil.copyfile(source_img, dest_img)
            except PermissionError:
                print(f"Permission error occurred while copying image for port {port}.")
                cleanup_launcher()
            except Exception as e:
                print(f"Error when copying image for port {port}: {e}")
        else:
            print(f"Image for port {port} already exists. Skipping.")

    try:
        client = docker.from_env()
    except docker.errors.DockerException:
        print("Error when trying to connect to Docker, is Docker running?")
        return
    except Exception as e:
        print("Unknown error: " + str(e))
        return


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

