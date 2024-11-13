from django.apps import AppConfig
import os
import zipfile


class MapTilesConfig(AppConfig):
    name = "map_tiles"

    def ready(self):
        """
        This method is called when the Django app registry is fully populated.
        It's a suitable place to perform initialization tasks.
        """
        # Prevent running initialization multiple times during development

        self.unzip_file()

    def unzip_file(self):
        app_path = self.path
        zip_path = os.path.join(app_path, "resources", "map_tiles_archive.zip")
        extract_path = os.path.join(app_path, "tile_data")

        # Check if extraction is already done to prevent redundancy
        if not os.path.exists(extract_path):
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                for member in zip_ref.namelist():
                    # Skip __MACOSX directory and .DS_Store files
                    if (
                        member.startswith("__MACOSX/")
                        or member.endswith(".DS_Store")
                        or os.path.basename(member).startswith(".")
                    ):
                        continue

                    # We just extract to app_path because the unzipped contents are already named "tile_data" - this is done when the zip file is created
                    zip_ref.extract(member, app_path)
        else:
            # If the files have already been extracted, do nothing
            return
