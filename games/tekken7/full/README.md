# Portraits

## Description: 

Bigger character portraits

## Where to put the files:

TournamentStreamHelper > assets > games > tekken7
inside the tekken 7 folder make one called "full", it has to be this for the VS screen index to see unless otherwise specified.

## To center images in the VS screen Index JSON:

on line 94/95 it will say:

background-image: url(../../${data[p+"_assets_path"][ASSET_TO_USE]});

${p == "p2" && FLIP_P2_ASSET ? "transform: scaleX(-1);" : ""}

Below the part telling it to flip the image add:

${data[p+"_assets_path"][ASSET_TO_USE].includes("tekken7")?"background-position: center 0;" : ""}
