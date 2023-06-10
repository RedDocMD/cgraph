#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>

int make_socket(const char *ip, int port)
{
	int ret, fd;
	if ((fd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
		return fd;

	struct sockaddr_in addr;
	memset(&addr, 0, sizeof(addr));
	addr.sin_family = AF_INET;
	addr.sin_port = htons(port);
	if (inet_pton(AF_INET, ip, &addr.sin_addr)) {
		ret = -EINVAL;
		goto cleanup;
	}

	if ((ret = bind(fd, (const struct sockaddr *)&addr, sizeof(addr))))
		goto cleanup;

	return fd;

cleanup:
	close(fd);
	return ret;
}

int main()
{
	int sock = make_socket("127.0.0.1", 10000);
	if (sock < 0) {
		fprintf(stderr, "socket creation failed: %s\n", strerror(sock));
		return 1;
	}
	return 0;
}