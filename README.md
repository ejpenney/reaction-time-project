# reaction-time-project

## Purpose/Goal

This tool was created for my son's science fair project. It gathers some demographical data, then displays a greyed out button. At random intervals the button enables, and the user must press it. Their reaction time is recorded.

## Setup

A docker-compose file is provided, simply download this source tree, cd to the directory, and run:

```bash
docker compose up -d
```

To shut down, run from this directory:

```bash
docker compose down
```

## Hosting

The two containers created above host the web page (`frontend/index.html`) on port 80, and a second containers hosts the backend endpoints on port 5500. However you host, you should map the root paths `/download` and '/submit` to these same paths on path 5500.

For example, if using [Nginx Proxy Manager](https://nginxproxymanager.com/), in "Advanced" -> "Custom Nginx Configuration" you might specify:

```nginx
location /submit {
    proxy_pass $forward_scheme://$server:5500/submit;
}

location /download {
    proxy_pass $forward_scheme://$server:5500/download;
}
```

## API Entrypoints

Two entry-points are provided by app.py

### /download

An HTTP_GET request to this endpoint retrieves a CSV with all data from the database.

### /submit

An HTTP_POST request to this endpoint submits all data gathered during the execution of the test.

## Handy Commands

One may notice that when you modify `backend/app.py` the Docker container is not automatically recreated. Before rerunning `docker compose up` you should run:

```bash
docker image rm reaction-time-project-api
```

Additionally, if making changes to the DB schema, it may be necessary to drop the entire database. To do so, run:

```bash
docker volume rm reaction-time-project_data
```

## Licensing

This repository is licensed with the [MIT License](./LICENSE.md)

