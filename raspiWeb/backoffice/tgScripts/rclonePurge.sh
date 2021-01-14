#!/bin/bash
rclone delete onedriveAOC:Personal/cubieSrv/cams --min-age 7d
rclone cleanup onedriveAOC:Personal/cubieSrv
# rclone about onedriveAOC:Personal/cubieSrv
