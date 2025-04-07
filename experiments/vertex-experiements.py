from vertexai import init, experiment

init(project="your-project", location="us-central1")

with experiment.start_run("test-run") as run:
    run.log_param("learning_rate", 0.01)
    run.log_metric("accuracy", 0.92)