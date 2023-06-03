pkgload::load_all()

path_to_json <- Sys.getenv("YT_API_RESP_PATH")
json_file <- list.files(path_to_json)
paths <- file.path(path_to_json, json_file)
videos_df <-
  purrr::map(paths, read_tidy_yt, .progress = TRUE) |>
  purrr::list_rbind()

