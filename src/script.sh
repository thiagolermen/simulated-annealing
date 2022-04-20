mkdir formulation_results
for FILE in ../data/instance*.dat
do 
    out_name="$(basename -s .dat ${FILE})"
    julia formulation.jl $FILE >> formulation_results/$out_name".txt" 
done
