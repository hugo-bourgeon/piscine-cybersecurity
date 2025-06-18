/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   source.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: hubourge <hubourge@student.42angouleme.    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/06/17 15:49:32 by hubourge          #+#    #+#             */
/*   Updated: 2025/06/18 16:21:24 by hubourge         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <string.h>

int main(char **argv, int argc) {
  const char key[] = "__stack_check";
  char buffer[100]; // 0x6c - 0x8 = 100

  printf("Please enter key: ");
  scanf("%31s", buffer);
  if (strcmp(buffer, key) == 0)
    printf("Good job.\n");
  else
    printf("Nope.\n");

  return (0);
}