compose_file_path <- function(file_name, data_dir) {
  stopifnot(is.character(file_name) && length(file_name) == 1)
  is_abs <- fs::is_absolute_path(file_name)
  if (is_abs) {
    file_name
  } else {
    file.path(data_dir, file_name)
  }
}

compose_file_name <- function(..., ext = "json") {
  args <- unlist(rlang::list2(...))
  compose_name <- str_c(args, collapse = "_")
  str_c(compose_name, ext, sep = ".")
}
