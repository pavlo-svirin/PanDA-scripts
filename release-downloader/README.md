ATLAS release delivery tool
===============================

After cloning execute "setup.sh" - this will configure the repositories config as it requires absolute path pointing to reposdir.

Usage for the tool: 

1) get-release.pl -d <destination_directory> [-c <cache_dir>] <release_name>

	where: <destination_directory> - release will be installed into "<destination_directory>/<release_name>"
		<cache_directory> - a place where cache data will be stored
		<release_name> - full name of the release to be installed, e.g., AtlasOffline_21.0.19_x86_64-slc6-gcc49-opt

	Example:
		get-release.sh -d /lustre/atlas/proj-shared/csc108/app_dir/atlas_app/atlas_rel/release-test/  AtlasOffline_21.0.19_x86_64-slc6-gcc49-opt

2) install_pacman.sh <pacman_dir>

	this will install pacman into <pacman_dir>/<pacman_version>

3) install_dbrelease.sh <pacman_dir> <release_directory> 

	where: <pacman_dir> is the same as at the previous step
		<release_directory> is "<destination_directory>/<release_name>" at step 1

