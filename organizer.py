from pathlib import Path
import shutil
from datetime import datetime


def log_check(logs_path: Path):
    logs_path.mkdir(exist_ok=True)

    log_files = list(logs_path.glob("*.csv"))

    if not log_files:
        return

    choice = input("Undo previous operation? (Y/N): ").strip().lower()
    if choice != "y":
        return

    print("\nAvailable logs:")
    for log in log_files:
        print(log.name)

    selected = input("\nChoose a log file: ").strip()
    selected_log = logs_path / selected

    if not selected_log.exists():
        print("Invalid log file.")
        return

    with selected_log.open("r") as f:
        for line in f:
            old_path, new_path = line.strip().split(",")

            try:
                shutil.move(new_path, old_path)
            except Exception as e:
                print(f"Error restoring {new_path}: {e}")

    print("Undo completed successfully.")


def organize_folder(source: str) -> None:
    source_path = Path(source)

    if not source_path.exists():
        print("\nSource folder does not exist.")
        return

    logs_path = Path.cwd() / "logs"
    log_check(logs_path)

    files = list(source_path.iterdir())

    print("\n----- Preview -----")

    preview_count = 0
    for file_path in files:
        if not file_path.is_file():
            continue

        folder = file_path.suffix[1:].lower() or "no_extension"
        print(f"{file_path.name}  →  {folder}/{file_path.name}")

        preview_count += 1
        if preview_count == 5:
            break

    if input("\nContinue? (Y/N): ").strip().upper() != "Y":
        print("Operation cancelled.")
        return

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = logs_path / f"{timestamp}.csv"

    duplicate_counter = 0

    with log_file.open("w") as log:
        for file_path in files:
            if not file_path.is_file():
                continue

            folder = file_path.suffix[1:].lower() or "no_extension"
            destination_folder = source_path / folder
            destination_folder.mkdir(exist_ok=True)

            destination = destination_folder / file_path.name

            try:
                shutil.move(str(file_path), str(destination))
                log.write(f"{file_path},{destination}\n")

            except FileExistsError:
                new_name = f"{file_path.stem}_{duplicate_counter}{file_path.suffix}"
                new_path = source_path / new_name
                file_path.rename(new_path)
                new_destination = destination_folder / new_name
                shutil.move(str(new_path), str(new_destination))
                log.write(f"{file_path},{new_destination}\n")
                duplicate_counter += 1

            except Exception as e:
                print(f"Error moving {file_path.name}: {e}")

    print("\nOrganisation completed successfully.")


def main():
    source = input("Enter folder path: ").strip()
    organize_folder(source)


if __name__ == "__main__":
    main()
