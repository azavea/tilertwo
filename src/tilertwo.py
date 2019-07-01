import argparse
import os
import shlex
import shutil
import subprocess
import tempfile
from urllib.parse import urlparse


class CommandError(RuntimeError):
    pass


def file_import_handler(input_uri, dest):
    copy_cmd = ["cp", input_uri.path, dest]
    subprocess.run(copy_cmd, check=True)
    print("Copied {} to: {}".format(input_uri.path, dest))


VALID_INPUT_SCHEMES = set(("file",))
import_handlers = {
    "file": file_import_handler
}
if set(import_handlers.keys()) != VALID_INPUT_SCHEMES:
    raise CommandError("Must implement import handler for each input scheme: {}"
                       .format(VALID_INPUT_SCHEMES))


def file_export_handler(static_tiles_dir, output_uri):
    copy_cmd = ["cp", "-r", static_tiles_dir, output_uri.path]
    subprocess.run(copy_cmd, check=True)
    print("Copied static tiles to: {}".format(output_uri.path))


VALID_OUTPUT_SCHEMES = set(("file",))
export_handlers = {
    "file": file_export_handler
}
if set(export_handlers.keys()) != VALID_OUTPUT_SCHEMES:
    raise CommandError("Must implement export handler for each input scheme: {}"
                       .format(VALID_OUTPUT_SCHEMES))


def main():

    parser = argparse.ArgumentParser(description="Generate vector tile pyramids from GeoJson")
    parser.add_argument("geojson_file_path",
                        help="Path to geojson file to process. It should include the scheme, " +
                             "such as file:///absolute/path/to.geojson. Supports schemes: "
                             .format(VALID_INPUT_SCHEMES))
    parser.add_argument("output_path",
                        help="Path to output directory, where mbtiles or mvts will be " +
                             "placed. It should include the scheme, such as " +
                             "file:///absolute/path/to/tiles. Supports schemes: {}."
                             .format(VALID_OUTPUT_SCHEMES))
    parser.add_argument("--skip-export", action="store_true",
                        help="If provided, skip tile export and just run Tippecanoe.")
    parser.add_argument("--tippecanoe-opts", default="-zg --drop-densest-as-needed",
                        help="Arguments to pass to Tippecanoe CLI call.")
    parser.add_argument("-t", "--tmp", default="/tmp",
                        help="Path to use for temporary working directory.")

    args = parser.parse_args()

    temp_dir = tempfile.mkdtemp(prefix=os.path.join(args.tmp, ""))
    try:
        input_uri = urlparse(args.geojson_file_path)
        output_uri = urlparse(args.output_path)
        if input_uri.scheme not in VALID_INPUT_SCHEMES:
            raise CommandError("geojson_file_path must be one of {}".format(VALID_INPUT_SCHEMES))
        if output_uri.scheme not in VALID_OUTPUT_SCHEMES:
            raise CommandError("output_path must be one of {}".format(VALID_OUTPUT_SCHEMES))

        if os.path.splitext(input_uri.path)[1] != ".geojson":
            raise CommandError("geojson_file_path must point to a .geojson file")

        print(args)

        tippecanoe_input_file = os.path.join(temp_dir, "data.geojson")
        import_handlers[input_uri.scheme](input_uri, tippecanoe_input_file)
        tippecanoe_output_file = os.path.join(temp_dir, "out.mbtiles")
        tippecanoe_cmd = ["tippecanoe",
                          "-o", tippecanoe_output_file,
                          *shlex.split(args.tippecanoe_opts),
                          tippecanoe_input_file]
        print(tippecanoe_cmd)
        subprocess.run(tippecanoe_cmd, check=True)
        print("tippecanoe wrote successfully to: {}".format(tippecanoe_output_file))

        mbutil_output_dir = os.path.join(temp_dir, "static-tiles")
        mbutil_cmd = ["mb-util",
                      "--image_format=pbf",
                      tippecanoe_output_file,
                      mbutil_output_dir]
        subprocess.run(mbutil_cmd, check=True)
        print("mb-util wrote successfully to: {}".format(mbutil_output_dir))

        export_handlers[output_uri.scheme](mbutil_output_dir, output_uri)

    except subprocess.CalledProcessError as e:
        print("\nError: {} failed with returncode {}\n".format(e.cmd, e.returncode))
    except CommandError as e:
        print("\nError: {}\n".format(e))
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":

    main()
