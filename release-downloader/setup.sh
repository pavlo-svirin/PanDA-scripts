#
#-- Setup script made by Pacman 3.29 and is often regenerated.  DO NOT EDIT
#
#
#-- begin pre-setup
#
export PAC_ANCHOR="/mnt/swia/tmp"
if [ -d "${PAC_ANCHOR}/pre-setup" ]; then
    for PACMANi in `/usr/bin/env find "${PAC_ANCHOR}/pre-setup" -maxdepth 1 -type f -name '*.sh' | sort`; do
        source "${PACMANi}"
    done
    unset PACMANi
fi
#
#-- end pre-setup
#
#
#-- package /mnt/swia/tmp:http://atlas.web.cern.ch/Atlas/GROUPS/DATABASE/pacman4/DBRelease:DBRelease-current
#
#
#-- begin post-setup
#
export PAC_ANCHOR="/mnt/swia/tmp"
if [ -d "${PAC_ANCHOR}/post-setup" ]; then
    for PACMANi in `/usr/bin/env find "${PAC_ANCHOR}/post-setup" -maxdepth 1 -type f -name '*.sh' | sort`; do
        source "${PACMANi}"
    done
    unset PACMANi
fi
#
#-- end post-setup
#
