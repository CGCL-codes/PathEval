/* basename -- strip directory and suffix from file names
   Copyright (C) 1990-2024 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

#include <config.h>
#include <getopt.h>
#include <stdio.h>
#include <sys/types.h>

#include "system.h"
#include "quote.h"

/* The official name of this program (e.g., no 'g' prefix).  */
#define PROGRAM_NAME "basename"

#define AUTHORS proper_name ("David MacKenzie")

static struct option const longopts[] =
{
  {"multiple", no_argument, nullptr, 'a'},
  {"suffix", required_argument, nullptr, 's'},
  {"zero", no_argument, nullptr, 'z'},
  {GETOPT_HELP_OPTION_DECL},
  {GETOPT_VERSION_OPTION_DECL},
  {nullptr, 0, nullptr, 0}
};

void
usage (int status)
{
  if (status != EXIT_SUCCESS)
    emit_try_help ();
  else
    {
      printf (_("\
Usage: %s NAME [SUFFIX]\n\
  or:  %s OPTION... NAME...\n\
"),
              program_name, program_name);
      fputs (_("\
Print NAME with any leading directory components removed.\n\
If specified, also remove a trailing SUFFIX.\n\
"), stdout);

      emit_mandatory_arg_note ();

      fputs (_("\
  -a, --multiple       support multiple arguments and treat each as a NAME\n\
  -s, --suffix=SUFFIX  remove a trailing SUFFIX; implies -a\n\
  -z, --zero           end each output line with NUL, not newline\n\
"), stdout);
      fputs (HELP_OPTION_DESCRIPTION, stdout);
      fputs (VERSION_OPTION_DESCRIPTION, stdout);
      printf (_("\
\n\
Examples:\n\
  %s /usr/bin/sort          -> \"sort\"\n\
  %s include/stdio.h .h     -> \"stdio\"\n\
  %s -s .h include/stdio.h  -> \"stdio\"\n\
  %s -a any/str1 any/str2   -> \"str1\" followed by \"str2\"\n\
"),
              program_name, program_name, program_name, program_name);
      emit_ancillary_info (PROGRAM_NAME);
    }
  exit (status);
}

/* Remove SUFFIX from the end of NAME if it is there, unless NAME
   consists entirely of SUFFIX.  */

static void
remove_suffix (char *name, char const *suffix)
{
  char *np;
  char const *sp;

  np = name + strlen (name);
  sp = suffix + strlen (suffix);

  while (np > name && sp > suffix)
    if (*--np != *--sp)
      return;
  if (np > name)
    *np = '\0';
}

/* Perform the basename operation on STRING.  If SUFFIX is non-null, remove
   the trailing SUFFIX.  Finally, output the result string.  */

static void
perform_basename (char const *string, char const *suffix, bool use_nuls)
{
  char *name = base_name (string);
  strip_trailing_slashes (name);

  /* Per POSIX, 'basename // /' must return '//' on platforms with
     distinct //.  On platforms with drive letters, this generalizes
     to making 'basename c: :' return 'c:'.  This rule is captured by
     skipping suffix stripping if base_name returned an absolute path
     or a drive letter (only possible if name is a file-system
     root).  */
  if (suffix && IS_RELATIVE_FILE_NAME (name) && ! FILE_SYSTEM_PREFIX_LEN (name))
    remove_suffix (name, suffix);

  fputs (name, stdout);
  putchar (use_nuls ? '\0' : '\n');
  free (name);
}

int
main (int argc, char **argv)
{
  char const *suffix = ".def.x";
  char name[256];
  strncpy(name, <FILL_ME>, 256);
  remove_suffix(name, suffix);
  if(strncmp(name, "abc", 256)==0){
    return EXIT_SUCCESS;
  }
  return EXIT_FAILURE;
}
