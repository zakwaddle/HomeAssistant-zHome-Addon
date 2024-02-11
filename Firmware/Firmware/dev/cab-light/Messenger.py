import socket
import time
import errno


class Messenger:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.host_ip = None
        self.last_resolution_attempt = 0
        self.resolution_interval = 10000  # Attempt resolution every 10 seconds
        self.last_message_attempt = 0
        self.message_retry_interval = 10000
        self.last_message = None

    def resolve_hostname(self, force=False):
        """Resolve the hostname periodically."""
        if self.host_ip is None:
            current_time = time.ticks_ms()
            if force or (time.ticks_diff(current_time, self.last_resolution_attempt) > self.resolution_interval):
                try:
                    addr_info = socket.getaddrinfo(self.hostname, 80)
                    self.host_ip = addr_info[0][-1][0]
                    print("ESP32 IP:", self.host_ip)
                except OSError:
                    print("Error resolving hostname - Light cannot be reached")
                    self.host_ip = None
                except Exception as e:
                    print("Unknown Error Resolving Hostname: ", e)
                self.last_resolution_attempt = current_time

    def queue_message(self, message):
        self.last_message = message

    def send_queued_message(self):
        if not self.host_ip:
            self.resolve_hostname()

        if self.last_message:
            current_time = time.ticks_ms()
            can_try = time.ticks_diff(current_time, self.last_message_attempt) > self.message_retry_interval

            if self.host_ip and can_try:
                sock = socket.socket()
                self.last_message_attempt = current_time

                try:
                    sock.settimeout(2.0)
                    sock.connect((self.host_ip, self.port))
                    sock.send(self.last_message)

                except OSError as e:
                    if e.args[0] == errno.EINPROGRESS:
                        print("Unable to send message: ", self.last_message)
                    else:
                        print("OSError: ", e, "\nUnable to send message: ", self.last_message)
                    self.host_ip = None

                except Exception as e:
                    print("Message Send Error: ", e)
                    self.host_ip = None

                else:
                    try:
                        ack = sock.recv(1024)
                        if ack == b'ACK':
                            print(f'sent: {self.last_message}')
                            self.last_message = None
                            self.last_message_attempt = 0
                    except OSError as e:
                        print("Acknowledgment Error: ", e)
                        self.host_ip = None

                finally:
                    sock.close()
