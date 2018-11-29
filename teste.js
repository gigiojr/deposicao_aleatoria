function busca_lateral(vtr, idx) {
    if (idx === vtr.length) {
        // avaliar apenas esquerda
        if (vtr[idx] > vtr[idx - 1])
            return busca_lateral(vtr, idx - 1);
        else
            return idx;
    } else if (idx === 0) {
        // avaliar apenas direita
        if (vtr[idx] > vtr[idx + 1])
            return busca_lateral(vtr, idx + 1);
        else
            return idx;
    }
    else {
        // avaliar os dois lados
        let idx_left = idx - 1;
        let idx_right = idx + 1;
        let idx_choose;
        if (vtr[idx_right] < vtr[idx_left]) {
            // testar o atual com a direita
            let idx_choose = idx_right;
        } else if (vtr[idx_left] < vtr[idx_right]) {
            // testar o atual com a esquerda
            idx_choose = idx_left
        } else {
            idx_choose = Math.random() % 2 === 0 ? idx_right : idx_left;
        }

        if (vtr[idx_choose] < vtr[idx]) {
            return busca_lateral(vtr, idx_choose);
        } else {
            return idx
        }
    }
}

function calcula_rugosidade(vetor, L) {
    let hMedia = 0;
    for (let i = 0; i < vetor.length; i++){
        hMedia += vetor[i]
    }
    hMedia = hMedia / vetor.length;

    somatorio = 0;
    for (let i = 0; i < vetor.length; i++){
        somatorio += (vetor[i] - hMedia) ** 2;
    }
    return Math.sqrt(somatorio / L);
}

function make_desposition_relaxation(l, t) {
    let w = [];
    let vtr = new Array(l).fill(0);
    for (let i = 0; i < t; i++){
        for (let j = 0; j < l; j++) {
            let random_index = Math.floor(Math.random() * (l - 1));
            let idx = busca_lateral(vtr, random_index);
            vtr[idx] += 1
        }
        w.push(calcula_rugosidade(vtr, l));
    }
    console.log(w);
}

make_desposition_relaxation(200, 100);