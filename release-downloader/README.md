ATLAS release delivery tool
===============================

Usage for the tool: 

1) After cloning execute "setup.sh" - this will configure the repositories config as it requires absolute path pointing to reposdir.

2) get-release.pl -d <destination_directory> -t <tmp_dir> <release_name>

	where: <destination_directory> - release will be installed into "<destination_directory>/<release_name>"
		<tmp_dir> - a path to directory where temporary files for the installation will be stored
		<release_name> - full name of the release to be installed, e.g., AtlasOffline_21.0.19_x86_64-slc6-gcc49-opt

	Example:
		get-release.sh -d /lustre/atlas/proj-shared/csc108/app_dir/atlas_app/atlas_rel/release-test/ -t /tmp/release_dl_tmp  AtlasOffline_21.0.19_x86_64-slc6-gcc49-opt

3) install_pacman.sh <pacman_dir>

	this will install pacman into <pacman_dir>/<pacman_version>

4) install_dbrelease.sh <pacman_dir> <release_directory> 

	where: <pacman_dir> is the same as at the previous step
		<release_directory> is "<destination_directory>/<release_name>" at step 2

