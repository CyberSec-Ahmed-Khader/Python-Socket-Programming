import socket
import threading
import subprocess


HOST = "0.0.0.0"
PORT = 5000



def execute_command(command):
    """
    Execute system command and return result
    """

    try:

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )


        if result.stdout:
            return result.stdout


        if result.stderr:
            return "ERROR:\n" + result.stderr


        return "Command executed successfully"


    except Exception as error:

        return f"Execution Error: {error}"




def handle_client(client_socket, client_address):

    print(f"[+] Client connected: {client_address}")


    try:

        while True:


            command = client_socket.recv(4096).decode()


            if not command:
                break



            print(
                f"[{client_address}] Command: {command}"
            )



            if command.lower() == "exit":

                client_socket.send(
                    "Session closed".encode()
                )

                break



            output = execute_command(command)



            client_socket.send(
                output.encode()
            )



    except ConnectionResetError:

        print(
            f"[-] Client disconnected unexpectedly: {client_address}"
        )


    except Exception as error:

        print(
            f"[!] Error with {client_address}: {error}"
        )


    finally:

        client_socket.close()

        print(
            f"[-] Connection closed: {client_address}"
        )





def start_server():


    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )


    try:


        server_socket.bind(
            (HOST, PORT)
        )


        server_socket.listen()



        print("==============================")
        print(" Remote Command Server")
        print("==============================")
        print(f"Listening on port {PORT}")
        print("Waiting for clients...\n")



        while True:



            client_socket, client_address = server_socket.accept()



            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address)
            )


            client_thread.start()



            print(
                f"Active Clients: {threading.active_count()-1}"
            )



    except OSError as error:


        print(
            f"Server Error: {error}"
        )


    finally:


        server_socket.close()





if __name__ == "__main__":

    start_server()