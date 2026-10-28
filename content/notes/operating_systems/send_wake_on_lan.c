#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>

typedef SOCKET socket_handle;
#define INVALID_SOCKET_HANDLE INVALID_SOCKET
#define close_socket closesocket
#else
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>

typedef int socket_handle;
#define INVALID_SOCKET_HANDLE (-1)
#define close_socket close
#endif


static int parse_mac_address(const char *text, unsigned char mac[6]) {
    unsigned int bytes[6];
    int characters_read = 0;
    int parsed = sscanf(
        text,
        "%2x:%2x:%2x:%2x:%2x:%2x%n",
        &bytes[0],
        &bytes[1],
        &bytes[2],
        &bytes[3],
        &bytes[4],
        &bytes[5],
        &characters_read
    );

    if (parsed != 6 || text[characters_read] != '\0') {
        return 0;
    }

    for (int index = 0; index < 6; ++index) {
        mac[index] = (unsigned char)bytes[index];
    }
    return 1;
}


static void print_socket_error(const char *message) {
#ifdef _WIN32
    fprintf(stderr, "%s: Winsock error %d\n", message, WSAGetLastError());
#else
    fprintf(stderr, "%s: %s\n", message, strerror(errno));
#endif
}


int main(int argc, char **argv) {
    const char *broadcast_address = argc >= 3 ? argv[2] : "255.255.255.255";
    const unsigned short port = 9;
    unsigned char mac[6];
    unsigned char packet[6 + 16 * 6];
    struct sockaddr_in destination;
    socket_handle sock;
    int allow_broadcast = 1;

    if (argc < 2 || argc > 3) {
        fprintf(
            stderr,
            "usage: %s MAC_ADDRESS [BROADCAST_ADDRESS]\n"
            "example: %s 01:23:45:67:89:ab 192.168.1.255\n",
            argv[0],
            argv[0]
        );
        return 2;
    }

    if (!parse_mac_address(argv[1], mac)) {
        fprintf(stderr, "invalid MAC address: %s\n", argv[1]);
        return 2;
    }

#ifdef _WIN32
    WSADATA winsock_data;
    if (WSAStartup(MAKEWORD(2, 2), &winsock_data) != 0) {
        print_socket_error("could not initialize Winsock");
        return 1;
    }
#endif

    memset(packet, 0xff, 6);
    for (int repetition = 0; repetition < 16; ++repetition) {
        memcpy(packet + 6 + repetition * 6, mac, 6);
    }

    sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sock == INVALID_SOCKET_HANDLE) {
        print_socket_error("could not create UDP socket");
#ifdef _WIN32
        WSACleanup();
#endif
        return 1;
    }

#ifdef _WIN32
    if (setsockopt(
            sock,
            SOL_SOCKET,
            SO_BROADCAST,
            (const char *)&allow_broadcast,
            sizeof(allow_broadcast)
        ) != 0) {
#else
    if (setsockopt(
            sock,
            SOL_SOCKET,
            SO_BROADCAST,
            &allow_broadcast,
            sizeof(allow_broadcast)
        ) != 0) {
#endif
        print_socket_error("could not enable UDP broadcast");
        close_socket(sock);
#ifdef _WIN32
        WSACleanup();
#endif
        return 1;
    }

    memset(&destination, 0, sizeof(destination));
    destination.sin_family = AF_INET;
    destination.sin_port = htons(port);
    if (inet_pton(AF_INET, broadcast_address, &destination.sin_addr) != 1) {
        fprintf(stderr, "invalid IPv4 broadcast address: %s\n", broadcast_address);
        close_socket(sock);
#ifdef _WIN32
        WSACleanup();
#endif
        return 2;
    }

    if (sendto(
            sock,
            (const char *)packet,
            sizeof(packet),
            0,
            (const struct sockaddr *)&destination,
            sizeof(destination)
        ) != (int)sizeof(packet)) {
        print_socket_error("could not send magic packet");
        close_socket(sock);
#ifdef _WIN32
        WSACleanup();
#endif
        return 1;
    }

    printf(
        "sent Wake-on-LAN packet for %s to %s:%u\n",
        argv[1],
        broadcast_address,
        port
    );

    close_socket(sock);
#ifdef _WIN32
    WSACleanup();
#endif
    return 0;
}
