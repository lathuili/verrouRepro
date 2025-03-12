#!/bin/bash

# Arguments en ligne de commande:
# - le répertoire où les résultats doivent être stockés
OUTDIR=$1

# Lancement du code avec Verrou, en stockant les résultats dans ${OUTDIR}
valgrind --tool=verrou --rounding-mode=random --libm=instrumented ./unitTestTask >${OUTDIR}/res.dat
