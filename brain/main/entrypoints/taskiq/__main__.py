import subprocess


def main() -> int:
    command = [
        "taskiq",
        "worker",
        "brain.main.entrypoints.taskiq.broker:broker",
        "brain.presentation.tgbot.tasks",
    ]
    return subprocess.call(command)


if __name__ == "__main__":
    raise SystemExit(main())
