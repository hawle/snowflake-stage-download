import os
import json
import snowflake.connector
from dotenv import load_dotenv


def set_action_outputs(output_name, value):
    """Sets the GitHub Action outputs if running as a GitHub Action,
    and otherwise logs these to terminal if running in CLI mode. Note
    that if the CLI mode is used within a GitHub Actions
    workflow, it will be treated the same as GitHub Actions mode.
    """
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            print("{0}={1}".format(output_name, value), file=f)
    else:
        print("\n\nLocal output (when running from Action in $GITHUB_OUTPUT):")
        print("{0}={1}".format(output_name, value))


def main():
    load_dotenv()  # only on local run
    # print(os.environ)

    snowflake_warehouse = os.environ["INPUT_SNOWFLAKE_WAREHOUSE"]
    snowflake_account = os.environ["INPUT_SNOWFLAKE_ACCOUNT"]
    snowflake_username = os.environ["INPUT_SNOWFLAKE_USERNAME"]
    snowflake_password = os.environ["INPUT_SNOWFLAKE_PASSWORD"]
    snowflake_database = os.environ["INPUT_SNOWFLAKE_DATABASE"]
    snowflake_schema = os.environ["INPUT_SNOWFLAKE_SCHEMA"]
    snowflake_stage = os.environ["INPUT_SNOWFLAKE_STAGE"]
    local_download_path = os.environ["INPUT_LOCAL_DOWNLOAD_PATH"]

    # Ensure the download directory exists
    os.makedirs(local_download_path, exist_ok=False)

    conn = snowflake.connector.connect(
        user=snowflake_username,
        password=snowflake_password,
        account=snowflake_account,
        warehouse=snowflake_warehouse,
        database=snowflake_database,
        schema=snowflake_schema,
    )

    try:
        json_results = []

        cur = conn.cursor()

        # List files in the stage
        list_files_query = f"LIST @{snowflake_stage};"
        cur.execute(list_files_query)
        files = cur.fetchall()

        for file in files:
            # Extract the file & path name
            file_path = os.path.dirname(file[0])
            file_name = os.path.basename(file[0])
            local_path = os.path.join(local_download_path, file_path)

            # Download the file
            os.makedirs(local_path, exist_ok=True)
            get_file_query = f"GET @{file[0]} file://{local_path};"
            cur.execute(get_file_query)

            json_results.append(f"{local_path}/{file_name}")
            print(f"Downloaded {local_path}/{file_name}")

    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()

        print(f"All files downloaded!")
        set_action_outputs("files", json.dumps(json_results))


if __name__ == "__main__":
    main()
