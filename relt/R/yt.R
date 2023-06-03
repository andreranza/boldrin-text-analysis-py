read_yt_response <- function(file_name, data_dir = Sys.getenv("YT_API_RESP_PATH")) {
  file_path <- compose_file_path(file_name, data_dir = data_dir)
  tibble::tibble(
    value = jsonlite::read_json(file_path),
    resource = names(value),
  )
}

tidy_yt_response <- function(data) {
  data_stats <-
    data |>
    dplyr::filter(resource %in% c("items", "etag")) |>
    tidyr::pivot_wider(values_from = value, names_from = resource) |>
    dplyr::rename(etag1 = etag) |>
    tidyr::unnest_longer(col = c(etag1, items)) |>
    tidyr::unnest_longer(items) |>
    dplyr::rename(value = items) |>
    tidyr::pivot_wider(values_from = value, names_from = items_id) |>
    tidyr::unnest_wider(
      col = c(statistics, contentDetails, snippet, recordingDetails),
    )

  rlang::try_fetch(
    expr = {
      data_stats |>
        tidyr::unnest_wider(col = c(tags, localized), names_sep = "_") |>
        tidy_yt_final()
    },
    error = function(cnd) {
      data_stats |>
        tidyr::unnest_wider(col = localized, names_sep = "_") |>
        tidy_yt_final()
    }
  )
}

tidy_yt_final <- function(data) {
  data |>
    tidyr::unnest_longer(col = c(kind, etag, id)) |>
    dplyr::select(-thumbnails) |>
    dplyr::rename_with(.fn = stringr::str_to_lower) |>
    dplyr::mutate(publishedat = lubridate::ymd_hms(publishedat)) |>
    dplyr::mutate(duration = lubridate::duration(duration)) |>
    dplyr::mutate(duration_secs = as.numeric(duration), .after = duration) |>
    dplyr::mutate(across(where(is.character), stringr::str_squish))
}

read_tidy_yt <- function(path) {
  read_yt_response(path) |>
    tidy_yt_response()
}
