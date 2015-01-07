CLUMPHOME="$(dirname $0)/.."
PYTHONPATH=$(realpath $CLUMPHOME) $CLUMPHOME/scripts/clump $*
