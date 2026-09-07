import socket


SERVER_IP = "127.0.0.1"
PORT = 5000




def start_client():


    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )



    try:


        client_socket.connect(
            (SERVER_IP, PORT)
        )



        print("==============================")
        print(" Connected To Remote Server")
        print(" Type exit to close")
        print("==============================")



        while True:



            command = input(
                "\nCommand >> "
            )



            client_socket.send(
                command.encode()
            )



            if command.lower() == "exit":

                break



            response = client_socket.recv(
                4096
            ).decode()



            print("\n========== OUTPUT ==========")

            print(response)

            print("============================")




    except ConnectionRefusedError:


        print(
            "Cannot connect. Server is offline."
        )



    except Exception as error:


        print(
            f"Client Error: {error}"
        )



    finally:


        client_socket.close()





if __name__ == "__main__":

    start_client()