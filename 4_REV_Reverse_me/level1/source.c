/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   source.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: hubourge <hubourge@student.42angouleme.    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/06/17 15:49:32 by hubourge          #+#    #+#             */
/*   Updated: 2025/06/17 15:53:12 by hubourge         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <string.h>

int main(char **argv, int argc) {
  char buf[32];

  printf("Please enter key: ");
  scanf("%31s", buf);
  if (strcmp(buf, "__stack_check") == 0)
    printf("Good job.\n");
  else
    printf("Nope.\n");

  return (0);
}