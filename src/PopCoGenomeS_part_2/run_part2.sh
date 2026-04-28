while read line; do
    bash align_and_construct_trees.sh ${line} < /dev/null
done<../PopCoGenomeS_part_1/output/${basename}*_cf_size_3.list