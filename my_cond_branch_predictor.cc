

#include "my_cond_branch_predictor.h"
#include <iostream>
#include <cinttypes>

extern BimodalPredictor cond_predictor_impl;

void print_bimodal_stats() {
    std::cout << "\n[BIMODAL Predictor Stats]\n";
    std::cout << "  Num branches: " << cond_predictor_impl.num_branches << "\n";
    std::cout << "  Num mispred : " << cond_predictor_impl.num_mispred  << "\n";

    double mr = 0.0;
    if (cond_predictor_impl.num_branches > 0)
        mr = 100.0 * (double)cond_predictor_impl.num_mispred /
                     (double)cond_predictor_impl.num_branches;

    std::cout << "  Mispred rate: " << mr << "%\n\n";
}