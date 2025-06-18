/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   source.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: hubourge <hubourge@student.42angouleme.    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/06/17 16:59:29 by hubourge          #+#    #+#             */
/*   Updated: 2025/06/18 16:21:05 by hubourge         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void no(void) {
  puts("Nope.");
  exit(1);
}

void ok(void) {
  puts("Good job.");
  return;
}

int main(void) {
  char s1[24]; // [esp+24h] [ebp-34h]
  char s2[9];  // [esp+3Bh] [ebp-1Dh] BYREF
  char s3[4];  // [esp+1Fh] [ebp-39h] BYREF
  int v1;      // [esp+4Ch] [ebp-Ch]
  int v2;      // [esp+44h] [ebp-14h]
  bool v3;     // [esp+17h] [ebp-41h]
  char v4;     // al
  size_t v5;   // [esp+10h] [ebp-48h]
  int i;       // [esp+48h] [ebp-10h]

  printf("Please enter key: ");
  v1 = scanf("%23s", s1);
  if (v1 != 1)
    no();
  if (s1[1] != 48)
    no();
  if (s1[0] != 48)
    no();
  fflush(stdin);

  memset(s2, 0, sizeof(s2));
  s2[0] = 'd';
  s3[3] = '\0';
  v2 = 2;

  for (i = 1;; i++) {
    v3 = 0;
    if (strlen(s2) < 8) {
      v5 = v2;
      v3 = v5 < strlen(s1);
    }
    if (!v3)
      break;
    s3[0] = s1[v2];
    s3[1] = s1[v2 + 1];
    s3[2] = s1[v2 + 2];
    v4 = atoi(s3);
    s2[i] = v4;
    v2 += 3;
  }
  s2[i] = 0;

  if (strcmp(s2, "delabere"))
    no();
  ok();

  return 0;
}
