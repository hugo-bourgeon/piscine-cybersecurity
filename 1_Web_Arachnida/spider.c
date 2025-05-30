/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   spider.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: hubourge <hubourge@student.42angouleme.    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/05/30 16:04:43 by hubourge          #+#    #+#             */
/*   Updated: 2025/05/30 16:32:16 by hubourge         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "spider.h"

void	init_config(t_config *cfg)
{
	cfg->recursive = 0;
	cfg->max_depth = 5;
	cfg->output_path = "./data/";
	cfg->url = NULL;
}

int	is_number(const char *str)
{
	if (!str || *str == '\0')
		return (0);
	for (int i = 0; str[i]; ++i)
		if (!isdigit((unsigned char)str[i]))
			return (0);
	return (1);
}

int	main(int argc, char **argv)
{
	t_config	config;
	int			opt;
	
	init_config(&config);

	while ((opt = getopt(argc, argv, "rl:p:")) != -1)
	{
		switch (opt)
		{
			case 'r':
				config.recursive = 1;
				break;
			case 'l':
				if (!is_number(optarg))
				{
					fprintf(stderr, "Error: -l requires a numeric argument.\n");
					exit(EXIT_FAILURE);
				}
				config.max_depth = atoi(optarg);
				if (config.max_depth < 0)
				{
					fprintf(stderr, "Error: -l must be a positive number.\n");
					exit(EXIT_FAILURE);
				}
				break;
			case 'p':
				if (strlen(optarg) == 0)
				{
					fprintf(stderr, "Error: -p requires a valid path.\n");
					exit(EXIT_FAILURE);
				}
				config.output_path = optarg;
				break;
			default:
				fprintf(stderr, "Usage: %s [-r] [-l N] [-p PATH] URL\n", argv[0]);
				exit(EXIT_FAILURE);
		}
	}

	if (optind >= argc)
	{
		fprintf(stderr, "Expected URL after options\n");
		exit(EXIT_FAILURE);
	}
	config.url = argv[optind];

	printf("Recursive:   %d\n", config.recursive);
	printf("Max depth:   %d\n", config.max_depth);
	printf("Output path: %s\n", config.output_path);
	printf("URL:         %s\n", config.url);

	return 0;
}