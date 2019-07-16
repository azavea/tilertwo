# Tiler Two

This repository contains a Docker image that can be used to take a GeoJson file or directory
of line-delimited GeoJson and generate a static vector tile set from it, using almost any
combination of available [Tippecanoe](https://github.com/mapbox/tippecanoe) options.

First, ensure [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) 3.0+ are installed. Then build the container with:

```bash
docker-compose build
```

For complete documentation, run `docker-compose run --rm tiler-two --help`

## Examples

### Only generate an mbtiles file using relative paths

The mbtiles file will be placed in the root of the mounted data volume.

```bash
docker-compose run --rm -v $(pwd)/sample-data:/data tiler-two \
    file:///data/ne_110m_admin_0_countries.geojson \
    file:///data/tiles/ne_110m_admin_0_countries \
    --no-clean \
    --skip-export \
    --tmp /data \
    --tippecanoe-opts "-l ne_110m_admin0 --drop-densest-as-needed -z14"
```

### Export tiles to S3 from a local geojson file

```bash
AWS_PROFILE='<profile>' docker-compose run --rm \
    -v $(pwd)/sample-data:/data tiler-two \
    file:///data/ne_110m_admin_0_countries.geojson \
    s3://bucket/path/to/tiles/ne_110m_admin_0_countries \
    --tippecanoe-opts "--drop-densest-as-needed -zg --coalesce --reorder --hilbert"
```

## Environment Variables

### `AWS_PROFILE`

If you're exporting tiles to S3, set this and mount your `~/.aws` directory to `/home/tilertwo/.aws` in the container.

If you run the container with the included `docker-compose` script, the aws directory mount is handled for you.

### `TIPPECANOE_VERSION`

Defaults to `1.34.3`. Update this and rebuild the image if you'd prefer to install a different version of Tippecanoe.
