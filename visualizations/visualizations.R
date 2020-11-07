library(dplyr)
library(ggplot2)


# TODO: Fill in the path of the folder containing the results (including /).
results_path <- "visualizations/"

results <- read.csv(paste0(results_path, "results.csv"))


create_density_plot <- function(data, x_values) {
  plot <- ggplot(data = data, mapping = aes_string(x = x_values, color = "model")) +
    geom_density() +
    labs(x = gsub("_", " ", x_values)) +
    scale_color_discrete(
      name = "Model",
      breaks = c(
        "Clock",
        "FirstComeFirstServe",
        "LocalOptimum",
        "GlobalOptimum"
      ),
      labels = c(
        "Clock",
        "First come first serve",
        "Local optimum\nwith priority",
        "Global optimum\nwith priority (distributed)"
      )
    )

  ggsave(filename = paste0(x_values, ".png"), plot = plot, path = paste0(results_path, "figures"), width = 5.5, height = 4)
}

create_density_plot(results, "mean_number_of_steps")
create_density_plot(results, "mean_number_of_traffic_lights")
create_density_plot(results, "mean_number_of_waiting_steps")
create_density_plot(results, "simulation_score")

# ANOVA
print(summary(aov(results$simulation_score ~ results$model)))
# T-test
simulation_score_local_optimum <- filter(results, model == 'LocalOptimum')$simulation_score
simulation_score_global_optimum <- filter(results, model == 'GlobalOptimum')$simulation_score
print(t.test(simulation_score_local_optimum, simulation_score_global_optimum, paired = TRUE))
