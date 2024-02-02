# Snowflake Stage File Donwloader Action

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This Github Action let's you download files recursively from a Snowflake stage, with the configuration described below.

The action uses the [GET SQL command](https://docs.snowflake.com/en/sql-reference/sql/get) to download files from your specified stage path. You only have to specify the path to your files, the action will download all files recursively. The `@` is already added to the stage name. 

```
  internalStage ::=
      @[<namespace>.]<int_stage_name>[/<path>]
    | @[<namespace>.]%<table_name>[/<path>]
    | @~[/<path>]
```

## Inputs

- `snowflake_account` - Account name for Snowflake DB.
- `snowflake_warehouse` - Set the warehouse context.
- `snowflake_username`, `snowflake_password` - Credentials for your DB.
  - It's recommended to use [Github's Secrets](https://docs.github.com/en/actions/reference/encrypted-secrets) for those arguments.
- `snowflake_database` - Sets the Snowflake database.
- `snowflake_stage` - Sets the Snowflake stage name and/or path. **Please do not add the `@` character.** 
- `local_download_path` - Specifies the download folder for the files.

## Output

`files` - Json string contains the results from all downloaded files.

It may be accessed in following steps. See [this](https://docs.github.com/en/actions/reference/context-and-expression-syntax-for-github-actions#tojson) guide for more github's action expressions examples.

## Usage

### Run multiple queries in one job

```yaml
steps:
  - name: Download stage files
    uses: hawle/snowflake-stage-download@v1.0.0
    id: sf_stage_download
    with:
        snowflake_account: ${{ secrets.SNOWFLAKE_ACCOUNT }}
        snowflake_warehouse: ${{ secrets.SNOWFLAKE_WAREHOUSE }}
        snowflake_username: ${{ secrets.SNOWFLAKE_USER }}
        snowflake_password: ${{ secrets.SNOWFLAKE_PASSWORD }}
        snowflake_database: ${{ secrets.SNOWFLAKE_DATABASE }}
        snowflake_schema: ${{ secrets.SNOWFLAKE_SCHEMA }}
        snowflake_stage: 'DATA_STAGE/MIRROR'
        local_download_path: './MyStageFiles'
    - name: List Files
        run: |
          echo ${{steps.sf_stage_download.outputs.files}}
```