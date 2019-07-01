# Tiler Two

This repository contains a Docker image that can be used to take a GeoJson file or directory
of line-delimited GeoJson and generate a static vector tile set from it, using almost any
combination of available [Tippecanoe](https://github.com/mapbox/tippecanoe) options.

## Examples

### Just generate an mbtiles file using relative paths

```
docker-compose run --rm -v $(pwd):/data tiler-two \
    file://ne_110m_admin_0_countries.geojson \
    file://tiles/ne_110m_admin_0_countries \
    --skip-export
    --tippecanoe-opts "--drop-densest-as-needed -zg -f"
```

### Export tiles to S3 using absolute input path

```
docker-compose run --rm -v $(pwd):/data tiler-two \
    file:///data/ne_110m_admin_0_countries.geojson \
    s3://azavea-datahub/tiles/ne_110m_admin_0_countries \
    --tippecanoe-opts "--drop-densest-as-needed -zg -f"
```

### Export tiles to file path using custom Tippecanoe script

```
docker-compose run --rm -v $(pwd):/data tiler-two \
    file:///data/ne_110m_admin_0_countries.geojson \
    file://tiles/ne_110m_admin_0_countries  \
    --tippecanoe-script "file://my_tippecanoe.sh"
```

## Environment Variables

### `AWS_PROFILE`

If you're exporting tiles to S3, set this and mount your `~/.aws` directory to `/home/tilertwo/.aws` in the container.

### `TIPPECANOE_VERSION`

Defaults to `1.34.3`. Update this and rebuild the image if you'd prefer to install a different version of Tippecanoe.
