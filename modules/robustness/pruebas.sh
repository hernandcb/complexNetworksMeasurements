#!/usr/bin/env bash

# Analisis de average path length sequencial sobre redes pequeñas

echo dolphins_apl_sequential
python robustness2.py ../../data/realNetworks/Dolphin\ social\ network/dolphins.gml dolphins_apl_sequential.png apl False

echo football_apl_sequential
python robustness2.py ../../data/realNetworks/American\ College\ football/football.gml football_apl_sequential.png apl False

echo celegans_apl_sequential
python robustness2.py ../../data/realNetworks/CElegans/celegans.gml celegans_apl_sequential.png apl False


# Analisis de average path length simultaneo sobre redes pequeñas

echo dolphins_apl_simultaneus
python robustness2.py ../../data/realNetworks/Dolphin\ social\ network/dolphins.gml dolphins_apl_simultaneus.png apl True

echo football_apl_simultaneus
python robustness2.py ../../data/realNetworks/American\ College\ football/football.gml football_apl_simultaneus.png apl True

echo celegans_apl_simultaneus
python robustness2.py ../../data/realNetworks/CElegans/celegans.gml celegans_apl_simultaneus.png apl True


# ------------------  Redes grandes -------------------------------

# Analisis de componente gigante sequencial sobre redes pequeñas

# echo dolphins_componentSize_sequential
# python robustness2.py ../../data/realNetworks/Dolphin\ social\ network/dolphins.gml dolphins_componentSize_sequential.png component False

# echo football_componentSize_sequential
# python robustness2.py ../../data/realNetworks/American\ College\ football/football.gml football_componentSize_sequential.png component False

# echo celegans_componentSize_sequential
# python robustness2.py ../../data/realNetworks/CElegans/celegans.gml celegans_componentSize_sequential.png component False


# Analisis de componente gigante simultaneo sobre redes pequeñas 

# echo dolphins_componentSize_simultaneus
# python robustness2.py ../../data/realNetworks/Dolphin\ social\ network/dolphins.gml dolphins_componentSize_simultaneus.png component True

# echo football_componentSize_simultaneus
# python robustness2.py ../../data/realNetworks/American\ College\ football/football.gml football_componentSize_simultaneus.png component True

# echo celegans_componentSize_simultaneus
# python robustness2.py ../../data/realNetworks/CElegans/celegans.gml celegans_componentSize_simultaneus.png component True


# Analisis de average path length sequencial sobre redes pequeñas 

# echo dolphins_apl_sequential
# python robustness2.py ../../data/realNetworks/Dolphin\ social\ network/dolphins.gml dolphins_apl_sequential.png apl False

# echo football_apl_sequential
# python robustness2.py ../../data/realNetworks/American\ College\ football/football.gml football_apl_sequential.png apl False

# echo celegans_apl_sequential
# python robustness2.py ../../data/realNetworks/CElegans/celegans.gml celegans_apl_sequential.png apl False


# Analisis de average path length simultaneo sobre redes pequeñas 

# echo dolphins_apl_simultaneus
# python robustness2.py ../../data/realNetworks/Dolphin\ social\ network/dolphins.gml dolphins_apl_simultaneus.png apl True

# echo football_apl_simultaneus
# python robustness2.py ../../data/realNetworks/American\ College\ football/football.gml football_apl_simultaneus.png apl True

# echo celegans_apl_simultaneus
# python robustness2.py ../../data/realNetworks/CElegans/celegans.gml celegans_apl_simultaneus.png apl True


# ------------------  Redes grandes -------------------------------


# Analisis de componente gigante sequencial sobre redes grandes

# echo ecoli_componentSize_sequential
# python robustness2.py ../../data/realNetworks/EColi/EColi.gml ecoli_componentSize_sequential.png component False

# echo email_componentSize_sequential
# python robustness2.py ../../data/realNetworks/Email\ network/email.gml email_componentSize_sequential.png component False

# echo power_componentSize_sequential
# python robustness2.py ../../data/realNetworks/Power\ grid/power.gml  power_componentSize_sequential.png component False


# Analisis de componente gigante simultaneo sobre redes grandes

# echo ecoli_componentSize_simultaneus
# python robustness2.py ../../data/realNetworks/EColi/EColi.gml ecoli_componentSize_simultaneus.png component True

# echo email_componentSize_simultaneus
# python robustness2.py ../../data/realNetworks/Email\ network/email.gml email_componentSize_simultaneus.png component True

# echo power_componentSize_simultaneus
# python robustness2.py ../../data/realNetworks/Power\ grid/power.gml  power_componentSize_simultaneus.png component True


# Analisis de average path length sequencial sobre redes grandes

# echo ecoli_apl_sequential
# python robustness2.py ../../data/realNetworks/EColi/EColi.gml ecoli_apl_sequential.png apl False

# echo email_apl_sequential
# python robustness2.py ../../data/realNetworks/Email\ network/email.gml email_apl_sequential.png apl False

# echo power_apl_sequential
# python robustness2.py ../../data/realNetworks/Power\ grid/power.graphml  power_apl_sequential.png apl False


# Analisis de average path length simultaneo sobre redes grandes

# echo ecoli_apl_simultaneus
# python robustness2.py ../../data/realNetworks/EColi/EColi.graphml ecoli_apl_simultaneus.png apl True

# echo email_apl_simultaneus
# python robustness2.py ../../data/realNetworks/Email\ network/email.graphml email_apl_simultaneus.png apl True

# echo power_apl_simultaneus
# python robustness2.py ../../data/realNetworks/Power\ grid/power.graphml  power_apl_simultaneus.png apl True


