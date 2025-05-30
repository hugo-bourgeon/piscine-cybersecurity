/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   spider.h                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: hubourge <hubourge@student.42angouleme.    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/05/30 16:20:05 by hubourge          #+#    #+#             */
/*   Updated: 2025/05/30 16:21:45 by hubourge         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef SPIDER_H
# define SPIDER_H

# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <unistd.h> 
# include <ctype.h> 

typedef struct s_config
{
	int		recursive;
	int		max_depth;
	char	*output_path;
	char	*url;
}	t_config;

void	init_config(t_config *cfg);
int		is_number(const char *str);

#endif