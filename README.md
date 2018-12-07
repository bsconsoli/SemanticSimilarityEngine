# Semantic Similarity Engine

# Pré-requisitos
 - Interpretador Python 3.x
 - Pacotes argparse, numpy, scipy, sklearn, requests, bs4, gensim (Para instalar dependências, executar *pip3 install -r requirements.txt* na pasta da ferramenta)

# Execução
 - Extrair e Anotar Corpus

    Argumentos de Entrada:
     *maltparser* ou *visl*, de acordo com o anotador desejado
     Corpus formatado no estilo ASSIN 2016 (exemplos em corpora/raw_corpora)

    Argumentos de Saída:
     Arquivo com dados anotados, pronto para uso com essa ferramenta (corpus_anotado.txt - O arquivo é substituído a cada execução)

    Exemplo de Uso:
    * ./annotate_corpus.sh maltparser corpora/raw_corpora/training_corpus.txt

 - Treinar e Testar Modelo de Aprendizado de Máquina

    Argumentos de Entrada:
     Arquivo com dados de treino anotados, no formato dado pela execução *Extrair e Anotar Corpus* (Exemplos em corpora/annotated_corpora)
     Arquivo com dados de teste anotados, no formato dado pela execução *Extrair e Anotar Corpus* (Exemplos em corpora/annotated_corpora)
     Modelo de word embeddings no formato word2vec (Modelo word embeddings não incluso nesse pacote, deve ser adquirido separadamente)

    Argumentos de Saída:
     Resultados de Pearson r e MSE para o modelo treinado impressos no terminal

    Exemplo de Uso:
    * ./train_test_model.sh corpora/annotated_corpora/corpus_anotado_malt_train.txt corpora/annotated_corpora/corpus_anotado_malt_test.txt semantic/NILC_cbow_s300.txt 
