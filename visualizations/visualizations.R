library(dplyr)
library(ggplot2)


# TODO: Fill in the path of the folder containing the results (including /).
results_path <- "" 

results <- read.csv(paste0(results_path, "results.csv"))


create_density_plot <- function(data, x_values) {
  ggplot(data = data, mapping = aes_string(x = x_values, color = "model")) +
    geom_density() +
    labs(x = gsub("_", " ", x_values)) +
    scale_color_discrete(name = "Model", labels = c("Clock model", "Local optimum\nwith priority model"))

  ggsave(paste0(results_path, x_values, ".png", sep = ""), width = 5.5, height = 4)
}

create_density_plot(results, "mean_number_of_steps")
create_density_plot(results, "mean_number_of_traffic_lights")
create_density_plot(results, "mean_number_of_waiting_steps")
create_density_plot(results, "simulation_score")


# T-test
simulation_score_clock <- filter(results, model == 'clock_model')$simulation_score
simulation_score_local_optimum <- filter(results, model == 'local_optimum_with_priority_model')$simulation_score
print(t.test(simulation_score_clock, simulation_score_local_optimum, paired = TRUE))

