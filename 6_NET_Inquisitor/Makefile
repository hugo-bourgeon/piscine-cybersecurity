# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: hubourge <hubourge@student.42angouleme.    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/04/24 15:32:18 by hubourge          #+#    #+#              #
#    Updated: 2025/06/23 16:31:33 by hubourge         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# /-------------- Makefile --------------/
NAME		= inquisitor

all:
	@ pyinstaller --noconsole --onefile inquisitor.py
	@ mv dist/inquisitor .
	@ rm -rf build dist *.spec

clean:
	@ rm -rf $(NAME)
	@ rm -rf build dist *.spec

fclean: clean

re: flean all

# /-------------- Docker --------------/
DOCKER_COMPOSE = docker-compose.yml
HACKER_NAME = hacker
TARGET_NAME = target

docker: docker-build docker-stats

docker-build:
	@docker compose -f $(DOCKER_COMPOSE) up --build -d

docker-stop:
	@docker compose -f $(DOCKER_COMPOSE) stop

docker-down:
	@docker compose -f $(DOCKER_COMPOSE) down -v

docker-erase: docker-stop docker-down
	@docker container prune -f
	@docker network rm inquisotor_net || true
	@docker system prune -af --volumes

docker-stats:
	@ echo "\n$(BIBlue)======= Docker stats ======="
	@ docker ps
	@ echo ""
	@ docker volume ls
	@ echo ""
	@ docker network ls

	@ echo "\n$(BIBlue)======= Network info ======="
	@ echo "NAME     IP                MAC "
	@ echo "$(BIBlue)$(HACKER_NAME)   $(RED)$(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(HACKER_NAME))\
		   $(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' $(HACKER_NAME)) $(NC)"
	@ echo "$(BIBlue)$(TARGET_NAME)   $(RED)$(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(TARGET_NAME))\
		   $(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' $(TARGET_NAME)) $(NC)"
	@ echo "$(NC)"


.PHONY: all docker-build docker-stop docker-down docker-erase docker-stats