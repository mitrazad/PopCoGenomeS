#!/usr/bin/env bash
# Mitra: added so it accesses the conda environments, otherwise it fails silently when it can't find the phybreak environment
source "$(conda info --base)/etc/profile.d/conda.sh"

# Mitra: added to make sure the script can find the config file, otherwise it would fail silently
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Annie: PHY_CONFIG=./phybreak_config.sh
PHY_CONFIG=$SCRIPT_DIR/phybreak_config.sh
source ${PHY_CONFIG}

# The config file is the list of vertically-inherited genome clusters
OUTFOLDER_2=$1

#define directory where the script is called
HOMEFOLDER=`pwd`

#define and construct workspace
THISWORKFOLDER=${project_dir_1}/${OUTFOLDER_2}
mkdir -p $THISWORKFOLDER
mkdir -p $THISWORKFOLDER/genomes
cp -R ${path_to_phybreak}/align_and_construct_trees $THISWORKFOLDER
cp ${PHY_CONFIG} $THISWORKFOLDER/align_and_construct_trees

project_dir=$THISWORKFOLDER
export project_dir
export OUTFOLDER_2

# make the output directory
mkdir -p ${output_dir}
echo ${output_dir}

cd ${project_dir}/align_and_construct_trees

#Run prep code
# Mitra: "module load conda" hashed out
conda activate ${path_to_PopCoGenomeS}
# Mitra: specified bash instead of sh
bash 00_prepare_phybreak.sh
echo Done!

#Generate multiple sequence alignment 
python phybreak1.generate_maf.py
python phybreak2.maf_to_fasta.py

#Run the tree building step
conda activate ${path_to_PopCoGenomeS_R}
Rscript fasta_to_phy.R $basename
cd ${project_dir}/align
#This tree uses a GTR+G+I model
phyml -i ${basename}.core.fasta.phy -m 'GTR' -t 'e' -a 'e' -f 'm' -v 'e' > ${basename}.core.phy_phyml_stat.txt

#copy tree back to output folder
cp ${basename}.core.fasta.phy_phyml_tree.txt $output_dir/${OUTFOLDER_2}.core.fasta.phy_phyml_tree.txt

