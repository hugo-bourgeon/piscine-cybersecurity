# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: hubourge <hubourge@student.42angouleme.    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/05/30 16:05:06 by hubourge          #+#    #+#              #
#    Updated: 2025/05/30 16:19:00 by hubourge         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

CXX				= gcc

CFLAGS			= -Wall -Wextra -Werror -g

NAME_SPIDER		= spider
NAME_SCORPION	= scorpion

SRC_SPIDER		= spider.c

SRC_SCORPION	= scorpion.c

OBJ_SPIDER      = $(SRC_SPIDER:.c=.o)
OBJ_SCORPION    = $(SRC_SCORPION:.c=.o)

YELLOW			=\033[0;33m
NC				=\033[0m

all: spider scorpion
	@ echo ""

spider: $(OBJ_SPIDER)
	@ echo "$(YELLOW)Compiling ./spider...$(NC)"
	@ $(CXX) $(CFLAGS) -o spider $^


scorpion: $(OBJ_SCORPION)
	@ echo "$(YELLOW)Compiling ./scorpion...$(NC)"
	@ $(CXX) $(CFLAGS) -o scorpion $^


%.o: %.c
	@ $(CXX) $(CFLAGS) -c $< -o $@

clean:
	@ echo "$(YELLOW)Cleaning in progress...$(NC)"
	@ rm -rf *.o
	@ echo "$(YELLOW)Cleaning completed$(NC)\n"

fclean: clean
	@ rm -rf $(NAME_SPIDER) $(NAME_SCORPION)

re: fclean all

.PHONY: all clean fclean re spider scorpion