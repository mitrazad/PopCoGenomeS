import os
import sys
import numpy

## Collect parameters
project_dir = ""
input_contig_dir = ""
contig_dir = ""
contig_extension = ""
output_prefix = ""
pop_infile_name = ""
ref_iso = ""
ref_contig = ""
len_block_threshold = 0
gap_prop_thresh = 0.0
MUGSY_source = ""


parameter_file = open("phybreak_parameters.txt","r")
for line in parameter_file:
	line = line.strip().split(" = ")
	if len(line) > 1:
		if line[0] == "project_dir":
			project_dir = line[1].split(" #")[0]
		elif line[0] == "input_contig_dir":
			input_contig_dir = line[1].split(" #")[0]
		elif line[0] == "contig_dir":
			contig_dir = line[1].split(" #")[0]
		elif line[0] == "input_contig_extension":
			contig_extension = line[1].split(" #")[0]
		elif line[0] == "output_prefix":
			output_prefix = line[1].split(" #")[0]
		elif line[0] == "pop_infile_name":
			pop_infile_name = line[1].split(" #")[0]
		elif line[0] == "ref_iso":
			ref_iso = line[1].split(" #")[0]
		elif line[0] == "ref_contig":
			ref_contig = line[1].split(" #")[0]
		elif line[0] == "len_block_threshold":
			len_block_threshold = int(line[1].split(" #")[0])
		elif line[0] == "gap_prop_thresh":
			gap_prop_thresh = float(line[1].split(" #")[0])

parameter_file.close()

#these directories will generate if they do not already exist
input_dir = os.path.join(project_dir,"align/")
alignment_dir = os.path.join(input_dir,"alignment_blocks/")

# write sanitized Mugsy-ready inputs to a separate directory
sanitized_contig_dir = os.path.join(contig_dir, "sanitized_inputs/")

#these are output file names
strain_list_filename = "strain_names.txt"
MSA_name = output_prefix+".core.fasta"
phy_prefix = output_prefix
block_loc_filename = output_prefix+".block_location.txt"



#################   MAIN   #################

# Create output directories if needed
if os.path.isdir(input_dir) == False:
    os.makedirs(input_dir)

if os.path.isdir(sanitized_contig_dir) == False:
    os.makedirs(sanitized_contig_dir)

## Unwrap contig fasta files, also remove all '-' and '.' characters from filenames
## and sequence headers. MUGSY output will not be readable by these scripts otherwise.
input_file_list = [f for f in os.listdir(input_contig_dir) if f.endswith(contig_extension)]

with open(os.path.join(project_dir, strain_list_filename), "w") as strain_list_file:
    for strain_line in input_file_list:
        original_strain = strain_line.strip().split(contig_extension)[0]
        sanitized_strain = original_strain.replace(".", "").replace("-", "")

        infile_path = os.path.join(input_contig_dir, strain_line)
        outfile_path = os.path.join(sanitized_contig_dir, sanitized_strain + ".fa")

        strain_list_file.write(sanitized_strain + "\n")

        with open(infile_path, "r") as infile, open(outfile_path, "w") as outfile:
            first_line = True
            contig_no = 0  # sequential numbering relative to headers in original fasta file

            for line in infile:
                line = line.strip()

                if not line:
                    continue

                if line[0] == ">":
                    contig_no += 1
                    head = ">" + sanitized_strain + "_" + str(contig_no)
                    if first_line == True:
                        outfile.write(head + "\n")
                        first_line = False
                    else:
                        outfile.write("\n" + head + "\n")
                else:
                    outfile.write(line)

            outfile.write("\n")

## Generate MUGSY multiple genome alignment
lis = []
with open(os.path.join(project_dir, strain_list_filename), "r") as infile:
    for line in infile:
        line = line.strip()
        if line:
            line = line + ".fa"
            lis.append(line)

print(output_prefix)

mugsyline = "mugsy "
for strain in lis:
    mugsyline = mugsyline + os.path.join(sanitized_contig_dir, strain) + " "
mugsyline = mugsyline + "--directory " + input_dir + " --prefix " + output_prefix

print(mugsyline)
#os.system(MUGSY_source+"\n"+mugsyline)
os.system(mugsyline)
