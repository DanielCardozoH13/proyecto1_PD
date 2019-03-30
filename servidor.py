import socket
from socket import socket, error
from threading import Thread


class Client(Thread):
    def __init__(self, conn, addr):
        # Inicializar clase padre.
        Thread.__init__(self)

        self.conn = conn
        self.addr = addr

    def run(self):
        while True:
            try:
                # Recibir datos del cliente.
                input_data = self.conn.recv(1024)
                # Reenviar la información recibida.
                if input_data == bytes("s", "utf-8") or input_data == bytes("S", "utf-8"):
                    msg = '1'
                else:
                    msg = '0'

                self.conn.send(bytes(msg, "utf-8"))
            except error:
                print("[%s] Error de lectura." % self.name)
                break
                

def main():
    s = socket()

    # Escuchar peticiones en el puerto 35000.
    s.bind(("localhost", 35000))
    s.listen(1)

    while True:
        conn, addr = s.accept()
        c = Client(conn, addr)
        c.start()
        print("%s:%d se ha conectado." % addr)


if __name__ == "__main__":
    main()