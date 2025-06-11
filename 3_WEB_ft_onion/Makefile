# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: hubourge <hubourge@student.42angouleme.    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/06/11 15:50:05 by hubourge          #+#    #+#              #
#    Updated: 2025/06/11 19:02:38 by hubourge         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME=ft_onion
HTTP_PORT=80
HTTP_PORT_HOST=8080
SSH_PORT=4242

build:
	docker build -t $(NAME) .

run:
	docker run -d --name $(NAME)_container -p $(HTTP_PORT_HOST):$(HTTP_PORT) -p $(SSH_PORT):$(SSH_PORT) $(NAME)

stop:
	docker stop $(NAME)_container || true
	docker rm $(NAME)_container || true

logs:
	docker logs $(NAME)_container

exec:
	docker exec -it $(NAME)_container /bin/bash

clean: stop
	docker rmi $(NAME) || true

.PHONY: build run stop logs exec clean
