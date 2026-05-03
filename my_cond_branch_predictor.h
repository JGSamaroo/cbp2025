

//#Jennys Code 
//use the sample predictor given for my branch types 

//add header for all predictors 
#ifndef MY_COND_BRANCH_PREDICTOR_H
#define MY_COND_BRANCH_PREDICTOR_H

#include <stdlib.h>
#include <cstdint>
#include <vector>
//#include <unordered_map>
#include <cassert>
#include <algorithm>

//#ifndef _BIMODAL_PREDICTOR_H_
//#define _BIMODAL_PREDICTOR_H_


//struct BimodalHist {
//    uint64_t ghist = 0;
    
//};

class BimodalPredictor {
    static constexpr int TABLE_SIZE = 4096;

    std::vector<int8_t> table;
    //BimodalHist active_hist;
    //std::unordered_map<uint64_t, BimodalHist> pred_time_histories;

public:
    uint64_t num_branches = 0;
    uint64_t num_mispred = 0;

    BimodalPredictor() {
        table.assign(TABLE_SIZE, 2);
    }

    void setup() {
        std::fill(table.begin(), table.end(), 2);
        num_branches = 0;
        num_mispred = 0;
        //active_hist = BimodalHist();
        //pred_time_histories.clear();
    }

    void terminate() {}

    uint64_t get_unique_inst_id(uint64_t seq_no, uint8_t piece) const {
        return (seq_no << 4) | (piece & 0xF);
    }

    bool predict(uint64_t seq_no, uint8_t piece, uint64_t PC) {
        //pred_time_histories.emplace(get_unique_inst_id(seq_no,piece), active_hist);
        uint32_t idx = PC & (TABLE_SIZE - 1);
        return table[idx] >= 2;
    }

    void history_update(uint64_t, uint8_t, uint64_t, bool, uint64_t) {
        //active_hist.ghist = (active_hist.ghist << 1) | (taken ? 1 : 0);
    }

    void update(uint64_t seq_no, uint8_t piece,
                uint64_t PC, bool resolveDir, bool predDir, uint64_t) {
        num_branches++;
        if (resolveDir != predDir) num_mispred++;

        uint32_t idx = PC & (TABLE_SIZE - 1);
        if (resolveDir && table[idx] < 3) table[idx]++;
        else if (!resolveDir && table[idx] > 0) table[idx]--;

        //pred_time_histories.erase(get_unique_inst_id(seq_no,piece));
    }

    //void update(uint64_t, bool, bool, uint64_t, const BimodalHist&) {}
};

static BimodalPredictor cond_predictor_impl;

#endif // MY_COND_BRANCH_PREDICTOR_H
